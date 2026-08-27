import json
import pytest

# Helper to build a valid payload
def make_payload(url="https://example.com", code=None):
    payload = {"url": url}
    if code is not None:
        payload["code"] = code
    return payload

def test_create_link_success(client):
    """Happy‑path: create a new short link."""
    resp = client.post(
        "/links",
        data=json.dumps(make_payload()),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert "code" in data
    assert data["url"] == "https://example.com"

def test_create_link_missing_payload(client):
    """Missing JSON body should yield a 400."""
    resp = client.post("/links", data="", content_type="application/json")
    assert resp.status_code == 400
    json_data = resp.get_json()
    # flexible assertion – the message may vary
    assert json_data is not None
    assert "error" in json_data

def test_create_link_invalid_url(client):
    """Invalid URL should be rejected."""
    resp = client.post(
        "/links",
        data=json.dumps(make_payload(url="not-a-url")),
        content_type="application/json",
    )
    assert resp.status_code == 400
    json_data = resp.get_json()
    assert json_data is not None
    assert "error" in json_data

def test_create_link_duplicate_code(client):
    """Attempt to reuse an existing code must be handled."""
    # First create a link with an explicit code
    payload = make_payload(code="mycode")
    first = client.post(
        "/links",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert first.status_code == 201

    # Second attempt with the same code should fail
    second = client.post(
        "/links",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert second.status_code == 409
    json_data = second.get_json()
    assert json_data is not None
    assert "error" in json_data