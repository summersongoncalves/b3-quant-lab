"""Building blocks for strategies. Every helper here is causal (uses only past data)."""

import pandas as pd


def session_bar_number(df: pd.DataFrame) -> pd.Series:
    """0 for the first bar of each day, 1 for the second, ..."""
    return df.groupby(df.index.normalize()).cumcount()


def only_between(position: pd.Series, start: str, end: str) -> pd.Series:
    """Zero the target position outside the [start, end] clock window (e.g. '09:15', '17:30')."""
    t = position.index.time
    inside = (t >= pd.Timestamp(start).time()) & (t <= pd.Timestamp(end).time())
    return position.where(inside, 0.0)


def hold_until_flat_signal(entries: pd.Series, exits: pd.Series) -> pd.Series:
    """Turn entry (+1/-1) and exit (True) events into a position that persists between them."""
    state = entries.where(entries != 0)
    state = state.where(~exits, 0.0)
    return state.ffill().fillna(0.0)


def vwap(df: pd.DataFrame, period: str = "D") -> pd.Series:
    """Volume-weighted average price since the start of the day ("D") or week ("W").

    Uses the typical price (high + low + close) / 3 of each bar, accumulated up to
    and including the current bar, so it is known at that bar's close. On a
    continuous futures series (e.g. WIN$N) the weekly VWAP of a roll week mixes
    two contracts.
    """
    day = df.index.normalize()
    if period == "D":
        key = day
    elif period == "W":
        key = day - pd.to_timedelta(df.index.day_of_week, unit="D")  # Monday of the week
    else:
        raise ValueError(f"period must be 'D' or 'W', got {period!r}")
    typical = (df["high"] + df["low"] + df["close"]) / 3
    volume = df["volume"].astype(float)
    cum_pv = (typical * volume).groupby(key).cumsum()
    cum_v = volume.groupby(key).cumsum()
    return (cum_pv / cum_v).where(cum_v > 0)


def relative_volume(df: pd.DataFrame, days: int = 20) -> pd.Series:
    """Day's volume so far / median of the same clock time over the previous `days` days.

    1.0 means a normal day up to this bar; 2.0 means twice the usual volume.
    NaN until there are `days` past days for that clock time.
    """
    cum = df["volume"].astype(float).groupby(df.index.normalize()).cumsum()
    usual = cum.groupby(df.index.time).transform(lambda s: s.rolling(days).median().shift(1))
    return cum / usual


def rsi_from_changes(delta: pd.Series, period: int = 2) -> pd.Series:
    """Wilder RSI computed on a series of changes (NaN treated as 0). NaN when no movement at all."""
    d = delta.fillna(0.0)
    au = d.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    ad = (-d).clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    total = au + ad
    return (100 * au / total).where(total > 0)
