from flask import Blueprint, request, jsonify, current_app
from urllib.parse import urlparse

# Assuming there is a Shortener service/class that handles the actual URL shortening logic.
# Import it accordingly. Adjust the import path based on the actual project structure.
try:
    from .shortener import Shortener
except ImportError:
    # Fallback import for projects that expose Shortener differently.
    from shortener import Shortener  # type: ignore

shorten_bp = Blueprint('shorten', __name__)

def _is_valid_url(url: str) -> bool:
    """
    Validate that the provided string is a well‑formed URL with a scheme and network location.
    """
    try:
        parsed = urlparse(url.strip())
        return all([parsed.scheme, parsed.netloc])
    except Exception:
        return False

def _validation_error(message: str):
    """
    Helper to create a consistent JSON error response for validation failures.
    """
    response = jsonify({"error": message})
    response.status_code = 400
    return response

@shorten_bp.route('/api/shorten', methods=['POST'])
def shorten():
    """
    POST /api/shorten
    Expects a JSON payload with a non‑empty string field ``url``.
    Performs validation on the URL structure before delegating to the shortening service.
    Returns:
        - 201 with JSON containing the shortened URL on success.
        - 400 with JSON error details on any validation failure.
    """
    # Ensure request content type is JSON
    if not request.is_json:
        return _validation_error("Request payload must be in JSON format.")

    # Parse JSON safely
    payload = request.get_json(silent=True)
    if payload is None:
        return _validation_error("Malformed JSON payload.")

    # Validate presence of 'url' key
    if 'url' not in payload:
        return _validation_error("Missing required field: 'url'.")

    url = payload['url']

    # Validate that 'url' is a non‑empty string
    if not isinstance(url, str):
        return _validation_error("Field 'url' must be a string.")
    if not url.strip():
        return _validation_error("Field 'url' cannot be empty or whitespace only.")

    # Validate URL structure (scheme and netloc required)
    if not _is_valid_url(url):
        return _validation_error("Field 'url' must be a valid URL with scheme and domain.")

    # At this point validation passed; proceed with shortening logic.
    try:
        short_code = Shortener.shorten(url)
    except Exception as exc:
        # If the underlying shortening service raises an error, return a generic 500.
        current_app.logger.exception("Error during URL shortening")
        return jsonify({"error": "Internal server error"}), 500

    return jsonify({"short_url": short_code}), 201