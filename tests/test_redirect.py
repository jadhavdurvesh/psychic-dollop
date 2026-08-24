import pytest
from app import app, db, Url

@pytest.fixture(autouse=True)
def _setup_and_teardown():
    """Create a fresh in‑memory database for each test.
    The Flask app is configured to use SQLite in‑memory, so we just need to
    create the tables before each test and drop them afterwards.
    """
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_redirect_success():
    short_code = 'abc123'
    original = 'https://example.com/some/path'
    # Insert a URL record.
    with app.app_context():
        url = Url(short_code=short_code, original_url=original, click_count=0)
        db.session.add(url)
        db.session.commit()
    client = app.test_client()
    response = client.get(f'/{short_code}')
    assert response.status_code == 301
    assert response.headers['Location'] == original
    # Verify click_count incremented.
    with app.app_context():
        refreshed = Url.query.filter_by(short_code=short_code).first()
        assert refreshed.click_count == 1

def test_redirect_not_found():
    client = app.test_client()
    response = client.get('/nonexistentcode')
    assert response.status_code == 404

def test_reserved_route_not_caught():
    client = app.test_client()
    response = client.get('/health')
    # Health endpoint is explicitly defined, so it should return 200, not be
    # captured by the generic short‑code route.
    assert response.status_code == 200
    assert response.data == b'OK'
