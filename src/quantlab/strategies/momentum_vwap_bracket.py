"""Frozen 12:00 momentum + daily VWAP + relative volume rule, with stop, target and risk sizing.

At the bar closing at 12:00, mov = ln(close / day open). If |mov| > 1.5 * (median
|mov| at that bar over the previous 20 days), the close is on the same side of the
daily VWAP as mov, and relative volume > 1, enter on the side of mov (one entry
per day). Stop = stop_mult * adr (mean daily high-low of the previous 20 days),
target = 2 * stop. Size w = min(1, 0.008 * close / stop) so a stop costs ~0.8%.
Days whose first bar starts after 10:10 are skipped. The engine flattens at the close.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import relative_volume, vwap

BAR = pd.Timedelta(minutes=5)
SIGNAL_LABEL = (pd.Timestamp("12:00") - BAR).time()  # bar that closes at 12:00
HISTORY_DAYS = 20
K = 1.5
LATEST_OPEN = pd.Timestamp("10:10").time()
RISK = 0.008
TARGET_MULT = 2.0


def signals(df: pd.DataFrame, stop_mult: float = 0.4) -> pd.DataFrame:
    day = df.index.normalize()

    day_open = df["open"].groupby(day).transform("first")
    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = pd.Series(first_start.dt.time <= LATEST_OPEN, index=df.index)

    mov = np.log(df["close"] / day_open)
    vw = vwap(df, "D")
    rv = relative_volume(df, HISTORY_DAYS)

    at_signal = pd.Series(df.index.time == SIGNAL_LABEL, index=df.index)
    abs_mov = mov.abs().where(at_signal).dropna()
    # previous 20 signal-time observations, current day excluded
    scale = abs_mov.rolling(HISTORY_DAYS).median().shift(1).reindex(df.index)

    # mean daily range over the previous 20 sessions, current day excluded
    daily_range = df["high"].groupby(day).max() - df["low"].groupby(day).min()
    adr_daily = daily_range.rolling(HISTORY_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=df.index)

    side = np.sign(mov)
    enter = (
        at_signal
        & valid_day
        & (mov.abs() > K * scale)
        & (np.sign(df["close"] - vw) == side)
        & (side != 0)
        & (rv > 1.0)
        & adr.notna()
    )

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
    name="momentum_vwap_bracket",
    description="Frozen 12:00 intraday momentum confirmed by daily VWAP and relative volume, with ADR-based stop, 2x target and fixed-risk sizing",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"stop_mult": 0.4},
    grid={"stop_mult": [0.3, 0.4, 0.5]},
    title="Momentum do dia com stop, alvo e risco fixo",
    summary="Se o preço se afastou muito da abertura até o meio-dia, está do mesmo lado da VWAP e o volume está acima do normal, entra a favor, com stop proporcional à amplitude diária, alvo de 2x o stop e posição que limita a perda no stop a cerca de 0,8% do capital.",
    param_help={
        "stop_mult": "Fração da amplitude média diária (máxima menos mínima dos 20 pregões anteriores) usada como distância do stop; o alvo é o dobro.",
    },
)
