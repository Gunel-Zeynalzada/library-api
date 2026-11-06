from .. import fines
from ..db import connection
from ..repositories import books as books_repo
from ..repositories import loans as loans_repo


def overdue_report():
    """Return (items, total_fines) for every unreturned loan past its due date."""
    with connection() as conn:
        rows = loans_repo.open_with_details(conn)
    items = []
    total = 0
    for row in rows:
        late = fines.days_late(row["due_date"])
        if late > 0:
            fine = fines.fine_for_days(late)
            total += fine
            items.append(
                {"loan_id": row["loan_id"], "title": row["title"], "member": row["member"],
                 "days_late": late, "fine": fine}
            )
    return items, total


def summary():
    """Return (total_books, on_loan, fines_outstanding)."""
    with connection() as conn:
        total_books = books_repo.count(conn)
        loans = loans_repo.list_all(conn)
    return total_books, fines.open_loan_count(loans), fines.amount_owed(loans)
