from fastapi import Header, HTTPException, Request
from local_bot.auth import verify_hmac_signature
import os


async def require_hmac(
    request: Request,
    x_signature: str | None = Header(default=None, convert_underscores=True),
    x_hub_signature_256: str | None = Header(default=None, convert_underscores=True),
) -> bytes:
    """
    Dependency that:
      1) reads raw body
      2) verifies HMAC using SIGNING_SECRET
      3) returns the raw body bytes if valid, otherwise raises HTTP 401
    """
    body = await request.body()
    secret = os.getenv("SIGNING_SECRET", "dev-secret")
    signature = x_signature or x_hub_signature_256
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature header")

    ok = verify_hmac_signature(
        secret=secret, body=body, signature_header=signature, algo="sha256"
    )
    if not ok:
        raise HTTPException(status_code=401, detail="Invalid signature")

    return body
