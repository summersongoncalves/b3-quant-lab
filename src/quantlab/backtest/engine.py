"""Vectorized bar-by-bar backtest.

Timing rule (the single most important thing in this file):
  A strategy's position for bar t is decided with data up to the CLOSE of
  bar t, and is executed at the OPEN of bar t+1. So the position held during
  bar t is positions.shift(1). Any strategy that "trades at the close it just
  saw" is peeking into the future.

P&L of bar t is split in two parts:
  - gap:      position held before the open  x (open_t  - close_{t-1})
  - intrabar: position held after the open   x (close_t - open_t)

Day trade mode: nothing is carried overnight. The first bar of each day starts
flat and every position is closed at the close of the day's last bar.

Sizing is fixed (no compounding): stocks use `capital` of notional per unit of
position, futures use `contracts` per unit. Positions are in [-1, 1].
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from quantlab.backtest.instruments import Instrument


@dataclass
class BacktestResult:
    bars: pd.DataFrame  # per bar: held, pnl_gross, cost, pnl
    trades: pd.DataFrame
    capital: float
    instrument: Instrument
    daytrade: bool


def run(
    df: pd.DataFrame,
    positions: pd.Series,
    instrument: Instrument,
    daytrade: bool,
    capital: float = 100_000.0,
    contracts: int = 1,
    cost_mult: float = 1.0,
) -> BacktestResult:
    target = positions.reindex(df.index).fillna(0.0).clip(-1, 1)
    day = pd.Series(df.index.normalize(), index=df.index)

    if daytrade:
        held = target.groupby(day).shift(1).fillna(0.0)
        prev_held = held.groupby(day).shift(1).fillna(0.0)
        last_bar_of_day = day != day.shift(-1)
    else:
        held = target.shift(1).fillna(0.0)
        prev_held = held.shift(1).fillna(0.0)
        last_bar_of_day = pd.Series(False, index=df.index)

    open_, close = df["open"], df["close"]
    prev_close = close.shift(1).fillna(open_)

    # Cost per unit of position traded, in R$.
    if instrument.kind == "future":
        unit_cost = contracts * (instrument.fee_per_unit(daytrade) + instrument.slippage_ticks * instrument.tick_size * instrument.point_value)
        gap = prev_held * (open_ - prev_close) * instrument.point_value * contracts
        intrabar = held * (close - open_) * instrument.point_value * contracts
    else:
        unit_cost = capital * (instrument.fee_per_unit(daytrade) + instrument.slippage_ticks * instrument.tick_size / open_)
        gap = prev_held * capital * (open_ / prev_close - 1)
        intrabar = held * capital * (close / open_ - 1)
    unit_cost = unit_cost * cost_mult

    traded_at_open = (held - prev_held).abs()
    closed_at_eod = held.abs().where(last_bar_of_day, 0.0)
    cost = (traded_at_open + closed_at_eod) * unit_cost

    bars = pd.DataFrame({
        "held": held,
        "gap": gap,
        "intrabar": intrabar,
        "pnl_gross": gap + intrabar,
        "cost": cost,
    })
    bars["pnl"] = bars["pnl_gross"] - bars["cost"]
    trades = _trades(bars, prev_held, traded_at_open, closed_at_eod, unit_cost, day, daytrade)
    return BacktestResult(bars=bars, trades=trades, capital=capital, instrument=instrument, daytrade=daytrade)


def _trades(bars, prev_held, traded_at_open, closed_at_eod, unit_cost, day, daytrade) -> pd.DataFrame:
    """A trade is a run of bars holding a position with the same sign."""
    held = bars["held"]
    sign = np.sign(held)
    prev_sign = np.sign(prev_held)
    new_trade = (sign != 0) & (sign != prev_sign)
    trade_id = new_trade.cumsum().where(sign != 0)

    # The gap at bar t belongs to whatever was held before the open of t.
    if daytrade:
        prev_trade_id = trade_id.groupby(day).shift(1)
    else:
        prev_trade_id = trade_id.shift(1)

    # Costs: resizing within a trade stays with it; a flip or exit charges the
    # closing part to the previous trade and the opening part to the new one.
    same_trade = (sign == prev_sign) & (sign != 0)
    exit_cost = np.where(same_trade, 0.0, prev_held.abs()) * unit_cost
    entry_cost = np.where(same_trade, traded_at_open, held.abs()) * unit_cost
    eod_cost = closed_at_eod * unit_cost

    parts = pd.concat([
        pd.DataFrame({"trade": trade_id, "pnl": bars["intrabar"] - entry_cost - eod_cost}),
        pd.DataFrame({"trade": prev_trade_id, "pnl": bars["gap"] - exit_cost}),
    ]).dropna(subset=["trade"])
    if parts.empty:
        return pd.DataFrame(columns=["entry", "exit", "side", "bars", "pnl"])

    in_trade = pd.DataFrame({"trade": trade_id, "time": bars.index, "side": sign}).dropna(subset=["trade"])
    spans = in_trade.groupby("trade").agg(entry=("time", "first"), exit=("time", "last"), side=("side", "first"), bars=("time", "size"))
    spans["pnl"] = parts.groupby("trade")["pnl"].sum()
    return spans.reset_index(drop=True)
