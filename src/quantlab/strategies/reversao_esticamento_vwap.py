"""Fade of a stretch away from the daily VWAP, with stop, target and risk sizing.

dev = (close - daily VWAP) / adr, where adr is the mean daily high-low of the
previous 20 sessions. On the first bar labelled 11:00-15:25 of the day with
|dev| > 0.5, enter against the stretch (short above VWAP, long below), one entry
per day. Stop = stop_mult * adr, target = 1.5 * stop. Size w = min(1, 0.008 *
close / stop) so a stop costs ~0.8%. Days whose first bar starts after 10:10
are skipped. No signal exit: the engine flattens at the close.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import vwap

HISTORY_DAYS = 20
THRESHOLD = 0.5
WINDOW_START = pd.Timestamp("11:00").time()
WINDOW_END = pd.Timestamp("15:25").time()
LATEST_OPEN = pd.Timestamp("10:10").time()
RISK = 0.008
TARGET_MULT = 1.5


def signals(df: pd.DataFrame, stop_mult: float = 0.35) -> pd.DataFrame:
    day = df.index.normalize()

    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = pd.Series(first_start.dt.time <= LATEST_OPEN, index=df.index)

    # mean daily range over the previous 20 sessions, current day excluded
    daily_range = df["high"].groupby(day).max() - df["low"].groupby(day).min()
    adr_daily = daily_range.rolling(HISTORY_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=df.index)

    vw = vwap(df, "D")
    dev = (df["close"] - vw) / adr

    t = df.index.time
    in_window = pd.Series((t >= WINDOW_START) & (t <= WINDOW_END), index=df.index)
    cond = in_window & valid_day & (dev.abs() > THRESHOLD)
    first = cond & (cond.astype(int).groupby(day).cumsum() == 1)

    side = -np.sign(dev)
    stop = stop_mult * adr
    weight = np.minimum(1.0, RISK * df["close"] / stop)
    out = pd.DataFrame(
        {"position": side * weight, "stop": stop, "target": TARGET_MULT * stop},
        index=df.index,
    ).where(first)
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="reversao_esticamento_vwap",
    description="Fade of a >0.5 adr stretch from the daily VWAP in the mid-session, with ADR-based stop, 1.5x target and fixed-risk sizing",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"stop_mult": 0.35},
    grid={"stop_mult": [0.25, 0.35, 0.5]},
    title="Reversão do esticamento em relação à VWAP",
    summary="Entre 11h e 15h30, na primeira vez em que o preço se afasta da VWAP do dia por mais de meio ADR, opera contra o afastamento, com stop proporcional à amplitude diária, alvo de 1,5x o stop e posição que limita a perda no stop a cerca de 0,8% do capital.",
    param_help={
        "stop_mult": "Fração da amplitude média diária (máxima menos mínima dos 20 pregões anteriores) usada como distância do stop; o alvo é 1,5 vez o stop.",
    },
)
