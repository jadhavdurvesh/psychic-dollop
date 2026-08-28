# Existing imports and class definitions
# -------------------------------------

# (Assuming the original file already defines a class `Store`)

class Store:
    """
    Simple in‑memory key‑value store used by the test suite.
    """
    def __init__(self):
        self._data = {}

    def set(self, key, value):
        """Store a value under the given key."""
        self._data[key] = value

    def get(self, key, default=None):
        """Retrieve a value by key, returning `default` if missing."""
        return self._data.get(key, default)

    def delete(self, key):
        """Remove a key from the store if it exists."""
        self._data.pop(key, None)

    def clear(self):
        """Remove all entries from the store."""
        self._data.clear()

    def items(self):
        """Return a view of the store's items."""
        return self._data.items()


# Export a singleton instance named `store` for test imports
# ---------------------------------------------------------

# The test suite expects `from store import store`. Providing a module‑level
# instance satisfies that contract while keeping the original `Store` class
# available for any advanced usage.
store = Store()

__all__ = ["Store", "store"]