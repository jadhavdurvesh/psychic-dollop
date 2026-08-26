from flask import Blueprint, request, jsonify, current_app
from urllib.parse import urlparse
from ..app import db, ShortUrl, generate_short_code

shorten_bp = Blueprint("shorten", __name__)

def _is_valid_url(url: str) -> bool:
    """
    Validate the structure of a URL using urllib.parse.urlparse.
    A valid URL must have a scheme (e.g., http, https) and a network location.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

@shorten_bp.route("/shorten", methods=["POST"])
def shorten():
    # Ensure request contains JSON
    if not request.is_json:
        return jsonify(error="Request body must be JSON"), 400

    data = request.get_json(silent=True) or {}

    # Verify 'url' field exists
    if "url" not in data:
        return jsonify(error="Missing 'url' field in JSON payload"), 400

    url = data["url"]

    # Validate that 'url' is a non‑empty string
    if not isinstance(url, str) or not url.strip():
        return jsonify(error="'url' must be a non‑empty string"), 400

    # Validate URL structure
    if not _is_valid_url(url):
        return jsonify(error="Invalid URL format"), 400

    # Existing shortening logic
    short_code = generate_short_code()
    short_entry = ShortUrl(original_url=url, short_code=short_code)
    db.session.add(short_entry)
    db.session.commit()

    short_url = request.host_url.rstrip("/") + "/" + short_code
    return jsonify(short_url=short_url), 201