from threading import Lock
from typing import Optional


class URLStore:
    """
    Thread‑safe in‑memory store for short_code → original_url mappings.
    """

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._lock = Lock()

    def set(self, code: str, url: str) -> None:
        """Store a mapping."""
        with self._lock:
            self._store[code] = url

    def get(self, code: str) -> Optional[str]:
        """Retrieve the original URL for a short code, or ``None`` if not found."""
        with self._lock:
            return self._store.get(code)

    def exists(self, code: str) -> bool:
        """Check whether a short code already exists."""
        with self._lock:
            return code in self._store


# A singleton store used throughout the application.
store = URLStore()