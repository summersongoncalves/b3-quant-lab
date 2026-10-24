"""WDO pullback to the daily VWAP in the direction of the 5-session trend.

Daily bias (past sessions only): delta(d) = close(d) - close(d-1), or close(d) - open(d) when d or
d-1 is in the rollover window (last two weekdays of the month, calendar only). T5(d) = sum of delta
over sessions d-5..d-1 divided by adr(d) (mean daily high-low of the 20 previous sessions).
bias = +1 if T5 >= z0*sqrt(5), -1 if T5 <= -z0*sqrt(5). Rollover days and days whose first bar is
after 09:05 are skipped.
Entry (first touch of the day, bars labelled 10:00-12:55): long if close[t-1] > vwap[t-1],
low[t] <= vwap[t] and close[t] > vwap[t]; short is the mirror. Stop = s*adr, target = k*stop (points),
fixed at the signal bar close. The side is held to the end of the session (ffill per day).
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import vwap

HISTORY_DAYS = 20
TREND_DAYS = 5
LAST_FIRST_BAR = pd.Timestamp("09:05").time()
WINDOW_START = pd.Timestamp("10:00").time()
WINDOW_END = pd.Timestamp("12:55").time()


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def signals(df: pd.DataFrame, s: float = 0.25, k: float = 1.5, z0: float = 0.5) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    t = pd.Series(idx.time, index=idx)

    g = df.groupby(day)
    daily_close = g["close"].last()
    daily_open = g["open"].first()
    adr_daily = (g["high"].max() - g["low"].min()).rolling(HISTORY_DAYS).mean().shift(1)
    first_t = pd.Series(idx, index=idx).groupby(day).first().dt.time

    roll = _rollover_days(daily_close.index)
    roll_prev = roll.shift(1, fill_value=True)  # first day of the dataset treated as rollover
    delta = (daily_close - daily_close.shift(1)).where(~(roll | roll_prev), daily_close - daily_open)
    t5 = delta.rolling(TREND_DAYS).sum().shift(1) / adr_daily
    thr = z0 * np.sqrt(TREND_DAYS)
    bias_daily = pd.Series(np.where(t5 >= thr, 1.0, np.where(t5 <= -thr, -1.0, 0.0)), index=t5.index)
    bias_daily = bias_daily.where(t5.notna() & adr_daily.notna(), 0.0)
    bias_daily = bias_daily.where((first_t <= LAST_FIRST_BAR) & ~roll, 0.0)

    bias = pd.Series(bias_daily.reindex(day).to_numpy(), index=idx)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=idx)

    vw = vwap(df, "D")
    prev_close = df["close"].groupby(day).shift(1)
    prev_vw = vw.groupby(day).shift(1)
    long_touch = (prev_close > prev_vw) & (df["low"] <= vw) & (df["close"] > vw)
    short_touch = (prev_close < prev_vw) & (df["high"] >= vw) & (df["close"] < vw)
    in_window = (t >= WINDOW_START) & (t <= WINDOW_END)
    touch = in_window & (((bias > 0) & long_touch) | ((bias < 0) & short_touch))
    first = touch & (touch.astype(int).groupby(day).cumsum() == 1)

    stop = s * adr
    target = k * stop
    valid = first & adr.notna() & (stop > 0) & (target > 0)
    out = pd.DataFrame({"position": bias, "stop": stop, "target": target}, index=idx).where(valid)
    # Hold the side to the end of the session so the engine does not re-enter after an exit.
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="recuo_vwap_tendencia_semanal",
    description="WDO: first pullback to the daily VWAP (10:00-12:55) in the direction of the 5-session trend; stop s*adr, target 1.5x stop",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"s": 0.25, "k": 1.5, "z0": 0.5},
    grid={"s": [0.20, 0.25, 0.30]},
    title="Recuo à VWAP a favor da tendência da semana",
    summary="Se o dólar tem tendência clara nos últimos 5 pregões, entra a favor dela no primeiro recuo da manhã até a VWAP do dia, com stop e alvo fixos proporcionais à amplitude média diária.",
    param_help={
        "s": "Tamanho do stop, em fração da amplitude média diária dos últimos 20 pregões.",
        "k": "Alvo em múltiplos da distância do stop.",
        "z0": "Força mínima da tendência de 5 pregões (em amplitude média diária vezes raiz de 5) para operar.",
    },
)
