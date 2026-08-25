import random
import string

# In‑memory mapping from short code to original URL
store: dict[str, str] = {}

def generate_short_code(length: int = 6) -> str:
    """
    Generate a random alphanumeric short code that is not already
    present in the global ``store``. The default length of 6 characters
    provides ~56 billion possible combinations which is sufficient for
    an in‑memory demo.
    """
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choices(characters, k=length))
        if code not in store:
            return code