"""WDO trade against the morning direction of WIN when the dollar has not followed yet.

For X in {WDO, WIN}: open_X = open of the first bar of the day; adr_X = mean daily high-low of the
20 previous sessions of X (shift(1)); z_X = (close of the 11:25 bar - open_X) / adr_X.
Signal bar = the bar labelled 11:25 of both assets. side = -sign(z_win). Enter if |z_win| >= k and
z_wdo * side <= m. Days are skipped if the first bar of either asset is after 09:05, if either has
fewer than 20 prior sessions, if the 11:25 bar is missing in either, or in the rollover window (last
two weekdays of the month, calendar only). Stop = s*adr_WDO, target = 1.5*stop (points), fixed at
the signal bar close; the side is held to the end of the session (ffill per day).

WIN data comes from `store.load("WIN$N", "M5")` (research period only) unless `win` is passed (used
by the causality test). Only WIN bars with timestamp <= the last WDO bar are used, only the 11:25 bar
of the same day and earlier sessions (for adr), and only days present in the WDO df are signalled.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
LAST_FIRST_BAR = pd.Timestamp("09:05").time()
SIGNAL_BAR = pd.Timestamp("11:25").time()
TARGET_MULT = 1.5


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def _daily(df: pd.DataFrame) -> pd.DataFrame:
    """Per-day open, adr (previous sessions only), first bar time and close of the 11:25 bar."""
    day = df.index.normalize()
    g = df.groupby(day)
    sig = df.loc[df.index.time == SIGNAL_BAR]
    return pd.DataFrame({
        "open": g["open"].first(),
        "adr": (g["high"].max() - g["low"].min()).rolling(HISTORY_DAYS).mean().shift(1),
        "first_t": pd.Series(df.index, index=df.index).groupby(day).first().dt.time,
        "close_sig": pd.Series(sig["close"].to_numpy(), index=sig.index.normalize()),
    })


def signals(df: pd.DataFrame, s: float = 0.25, k: float = 0.30, m: float = 0.20,
            win: pd.DataFrame | None = None) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    if win is None:
        from quantlab.data import store
        win = store.load("WIN$N", "M5")  # research period only, never the holdout
    win = win.loc[win.index <= idx[-1]]  # nothing newer than the current WDO bar

    d = _daily(df)
    w = _daily(win).reindex(d.index)
    z_win = (w["close_sig"] - w["open"]) / w["adr"]
    z_wdo = (d["close_sig"] - d["open"]) / d["adr"]
    side = -np.sign(z_win)
    ok = (
        (z_win.abs() >= k) & (z_wdo * side <= m) & (side != 0)
        & (d["first_t"] <= LAST_FIRST_BAR) & (w["first_t"] <= LAST_FIRST_BAR)
        & ~_rollover_days(d.index) & d["adr"].notna() & w["adr"].notna()
    ).fillna(False)

    on_bar = pd.Series(idx.time == SIGNAL_BAR, index=idx)
    side_b = pd.Series(side.where(ok).reindex(day).to_numpy(), index=idx)
    adr = pd.Series(d["adr"].reindex(day).to_numpy(), index=idx)
    stop = s * adr
    target = TARGET_MULT * stop
    valid = on_bar & side_b.notna() & (stop > 0) & (target > 0)
    out = pd.DataFrame({"position": side_b, "stop": stop, "target": target}, index=idx).where(valid)
    out = out.groupby(day).ffill()  # hold the side to the end of the session
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="defasagem_dolar_bolsa",
    description="WDO: at 11:30, trade against the WIN morning move when the dollar has not followed; stop s*adr, target 1.5x stop",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"s": 0.25, "k": 0.30, "m": 0.20},
    grid={"s": [0.20, 0.25, 0.30]},
    title="Defasagem do dólar em relação à bolsa",
    summary="Se o Ibovespa futuro (WIN) andou bem para um lado até 11:30 e o dólar ainda não acompanhou, opera o dólar no lado oposto ao da bolsa, com stop e alvo fixos proporcionais à amplitude média diária.",
    param_help={
        "s": "Tamanho do stop, em fração da amplitude média diária do dólar nos últimos 20 pregões (o alvo é 1,5 vez o stop).",
        "k": "Movimento mínimo do WIN desde a abertura até 11:30, em fração da amplitude média diária do WIN.",
        "m": "Movimento máximo que o dólar pode ter feito a favor do lado esperado, em fração da amplitude média diária do dólar.",
    },
)
