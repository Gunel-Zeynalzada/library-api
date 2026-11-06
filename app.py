"""Entry point. Builds the Flask app; all real work lives in the `library` package."""
import os

from flask import Flask, jsonify

from library import config
from library.db import init_db
from library.errors import LibraryError
from library.routes import ALL_BLUEPRINTS

app = Flask(__name__)

for blueprint in ALL_BLUEPRINTS:
    app.register_blueprint(blueprint)


@app.errorhandler(LibraryError)
def handle_library_error(error):
    return jsonify({"error": error.message}), error.status_code


if not os.path.exists(config.DB_PATH):
    init_db()
