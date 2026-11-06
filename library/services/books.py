from .. import validation
from ..db import connection
from ..errors import ConflictError, NotFoundError, ValidationError
from ..repositories import books as books_repo


def list_books(available_only=False):
    with connection() as conn:
        return books_repo.list_all(conn, available_only)


def get_book(book_id):
    with connection() as conn:
        book = books_repo.get(conn, book_id)
    if book is None:
        raise NotFoundError("book not found")
    return book


def create_book(data):
    if not data.get("title") or not data.get("author"):
        raise ValidationError("title and author are required")
    if not validation.is_valid_isbn(data.get("isbn")):
        raise ValidationError("invalid isbn")
    with connection() as conn:
        return books_repo.insert(conn, data["title"], data["author"], data["isbn"])


def delete_book(book_id):
    with connection() as conn:
        book = books_repo.get(conn, book_id)
        if book is None:
            raise NotFoundError("book not found")
        if not book["available"]:
            raise ConflictError("book is on loan")
        books_repo.delete(conn, book_id)
