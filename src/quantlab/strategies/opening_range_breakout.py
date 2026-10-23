"""Baseline day trade strategy: opening range breakout.

The first `range_bars` bars of the session define a high/low range. After
that, go long when a bar closes above the range high and short when it closes
below the range low. Positions are closed by the engine at the end of the day,
and no new entries are taken after `last_entry`.
"""

import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import session_bar_number


def signals(df: pd.DataFrame, range_bars: int, last_entry: str) -> pd.Series:
    day = df.index.normalize()
    bar_no = session_bar_number(df)
    in_range = bar_no < range_bars
    range_high = df["high"].where(in_range).groupby(day).cummax().groupby(day).ffill()
    range_low = df["low"].where(in_range).groupby(day).cummin().groupby(day).ffill()

    breakout = pd.Series(0.0, index=df.index)
    breakout[df["close"] > range_high] = 1.0
    breakout[df["close"] < range_low] = -1.0
    breakout[in_range] = 0.0
    late = df.index.time > pd.Timestamp(last_entry).time()

    # Only the first breakout of the day counts; its side is held until the close.
    is_entry = (breakout != 0) & ~late
    first_entry = is_entry & (is_entry.groupby(day).cumsum() == 1)
    return breakout.where(first_entry).groupby(day).ffill().fillna(0.0)


STRATEGY = Strategy(
    name="opening_range_breakout",
    description="Opening range breakout, flat at the close (baseline day trade)",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"range_bars": 6, "last_entry": "12:00"},
    grid={"range_bars": [3, 6, 12], "last_entry": ["11:00", "12:00", "14:00"]},
    title="Rompimento da faixa de abertura",
    summary="Marca a máxima e a mínima das primeiras barras do dia e entra quando o preço fecha fora dessa faixa; zera no fim do pregão.",
    param_help={
        "range_bars": "Quantas barras de 5 min do início do dia formam a faixa (3 = 15 min, 12 = 1 hora).",
        "last_entry": "Horário limite para entrar; depois disso não abre posição nova.",
    },
)
