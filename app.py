from flask import Flask

from src.redirect_route import register_redirect
from src.shorten_route import bp as shorten_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Register the redirect endpoint (GET /<code>)
    register_redirect(app)

    # Register the URL‑shortening API (POST /api/shorten)
    app.register_blueprint(shorten_bp)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run()