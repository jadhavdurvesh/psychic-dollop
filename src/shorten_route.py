import urllib.parse

from flask import Blueprint, request, jsonify, current_app

shorten_bp = Blueprint('shorten', __name__)


def _is_valid_url(url: str) -> bool:
    """
    Validate that the supplied string is a well‑formed HTTP/HTTPS URL.

    Returns True if the URL has a scheme of http or https and a non‑empty netloc.
    """
    try:
        parsed = urllib.parse.urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except Exception:
        return False


@shorten_bp.route("/api/shorten", methods=["POST"])
def shorten():
    """
    Accept a JSON payload containing a ``url`` key and return a shortened URL.

    Validation performed:
    * request must be JSON
    * payload must be a JSON object
    * ``url`` key must be present
    * ``url`` must be a non‑empty string
    * ``url`` must be a syntactically valid HTTP/HTTPS URL
    """
    # Ensure request is JSON
    if not request.is_json:
        return jsonify(error="Invalid request: JSON payload required"), 400

    # Parse JSON safely
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Invalid request: JSON object required"), 400

    # Presence of 'url' field
    if "url" not in data:
        return jsonify(error="Invalid request: 'url' field missing"), 400

    url = data["url"]

    # ``url`` must be a string
    if not isinstance(url, str):
        return jsonify(error="Invalid request: 'url' must be a string"), 400

    # Strip whitespace and ensure non‑empty
    url = url.strip()
    if not url:
        return jsonify(error="Invalid request: 'url' cannot be empty"), 400

    # Validate URL structure
    if not _is_valid_url(url):
        return jsonify(error="Invalid request: malformed URL"), 400

    # Existing shortening logic – delegate to the configured shortener service
    short_code = current_app.config["SHORTENER"].shorten(url)
    short_url = f"{request.host_url}{short_code}"
    return jsonify(short_url=short_url), 201