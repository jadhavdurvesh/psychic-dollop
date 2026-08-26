import threading
from typing import Optional


class URLStore:
    """
    Thread‑safe in‑memory store for short_code → original_url mappings.
    """

    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._lock = threading.Lock()

    def get(self, code: str) -> Optional[str]:
        """Return the original URL for *code* or ``None`` if not present."""
        with self._lock:
            return self._store.get(code)

    def set(self, code: str, url: str) -> None:
        """Persist *code* → *url* mapping."""
        with self._lock:
            self._store[code] = url

    def exists(self, code: str) -> bool:
        """Check whether *code* already exists in the store."""
        with self._lock:
            return code in self._store


# A single global store instance used by the application.
store = URLStore()