from flask import Flask

def create_app() -> Flask:
    """
    Factory function to create and configure the Flask application.
    """
    app = Flask(__name__)

    @app.route("/")
    def index():
        return "Hello, World!"

    # Additional route registrations or blueprint imports can be added here.
    return app

# Expose a ready‑to‑use app instance for testing and development.
app = create_app()