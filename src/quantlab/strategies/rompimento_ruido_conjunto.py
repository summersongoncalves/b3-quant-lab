"""WDO follows a noise-band breakout when WIN breaks its own band on the opposite side.

For X in {WDO, WIN}: open_X = open of the first bar of the day; mv_X(t) = |close_X(t) - open_X|;
band_X(t) = mean of mv_X at the same hh:mm over the previous `faixa` sessions (day x time table,
shift(1); any missing session => no signal) (Zarattini, Aziz & Barbon 2024). rompe_X = +1 above
open + band, -1 below open - band, else 0. conj(t) = rompe_WDO != 0 and rompe_WIN == -rompe_WDO.
Trigger = conj(t) and not conj(t-1) (previous bar of the same session), signal bar labelled
10:00..15:30, first trigger of the day only. Side = rompe_WDO. Stop = s*adr_WDO (adr = mean daily
high-low of the 20 previous sessions), target = 1.5*stop, fixed at the signal bar close. The side is
held for `horizonte` bars from the signal bar (bars t..t+horizonte-1), then position = 0 until the
end of the session. Rollover window (last two weekdays of the month) skipped with a calendar only.

WIN comes from `store.load("WIN$N", "M5")` (research period only) unless `win` is passed (used by the
causality test); only WIN bars with timestamp <= the last WDO bar are used and aligned by exact timestamp.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

ADR_DAYS = 20
TARGET_MULT = 1.5
FIRST_SIGNAL = pd.Timestamp("10:00").time()
LAST_SIGNAL = pd.Timestamp("15:30").time()


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def _breakout(df: pd.DataFrame, n: int) -> pd.Series:
    """rompe_X per bar: +1/-1 outside open_day +/- mean |close-open_day| at the same time (n prior days)."""
    day = df.index.normalize()
    op = df["open"].groupby(day).transform("first")
    mv = (df["close"] - op).abs()
    times = pd.Index(df.index.time)
    tab = pd.DataFrame({"d": day, "t": times, "mv": mv.to_numpy()}).pivot(index="d", columns="t", values="mv")
    band = tab.rolling(n, min_periods=n).mean().shift(1)  # previous sessions only
    r = band.index.get_indexer(day)
    c = band.columns.get_indexer(times)
    b = pd.Series(band.to_numpy()[r, c], index=df.index)
    up = df["close"] > op + b
    dn = df["close"] < op - b
    out = pd.Series(np.where(up, 1.0, np.where(dn, -1.0, 0.0)), index=df.index)
    return out.where(b.notna())


def signals(df: pd.DataFrame, s: float = 0.20, faixa: int = 14, horizonte: int = 24,
            win: pd.DataFrame | None = None) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    if win is None:
        from quantlab.data import store
        win = store.load("WIN$N", "M5")  # research period only, never the holdout
    win = win.loc[win.index <= idx[-1]]  # nothing newer than the current WDO bar

    r_wdo = _breakout(df, faixa)
    r_win = _breakout(win, faixa).reindex(idx)  # exact timestamp; missing => NaN => no signal
    conj = ((r_wdo != 0) & (r_win == -r_wdo) & r_wdo.notna() & r_win.notna())
    prev = conj.groupby(day).shift(1).fillna(False).astype(bool)
    trig = conj & ~prev
    t = pd.Series(idx.time, index=idx)
    in_win = (t >= FIRST_SIGNAL) & (t <= LAST_SIGNAL)

    adr_daily = (df["high"].groupby(day).max() - df["low"].groupby(day).min()).rolling(ADR_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=idx)
    roll = pd.Series(_rollover_days(adr_daily.index).reindex(day).to_numpy(), index=idx)
    stop = s * adr
    target = TARGET_MULT * stop

    cand = trig & in_win & ~roll & adr.notna() & (stop > 0) & (target > 0)
    first = cand & (cand.astype(int).groupby(day).cumsum() == 1)

    # Hold the side for `horizonte` bars (signal bar included), then flat until the end of the session.
    pos_in_day = pd.Series(np.arange(len(idx)), index=idx)
    entry_pos = pos_in_day.where(first).groupby(day).ffill()
    held = entry_pos.notna() & ((pos_in_day - entry_pos) < horizonte)
    side = r_wdo.where(first).groupby(day).ffill()
    out = pd.DataFrame({
        "position": side.where(held, 0.0).fillna(0.0),
        "stop": stop.where(held),
        "target": target.where(held),
    }, index=idx)
    return out


STRATEGY = Strategy(
    name="rompimento_ruido_conjunto",
    description="WDO: follow the noise-band breakout when WIN breaks out on the opposite side; stop s*adr, target 1.5x stop, 24-bar time exit",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"s": 0.20, "faixa": 14, "horizonte": 24},
    grid={"s": [0.20, 0.25]},
    title="Rompimento conjunto da faixa de ruído",
    summary="Se o dólar e a bolsa saem da faixa de ruído da abertura ao mesmo tempo, em lados opostos, entra no lado do rompimento do dólar, com stop e alvo fixos e saída por tempo em 2 horas.",
    param_help={
        "s": "Tamanho do stop, em fração da amplitude média diária do dólar nos últimos 20 pregões (o alvo é 1,5 vez o stop).",
        "faixa": "Número de pregões anteriores usados para calcular a faixa de ruído no mesmo horário (fixo em 14, valor do artigo).",
        "horizonte": "Número de barras de 5 minutos até a saída por tempo (fixo em 24, ou seja, 2 horas).",
    },
)
