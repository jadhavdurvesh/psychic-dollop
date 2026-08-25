from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from src.store import store

router = APIRouter()


@router.get("/{short_code}")
def redirect(short_code: str):
    """
    Resolve ``short_code`` to its original URL and issue a redirect.
    """
    original_url = store.get(short_code)
    if original_url is None:
        raise HTTPException(status_code=404, detail="Short code not found")
    return RedirectResponse(url=original_url)