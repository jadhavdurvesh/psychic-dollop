## Relevant Architecture

| File | Role |
|------|------|
| **app.py** | Creates the Flask app and registers route modules. |
| **src/redirect_route.py** | Handles `GET /<short_code>` – looks up a stored mapping and redirects. |
| **src/*** (new) **store.py** | Central in‑memory store (`url_map`) shared by all route handlers. |
| **src/shorten_route.py** (new) | Will expose `POST /api/shorten` that creates a short‑code, stores the mapping and returns JSON. |
| **tests/*** | Verify both redirect and new shorten behavior. |

The existing `redirect_route` already needs a storage location for the code‑→‑URL map. By introducing a dedicated `store.py` we give both the redirect and the new shorten endpoint a single source of truth without changing the public API.

## Files that need to be changed / added

| Path | Change |
|------|--------|
| **src/store.py** *(new)* | ```python\nurl_map: dict[str, str] = {}\n``` |
| **src/redirect_route.py** | Import `url_map` from `src.store` (instead of any private dict) and use it for look‑ups. |
| **src/shorten_route.py** *(new)* | Implement the POST endpoint, generate a unique short code, store it in `url_map`, and return `short_code` & `short_url`. |
| **app.py** | Register the new route module (`from src.shorten_route import register_routes as register_shorten; register_shorten(app)`). |
| **tests/test_app.py** (if needed) | No code change – the existing tests will now hit the new endpoint. |

## What needs to be changed & approach

1. **Create a shared store** (`src/store.py`).  
   - Simple dict is sufficient for unit‑test scope.  
   - Exported as `url_map`.

2. **Update redirect route** to use the shared store:  
   ```python
   from src.store import url_map
   # existing logic stays the same, just reference url_map
   ```

3. **Add shorten route** (`src/shorten_route.py`):  
   - Validate JSON payload (`original_url` required).  
   - Generate a random alphanumeric code (`6` chars by default).  
   - Ensure uniqueness by looping if the generated code already exists in `url_map`.  
   - Store mapping `url_map[code] = original_url`.  
   - Build `short_url` using the request’s host (`request.host_url.rstrip('/') + '/' + code`).  
   - Return JSON `{ "short_code": code, "short_url": short_url }` with status **200**.  
   - Return **400** with an error JSON if payload is malformed.

4. **Register the new route** in `app.py` after the existing route registration so both GET and POST work.

## What could break / needs careful handling

| Issue | Mitigation |
|-------|------------|
| **Collision of short codes** – extremely low but possible. | Loop until a fresh code is generated (`while code in url_map`). |
| **`request.host_url` formatting** – may already end with `/`. | Use `rstrip('/')` before appending the code to avoid double slashes. |
| **Missing/invalid JSON** – Flask’s `request.get_json()` returns `None` on bad payload. | Explicitly check for `None` and missing `original_url`, return 400 with clear error. |
| **Thread‑safety** – In‑memory dict is not safe for production concurrency.