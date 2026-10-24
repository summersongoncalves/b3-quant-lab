"""Breakout of the previous session's high/low in WDO (stop cascade), stop back inside the old range.

PDH/PDL = high/low of the previous session; adr = mean daily high-low of the 20 previous sessions.
Trades only days whose first bar starts by 09:05, that open inside (PDL, PDH), that are not in the
rollover window (last 2 weekdays of the month, calendar only) and whose previous dataset session was
not in that window. If any 09:00-09:25 bar closes beyond PDH/PDL the day is skipped. In the 09:30-12:55
bars, the first close above PDH (long) or below PDL (short) is the only event of the day; if
over = |close - level| > over_max * adr the day does not trade. Stop distance =
max(over + b * adr, 0.20 * adr), target = k * stop, both measured from the signal close. The side is held
until the end of the session (the engine exits on stop, target or close).
"""

import numpy as np
import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
STOP_FLOOR = 0.20
MAX_FIRST_BAR = pd.Timestamp("09:05").time()
EARLY_START = pd.Timestamp("09:00").time()
EARLY_END = pd.Timestamp("09:25").time()
SIG_START = pd.Timestamp("09:30").time()
SIG_END = pd.Timestamp("12:55").time()


def _rollover_days(days: pd.DatetimeIndex) -> pd.Series:
    """True for dates >= (last weekday of the month - 1 weekday); calendar only, no look-ahead."""
    month_end = days + pd.offsets.BMonthEnd(0)
    return pd.Series(days >= month_end - pd.offsets.BDay(1), index=days)


def signals(df: pd.DataFrame, b: float = 0.20, k: float = 1.5, over_max: float = 0.15) -> pd.DataFrame:
    idx = df.index
    day = idx.normalize()
    t = pd.Series(idx.time, index=idx)

    # Daily quantities, shifted so only past sessions are used.
    d_high = df["high"].groupby(day).max()
    d_low = df["low"].groupby(day).min()
    adr_d = (d_high - d_low).rolling(HISTORY_DAYS).mean().shift(1)
    pdh_d, pdl_d = d_high.shift(1), d_low.shift(1)
    roll = _rollover_days(d_high.index)
    roll_ok = ~roll & ~roll.shift(1, fill_value=True)  # also skip the session after a rollover-window one
    first_t = pd.Series(idx, index=idx).groupby(day).first().dt.time
    day_ok = (first_t <= MAX_FIRST_BAR) & roll_ok

    def up(s):
        return pd.Series(s.reindex(day).to_numpy(), index=idx)

    adr, pdh, pdl, ok = up(adr_d), up(pdh_d), up(pdl_d), up(day_ok).astype(bool)
    opening = df["open"].groupby(day).transform("first")
    close = df["close"]

    broke = (close > pdh) | (close < pdl)
    early = ((t >= EARLY_START) & (t <= EARLY_END) & broke).groupby(day).transform("max")
    inside_open = (opening > pdl) & (opening < pdh)

    in_window = (t >= SIG_START) & (t <= SIG_END)
    event = in_window & broke
    first = event & (event.astype(int).groupby(day).cumsum() == 1)

    side = pd.Series(np.where(close > pdh, 1.0, -1.0), index=idx)
    level = pd.Series(np.where(close > pdh, pdh, pdl), index=idx)
    over = (close - level).abs()
    stop = np.maximum(over + b * adr, STOP_FLOOR * adr)
    target = k * stop

    valid = (
        first
        & ok
        & ~early
        & inside_open
        & adr.notna()
        & pdh.notna()
        & (over <= over_max * adr)
        & (stop > 0)
        & (target > 0)
    )
    out = pd.DataFrame({"position": side, "stop": stop, "target": target}, index=idx).where(valid)
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="rompimento_extremo_anterior",
    description="WDO: first M5 close beyond the previous day's high/low (09:30-12:55); stop back inside the old range, target 1.5x stop",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"b": 0.20, "k": 1.5, "over_max": 0.15},
    grid={"b": [0.15, 0.20, 0.25]},
    title="Rompimento da máxima ou mínima do dia anterior",
    summary="Se o dólar abre dentro do range de ontem e, depois das 09:30, fecha pela primeira vez acima da máxima (ou abaixo da mínima) de ontem, entra a favor do rompimento, com stop de volta dentro do range anterior e alvo de 1,5 vez o stop.",
    param_help={
        "b": "Folga do stop dentro do range anterior, em fração da amplitude média diária.",
        "k": "Tamanho do alvo em múltiplos da distância do stop.",
        "over_max": "Quanto a barra de sinal pode ter passado do nível, em fração da amplitude média diária; acima disso o dia não opera.",
    },
)
