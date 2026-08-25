from flask import Flask, request, jsonify, redirect, abort
from src.store import store, generate_short_code

app = Flask(__name__)

# Placeholder to keep legacy imports happy (tests import ``db``)
db = None

def greet() -> str:
    """Simple health‑check endpoint used by the tests."""
    return "Hello, World!"

@app.route("/", methods=["GET"])
def root():
    return greet()

@app.route("/<code>", methods=["GET"])
def redirect_short(code: str):
    """
    Redirect to the original URL associated with ``code``.
    Returns 404 if the code does not exist.
    """
    original_url = store.get(code)
    if original_url:
        return redirect(original_url)
    abort(404)

@app.route("/api/shorten", methods=["POST"])
def shorten():
    """
    Accept JSON payload ``{"url": "<original_url>"}``, generate a unique
    short code, store the mapping, and return both the code and the
    complete short URL.
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    code = generate_short_code()
    store[code] = original_url

    short_url = f"{request.host_url.rstrip('/')}/{code}"
    return jsonify({"code": code, "short_url": short_url}), 201

if __name__ == "__main__":
    app.run(debug=True)