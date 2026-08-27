from typing import Dict

_links: Dict[str, str] = {}
import uuid

def _generate_code() -> str:
    return uuid.uuid4().hex[:6]

def add_link(url: str, code: str = None) -> str:
    """Add a URL to the store. Returns the short code.

    Raises:
        ValueError: If the provided code already exists.
    """
    if code:
        if code in _links:
            raise ValueError("Code already exists")
        _links[code] = url
        return code
    # generate a unique code
    while True:
        gen = _generate_code()
        if gen not in _links:
            _links[gen] = url
            return gen

def get_link(code: str) -> str:
    return _links.get(code)

def clear_store() -> None:
    """Remove all entries – used by test fixtures."""
    _links.clear()