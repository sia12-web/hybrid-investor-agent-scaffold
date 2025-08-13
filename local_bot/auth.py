from __future__ import annotations
import hashlib
import hmac

class SignatureError(Exception):
    pass

def _parse_signature_header(signature_header: str, expected_algo: str = "sha256") -> str:
    if not signature_header:
        raise SignatureError("Missing signature header")
    sig = signature_header.strip()
    prefix = f"{expected_algo}="
    if sig.lower().startswith(prefix):
        return sig[len(prefix):]
    return sig

def sign_body(secret: str, body: bytes, algo: str = "sha256") -> str:
    mac = hmac.new(secret.encode("utf-8"), body, getattr(hashlib, algo))
    return f"{algo}=" + mac.hexdigest()

def verify_hmac_signature(
    *,
    secret: str,
    body: bytes,
    signature_header: str,
    algo: str = "sha256",
) -> bool:
    provided_hex = _parse_signature_header(signature_header, expected_algo=algo)
    computed = hmac.new(secret.encode("utf-8"), body, getattr(hashlib, algo)).hexdigest()
    return hmac.compare_digest(provided_hex, computed)
