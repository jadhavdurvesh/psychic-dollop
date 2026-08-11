# Task Queue — psychic-dollop

This is a URL shortener API built incrementally by the multi-agent-lab
agents. Each task is one agent run. The `seed-tasks.yml` workflow in this
repo reads this file and creates GitHub Issues labeled `agent-task` — the
external workflow in `jadhavdurvesh/Multi-agent-lab` picks them up every
20 minutes and works on them automatically.

**To add work:** add a `- ` line below and push to main.

---

## App: URL Shortener

Tasks are ordered — each one builds on the previous. The agents work
through them one at a time, opening a PR for each.

- Replace app.py with a Flask app factory (create_app function, config object, app.run in __main__) and update requirements.txt to include flask
- Add a SQLite database layer in db.py with a urls table: id, short_code, original_url, created_at, click_count
- Add POST /api/shorten endpoint that accepts JSON with original_url and returns a generated 6-char alphanumeric short_code and the full short URL
- Add GET /<short_code> redirect endpoint that looks up the code, increments click_count, and returns a 301 redirect to the original URL or 404 if not found
- Add GET /api/stats/<short_code> endpoint that returns short_code, original_url, created_at, and click_count as JSON
- Add GET /api/links endpoint that returns all shortened links with their stats sorted by click_count descending
- Add input validation to POST /api/shorten: reject missing or malformed URLs, return 400 with a descriptive error message
- Add DELETE /api/links/<short_code> endpoint that removes a link and returns 204, or 404 if not found
- Add optional custom short code support to POST /api/shorten: if custom_code is provided in the request body use it instead of generating one, reject if already taken
- Add a simple HTML page served at GET / with a form to shorten URLs and a table showing all existing links with their click counts
- Write comprehensive pytest tests for all endpoints covering happy paths and error cases
