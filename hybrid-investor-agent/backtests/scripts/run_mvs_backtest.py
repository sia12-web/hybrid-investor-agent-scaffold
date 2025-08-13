import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "src"))

import backtrader as bt
from strategies.mvs_bt import MVSStrategy


class CSV5m(bt.feeds.GenericCSVData):
    params = dict(
        dtformat="%Y-%m-%d %H:%M:%S",
        datetime=0,
        open=1,
        high=2,
        low=3,
        close=4,
        volume=5,
        openinterest=-1,
    )


if __name__ == "__main__":
    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..", "data", "synthetic_5m.csv")
    )
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"CSV not found at {csv_path}. Create it first under ./data/synthetic_5m.csv"
        )

    data = CSV5m(dataname=csv_path)

    cerebro = bt.Cerebro()
    cerebro.adddata(data)

    # Use smaller lookbacks so a short CSV doesn’t crash
    cerebro.addstrategy(
        MVSStrategy, ema_len=5, donchian_len=5, vol_lookback=5, atr_len=7
    )

    cerebro.broker.setcash(500.0)

    # Key part: avoid vectorized run and preloading when data is very short
    cerebro.run(runonce=False, preload=False)
    print("Backtest OK. Final cash:", cerebro.broker.getvalue())
