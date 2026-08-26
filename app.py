from flask import Flask
from store import Store
from routes.links_route import links_bp

def create_app():
    app = Flask(__name__)
    store = Store()
    # Attach the store to the app for easy access in routes
    app.store = store

    # Register blueprints
    app.register_blueprint(links_bp, url_prefix="/api")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)