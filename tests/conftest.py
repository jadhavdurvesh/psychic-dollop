import pytest
from app import app, db

@pytest.fixture
def client():
    """
    Provides a Flask test client for making HTTP requests.
    """
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clear_in_memory_store():
    """
    Clears the in‑memory link store before each test to guarantee isolation.
    """
    db["url_to_code"].clear()
    db["code_to_url"].clear()