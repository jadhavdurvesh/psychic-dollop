import pytest
from app import app as flask_app
from store import store

@pytest.fixture
def app():
    """Provide the Flask application instance to pytest‑flask."""
    return flask_app

@pytest.fixture(autouse=True)
def clear_store():
    """Clear the in‑memory store before each test to guarantee isolation."""
    store.clear()