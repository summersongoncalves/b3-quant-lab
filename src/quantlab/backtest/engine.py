"""Vectorized bar-by-bar backtest.

Timing rule (the single most important thing in this file):
  A strategy's position for bar t is decided with data up to the CLOSE of
  bar t, and is executed at the OPEN of bar t+1. So the position held during
  bar t is positions.shift(1). Any strategy that "trades at the close it just
  saw" is peeking into the future.

P&L of bar t is split in two parts:
  - gap:      position carried into the bar  x (open_t  - close_{t-1})
  - intrabar: position held after the open   x (exit_t  - open_t)
  where exit_t is close_t, or the stop/target price if a bracket filled in t.

Day trade mode: nothing is carried overnight. The first bar of each day starts
flat and every position is closed at the close of the day's last bar.

Brackets (stop loss / take profit): a strategy may return a DataFrame with
columns `position`, `stop`, `target` instead of a Series. `stop` and `target`
are DISTANCES in price units from the entry fill, decided at the signal bar
(same timing rule) and fixed for the life of the trade; NaN means no order.
Inside a bar the path between high and low is unknown, so:
  - if both stop and target are touched in the same bar, the stop wins
    (marked "stop_both", so the weight of this assumption can be measured);
  - an open beyond the stop fills at the open (gap risk), not at the stop;
  - every bracket fill pays the full unit cost, slippage included.
After a bracket exit the strategy stays flat until its target position goes
to zero or flips sign; it does not re-enter the same signal.

Sizing is fixed (no compounding): stocks use `capital` of notional per unit of
position, futures use `contracts` per unit. Positions are in [-1, 1].
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from quantlab.backtest.instruments import Instrument


@dataclass
class BacktestResult:
    bars: pd.DataFrame  # per bar: held, gap, intrabar, pnl_gross, cost, pnl, exit_kind
    trades: pd.DataFrame
    capital: float
    instrument: Instrument
    daytrade: bool


def run(
    df: pd.DataFrame,
    positions: pd.Series | pd.DataFrame,
    instrument: Instrument,
    daytrade: bool,
    capital: float = 100_000.0,
    contracts: int = 1,
    cost_mult: float = 1.0,
) -> BacktestResult:
    if isinstance(positions, pd.DataFrame):
        frame = positions.reindex(df.index)
        target = frame["position"]
        stop = frame["stop"] if "stop" in frame else None
        take = frame["target"] if "target" in frame else None
    else:
        target, stop, take = positions.reindex(df.index), None, None
    target = target.fillna(0.0).clip(-1, 1)
    day = pd.Series(df.index.normalize(), index=df.index)

    if daytrade:
        held = target.groupby(day).shift(1).fillna(0.0)
        last_bar_of_day = day != day.shift(-1)
    else:
        held = target.shift(1).fillna(0.0)
        last_bar_of_day = pd.Series(False, index=df.index)

    open_, close = df["open"], df["close"]
    exit_kind = pd.Series("", index=df.index)
    if stop is not None or take is not None:
        held, held_end, exit_px, exit_kind = _brackets(df, held, stop, take)
    else:
        held_end, exit_px = held.copy(), close.copy()
    held_end = held_end.where(~last_bar_of_day, 0.0)
    exit_kind = exit_kind.where((exit_kind != "") | ~last_bar_of_day | (held == 0), "close")
    # Position carried into bar t: whatever was left at the end of t-1.
    prev_held = held_end.shift(1).fillna(0.0)
    prev_close = close.shift(1).fillna(open_)

    # Cost per unit of position traded, in R$.
    if instrument.kind == "future":
        unit_cost = contracts * (instrument.fee_per_unit(daytrade) + instrument.slippage_ticks * instrument.tick_size * instrument.point_value)
        gap = prev_held * (open_ - prev_close) * instrument.point_value * contracts
        intrabar = held * (exit_px - open_) * instrument.point_value * contracts
    else:
        unit_cost = capital * (instrument.fee_per_unit(daytrade) + instrument.slippage_ticks * instrument.tick_size / open_)
        gap = prev_held * capital * (open_ / prev_close - 1)
        intrabar = held * capital * (exit_px / open_ - 1)
    unit_cost = unit_cost * cost_mult

    traded_at_open = (held - prev_held).abs()
    closed_in_bar = (held - held_end).abs()
    cost = (traded_at_open + closed_in_bar) * unit_cost

    bars = pd.DataFrame({
        "held": held,
        "gap": gap,
        "intrabar": intrabar,
        "pnl_gross": gap + intrabar,
        "cost": cost,
    })
    bars["pnl"] = bars["pnl_gross"] - bars["cost"]
    bars["exit_kind"] = exit_kind
    trades = _trades(bars, prev_held, traded_at_open, closed_in_bar, unit_cost)
    return BacktestResult(bars=bars, trades=trades, capital=capital, instrument=instrument, daytrade=daytrade)


def _brackets(df, held, stop, take):
    """Walk the bars applying stop/target orders. Returns the position at the
    open, the position at the close, the exit price of each bar and the kind of
    bracket that filled ("stop", "stop_both", "target" or "")."""
    want_all = held.to_numpy()
    # Distances are decided at the signal bar, so they apply from the next bar.
    nan = np.full(len(df), np.nan)
    stop_d = stop.shift(1).to_numpy(dtype=float) if stop is not None else nan
    take_d = take.shift(1).to_numpy(dtype=float) if take is not None else nan
    o, h, l, c = (df[col].to_numpy(dtype=float) for col in ("open", "high", "low", "close"))

    start, end = want_all.copy(), want_all.copy()
    exit_px = c.copy()
    kind = np.full(len(df), "", dtype=object)
    pos, blocked = 0.0, 0.0
    sl = tp = np.nan
    for t in range(len(df)):
        want = want_all[t]
        if blocked:
            if np.sign(want) == blocked:
                want = 0.0
            else:
                blocked = 0.0
        side = np.sign(want)
        if side != 0 and side != np.sign(pos):
            sl = o[t] - side * stop_d[t]
            tp = o[t] + side * take_d[t]
        pos = want
        start[t] = pos
        if side != 0:
            stop_hit = (side > 0 and l[t] <= sl) or (side < 0 and h[t] >= sl)
            take_hit = (side > 0 and h[t] >= tp) or (side < 0 and l[t] <= tp)
            if stop_hit:
                exit_px[t] = o[t] if (o[t] - sl) * side <= 0 else sl
                kind[t] = "stop_both" if take_hit else "stop"
            elif take_hit:
                exit_px[t] = o[t] if (o[t] - tp) * side >= 0 else tp
                kind[t] = "target"
            if kind[t]:
                blocked, pos = side, 0.0
        end[t] = pos
    idx = df.index
    return pd.Series(start, idx), pd.Series(end, idx), pd.Series(exit_px, idx), pd.Series(kind, idx)


def _trades(bars, prev_held, traded_at_open, closed_in_bar, unit_cost) -> pd.DataFrame:
    """A trade is a run of bars holding a position with the same sign."""
    held = bars["held"]
    sign = np.sign(held)
    prev_sign = np.sign(prev_held)
    new_trade = (sign != 0) & (sign != prev_sign)
    trade_id = new_trade.cumsum().where(sign != 0)

    # The gap at bar t belongs to whatever was carried into t.
    prev_trade_id = trade_id.shift(1).where(prev_held != 0)

    # Costs: resizing within a trade stays with it; a flip or exit charges the
    # closing part to the previous trade and the opening part to the new one.
    same_trade = (sign == prev_sign) & (sign != 0)
    exit_cost = np.where(same_trade, 0.0, prev_held.abs()) * unit_cost
    entry_cost = np.where(same_trade, traded_at_open, held.abs()) * unit_cost
    close_cost = closed_in_bar * unit_cost

    parts = pd.concat([
        pd.DataFrame({"trade": trade_id, "pnl": bars["intrabar"] - entry_cost - close_cost}),
        pd.DataFrame({"trade": prev_trade_id, "pnl": bars["gap"] - exit_cost}),
    ]).dropna(subset=["trade"])
    if parts.empty:
        return pd.DataFrame(columns=["entry", "exit", "side", "bars", "exit_reason", "pnl"])

    in_trade = pd.DataFrame({"trade": trade_id, "time": bars.index, "side": sign,
                             "kind": bars["exit_kind"]}).dropna(subset=["trade"])
    spans = in_trade.groupby("trade").agg(entry=("time", "first"), exit=("time", "last"), side=("side", "first"),
                                          bars=("time", "size"), exit_reason=("kind", "last"))
    spans["exit_reason"] = spans["exit_reason"].replace("", "signal")
    spans["pnl"] = parts.groupby("trade")["pnl"].sum()
    return spans.reset_index(drop=True)
