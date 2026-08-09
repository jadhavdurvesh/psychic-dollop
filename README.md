# psychic-dollop

A minimal starter project. This exists mainly so the `multi-agent-lab`
GitHub Actions workflow has a real branch, a real test suite, and real
files to work with — give it a `--task` and it takes it from here.

## What's here

- `app.py` — one trivial function, so there's something to point a task at
- `tests/test_app.py` — one passing test, so `pytest -q` (the default
  Tester command) has something to run and pass on a clean checkout
- `requirements.txt` — empty for now, add real dependencies as the
  project grows

## Running the tests

```bash
pip install -r requirements.txt
pytest -q
```
