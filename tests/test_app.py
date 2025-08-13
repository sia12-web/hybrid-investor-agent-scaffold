import os, json, hmac, hashlib
from fastapi.testclient import TestClient
from local_bot.app import app

def _sign(secret: str, body: bytes) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

def test_signal_valid_request(monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("SIGNING_SECRET", secret)
    client = TestClient(app)

    payload = {"symbol": "AAPL", "side": "buy", "qty": 1}
    body = json.dumps(payload, separators=(",", ":")).encode()
    sig = _sign(secret, body)

    r = client.post(
        "/signal",
        content=body,  # use content instead of data (httpx deprecation fix)
        headers={"Content-Type": "application/json", "X-Signature": sig},
    )

    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert data["received"]["symbol"] == "AAPL"
    assert data["received"]["qty"] == 1

def test_signal_tampered_body(monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("SIGNING_SECRET", secret)
    client = TestClient(app)

    signed = json.dumps({"a": 1}, separators=(",", ":")).encode()
    sig = _sign(secret, signed)

    tampered = json.dumps({"a": 2}, separators=(",", ":")).encode()
    r = client.post(
        "/signal",
        content=tampered,
        headers={"Content-Type": "application/json", "X-Signature": sig},
    )

    assert r.status_code == 401
    assert r.json()["detail"] == "Invalid signature"

def test_signal_missing_header(monkeypatch):
    secret = "test-secret"
    monkeypatch.setenv("SIGNING_SECRET", secret)
    client = TestClient(app)

    body = json.dumps({"a": 1}, separators=(",", ":")).encode()
    r = client.post(
        "/signal",
        content=body,
        headers={"Content-Type": "application/json"},
    )

    assert r.status_code == 400
    assert r.json()["detail"] == "Missing signature header"
