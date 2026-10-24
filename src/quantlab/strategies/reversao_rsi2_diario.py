"""WDO daily RSI(2) reversal bias: buy after an oversold extreme, sell after an overbought one.

Daily change is close(d) - close(d-1), except on/after the rollover window (last two weekdays of
the month, calendar only) where it is close(d) - open(d). RSI(2) (Wilder, alpha 1/2) of that change
is shifted one session, so day d only sees closes up to d-1. If rsi <= lim go long, if rsi >= 100-lim
go short. Signal on the 10:10 bar (executes 10:15), once per day, held to the close. Days in the
rollover window, days not opening by 09:05, and the first 25 sessions are skipped.
stop = s * adr (adr = mean daily range of the previous 20 sessions), target = k * stop (points).
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import rsi_from_changes

HISTORY_DAYS = 20
WARMUP_DAYS = 25
SIGNAL_TIME = pd.Timestamp("10:10").time()
LATEST_OPEN = pd.Timestamp("09:05").time()


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def signals(df: pd.DataFrame, s: float = 0.25, k: float = 1.5, lim: float = 10.0) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    t = pd.Series(idx.time, index=idx)

    g = df.groupby(day)
    d_open, d_close = g["open"].first(), g["close"].last()
    adr_daily = (g["high"].max() - g["low"].min()).rolling(HISTORY_DAYS).mean().shift(1)
    first_t = pd.Series(idx, index=idx).groupby(day).first().dt.time

    roll = _rollover_days(d_close.index)
    roll_prev = roll.shift(1, fill_value=True)
    delta = (d_close - d_close.shift(1)).where(~(roll | roll_prev), d_close - d_open)
    rsi = rsi_from_changes(delta, 2).shift(1)  # value known at the previous close
    bias = pd.Series(np.where(rsi <= lim, 1.0, np.where(rsi >= 100 - lim, -1.0, 0.0)), index=rsi.index)

    warm = pd.Series(np.arange(len(d_close)) >= WARMUP_DAYS, index=d_close.index)
    day_ok = (first_t <= LATEST_OPEN) & ~roll & warm & rsi.notna() & adr_daily.notna()

    side = pd.Series(bias.reindex(day).to_numpy(), index=idx)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=idx)
    ok = pd.Series(day_ok.reindex(day).to_numpy(), index=idx)
    stop = s * adr
    target = k * stop

    valid = (t == SIGNAL_TIME) & ok & (side != 0) & (stop > 0) & (target > 0)
    out = pd.DataFrame({"position": side, "stop": stop, "target": target}, index=idx).where(valid)
    # Keep the side until the end of the session so the engine does not re-enter after an exit.
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="reversao_rsi2_diario",
    description="WDO: trade against a daily RSI(2) extreme (<=10 buy, >=90 sell) at 10:15, stop 0.25 adr, target 1.5x stop",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"s": 0.25, "k": 1.5, "lim": 10.0},
    grid={"s": [0.25, 0.30, 0.35]},
    title="Reversão do RSI(2) diário",
    summary="Se o dólar fechou esticado nos últimos pregões (RSI de 2 períodos diário abaixo de 10 ou acima de 90), entra contra o esticamento às 10:15, com stop e alvo proporcionais à amplitude média diária.",
    param_help={
        "s": "Tamanho do stop, em fração da amplitude média diária dos últimos 20 pregões.",
        "k": "Alvo em múltiplos do stop.",
        "lim": "Limiar do RSI(2) diário: compra se estiver abaixo dele, vende se estiver acima de 100 menos ele.",
    },
)
