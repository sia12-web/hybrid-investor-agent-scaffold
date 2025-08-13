from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os
import json
from datetime import datetime, timezone

app = FastAPI()

SHARED_SECRET = os.getenv("WEBHOOK_SHARED_SECRET", "change_me")


class Alert(BaseModel):
    source: str
    strategy: str
    symbol: str
    exchange: str | None = None
    timeframe: str
    event_time: str
    side: str
    entry_price: float
    trigger_level: float | None = None
    stop_basis: str | None = None
    atr: float | None = None
    volume: float | None = None
    avg_volume: float | None = None
    chart_id: str | None = None


def utcnow_iso():
    return datetime.now(timezone.utc).isoformat()


@app.get("/health")
def health():
    return {"ok": True, "time": utcnow_iso()}


@app.post("/alerts/mvs")
async def alerts_mvs(alert: Alert, x_shared_secret: str | None = Header(default=None)):
    if x_shared_secret != SHARED_SECRET:
        raise HTTPException(status_code=401, detail="bad secret")
    # Basic schema & timeliness checks
    try:
        event_dt = datetime.fromisoformat(alert.event_time.replace("Z", "+00:00"))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"bad event_time: {e}")
    # Reject if too old (> 10 minutes)
    if (datetime.now(timezone.utc) - event_dt).total_seconds() > 600:
        raise HTTPException(status_code=422, detail="stale alert")
    payload = alert.model_dump()
    print("[MVS ALERT]", json.dumps(payload))
    # For Phase 0, we just acknowledge.
    return {"received": True, "ts": utcnow_iso(), "payload": payload}
