from flask import Blueprint, jsonify, request

from ..serializers import book_json
from ..services import books as service

bp = Blueprint("books", __name__)


@bp.route("/books", methods=["GET"])
def list_books():
    available_only = request.args.get("available") == "true"
    return jsonify([book_json(b) for b in service.list_books(available_only)])


@bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return jsonify(book_json(service.get_book(book_id)))


@bp.route("/books", methods=["POST"])
def create_book():
    data = request.get_json(silent=True) or {}
    return jsonify(book_json(service.create_book(data))), 201


@bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    service.delete_book(book_id)
    return "", 204
