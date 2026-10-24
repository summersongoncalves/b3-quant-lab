"""Day direction: follow the morning excursion at 10:30, stop behind the open, target one ADR from the open.

At the close of the 10:25 bar, side = +1 if the day moved >= 0.3 * adr above the open
(and not that far below), -1 for the mirror case, else no trade. adr is the mean daily
high-low of the previous 20 sessions. The trade needs (close - open) * side >= 0.1 * adr.
Stop level = open -/+ 0.1 * adr, target level = open +/- 1.0 * adr. Distances are
measured from the signal bar close (approximation of the next-open entry). One entry per
day; the position holds until the engine's stop, target or close. Days whose first bar
starts after 09:30 are skipped. No free parameters.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
EXCURSION = 0.3
SIDE_FILTER = 0.1
STOP_MULT = 0.1
TARGET_MULT = 1.0
LATEST_OPEN = pd.Timestamp("09:30").time()
SIGNAL_BAR = pd.Timestamp("10:25").time()


def signals(df: pd.DataFrame) -> pd.DataFrame:
    day = df.index.normalize()
    g_high = df["high"].groupby(day)
    g_low = df["low"].groupby(day)

    day_open = df["open"].groupby(day).transform("first")
    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = pd.Series(first_start.dt.time <= LATEST_OPEN, index=df.index)

    daily_range = g_high.max() - g_low.min()
    adr_daily = daily_range.rolling(HISTORY_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=df.index)

    max_m = g_high.cummax()
    min_m = g_low.cummin()
    exc_up = (max_m - day_open) >= EXCURSION * adr
    exc_down = (day_open - min_m) >= EXCURSION * adr
    side = exc_up.astype(float) - exc_down.astype(float)  # 0 when both or neither

    moved = (df["close"] - day_open) * side
    stop = moved + STOP_MULT * adr
    target = (day_open + side * TARGET_MULT * adr - df["close"]) * side

    is_signal = pd.Series(df.index.time == SIGNAL_BAR, index=df.index)
    valid = is_signal & valid_day & adr.notna() & (side != 0) & (moved >= SIDE_FILTER * adr) & (stop > 0) & (target > 0)

    out = pd.DataFrame({"position": side, "stop": stop, "target": target}, index=df.index).where(valid)
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="direcao_do_dia",
    description="Follow the morning excursion (>= 0.3 ADR from the open, one side) at 10:30; stop at open -/+ 0.1 ADR, target at open +/- 1 ADR",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={},
    grid={},
    title="Direção do dia",
    summary="Se até as 10:30 o preço se afastou pelo menos 0,3 da amplitude média diária da abertura, para um lado só, e ainda está desse lado, entra a favor, com stop um pouco além da abertura e alvo a uma amplitude média da abertura.",
    param_help={},
)
