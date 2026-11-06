"""Every tunable value lives here, so a rule change is a one-line edit."""

# Relative paths on purpose: files are created in the folder the API runs from.
DB_PATH = "library.db"
OUTBOX_PATH = "outbox.txt"

LOAN_PERIOD_DAYS = 14
RENEWAL_PERIOD_DAYS = 14
MAX_RENEWALS = 1

FINE_PER_DAY = 0.50

LOAN_LIMITS = {"student": 3, "staff": 5}
DEFAULT_LOAN_LIMIT = LOAN_LIMITS["student"]
MEMBER_TYPES = tuple(LOAN_LIMITS)
