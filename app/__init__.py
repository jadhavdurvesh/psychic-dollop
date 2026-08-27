import os
from flask import Flask

def create_app():
    """
    Application factory that creates and configures the Flask app.
    Registers the blueprint that contains the link creation and redirect routes.
    """
    app = Flask(__name__)
    app.config.from_mapping(
        TESTING=os.getenv("FLASK_TESTING", False)
    )

    # Register blueprints
    from .routes import links_bp, reset_store
    app.register_blueprint(links_bp)

    # Expose reset_store at the app level for testing convenience
    app.reset_store = reset_store

    return app