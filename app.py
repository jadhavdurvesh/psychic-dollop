from flask import Flask, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
import string
import random

# Initialize Flask app and database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Simple model for storing shortened URLs
class ShortUrl(db.Model):
    __tablename__ = "short_urls"
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)

    def __repr__(self):
        return f"<ShortUrl {self.short_code} -> {self.original_url}>"

# Create tables
with app.app_context():
    db.create_all()

# Helper to generate a random short code
def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    while True:
        code = "".join(random.choices(characters, k=length))
        if not ShortUrl.query.filter_by(short_code=code).first():
            return code

# Greeting endpoint used by tests
def greet() -> str:
    """Simple greeting function required by the test suite."""
    return "Hello, World!"

# Register blueprint for shortening routes
from src.shorten_route import shorten_bp
app.register_blueprint(shorten_bp, url_prefix="/api")

# Redirect endpoint (used by test_redirect)
@app.route("/<short_code>")
def redirect_short_url(short_code: str):
    entry = ShortUrl.query.filter_by(short_code=short_code).first_or_404()
    return redirect(entry.original_url)

# Expose objects for tests
__all__ = ["app", "db", "greet"]