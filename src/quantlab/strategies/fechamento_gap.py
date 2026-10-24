"""Opening gap fade in WDO: sell an up gap (buy a down gap) at 09:15, target the previous close.

pc = close of the last bar of the previous session; adr = mean daily high-low of the previous
20 sessions; g = (open - pc) / adr. On the 09:10 bar (closes 09:15), if g_min <= |g| <= g_max
and the target distance |pc - close| * side >= 0.10 * adr, enter against the gap (1 entry/day).
Stop distance = max(|OR extreme -/+ b*adr level - close|, 0.20 * adr), where OR is the high/low of
the 09:00-09:10 bars; target distance = (pc - close) * side. Both are measured from the 09:10
close. The last two weekdays of each month (rollover window) are skipped using only a calendar
(pandas BMonthEnd/BDay, no holidays, no dataset dates). Days not starting at 09:00 or lacking
the 09:00/09:05/09:10 bars are skipped. The position stays on until stop, target or close.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
STOP_FLOOR = 0.20
MIN_TARGET = 0.10
SIGNAL_TIME = pd.Timestamp("09:10").time()
FIRST_TIME = pd.Timestamp("09:00").time()
OR_TIMES = {pd.Timestamp(x).time() for x in ("09:00", "09:05", "09:10")}


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def signals(df: pd.DataFrame, g_min: float = 0.15, b: float = 0.10, g_max: float = 0.8) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    t = pd.Series(idx.time, index=idx)
    g_high = df["high"].groupby(day)
    g_low = df["low"].groupby(day)

    # Daily (per-session) quantities, shifted so that only past sessions are used.
    pc_daily = df["close"].groupby(day).last().shift(1)
    adr_daily = (g_high.max() - g_low.min()).rolling(HISTORY_DAYS).mean().shift(1)
    udays = pc_daily.index
    roll = _rollover_days(udays)
    first_t = pd.Series(idx, index=idx).groupby(day).first().dt.time
    n_or = t.isin(OR_TIMES).groupby(day).sum()
    day_ok = (first_t == FIRST_TIME) & (n_or == 3) & ~roll

    pc = pd.Series(pc_daily.reindex(day).to_numpy(), index=idx)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=idx)
    ok = pd.Series(day_ok.reindex(day).to_numpy(), index=idx)
    opening = df["open"].groupby(day).transform("first")

    in_or = t.isin(OR_TIMES)
    or_max = df["high"].where(in_or).groupby(day).transform("max")
    or_min = df["low"].where(in_or).groupby(day).transform("min")

    g = (opening - pc) / adr
    side = pd.Series(np.where(g > 0, -1.0, np.where(g < 0, 1.0, 0.0)), index=idx)
    level = np.where(side < 0, or_max + b * adr, or_min - b * adr)
    stop = np.maximum(np.abs(level - df["close"]), STOP_FLOOR * adr)
    target = (pc - df["close"]) * side

    valid = (
        (t == SIGNAL_TIME)
        & ok
        & adr.notna()
        & pc.notna()
        & (g.abs() >= g_min)
        & (g.abs() <= g_max)
        & (side != 0)
        & (target >= MIN_TARGET * adr)
        & (stop > 0)
        & (target > 0)
    )
    out = pd.DataFrame({"position": side, "stop": stop, "target": target}, index=idx).where(valid)
    # Keep the side until the end of the session so the engine does not re-enter after an exit.
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="fechamento_gap",
    description="Fade the WDO opening gap at 09:15; stop behind the first-15-minute range, target at the previous close",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"g_min": 0.15, "b": 0.10, "g_max": 0.8},
    grid={"g_min": [0.15, 0.25], "b": [0.10, 0.15]},
    title="Fechamento do gap de abertura",
    summary="Se o dólar abre com um gap moderado em relação ao fechamento anterior, entra contra o gap às 09:15, com stop além da faixa dos 15 primeiros minutos e alvo no fechamento anterior.",
    param_help={
        "g_min": "Tamanho mínimo do gap, em fração da amplitude média diária, para operar.",
        "b": "Folga do stop além da faixa dos 15 primeiros minutos, em fração da amplitude média diária.",
        "g_max": "Tamanho máximo do gap, em fração da amplitude média diária; gaps maiores (notícia) ficam de fora.",
    },
)
