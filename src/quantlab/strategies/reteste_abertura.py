"""Retest of the day open after a morning excursion, with stop behind the open and target at the day extreme.

Excursion: the day moved at least 0.3 * adr (mean daily high-low of the previous 20
sessions) away from the day open, on one side only, up to the previous bar. From 10:30
to 14:55 (bar labels), the first bar that touches the open and closes back on the
excursion side triggers an entry on that side (one per day). Stop distance =
(close - open) * side + stop_mult * adr; target distance = day extreme so far - close
(long) or close - day extreme (short). Distances are measured from the signal close
(approximation of the next-open entry). Days whose first bar starts after 09:30 are
skipped. The position is held until the engine's stop, target or close.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
EXCURSION = 0.3
LATEST_OPEN = pd.Timestamp("09:30").time()
WINDOW_START = pd.Timestamp("10:30").time()
WINDOW_END = pd.Timestamp("14:55").time()


def signals(df: pd.DataFrame, stop_mult: float = 0.25) -> pd.DataFrame:
    day = df.index.normalize()
    g_high = df["high"].groupby(day)
    g_low = df["low"].groupby(day)

    day_open = df["open"].groupby(day).transform("first")
    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = pd.Series(first_start.dt.time <= LATEST_OPEN, index=df.index)

    # mean daily range over the previous 20 sessions, current day excluded
    daily_range = g_high.max() - g_low.min()
    adr_daily = daily_range.rolling(HISTORY_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=df.index)

    cum_max = g_high.cummax()
    cum_min = g_low.cummin()
    max_prev = cum_max.groupby(day).shift(1)
    min_prev = cum_min.groupby(day).shift(1)
    exc_up = (max_prev - day_open) >= EXCURSION * adr
    exc_down = (day_open - min_prev) >= EXCURSION * adr

    t = df.index.time
    in_window = pd.Series((t >= WINDOW_START) & (t <= WINDOW_END), index=df.index)
    base = in_window & valid_day & adr.notna()

    long_ = base & exc_up & ~exc_down & (df["low"] <= day_open) & (df["close"] > day_open)
    short_ = base & exc_down & ~exc_up & (df["high"] >= day_open) & (df["close"] < day_open)
    side = long_.astype(float) - short_.astype(float)

    stop = (df["close"] - day_open) * side + stop_mult * adr
    target = np.where(side > 0, cum_max - df["close"], df["close"] - cum_min)
    target = pd.Series(target, index=df.index)

    valid = (side != 0) & (stop > 0) & (target > 0)
    first = valid & (valid.astype(int).groupby(day).cumsum() == 1)

    out = pd.DataFrame({"position": side, "stop": stop, "target": target}, index=df.index).where(first)
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="reteste_abertura",
    description="Retest of the day open after a 0.3 ADR morning excursion, stop behind the open, target at the day extreme",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"stop_mult": 0.25},
    grid={"stop_mult": [0.2, 0.25, 0.3]},
    title="Reteste da abertura",
    summary="Depois de o preço se afastar pelo menos 0,3 da amplitude média diária da abertura, se ele volta a tocar a abertura e uma barra fecha de volta do lado do movimento, entra a favor, com stop atrás da abertura e alvo no extremo do dia.",
    param_help={
        "stop_mult": "Fração da amplitude média diária (20 pregões anteriores) colocada além do preço de abertura para posicionar o stop.",
    },
)
