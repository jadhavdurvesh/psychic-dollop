# Task Queue — psychic-dollop

The multi-agent-lab external workflow picks tasks from this file every
20 minutes. Edit this file and push to main — the seed-tasks workflow
creates GitHub Issues automatically.

## URL Shortener — remaining tasks

The app already has: Flask app, SQLAlchemy, URL model, POST /shorten,
GET /<short_code> redirect. These are what remains:

- Add POST /api/shorten endpoint that accepts JSON with original_url field and returns short_code and short_url in response
- Add GET /api/stats/<short_code> endpoint that returns short_code, original_url, created_at, and click_count as JSON, or 404 if not found
- Add GET /api/links endpoint that returns all shortened links sorted by click_count descending as a JSON array
- Add DELETE /api/links/<short_code> endpoint that removes a link and returns 204, or 404 if not found
- Add input validation to POST /api/shorten that rejects missing or malformed URLs and returns 400 with a descriptive error message
- Add a simple HTML page served at GET / with a form to shorten URLs and a table showing all existing links with their stats
- Write comprehensive pytest tests for all endpoints covering happy paths and error cases using pytest-flask fixtures
