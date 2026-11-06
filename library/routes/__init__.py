"""HTTP layer: one blueprint per resource. Handlers read the request, call a
service and shape the response. No SQL and no business rules."""
from .books import bp as books_bp
from .loans import bp as loans_bp
from .members import bp as members_bp
from .reports import bp as reports_bp

ALL_BLUEPRINTS = (books_bp, members_bp, loans_bp, reports_bp)
