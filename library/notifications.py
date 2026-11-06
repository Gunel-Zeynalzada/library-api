"""Outgoing messages. The only module that knows messages go to outbox.txt
(a stand-in for a real mail server)."""
from . import config


def send(to_email, subject, body):
    with open(config.OUTBOX_PATH, "a") as f:
        f.write(f"TO: {to_email} | SUBJECT: {subject} | BODY: {body}\n")


def book_checked_out(member, book):
    send(member["email"], "Book checked out", "You checked out " + book["title"])


def loan_renewed(member, book):
    send(member["email"], "Loan renewed", "You renewed " + book["title"])


def book_returned(member, book, fine):
    send(member["email"], "Book returned", f"You returned {book['title']}. Fine: ${fine}")


def fine_paid(member, amount):
    send(member["email"], "Fine paid", f"We received ${amount}")
