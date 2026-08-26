import threading
from typing import Optional, List
from datetime import datetime

# Import inside functions to avoid circular imports
# from src.models import Link

class URLStore:
    """
    Thread‑safe in‑memory store for short_code → Link mappings.
    """

    def __init__(self) -> None:
        self._store: dict[str, "Link"] = {}
        self._lock = threading.Lock()
        self._next_id: int = 1  # incremental id for Link instances

    def _generate_id(self) -> int:
        """Generate a new incremental id for a Link."""
        with self._lock:
            cur = self._next_id
            self._next_id += 1
            return cur

    def get(self, code: str) -> Optional["Link"]:
        """Return the Link for *code* or ``None`` if not present."""
        with self._lock:
            return self._store.get(code)

    def set(self, code: str, link: "Link") -> None:
        """Persist *code* → *link* mapping."""
        with self._lock:
            self._store[code] = link

    def exists(self, code: str) -> bool:
        """Check whether *code* already exists in the store."""
        with self._lock:
            return code in self._store

    def get_all_links_sorted(self) -> List["Link"]:
        """
        Return a list of all Link objects ordered by ``click_count`` descending.
        """
        with self._lock:
            return sorted(self._store.values(), key=lambda l: l.click_count, reverse=True)


# A single global store instance used by the application.
store = URLStore()


# Helper functions used by the Flask app – kept thin to avoid circular imports.
def add_url(short_code: str, original_url: str, click_count: int = 0, created_at: Optional[datetime] = None) -> None:
    """
    Create a new ``Link`` and store it.
    """
    from src.models import Link  # Local import to avoid circular reference

    link = Link(
        id=store._generate_id(),
        short_code=short_code,
        original_url=original_url,
        click_count=click_count,
        created_at=created_at or datetime.utcnow(),
    )
    store.set(short_code, link)


def get_url(short_code: str) -> Optional["Link"]:
    """
    Retrieve a Link object for the given short_code.
    """
    return store.get(short_code)


def exists(short_code: str) -> bool:
    """
    Check whether a short_code already exists.
    """
    return store.exists(short_code)


def get_all_links_sorted() -> List["Link"]:
    """
    Public wrapper around the store's sorting method.
    """
    return store.get_all_links_sorted()