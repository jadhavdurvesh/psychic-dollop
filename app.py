"""Flask application for URL shortening service.

Provides:
- `greet` function for basic health check (used in tests).
- `GET /<short_code>` endpoint that redirects to the original URL, increments click count,
  and returns a 301 response. Returns 404 if the short code does not exist.
"""

from flask import Flask, request, jsonify, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
# Use a simple SQLite database file for persistence.
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Url(db.Model):
    __tablename__ = "urls"
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    click_count = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Url {self.short_code} -> {self.original_url}>"

# Ensure tables are created before the first request.
@app.before_first_request
def create_tables():
    db.create_all()

def generate_short_code(length: int = 6) -> str:
    """Generate a random alphanumeric short code."""
    chars = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choice(chars) for _ in range(length))
        if not Url.query.filter_by(short_code=code).first():
            return code

# ---------------------------------------------------------------------------
# Helper / test endpoint
# ---------------------------------------------------------------------------

def greet() -> str:
    """Simple function used by the test suite to verify import works.

    Returns a static greeting string.
    """
    return "Hello, World!"

# ---------------------------------------------------------------------------
# API endpoints (existing ones would be placed here)
# ---------------------------------------------------------------------------
# Example placeholder for a URL‑creation endpoint.  The actual implementation
# is not required for the current test suite but is kept to illustrate a
# realistic service.
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json() or {}
    original = data.get("url")
    if not original:
        return jsonify({"error": "Missing 'url' in request body"}), 400
    short_code = generate_short_code()
    new_url = Url(original_url=original, short_code=short_code)
    db.session.add(new_url)
    db.session.commit()
    return jsonify({"short_code": short_code}), 201

# ---------------------------------------------------------------------------
# Redirect endpoint – must be defined after all explicit routes to avoid
# shadowing.
# ---------------------------------------------------------------------------
@app.route("/<short_code>", methods=["GET"])
def redirect_short_code(short_code: str):
    """Redirect to the original URL associated with *short_code*.

    - If the code does not exist, abort with a 404.
    - Increment the click counter and persist the change.
    - Issue a 301 (Moved Permanently) redirect to the stored original URL.
    """
    url_record = Url.query.filter_by(short_code=short_code).first()
    if not url_record:
        abort(404)
    # Increment click count and commit.
    url_record.click_count += 1
    db.session.commit()
    return redirect(url_record.original_url, code=301)

# ---------------------------------------------------------------------------
# Application entry point (used when running `python app.py` directly).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
