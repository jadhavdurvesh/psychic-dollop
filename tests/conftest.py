import pytest
from app import create_app, reset_store

@pytest.fixture
def app():
    """
    Provide a Flask app instance for pytest‑flask.
    """
    app = create_app()
    # Ensure the store is cleared for each test run
    with app.app_context():
        reset_store()
    yield app

@pytest.fixture(autouse=True)
def clear_store():
    """
    Automatically clear the in‑memory store before every test function.
    """
    reset_store()