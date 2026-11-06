from .. import fines, validation
from ..db import connection
from ..errors import ConflictError, NotFoundError, ValidationError
from ..repositories import loans as loans_repo
from ..repositories import members as members_repo


def list_members():
    with connection() as conn:
        return members_repo.list_all(conn)


def get_member(member_id):
    with connection() as conn:
        member = members_repo.get(conn, member_id)
    if member is None:
        raise NotFoundError("member not found")
    return member


def create_member(data):
    if not data.get("name"):
        raise ValidationError("name is required")
    if not validation.is_valid_email(data.get("email")):
        raise ValidationError("invalid email")
    member_type = data.get("type", "student")
    if not validation.is_valid_member_type(member_type):
        raise ValidationError("type must be student or staff")
    with connection() as conn:
        if members_repo.get_by_email(conn, data["email"]) is not None:
            raise ConflictError("email already registered")
        return members_repo.insert(conn, data["name"], data["email"], member_type)


def get_member_loans(member_id):
    """Return (member, loans, total_owed, loans_remaining)."""
    with connection() as conn:
        member = members_repo.get(conn, member_id)
        if member is None:
            raise NotFoundError("member not found")
        loans = loans_repo.for_member(conn, member_id)
    return (
        member,
        loans,
        fines.amount_owed(loans),
        fines.loans_remaining(member["type"], loans),
    )
