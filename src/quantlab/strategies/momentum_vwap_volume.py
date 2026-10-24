"""Intraday momentum confirmed by daily VWAP and relative volume.

At the bar whose close is `signal_time`, mov = ln(close / day open). If
|mov| > k * (median |mov| at the same time over the previous 20 days), the
close is on the same side of the daily VWAP as mov, and relative volume > 1,
take the side of mov (one entry per day) and hold until the engine flattens at
the close. Days whose first bar starts after 10:05 are skipped.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import relative_volume, vwap

BAR = pd.Timedelta(minutes=5)
HISTORY_DAYS = 20
LATEST_OPEN = pd.Timestamp("10:05").time()


def signals(df: pd.DataFrame, signal_time: str, k: float) -> pd.Series:
    day = df.index.normalize()
    label = (pd.Timestamp(signal_time) - BAR).time()  # bar that closes at signal_time

    day_open = df["open"].groupby(day).transform("first")
    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = pd.Series(first_start.dt.time <= LATEST_OPEN, index=df.index)

    mov = np.log(df["close"] / day_open)
    vw = vwap(df, "D")
    rv = relative_volume(df, HISTORY_DAYS)

    at_signal = pd.Series(df.index.time == label, index=df.index)
    abs_mov = mov.abs().where(at_signal).dropna()
    # previous 20 signal-time observations, current day excluded
    scale = abs_mov.rolling(HISTORY_DAYS).median().shift(1).reindex(df.index)

    side = np.sign(mov)
    enter = (
        at_signal
        & valid_day
        & (mov.abs() > k * scale)
        & (np.sign(df["close"] - vw) == side)
        & (side != 0)
        & (rv > 1.0)
    )
    entry = side.where(enter)
    return entry.groupby(day).ffill().fillna(0.0)


STRATEGY = Strategy(
    name="momentum_vwap_volume",
    description="Intraday momentum from the open confirmed by daily VWAP and relative volume, flat at the close",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"signal_time": "12:00", "k": 1.5},
    grid={"signal_time": ["12:00", "13:00", "14:00"], "k": [1.0, 1.5, 2.0]},
    title="Momentum do dia confirmado por VWAP e volume",
    summary="Se o preço se afastou muito da abertura até o meio do dia, está do mesmo lado da VWAP e o volume está acima do normal, entra a favor do movimento e zera no fim do pregão.",
    param_help={
        "signal_time": "Horário em que o movimento desde a abertura é medido e a entrada é decidida.",
        "k": "Quantas vezes o movimento precisa superar o movimento típico (mediana dos 20 dias anteriores) nesse horário.",
    },
)
