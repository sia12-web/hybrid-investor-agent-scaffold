import os
import json
import hmac
import hashlib
import requests

SECRET = os.environ.get("SIGNING_SECRET", "dev-secret").encode()
URL = "http://127.0.0.1:8000/signal"


def post(body_dict):
    body = json.dumps(body_dict, separators=(",", ":")).encode()
    sig = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    r = requests.post(
        URL, headers={"X-Signature": sig, "Content-Type": "application/json"}, data=body
    )
    print(r.status_code, r.text)


print("== valid body ==")
post({"symbol": "AAPL", "side": "buy", "qty": 1})

print("\n== tampered (should 401) ==")
orig = {"a": 1}
orig_bytes = json.dumps(orig, separators=(",", ":")).encode()
sig = "sha256=" + hmac.new(SECRET, orig_bytes, hashlib.sha256).hexdigest()
tampered = {"a": 2}
tampered_bytes = json.dumps(tampered, separators=(",", ":")).encode()
r = requests.post(
    URL,
    headers={"X-Signature": sig, "Content-Type": "application/json"},
    data=tampered_bytes,
)
print(r.status_code, r.text)
