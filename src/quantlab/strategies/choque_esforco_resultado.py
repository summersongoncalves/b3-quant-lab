"""WDO follows a shock bar: wide range, high volume for the time of day, close at the extreme.

rng = high - low. rng_ref / vol_ref = median of rng / volume at the same hh:mm over the previous 20
sessions (day x time table, rolling(20, min_periods=20).median().shift(1)). rr = rng/rng_ref,
rv = volume/vol_ref, clv = (close - low) / rng. Shock = rr >= k and rv >= k. Buy if clv >= 0.75,
sell if clv <= 0.25. Signal bar labelled 09:30..16:00, first qualifying bar of the day only
(so only bars up to the current one are used). Stop = s*adr (adr = mean daily high-low of the 20
previous sessions), target = 1.5*stop, both fixed at the signal bar close. The side is held for
`horizonte` bars from the signal bar (bars t..t+horizonte-1), then position = 0 until the end of
the session. Rollover window (last two weekdays of the month) skipped with a calendar only.
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

REF_DAYS = 20
ADR_DAYS = 20
TARGET_MULT = 1.5
CLV_HI = 0.75
CLV_LO = 0.25
FIRST_SIGNAL = pd.Timestamp("09:30").time()
LAST_SIGNAL = pd.Timestamp("16:00").time()


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def _same_time_median(values: pd.Series, day: pd.DatetimeIndex, times: pd.Index) -> pd.Series:
    """Median of `values` at the same hh:mm over the previous REF_DAYS sessions (NaN if fewer)."""
    tab = pd.DataFrame({"d": day, "t": times, "v": values.to_numpy()}).pivot(index="d", columns="t", values="v")
    ref = tab.rolling(REF_DAYS, min_periods=REF_DAYS).median().shift(1)  # previous sessions only
    r = ref.index.get_indexer(day)
    c = ref.columns.get_indexer(times)
    return pd.Series(ref.to_numpy()[r, c], index=values.index)


def signals(df: pd.DataFrame, s: float = 0.20, k: float = 2.5, horizonte: int = 12) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    times = pd.Index(idx.time)

    rng = df["high"] - df["low"]
    rr = rng / _same_time_median(rng, day, times)
    rv = df["volume"].astype(float) / _same_time_median(df["volume"].astype(float), day, times)
    clv = (df["close"] - df["low"]) / rng.where(rng > 0)

    side = pd.Series(np.where(clv >= CLV_HI, 1.0, np.where(clv <= CLV_LO, -1.0, 0.0)), index=idx)
    shock = (rr >= k) & (rv >= k) & clv.notna() & (side != 0)
    t = pd.Series(times, index=idx)
    in_win = (t >= FIRST_SIGNAL) & (t <= LAST_SIGNAL)

    adr_daily = (df["high"].groupby(day).max() - df["low"].groupby(day).min()).rolling(ADR_DAYS).mean().shift(1)
    adr = pd.Series(adr_daily.reindex(day).to_numpy(), index=idx)
    roll = pd.Series(_rollover_days(adr_daily.index).reindex(day).to_numpy(), index=idx)
    stop = s * adr
    target = TARGET_MULT * stop

    cand = shock & in_win & ~roll & adr.notna() & (stop > 0) & (target > 0)
    first = cand & (cand.astype(int).groupby(day).cumsum() == 1)

    # Hold the side for `horizonte` bars (signal bar included), then flat until the end of the session.
    pos_in_day = pd.Series(np.arange(len(idx)), index=idx)
    entry_pos = pos_in_day.where(first).groupby(day).ffill()
    held = entry_pos.notna() & ((pos_in_day - entry_pos) < horizonte)
    held_side = side.where(first).groupby(day).ffill()
    return pd.DataFrame({
        "position": held_side.where(held, 0.0).fillna(0.0),
        "stop": stop.where(held),
        "target": target.where(held),
    }, index=idx)


STRATEGY = Strategy(
    name="choque_esforco_resultado",
    description="WDO: follow a wide, high-volume bar closing at its extreme; stop s*adr, target 1.5x stop, 12-bar time exit",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"s": 0.20, "k": 2.5, "horizonte": 12},
    grid={"s": [0.15, 0.20]},
    title="Barra de choque com esforço e resultado",
    summary="Quando uma barra de 5 minutos do dólar é muito larga, tem volume muito alto para o horário e fecha perto de uma ponta, entra no lado do fechamento, com stop e alvo fixos e saída por tempo em 1 hora.",
    param_help={
        "s": "Tamanho do stop, em fração da amplitude média diária do dólar nos últimos 20 pregões (o alvo é 1,5 vez o stop).",
        "k": "Quantas vezes a amplitude e o volume da barra precisam superar a mediana do mesmo horário nos 20 pregões anteriores (fixo em 2,5).",
        "horizonte": "Número de barras de 5 minutos até a saída por tempo (fixo em 12, ou seja, 1 hora).",
    },
)
