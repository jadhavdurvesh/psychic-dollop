from threading import Lock
from typing import List

from src.models import Link

# In‑memory storage; a real implementation would use a DB.
_links: List[Link] = []
_lock = Lock()
_next_id = 1


def add_link(
    original_url: str,
    short_code: str,
    click_count: int = 0,
    created_at: "datetime | None" = None,
) -> Link:
    """
    Create a new Link, assign a unique integer ``id`` and store it.
    """
    global _next_id
    with _lock:
        link = Link(
            id=_next_id,
            original_url=original_url,
            short_code=short_code,
            click_count=click_count,
            created_at=created_at,
        )
        _links.append(link)
        _next_id += 1
    return link


def get_all_links_sorted() -> List[Link]:
    """
    Return all stored links sorted by ``click_count`` descending.
    """
    with _lock:
        # ``sorted`` creates a new list; callers can modify it safely.
        return sorted(_links, key=lambda l: l.click_count, reverse=True)


def clear_links() -> None:
    """
    Helper used in tests to reset the in‑memory store.
    """
    global _links, _next_id
    with _lock:
        _links = []
        _next_id = 1