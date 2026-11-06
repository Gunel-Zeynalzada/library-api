from flask import Blueprint, jsonify

from ..serializers import money
from ..services import reports as service

bp = Blueprint("reports", __name__)


@bp.route("/reports/overdue", methods=["GET"])
def report_overdue():
    items, total = service.overdue_report()
    for item in items:
        item["fine"] = money(item["fine"])
    return jsonify({"items": items, "total_fines": money(total)})


@bp.route("/reports/summary", methods=["GET"])
def report_summary():
    total_books, on_loan, outstanding = service.summary()
    return jsonify(
        {"total_books": total_books, "on_loan": on_loan, "fines_outstanding": money(outstanding)}
    )
