import pytest

def test_successful_redirect(client):
    # First, create a short link to have a known code
    create_resp = client.post('/links', json={'url': 'http://redirect.com'})
    assert create_resp.status_code == 201
    code = create_resp.get_json()['code']

    # Follow the redirect
    redirect_resp = client.get(f'/{code}', follow_redirects=False)
    assert redirect_resp.status_code in (301, 302)
    assert redirect_resp.headers['Location'] == 'http://redirect.com'

def test_redirect_not_found(client):
    # Access a code that does not exist
    resp = client.get('/nonexistent')
    assert resp.status_code == 404
    data = resp.get_json()
    assert 'error' in data

def test_redirect_malformed_code(client):
    # The code format is arbitrary; treat an obviously malformed code as not found
    resp = client.get('/!!!')
    assert resp.status_code == 404
    data = resp.get_json()
    assert 'error' in data