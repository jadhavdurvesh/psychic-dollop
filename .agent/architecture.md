## Relevant Architecture
- **Flask app** – defined in `src/app.py` (registered in the top‑level `app.py`).  
- **Route definition** – the POST `/api/shorten` endpoint lives in `src/shorten_route.py`.  
- **Data store** – `src/store.py` is called from the route after the URL has been validated.  
- **Tests** – `tests/test_app.py` exercises the `/api/shorten` endpoint and will verify the new validation behaviour.

## Files that need to change
| Path | Reason |
|------|--------|
| `src/shorten_route.py` | Contains the POST handler; we must add validation and return `400` on failure. |
| *(optional)* `src/app.py` | If the route imports a helper for error responses, we may add one here, but not required. |
| `tests/test_app.py` | May need to be updated only if the test expectations for the error payload differ from our implementation (usually not needed). |

## What to change & approach
1. **Import needed utilities** at the top of `src/shorten_route.py`  
   ```python
   from flask import request, jsonify
   from urllib.parse import urlparse
   ```

2. **Add a validation helper** (inline or separate function)  
   ```python
   def _is_valid_url(url: str) -> bool:
       try:
           result = urlparse(url)
           return all([result.scheme, result.netloc])
       except Exception:
           return False
   ```

3. **Update the POST handler** (`shorten`)  
   ```python
   @bp.post("/api/shorten")
   def shorten():
       payload = request.get_json(silent=True)
       if not payload or "url" not in payload:
           return jsonify({"error": "Missing 'url' in request body"}), 400

       url = payload["url"]
       if not isinstance(url, str) or not url.strip():
           return jsonify({"error": "URL must be a non‑empty string"}), 400

       if not _is_valid_url(url):
           return jsonify({"error": "Malformed URL"}), 400

       # existing logic – generate short code, store, and return response
       short_code = generate_code()
       store.save(short_code, url)
       return jsonify({"short_code": short_code}), 201
   ```

4. **Keep existing success flow unchanged** – the only new code is the early‑return checks.

5. **Run test suite** – ensure `tests/test_app.py` now passes for both valid and invalid payloads.

## What could break / needs careful handling
| Concern | Why it matters | Mitigation |
|---------|----------------|------------|
| **Missing JSON or wrong `Content-Type`** | `request.get_json(silent=True)` returns `None` when body isn’t JSON. | We explicitly check for `payload` being falsy and return a 400. |
| **Non‑string `url`** | `urlparse` expects a string; passing other types raises `TypeError`. | Guard with `isinstance(url, str)`. |
| **Very long or malicious URLs** | Not part of the current spec, but could cause performance issues. | The simple validation only checks scheme/netloc; deeper checks can be added later without breaking existing behaviour. |
| **Existing tests expecting a different error key** | If tests look for `message` instead of `error`, they will fail. | Align the JSON key (`error`) with what the tests assert; adjust tests if they are outdated. |
| **Import side‑effects** | Adding `urlparse` is safe; no new external dependencies. | No extra packages required, keeping `requirements.txt` unchanged. |
| **Route registration** | The route is already registered via Blueprint in `src/app.py`; adding validation does not affect registration. | No change needed in `src/app.py`. |

## Summary of changes
- **`src/shorten_route.py`** – import `jsonify`, `request`, `urlparse`; add `_is_valid_url`; prepend validation checks to the POST handler; return `400` with a clear JSON error payload when validation fails.  
- No other files need modification unless the test suite expects a different error structure.  

After implementing the above, the API will reject missing or malformed URLs with a `400 Bad Request` and a descriptive error message, satisfying the task requirements.