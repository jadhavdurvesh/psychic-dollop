import pytest
from app import reset_store

@pytest.fixture(autouse=True)
def clear_links_store():
    """
    Automatically clear the in‑memory link store before each test.
    """
    reset_store()