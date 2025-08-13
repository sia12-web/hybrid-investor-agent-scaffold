from fastapi import FastAPI, Depends
from local_bot.models import TradeSignal
from local_bot.security import require_hmac
import json

app = FastAPI()


@app.post("/signal")
async def receive_signal(raw: bytes = Depends(require_hmac)):
    """
    HMAC is enforced by the dependency. We parse JSON only after validation.
    """
    data = json.loads(raw.decode("utf-8"))
    signal = TradeSignal.model_validate(data)
    return {"ok": True, "received": signal.model_dump()}
