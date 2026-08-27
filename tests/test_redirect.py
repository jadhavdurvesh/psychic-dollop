import pytest

def test_redirect_success(client):
    """Redirect should succeed for a known short code."""
    # First create a link
    resp = client.post(
        "/links",
        json={"url": "https://example.org"},
    )
    assert resp.status_code == 201
    code = resp.get_json()["code"]

    # Now follow the redirect
    redirect_resp = client.get(f"/{code}", follow_redirects=False)
    assert redirect_resp.status_code in (301, 302)
    assert redirect_resp.headers["Location"] == "https://example.org"

def test_redirect_not_found(client):
    """Requesting an unknown code must return 404."""
    resp = client.get("/nonexistentcode", follow_redirects=False)
    assert resp.status_code == 404
    json_data = resp.get_json()
    assert json_data is not None
    assert "error" in json_data

def test_redirect_malformed_code(client):
    """A malformed code (e.g., containing illegal characters) should be treated as not found."""
    resp = client.get("/invalid!!code", follow_redirects=False)
    # The implementation may treat this as 404 or 400; accept both
    assert resp.status_code in (400, 404)
    json_data = resp.get_json()
    assert json_data is not None
    assert "error" in json_data