from flask import Blueprint, request, jsonify, redirect, abort, current_app
import string
import random

# In‑memory store for short code → original URL
_LINK_STORE = {}

def _generate_code(length=6):
    """Generate a random alphanumeric code of given length."""
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if code not in _LINK_STORE:
            return code

def reset_store():
    """Clear the in‑memory link store. Used by tests to guarantee isolation."""
    _LINK_STORE.clear()

def _is_valid_code(code):
    """A valid code consists only of alphanumerics and is non‑empty."""
    return bool(code) and code.isalnum()

links_bp = Blueprint('links', __name__)

@links_bp.route('/links', methods=['POST'])
def create_link():
    """
    Create a new shortened link.
    Expected JSON payload: {"url": "<target_url>", "code": "<optional_custom_code>"}
    Returns JSON with the assigned code.
    """
    if not request.is_json:
        return jsonify(error="Invalid or missing JSON payload"), 400

    data = request.get_json(silent=True) or {}
    url = data.get('url')
    code = data.get('code')

    if not url or not isinstance(url, str):
        return jsonify(error="Missing or invalid 'url' field"), 400

    if code:
        if not isinstance(code, str) or not _is_valid_code(code):
            return jsonify(error="Invalid custom code"), 400
        if code in _LINK_STORE:
            return jsonify(error="Code already exists"), 409
    else:
        code = _generate_code()

    _LINK_STORE[code] = url
    return jsonify(code=code), 201

@links_bp.route('/<code>', methods=['GET'])
def redirect_link(code):
    """
    Redirect to the original URL based on the short code.
    """
    if not _is_valid_code(code):
        return jsonify(error="Malformed code"), 400

    url = _LINK_STORE.get(code)
    if url is None:
        return jsonify(error="Code not found"), 404

    return redirect(url, code=302)