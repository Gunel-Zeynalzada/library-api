from datetime import date, timedelta

from .. import config, fines, notifications, validation
from ..db import connection
from ..errors import ConflictError, NotFoundError, ValidationError
from ..repositories import books as books_repo
from ..repositories import loans as loans_repo
from ..repositories import members as members_repo


def list_loans(overdue_only=False):
    with connection() as conn:
        loans = loans_repo.list_all(conn)
    if overdue_only:
        loans = [
            loan for loan in loans
            if not loan["returned"] and fines.is_overdue(loan["due_date"])
        ]
    return loans


def get_loan(loan_id):
    with connection() as conn:
        loan = loans_repo.get(conn, loan_id)
    if loan is None:
        raise NotFoundError("loan not found")
    return loan


def checkout(data):
    if not data.get("book_id") or not data.get("member_id"):
        raise ValidationError("book_id and member_id are required")
    if data.get("due_date") and not validation.is_valid_date(data["due_date"]):
        raise ValidationError("invalid due_date")

    with connection() as conn:
        book = books_repo.get(conn, data["book_id"])
        if book is None:
            raise NotFoundError("book not found")
        member = members_repo.get(conn, data["member_id"])
        if member is None:
            raise NotFoundError("member not found")
        if not book["available"]:
            raise ConflictError("book is not available")

        member_loans = loans_repo.for_member(conn, member["id"])
        if fines.amount_owed(member_loans) > 0:
            raise ConflictError("member has unpaid fines")
        if fines.open_loan_count(member_loans) >= fines.loan_limit(member["type"]):
            raise ConflictError("loan limit reached")

        today = date.today()
        due_date = data.get("due_date") or (
            today + timedelta(days=config.LOAN_PERIOD_DAYS)
        ).isoformat()
        loan = loans_repo.insert(conn, book["id"], member["id"], due_date, today.isoformat())
        books_repo.set_available(conn, book["id"], False)

    notifications.book_checked_out(member, book)
    return loan


def return_book(loan_id):
    with connection() as conn:
        loan = _get_open_loan(conn, loan_id)
        fine = fines.open_loan_fine(loan["due_date"])
        updated = loans_repo.mark_returned(conn, loan_id, fine)
        books_repo.set_available(conn, loan["book_id"], True)
        member = members_repo.get(conn, loan["member_id"])
        book = books_repo.get(conn, loan["book_id"])

    notifications.book_returned(member, book, fine=fines.money(fine))
    return updated


def renew(loan_id):
    with connection() as conn:
        loan = _get_open_loan(conn, loan_id)
        if fines.is_overdue(loan["due_date"]):
            raise ConflictError("overdue loans cannot be renewed")
        if loan["renewals"] >= config.MAX_RENEWALS:
            raise ConflictError("loan was already renewed")

        new_due = date.fromisoformat(loan["due_date"]) + timedelta(days=config.RENEWAL_PERIOD_DAYS)
        updated = loans_repo.extend(conn, loan_id, new_due.isoformat())
        member = members_repo.get(conn, loan["member_id"])
        book = books_repo.get(conn, loan["book_id"])

    notifications.loan_renewed(member, book)
    return updated


def pay_fine(loan_id):
    with connection() as conn:
        loan = get_loan_or_404(conn, loan_id)
        if not loan["returned"]:
            raise ConflictError("return the book before paying")
        if loan["fine"] <= 0 or loan["fine_paid"]:
            raise ConflictError("no fine to pay")
        updated = loans_repo.mark_fine_paid(conn, loan_id)
        member = members_repo.get(conn, loan["member_id"])

    notifications.fine_paid(member, fines.money(loan["fine"]))
    return updated


# ---------- helpers ----------


def get_loan_or_404(conn, loan_id):
    loan = loans_repo.get(conn, loan_id)
    if loan is None:
        raise NotFoundError("loan not found")
    return loan


def _get_open_loan(conn, loan_id):
    loan = get_loan_or_404(conn, loan_id)
    if loan["returned"]:
        raise ConflictError("loan already returned")
    return loan

