import threading
import itertools
from urllib.parse import urlparse

# Thread‑safe in‑memory storage for shortened URLs.
_lock = threading.Lock()
_id_counter = itertools.count(1)
_code_to_url = {}

def _int_to_base62(num: int) -> str:
    """Convert a positive integer to a base‑62 string."""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num == 0:
        return chars[0]
    result = []
    base = len(chars)
    while num:
        num, rem = divmod(num, base)
        result.append(chars[rem])
    return "".join(reversed(result))

def shorten_url(original_url: str) -> str:
    """
    Store *original_url* and return a short code.

    The function is thread‑safe and guarantees a unique short code for each call.
    """
    if not isinstance(original_url, str):
        raise TypeError("original_url must be a string")
    with _lock:
        # Generate a unique integer then convert to a base‑62 string.
        new_id = next(_id_counter)
        short_code = _int_to_base62(new_id)
        _code_to_url[short_code] = original_url
    return short_code

def get_original_url(short_code: str) -> str | None:
    """
    Retrieve the original URL for *short_code*.
    Returns ``None`` if the code does not exist.
    """
    return _code_to_url.get(short_code)

def reset_storage() -> None:
    """
    Helper used in tests to clear the in‑memory store.
    """
    global _code_to_url, _id_counter
    with _lock:
        _code_to_url = {}
        _id_counter = itertools.count(1)