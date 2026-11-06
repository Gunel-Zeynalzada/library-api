"""Database rows -> JSON-ready dicts. The API's response shapes are defined here."""
from . import fines


money = fines.money


def book_json(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "isbn": book["isbn"],
        "available": bool(book["available"]),
    }


def member_json(member):
    return {
        "id": member["id"],
        "name": member["name"],
        "email": member["email"],
        "type": member["type"],
    }


def loan_json(loan):
    return {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
        "renewals": loan["renewals"],
        "checked_out": loan["checked_out"],
    }


def loan_detail_json(loan):
    """A loan plus the fine it has right now."""
    data = loan_json(loan)
    data["current_fine"] = money(fines.loan_fine_now(loan))
    return data


def member_loan_json(loan):
    return {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
    }
