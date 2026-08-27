import pytest

def test_create_link_happy_path(client):
    # Create a new shortened link
    response = client.post('/links', json={'url': 'http://example.com'})
    assert response.status_code == 201
    data = response.get_json()
    assert 'code' in data
    assert isinstance(data['code'], str)
    # Verify the code can be used for a redirect
    redirect_resp = client.get(f"/{data['code']}")
    assert redirect_resp.status_code in (301, 302)
    assert redirect_resp.headers['Location'] == 'http://example.com'

def test_create_link_missing_payload(client):
    # Empty JSON payload should be rejected
    response = client.post('/links', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_create_link_invalid_payload(client):
    # Payload without the required 'url' key should be rejected
    response = client.post('/links', json={'invalid': 'field'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_create_link_duplicate_handling(client):
    # First creation
    first_resp = client.post('/links', json={'url': 'http://duplicate.com'})
    assert first_resp.status_code == 201
    first_code = first_resp.get_json()['code']

    # Second creation of the same URL – implementation may return the same code
    second_resp = client.post('/links', json={'url': 'http://duplicate.com'})
    # Accept either 200 (already exists) or 201 (idempotent creation)
    assert second_resp.status_code in (200, 201)
    second_code = second_resp.get_json()['code']
    assert second_code == first_code