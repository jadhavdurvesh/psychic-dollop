## Architecture Overview
The project is a Flask‑based URL‑shortener:

| File | Role |
|------|------|
| **src/app.py** – creates the Flask app and registers route modules. |
| **src/shorten_route.py** – `POST /api/shorten` (creates a new short link). |
| **src/redirect_route.py** – `GET /<code>` (redirects and increments `click_count`). |
| **src/store.py** – persistence layer (SQLAlchemy or an in‑memory store). |
| **models.py** – defines the `Link` model (fields: `id`, `original_url`, `short_code`, `click_count`, …). |
| **tests/** – integration tests that hit the public API. |

The new **GET /api/links** endpoint will sit alongside the existing API routes and will query the store for all `Link` records, sort them by `click_count` descending, and return a JSON array.

---

## Files that need to be touched
| Path | Reason |
|------|--------|
| **src/app.py** | Register the new route (or import a new route module). |
| **src/links_route.py** *(new file)* | Holds the implementation of `GET /api/links`. |
| **src/store.py** | Add a helper `get_all_links_sorted()` that returns the ordered list. |
| **models.py** | Ensure `Link` can be serialised (`to_dict` method) – add if missing. |
| **tests/test_app.py** | (Likely already expects the endpoint; no change needed unless the test checks field names.) |

---

## Concrete Changes

### 1. `src/links_route.py` *(new)*
```python
# src/links_route.py
from flask import Blueprint, jsonify
from . import store  # store module lives in src/store.py
from ..models import Link  # adjust import if models live at project root

bp = Blueprint('links', __name__)

@bp.route('/api/links', methods=['GET'])
def list_links():
    """
    Return all shortened links sorted by click_count (desc).
    """
    links = store.get_all_links_sorted()
    # Convert each Link object to a plain dict for JSON serialization
    data = [link.to_dict() for link in links]
    return jsonify(data), 200
```

*Why a Blueprint?*  
All existing route files (`shorten_route.py`, `redirect_route.py`) already use a `Blueprint` pattern (typical for this repo). Adding a new blueprint keeps the style consistent and lets `app.py` simply register it.

### 2. Register the Blueprint in `src/app.py`
```python
# src/app.py (excerpt)
from flask import Flask
# existing imports …
from .shorten_route import bp as shorten_bp
from .redirect_route import bp as redirect_bp
from .links_route import bp as links_bp   # <-- NEW

def create_app():
    app = Flask(__name__)

    # existing config / db init …
    app.register_blueprint(shorten_bp)
    app.register_blueprint(redirect_bp)
    app.register_blueprint(links_bp)       # <-- NEW

    return app
```

### 3. Add the store helper in `src/store.py`
```python
# src/store.py (excerpt)
from ..models import Link   # adjust import path as needed
# existing imports …

def get_all_links_sorted():
    """
    Return a list of Link objects ordered by click_count descending.
    """
    # If using SQLAlchemy:
    return Link.query.order_by(Link.click_count.desc()).all()

    # If using an in‑memory dict called _links:
    # return sorted(_links.values(),
    #               key=lambda l: l.click_count,
    #               reverse=True)
```

*If the project currently uses a different ORM or a simple dict, replace the body accordingly. The function must return a **list of `Link` objects**.*

### 4. Ensure `Link` can be JSON‑serialised (`models.py`)
```python
# models.py (excerpt)
class Link(db.Model):          # or a plain class if not using SQLAlchemy
    __tablename__ = 'links'
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String, nullable=False)
    short_code = db.Column(db.String, unique=True, nullable=False)
    click_count = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Return a JSON‑friendly dict representation."""
        return {
            "id": self.id,
            "original_url": self.original_url,
            "short_code": self.short_code,
            "click_count": self.click_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
```
*If `to_dict` already exists, no change needed. If not, add it.*

---

## What Could Break / Needs Careful Handling

| Area | Risk | Mitigation |
|------|------|------------|
| **Import Paths** | The repo mixes top‑level `app.py` with `src/app.py`. Use relative imports consistent with the rest of the code (`from . import store` vs `from src.store import …`). | Verify existing route files for their import style and copy it. |
| **ORM vs In‑Memory Store** | `store.get_all_links_sorted()` must return `Link` objects that have `to_dict`. If the store currently returns raw dicts, adjust the route accordingly (skip `to_dict`). | Look at the existing `store` implementation; mirror its return type. |
| **Circular Imports** | Adding `from ..models import Link` inside `store.py` (or vice‑versa) could create a cycle. | Keep model import inside functions or place the helper in `store.py` where the model is already imported. |
| **JSON Serialisation of datetime** | `created_at` may be a `datetime` object; default `jsonify` cannot handle it. The `to_dict` method converts it to ISO‑8601 string. | Ensure `to_dict` does the conversion (as shown). |
| **Duplicate Blueprint Names** | Blueprint name `'links'` must be unique across the app. | Use a distinct name (`'links'`) that isn’t already taken. |
| **Tests Expecting Specific Fields** | If tests assert on particular keys (e.g., `url`, `code`), our dict keys must match. | Align `to_dict` keys with what the test suite checks; adjust names if needed. |
| **Performance** | Sorting in Python on a huge list could be heavy. | When using a real DB, leverage `ORDER BY` as shown; for in‑memory, it’s acceptable for the test dataset. |

---

## Summary of Steps

1. **Create `src/links_route.py`** with a Blueprint exposing `GET /