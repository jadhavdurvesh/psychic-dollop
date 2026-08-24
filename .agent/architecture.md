## Architecture Overview
The project is a simple Flask‑SQLAlchemy web service that stores **short‑code → original‑URL** mappings.  
- **`app.py`** creates the Flask app, configures the DB, defines the data model (`Url`) and registers the HTTP endpoints.  
- **`tests/test_app.py`** drives the required behaviour (creation, lookup, redirection, error handling).  

The architecture is a classic **single‑module Flask app**:

```
app.py
 ├─ Flask app instance
 ├─ SQLAlchemy db (db = SQLAlchemy(app))
 ├─ Url model (id, short_code, original_url, click_count, …)
 └─ Existing route functions (e.g. POST /shorten)
```

To add the redirect functionality we only need to extend `app.py` with a new route that:

1. Receives a **dynamic path component** (`/<short_code>`).  
2. Queries the `Url` table for that `short_code`.  
3. If found, increments `click_count`, commits, and returns a **301 Moved Permanently** response pointing at `original_url`.  
4. If not found, returns a **404 Not Found**.

---

## Files that need to be touched
| Path | Reason |
|------|--------|
| `app.py` | Holds the Flask app, DB model, and existing endpoints – the only place to add the new route and any required imports. |
| `tests/test_app.py` | May need minor updates if the test suite expects a particular response format (e.g., `Location` header). Usually just to verify the new behavior, but **no code changes** are required unless the test suite is currently failing. |
| `README.md` (optional) | If you want to document the new endpoint for developers/users. Not required for functional change. |

---

## What to change & concrete implementation steps

1. **Import needed Flask helpers** at the top of `app.py` (if not already present):
   ```python
   from flask import redirect, abort
   ```

2. **Add the redirect route** *after* any more‑specific routes (e.g., after `/shorten`, `/stats`, etc.) to avoid it swallowing those paths:
   ```python
   @app.route('/<short_code>', methods=['GET'])
   def redirect_short_code(short_code):
       # Look up the short code
       url_entry = Url.query.filter_by(short_code=short_code).first()
       if url_entry is None:
           # No such code → 404
           abort(404)

       # Increment click count atomically
       url_entry.click_count = Url.click_count + 1
       db.session.commit()

       # 301 redirect to the original URL
       return redirect(url_entry.original_url, code=301)
   ```

   *Key points*:
   - Use `abort(404)` to generate the proper Flask 404 response.
   - Increment `click_count` **before** committing; using `url_entry.click_count += 1` works as well.
   - `redirect(..., code=301)` sends a permanent redirect; Flask sets the `Location` header automatically.

3. **Guard against empty or reserved short codes** (optional but recommended):
   ```python
   if short_code in {'static', 'favicon.ico', ...}:
       abort(404)
   ```
   This prevents the generic route from colliding with static files or future endpoints.

4. **Run the test suite** to ensure nothing else broke:
   ```bash
   pytest -q
   ```

5. **(Optional) Update documentation** in `README.md`:
   ```markdown
   ## GET /<short_code>
   Redirects to the original URL stored for `short_code`.  
   - **Response**: `301 Moved Permanently` with `Location` header set to the original URL.  
   - **Error**: `404 Not Found` if the code does not exist.
   ```

---

## Risks / What could break

| Issue | Why it matters | Mitigation |
|-------|----------------|------------|
| **Route shadowing** – the new `/<short_code>` route may capture requests meant for other endpoints (`/health`, `/static/*`, etc.). | Flask matches the first rule that fits; a catch‑all route placed too early can hide later routes. | Place the new route **after** all explicit routes, or add a whitelist/negative check for reserved words. |
| **Database race condition** – simultaneous clicks could cause lost increments. | `click_count = click_count + 1` followed by `commit()` is safe for SQLite in a single‑process dev server, but high concurrency may need `with_for_update()` or atomic DB functions. | For this simple app, accept the risk; note in comments that production would need a more robust counter (e.g., `UPDATE Url SET click_count = click_count + 1 WHERE id = …`). |
| **Invalid URLs** – stored `original_url` might be malformed; Flask’s `redirect` will still emit a `Location` header, but browsers may reject it. | Could lead to confusing redirects or security issues. | Validation is already performed when creating entries (assume existing code does that). |
| **Missing import** – forgetting to import `redirect`/`abort` causes a `NameError`. | Tests will fail. | Add imports at the top; run lint/test to confirm. |
| **Commit failure** – DB commit could raise an exception (e.g., DB locked). | 500 error instead of 301/404. | Wrap commit in a try/except, roll back on error, and return a 500 if needed (optional). |

---

## Summary of changes

```diff
--- a/app.py
+++ b/app.py
@@
 from flask import Flask, request, jsonify, redirect, abort
@@
 # existing code (model, other routes)
@@
 @app.route('/<short_code>', methods=['GET'])
 def redirect_short_code(short_code):
     # 1️⃣ Look up the short code
-    url_entry = Url.query.filter_by(short_code=short_code).first()
-    if url_entry is None:
-        abort(404)
+    url_entry = Url.query.filter_by(short_code=short_code).first()
+    if url_entry is None:
+        abort(404)
 
-    # 2️⃣ Increment click count
-    url_entry.click_count += 1
-    db.session.commit()
+    # 2️⃣ Increment click count atomically
+    url_entry.click_count = Url.click_count + 1
+    db.session.commit()
 
-    # 3️⃣ Return a permanent redirect
-    return redirect(url_entry.original_url, code=301)
+    # 3️⃣ Return a permanent redirect (301)
+    return redirect(url_entry.original_url, code=301)
```

After applying the diff, run the test suite; the new endpoint should satisfy the required behavior:

- `GET /abc123` → 301 redirect to stored URL, `click_count` increased by 1.  
- `GET /nonexistent` → 404 response.  

That’s all that’s needed to fulfill the task.