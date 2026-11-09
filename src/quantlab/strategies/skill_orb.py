"""Faithful B3 port of the opening range breakout from github.com/jakeschincariol/day-trader-skill
(trader-entry + trader-exit, commit 3d0f4ef). Studied for a video; the skill itself is US-only.

Rules, as in the skill:
- Opening range = the first 15 minutes (3 five-minute bars) of the session.
- Long only. Entry on the first CLOSED bar after the range whose close is ABOVE the range high
  (a close equal to the high does not count).
- No entries in the last 30 minutes of the session (the skill: none after 15:30 New York, close 16:00).
- Stop = opening-range midpoint ("or-mid", the skill's default). Target = `target_r` x risk
  (the skill's default is 2R; its README example uses 1R).
- The skill refuses a stop closer than 0.05% of the price (too tight to survive the spread).
- Flat at the close (the skill: flat by 15:55; here the engine closes at the last bar).

Differences forced by the engine: the skill enters at the signal bar's close; the engine fills at the
next bar's open, so stop/target are distances fixed at the signal bar and applied from that fill.
The session close is taken from the previous session's last bar (known in advance, no peeking),
so it works for WIN, WDO and stocks alike; the first day of the data has no entries. One entry per day, full size (weight 1): results are read in R multiples by
`python -m quantlab.research.skill_orb_report`.
"""

import pandas as pd

from quantlab.strategies import Strategy
from quantlab.strategies._helpers import session_bar_number

MIN_RISK_PCT = 0.0005


def signals(df: pd.DataFrame, range_bars: int = 3, target_r: float = 2.0, no_entry_last_min: int = 30) -> pd.DataFrame:
    day = df.index.normalize()
    bar_no = session_bar_number(df)
    in_range = bar_no < range_bars

    or_high = df["high"].where(in_range).groupby(day).transform("max")
    or_low = df["low"].where(in_range).groupby(day).transform("min")
    or_mid = (or_high + or_low) / 2
    full_range = in_range.groupby(day).transform("sum") == range_bars

    # Session close = the previous session's last bar time of day. Reading today's own last bar
    # would peek at the future (the validator's look-ahead check caught it on WDO).
    ts = pd.Series(df.index, index=df.index)
    last_tod = (ts.groupby(day).max() - ts.groupby(day).max().index).shift(1)
    cutoff = day + day.map(last_tod) - pd.Timedelta(minutes=no_entry_last_min)
    cutoff = pd.Series(cutoff, index=df.index)
    bar_close_time = pd.Series(df.index + pd.Timedelta(minutes=5), index=df.index)
    on_time = bar_close_time <= cutoff

    risk = df["close"] - or_mid
    trigger = (~in_range) & full_range & on_time & (df["close"] > or_high) & (risk >= MIN_RISK_PCT * df["close"])
    first = trigger & (trigger.groupby(day).cumsum() == 1)

    out = pd.DataFrame({"position": 1.0, "stop": risk, "target": target_r * risk}, index=df.index).where(first)
    out = out.groupby(day).ffill()
    out["position"] = out["position"].fillna(0.0)
    return out


STRATEGY = Strategy(
    name="skill_orb",
    description="day-trader-skill ORB ported to B3: 15-min range, long on close above, stop at range mid, target in R",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"range_bars": 3, "target_r": 2.0, "no_entry_last_min": 30},
    grid={"target_r": [1.0, 2.0]},
    title="Rompimento da abertura (regra da day-trader-skill)",
    summary="Cópia da regra da skill do TikTok: marca a máxima e a mínima dos primeiros 15 minutos, compra quando uma barra fecha acima da máxima, stop no meio da faixa, alvo de 1R ou 2R e zera no fim do dia.",
    param_help={
        "range_bars": "Barras de 5 min que formam a faixa de abertura (3 = 15 min, como na skill).",
        "target_r": "Alvo em múltiplos do risco: 1 = ganha o mesmo que arrisca; 2 = o dobro (padrão da skill).",
        "no_entry_last_min": "Minutos finais do pregão sem entradas novas (a skill usa 30).",
    },
)
