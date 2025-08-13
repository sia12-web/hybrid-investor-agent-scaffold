from local_bot.auth import verify_hmac_signature, sign_body


def test_verify_raw_body_roundtrip():
    secret = "test-secret"
    body = b'{"symbol":"AAPL","side":"buy","qty":1,"extra":"kept"}'
    signature = sign_body(secret, body, algo="sha256")
    assert verify_hmac_signature(
        secret=secret, body=body, signature_header=signature, algo="sha256"
    )


def test_reject_modified_body():
    secret = "test-secret"
    body = b'{"a":1}'
    sig = sign_body(secret, body, "sha256")
    tampered = b'{"a":2}'
    assert not verify_hmac_signature(
        secret=secret, body=tampered, signature_header=sig, algo="sha256"
    )
