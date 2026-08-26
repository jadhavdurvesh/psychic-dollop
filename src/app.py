from flask import Flask

from .store import init_db
from .links_route import links_bp

def create_app():
    app = Flask(__name__)

    # Initialise the database (tables, etc.)
    init_db()

    # Register blueprints / routes
    app.register_blueprint(links_bp)

    # If there are other blueprints they would be registered here as well.
    return app