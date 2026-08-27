from flask import Flask, request, jsonify, redirect, abort

app = Flask(__name__)

# In‑memory store for short code → target URL mappings
links_store = {}


def reset_store():
    """Clear the in‑memory link store. Used by tests to ensure isolation."""
    links_store.clear()


def greet():
    """Simple health‑check/helper function used by tests."""
    return "Hello, World!"


@app.route("/links", methods=["POST"])
def create_link():
    """
    Create a new short link.

    Expected JSON payload:
    {
        "code": "<short_code>",
        "url": "<target_url>"
    }
    """
    if not request.is_json:
        return jsonify({"error": "Invalid JSON payload"}), 400

    data = request.get_json()
    code = data.get("code")
    url = data.get("url")

    if not code or not url:
        return jsonify({"error": "Both 'code' and 'url' are required"}), 400

    if code in links_store:
        return jsonify({"error": f"Code '{code}' already exists"}), 409

    links_store[code] = url
    return jsonify({"message": f"Link created for code '{code}'"}), 201


@app.route("/<code>", methods=["GET"])
def redirect_link(code):
    """
    Redirect to the stored URL for the given short code.
    """
    url = links_store.get(code)
    if not url:
        abort(404, description=f"No link found for code '{code}'")
    return redirect(url, code=302)


# Optional: expose the Flask app when running directly
if __name__ == "__main__":
    app.run(debug=True)