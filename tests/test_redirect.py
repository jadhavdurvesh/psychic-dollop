import pytest
from app import app, db
from models import Url

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

def test_redirect_success(client):
    # Create a short URL entry directly in the DB
    url = Url(original_url='https://example.com', short_code='abc123', click_count=0)
    db.session.add(url)
    db.session.commit()

    response = client.get('/abc123', follow_redirects=False)
    assert response.status_code == 301
    assert response.headers['Location'] == 'https://example.com'

    # Verify click count incremented
    updated = Url.query.filter_by(short_code='abc123').first()
    assert updated.click_count == 1

def test_redirect_not_found(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_reserved_route_not_caught(client):
    # Ensure reserved path like /health is not intercepted by catch‑all
    response = client.get('/health')
    # Assuming /health route returns 200 OK
    assert response.status_code == 200
