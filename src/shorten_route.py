import string
import secrets

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from src.store import store

router = APIRouter()

# Characters allowed in the generated short code.
ALPHANUM = string.ascii_letters + string.digits
CODE_LENGTH = 6  # Adjust length as needed for collision probability.


def _generate_unique_code() -> str:
    """
    Generate a random alphanumeric code that does not already exist in the store.
    """
    while True:
        candidate = "".join(secrets.choice(ALPHANUM) for _ in range(CODE_LENGTH))
        if not store.exists(candidate):
            return candidate


@router.post("/api/shorten")
async def shorten(request: Request):
    """
    Create a short URL for a given ``original_url``.
    Expected JSON payload: ``{"original_url": "<url>"}``.
    Returns JSON with ``short_code`` and ``short_url``.
    """
    # ------------------------------------------------------------------
    # Validate JSON payload.
    # ------------------------------------------------------------------
    try:
        payload = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    original_url = payload.get("original_url")
    if not isinstance(original_url, str) or not original_url.strip():
        raise HTTPException(
            status_code=400,
            detail="original_url must be a non‑empty string",
        )

    # ------------------------------------------------------------------
    # Generate a unique short code and store the mapping.
    # ------------------------------------------------------------------
    code = _generate_unique_code()
    store.set(code, original_url.strip())

    # ------------------------------------------------------------------
    # Build the absolute short URL using the request's base URL.
    # ------------------------------------------------------------------
    base_url = str(request.base_url).rstrip("/")  # Normalise trailing slash.
    short_url = f"{base_url}/{code}"

    return JSONResponse(content={"short_code": code, "short_url": short_url})