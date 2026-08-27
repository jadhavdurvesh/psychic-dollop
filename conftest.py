import pytest
from src.store import clear_store

@pytest.fixture(autouse=True)
def reset_store():
    """Clear the in‑memory link store before each test to guarantee isolation."""
    clear_store()