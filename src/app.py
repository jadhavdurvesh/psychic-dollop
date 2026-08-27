from flask import Flask, request, jsonify, redirect, abort
from src.store import add_link, get_link, clear_store

app = Flask(__name__)

@app.route("/links", methods=["POST"])
def create_link():
    if not request.is_json:
        return jsonify(error="Request body must be JSON"), 400
    data = request.get_json()
    url = data.get("url")
    code = data.get("code")

    if not url:
        return jsonify(error="Missing 'url' in request payload"), 400

    # Basic validation for URL – can be expanded
    if not (url.startswith("http://") or url.startswith("https://")):
        return jsonify(error="Invalid URL format"), 400

    try:
        stored_code = add_link(url, code)
    except ValueError as exc:
        return jsonify(error=str(exc)), 409

    return jsonify(code=stored_code, url=url), 201

@app.route("/<string:code>", methods=["GET"])
def resolve(code):
    link = get_link(code)
    if not link:
        return jsonify(error="Link not found"), 404
    return redirect(link, code=302)

# Expose a utility for tests if needed
@app.route("/_reset", methods=["POST"])
def reset():
    clear_store()
    return "", 204