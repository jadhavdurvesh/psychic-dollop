import pytest
from app import app, db
from models import Url
from flask import url_for

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
    # Create a short URL entry
    short_code = 'abc123'
    original_url = 'http://example.com'
    url = Url(short_code=short_code, original_url=original_url, click_count=0)
    db.session.add(url)
    db.session.commit()

    response = client.get(f'/{short_code}')
    assert response.status_code == 301
    assert response.headers['Location'] == original_url
    # Verify click count incremented
    refreshed = Url.query.filter_by(short_code=short_code).first()
    assert refreshed.click_count == 1

def test_redirect_not_found(client):
    response = client.get('/nonexistent')
    assert response.status_code == 404

def test_reserved_route_not_caught(client):
    # Define a reserved route dynamically for the test
    @app.route('/health')
    def health():
        return 'OK', 200

    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'OK'
