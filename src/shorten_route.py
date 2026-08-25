import random
import string

from flask import Blueprint, current_app, jsonify, request

from .store import store

bp = Blueprint("shorten", __name__)


def _generate_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code."""
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


@bp.route("/api/shorten", methods=["POST"])
def shorten():
    """
    Accept a JSON payload ``{ "original_url": "<url>" }`` and return a
    newly‑generated short code together with the full short URL.

    Errors:
        * 400 – malformed JSON or missing/invalid ``original_url``.
        * 500 – unable to generate a unique short code after several attempts.
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    original_url = data.get("original_url")
    if not original_url or not isinstance(original_url, str):
        return jsonify({"error": "Missing or invalid 'original_url'"}), 400

    # Try to generate a unique short code.
    for _ in range(10):
        code = _generate_code()
        if not store.exists(code):
            store.set(code, original_url)
            break
    else:
        # Extremely unlikely, but we guard against an endless loop.
        return jsonify({"error": "Could not generate a unique short code"}), 500

    # Build the absolute short URL using the request host.
    host = request.host_url.rstrip("/")
    short_url = f"{host}/{code}"
    return jsonify({"code": code, "short_url": short_url}), 201