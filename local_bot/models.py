from pydantic import BaseModel

class TradeSignal(BaseModel):
    symbol: str
    side: str      # e.g., "buy" or "sell"
    qty: int
    # any extra keys in the JSON body are allowed; we only validate after signature check
