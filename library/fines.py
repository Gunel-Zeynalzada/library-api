"""Pure business rules about time, fines and limits.

Nothing here touches Flask, SQL or files, so every rule can be tested with
plain function calls. The fine rate appears in exactly one place
(config.FINE_PER_DAY) and is applied in exactly one function (fine_for_days).
"""
from datetime import date

from . import config


def money(x):
    """Round an amount of dollars to cents."""
    return round(float(x), 2)


def days_late(due_date, today=None):
    """Days past the due date (negative or zero when not yet late)."""
    today = today or date.today()
    return (today - date.fromisoformat(due_date)).days


def fine_for_days(days):
    return max(0, days) * config.FINE_PER_DAY


def open_loan_fine(due_date, today=None):
    """Fine accrued so far on a loan that has not been returned."""
    return fine_for_days(days_late(due_date, today))


def is_overdue(due_date, today=None):
    return days_late(due_date, today) > 0


def loan_fine_now(loan, today=None):
    """Fine to show for a loan: accruing if open, frozen if returned."""
    if not loan["returned"]:
        return open_loan_fine(loan["due_date"], today)
    return loan["fine"]


def amount_owed(loans, today=None):
    """Total unpaid fines: accrued on open loans plus unpaid fines on returned ones."""
    owed = 0
    for loan in loans:
        if not loan["returned"]:
            owed += open_loan_fine(loan["due_date"], today)
        elif not loan["fine_paid"]:
            owed += loan["fine"]
    return owed


def open_loan_count(loans):
    return sum(1 for loan in loans if not loan["returned"])


def loan_limit(member_type):
    return config.LOAN_LIMITS.get(member_type, config.DEFAULT_LOAN_LIMIT)


def loans_remaining(member_type, loans):
    return loan_limit(member_type) - open_loan_count(loans)
