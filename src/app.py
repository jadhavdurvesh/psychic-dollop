from flask import Flask, request, jsonify, redirect, abort, url_for
import string
import random

from src.store import add_url, get_url, exists

app = Flask(__name__)

def _generate_unique_code(length: int = 6) -> str:
    """Generate a unique short code consisting of alphanumeric characters."""
    chars = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(chars, k=length))
        if not exists(code):
            return code

@app.route('/<string:short_code>', methods=['GET'])
def redirect_short_url(short_code: str):
    """
    Redirect to the original URL based on the provided short_code.
    Returns 404 if the short_code is not found.
    """
    url_obj = get_url(short_code)
    if url_obj is None:
        abort(404, description="Short URL not found")
    return redirect(url_obj.original_url, code=302)

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    """
    Accept JSON payload with a key 'url' and create a short URL.
    Returns JSON containing the generated short code and the full short URL.
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON payload"}), 400

    data = request.get_json()
    original_url = data.get('url')

    if not original_url or not isinstance(original_url, str):
        return jsonify({"error": "Field 'url' must be a non‑empty string"}), 400

    # Generate a unique short code and store the mapping
    short_code = _generate_unique_code()
    add_url(short_code, original_url)

    # Build the full short URL using the request host information
    short_url = f"{request.host_url.rstrip('/')}/{short_code}"
    return jsonify({"code": short_code, "short_url": short_url}), 201

if __name__ == '__main__':
    # When run directly, start the development server
    app.run(host='0.0.0.0', port=5000, debug=True)