# Backtrader strategy stub for the MVS logic.
import backtrader as bt

class MVSStrategy(bt.Strategy):
    params = dict(
        ema_len=20,
        donchian_len=20,
        vol_lookback=20,
        vol_mult=1.5,
        atr_len=14,
        atr_k=1.0,
        rr_target=3.0,
        risk_usd=5.0,
    )

    def __init__(self):
        self.ema = bt.ind.EMA(period=self.p.ema_len)
        self.atr = bt.ind.ATR(period=self.p.atr_len)
        self.dc_hi = bt.ind.Highest(self.data.high, period=self.p.donchian_len)
        self.dc_lo = bt.ind.Lowest(self.data.low, period=self.p.donchian_len)
        self.vol_ma = bt.ind.SMA(self.data.volume, period=self.p.vol_lookback)

        # compute the warmup needed for all indicators safely
        self._warmup = max(self.p.ema_len, self.p.atr_len, self.p.donchian_len, self.p.vol_lookback) + 1

    def next(self):
        # Skip until we have enough bars for all indicators (prevents index errors)
        if len(self.data) < self._warmup:
            return

        # Momentum condition
        mom_ok = self.ema[0] > self.ema[-1]

        # Breakout conditions use prior Donchian value (safe now due to warmup)
        long_break = self.data.close[0] > self.dc_hi[-1]
        short_break = self.data.close[0] < self.dc_lo[-1]

        # Volume filter (guard in case a feed lacks volume)
        vol_ok = True
        if hasattr(self.data, "volume") and self.data.volume[0] is not None and self.vol_ma[0] is not None:
            vol_ok = self.data.volume[0] >= self.p.vol_mult * (self.vol_ma[0] or 0)

        # Example entry (stub) — real sizing handled elsewhere later
        if not self.position and mom_ok and long_break and vol_ok:
            self.buy()
        elif not self.position and (not mom_ok) and short_break and vol_ok:
            self.sell()
