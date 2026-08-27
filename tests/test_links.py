import pytest

def test_create_link_success(client):
    """Happy path – a valid URL returns a new short code."""
    response = client.post("/links", json={"url": "https://example.com"})
    assert response.status_code == 201
    payload = response.get_json()
    assert isinstance(payload, dict)
    assert "code" in payload
    assert isinstance(payload["code"], str)
    assert len(payload["code"]) > 0

def test_missing_url_field(client):
    """POST without a `url` field should be rejected."""
    response = client.post("/links", json={})
    assert response.status_code == 400
    payload = response.get_json()
    assert isinstance(payload, dict)
    assert "error" in payload

def test_invalid_url_format(client):
    """A malformed URL must be rejected."""
    response = client.post("/links", json={"url": "not-a-valid-url"})
    assert response.status_code == 400
    payload = response.get_json()
    assert isinstance(payload, dict)
    assert "error" in payload

def test_duplicate_url_returns_existing_code(client):
    """Submitting the same URL twice should return the same short code."""
    payload = {"url": "https://duplicate.com"}
    first = client.post("/links", json=payload)
    assert first.status_code == 201
    first_code = first.get_json()["code"]

    second = client.post("/links", json=payload)
    # Implementation may return 200 for an existing mapping; accept both 200 and 201
    assert second.status_code in (200, 201)
    second_code = second.get_json()["code"]
    assert second_code == first_code