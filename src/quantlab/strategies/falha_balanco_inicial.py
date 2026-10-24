"""Failed extension of the initial balance (IB) in WDO: fade it, target the other side of the IB.

IB = high/low of the 09:00-09:55 bars (needs >= 11 bars), usable only from the 10:00 bar.
adr = mean daily high-low of the previous 20 sessions. In the 10:00-13:55 window, the first
bar where the day's running high >= IBH + e*adr and the close is back inside the IB sells
(mirror for buys). If both sides trigger on that bar, or a distance is invalid, the day is
skipped. One entry per day, held until stop, target or close.
Stop distance = max(|extreme - close| + b*adr, 0.15*adr); target = close - IBL (short) or
IBH - close (long), both measured from the signal bar close. Targets < 3 * round-trip cost
(3.72 points) are discarded. Days whose first bar starts after 09:05 are skipped.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
MIN_IB_BARS = 11
STOP_FLOOR = 0.15
MIN_TARGET = 3 * 1.24  # 3 x round-trip cost in points
LATEST_OPEN = pd.Timestamp("09:05").time()
IB_START, IB_END = pd.Timestamp("09:00").time(), pd.Timestamp("09:55").time()
WIN_START, WIN_END = pd.Timestamp("10:00").time(), pd.Timestamp("13:55").time()


def signals(df: pd.DataFrame, e: float = 0.10, b: float = 0.05) -> pd.DataFrame:
    day = df.index.normalize()
    t = df.index.time
    g_high = df["high"].groupby(day)
    g_low = df["low"].groupby(day)

    first_start = pd.Series(df.index, index=df.index).groupby(day).transform("first")
    valid_day = pd.Series(first_start.dt.time <= LATEST_OPEN, index=df.index)

    adr_daily = (g_high.max() - g_low.min()).rolling(HISTORY_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=df.index)

    in_ib = pd.Series((t >= IB_START) & (t <= IB_END), index=df.index)
    ibh = df["high"].where(in_ib).groupby(day).transform("max")
    ibl = df["low"].where(in_ib).groupby(day).transform("min")
    ib_bars = in_ib.astype(int).groupby(day).transform("sum")

    window = pd.Series((t >= WIN_START) & (t <= WIN_END), index=df.index)
    max_m = g_high.cummax()
    min_m = g_low.cummin()
    inside = (df["close"] > ibl) & (df["close"] < ibh)
    short_c = (max_m >= ibh + e * adr) & inside
    long_c = (min_m <= ibl - e * adr) & inside

    base = window & valid_day & adr.notna() & (ib_bars >= MIN_IB_BARS)
    event = base & (short_c | long_c)
    first = event & (event.astype(int).groupby(day).cumsum() == 1)
    side = np.where(short_c & long_c, 0.0, np.where(short_c, -1.0, np.where(long_c, 1.0, 0.0)))
    side = pd.Series(side, index=df.index)

    extreme_dist = np.where(side < 0, max_m - df["close"], df["close"] - min_m)
    stop = np.maximum(np.abs(extreme_dist) + b * adr, STOP_FLOOR * adr)
    target = np.where(side < 0, df["close"] - ibl, ibh - df["close"])
    stop = pd.Series(stop, index=df.index)
    target = pd.Series(target, index=df.index)

    valid = first & (side != 0) & (stop > 0) & (target >= MIN_TARGET)
    out = pd.DataFrame({"position": side, "stop": stop, "target": target}, index=df.index).where(valid)
    # Only the first event of the day may trade, even if it was discarded.
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="falha_balanco_inicial",
    description="Fade a failed extension of the first-hour range (IB) in WDO; stop behind the failed extreme, target at the opposite IB side",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"e": 0.10, "b": 0.05},
    grid={"e": [0.05, 0.10, 0.15], "b": [0.05, 0.10]},
    title="Falha do balanço inicial",
    summary="Se o preço ultrapassa a máxima (ou mínima) da primeira hora e uma barra fecha de volta dentro dela, entra contra o rompimento, com stop além do extremo que falhou e alvo no outro lado da primeira hora.",
    param_help={
        "e": "Quanto o preço precisa passar da faixa da primeira hora, em fração da amplitude média diária, para contar como rompimento.",
        "b": "Folga do stop além do extremo que falhou, em fração da amplitude média diária.",
    },
)
