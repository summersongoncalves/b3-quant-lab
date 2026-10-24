"""Failed breakout of the previous 20-session low/high ("Turtle Soup"), with stop, target and risk sizing.

L20/H20 are the lowest low / highest high of the previous 20 sessions (current day
excluded). In the signal window (bars labelled 10:30 to 14:55), go long on the first
bar where the day's running low is below L20 and the bar closes back above L20; go
short on the first bar where the running high is above H20 and the bar closes below
H20. One entry per day (earliest side wins; a tie on the same bar skips the day).
Stop = stop_mult * adr (mean daily high-low of the previous 20 days), target = 2 * stop.
Size w = min(1, 0.008 * close / stop). Days whose first bar starts after 10:10 are
skipped. The engine flattens at the close.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
LATEST_OPEN = pd.Timestamp("10:10").time()
WINDOW_START = pd.Timestamp("10:30").time()
WINDOW_END = pd.Timestamp("14:55").time()
RISK = 0.008
TARGET_MULT = 2.0


def _daily_to_bars(daily: pd.Series, day: pd.DatetimeIndex, index: pd.Index) -> pd.Series:
    return pd.Series(daily.reindex(day).to_numpy(), index=index)


def signals(df: pd.DataFrame, stop_mult: float = 0.4) -> pd.DataFrame:
    day = df.index.normalize()

    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = first_start.dt.time <= LATEST_OPEN
    t = pd.Series(df.index.time, index=df.index)
    in_window = (t >= WINDOW_START) & (t <= WINDOW_END)

    # previous 20 sessions only (shift(1) at the daily level)
    d_high = df["high"].groupby(day).max()
    d_low = df["low"].groupby(day).min()
    adr = _daily_to_bars((d_high - d_low).rolling(HISTORY_DAYS).mean().shift(1), day, df.index)
    l20 = _daily_to_bars(d_low.rolling(HISTORY_DAYS).min().shift(1), day, df.index)
    h20 = _daily_to_bars(d_high.rolling(HISTORY_DAYS).max().shift(1), day, df.index)

    min_today = df["low"].groupby(day).cummin()
    max_today = df["high"].groupby(day).cummax()

    ok = in_window & valid_day & adr.notna() & l20.notna() & h20.notna()
    long_ev = ok & (min_today < l20) & (df["close"] > l20)
    short_ev = ok & (max_today > h20) & (df["close"] < h20)

    # first event of each side per day (bar number), earliest side wins
    n = pd.Series(np.arange(len(df), dtype=float), index=df.index)
    first_long = n.where(long_ev).groupby(day).transform("min")
    first_short = n.where(short_ev).groupby(day).transform("min")
    long_entry = long_ev & (n == first_long) & ~(first_short <= first_long)
    short_entry = short_ev & (n == first_short) & ~(first_long <= first_short)

    side = long_entry.astype(float) - short_entry.astype(float)
    enter = side != 0

    stop = stop_mult * adr
    weight = np.minimum(1.0, RISK * df["close"] / stop)
    out = pd.DataFrame(
        {"position": side * weight, "stop": stop, "target": TARGET_MULT * stop},
        index=df.index,
    ).where(enter)
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="falso_rompimento_20d",
    description="Fade of a failed breakout of the previous 20-session low/high on M5, with ADR-based stop, 2x target and fixed-risk sizing",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"stop_mult": 0.4},
    grid={"stop_mult": [0.3, 0.4, 0.5]},
    title="Falso rompimento da mínima/máxima de 20 pregões",
    summary="Se o preço fura a mínima (ou máxima) dos 20 pregões anteriores e a barra de 5 minutos fecha de volta para dentro, entra na direção da volta, com stop proporcional à amplitude diária, alvo de 2x o stop e posição que limita a perda no stop a cerca de 0,8% do capital.",
    param_help={
        "stop_mult": "Fração da amplitude média diária (máxima menos mínima dos 20 pregões anteriores) usada como distância do stop; o alvo é o dobro.",
    },
)
