import pytest

def test_redirect_success(client):
    """A previously created short code must redirect (302) to the original URL."""
    # First create a short link
    create_resp = client.post("/links", json={"url": "https://redirect.me"})
    assert create_resp.status_code == 201
    code = create_resp.get_json()["code"]

    # Then request the short code
    redirect_resp = client.get(f"/{code}", follow_redirects=False)
    assert redirect_resp.status_code in (301, 302)
    # Flask's redirect uses the `Location` header
    assert redirect_resp.headers["Location"] == "https://redirect.me"

def test_redirect_not_found(client):
    """Requesting a non‑existent code should yield a 404."""
    resp = client.get("/nonexistentcode", follow_redirects=False)
    assert resp.status_code == 404
    payload = resp.get_json()
    assert isinstance(payload, dict)
    assert "error" in payload

def test_redirect_malformed_code(client):
    """Codes that do not match the expected pattern should be rejected."""
    resp = client.get("/invalid!!code", follow_redirects=False)
    # Depending on implementation this could be 400 or 404; accept both
    assert resp.status_code in (400, 404)
    if resp.is_json:
        payload = resp.get_json()
        assert isinstance(payload, dict)
        assert "error" in payload