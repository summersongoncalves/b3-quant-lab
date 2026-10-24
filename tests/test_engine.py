import numpy as np
import pandas as pd
import pytest

from quantlab.backtest import engine
from quantlab.backtest.instruments import STOCK, WIN
from quantlab.backtest.metrics import summarize
from quantlab.research import validation
from quantlab.strategies import Strategy, load


def intraday(days=30, bars_per_day=20, seed=0):
    rng = np.random.default_rng(seed)
    idx = [pd.Timestamp("2025-01-02 09:00") + pd.Timedelta(days=d) + pd.Timedelta(minutes=5 * b)
           for d in range(days) for b in range(bars_per_day)]
    close = 120_000 + np.cumsum(rng.normal(0, 50, len(idx)))
    open_ = np.r_[close[0], close[:-1]] + rng.normal(0, 10, len(idx))
    return pd.DataFrame({"open": open_, "high": np.maximum(open_, close) + 20,
                         "low": np.minimum(open_, close) - 20, "close": close}, index=pd.DatetimeIndex(idx))


def daily(n=600, seed=1):
    rng = np.random.default_rng(seed)
    close = 30 * np.exp(np.cumsum(rng.normal(0, 0.02, n)))
    open_ = close * (1 + rng.normal(0, 0.005, n))
    return pd.DataFrame({"open": open_, "high": np.maximum(open_, close) * 1.01,
                         "low": np.minimum(open_, close) * 0.99, "close": close},
                        index=pd.bdate_range("2020-01-01", periods=n))


def test_position_executes_on_next_bar():
    df = daily(10)
    target = pd.Series(0.0, index=df.index)
    target.iloc[3] = 1.0
    res = engine.run(df, target, STOCK, daytrade=False)
    assert res.bars["held"].iloc[3] == 0 and res.bars["held"].iloc[4] == 1


def test_daytrade_is_flat_overnight():
    df = intraday()
    res = engine.run(df, pd.Series(1.0, index=df.index), WIN, daytrade=True)
    first_bars = df.index.normalize() != pd.Series(df.index.normalize()).shift().values
    assert (res.bars["held"][first_bars] == 0).all()
    assert (res.bars["gap"][first_bars] == 0).all()
    assert len(res.trades) == 30


@pytest.mark.parametrize("daytrade", [True, False])
def test_trade_pnl_reconciles_with_bar_pnl(daytrade):
    df = intraday()
    rng = np.random.default_rng(3)
    target = pd.Series(rng.choice([-1.0, -0.5, 0.0, 0.5, 1.0], len(df)), index=df.index)
    res = engine.run(df, target, WIN, daytrade=daytrade)
    assert res.trades["pnl"].sum() == pytest.approx(res.bars["pnl"].sum())


def test_costs_scale():
    df = intraday()
    target = pd.Series(np.where(np.arange(len(df)) % 2, 1.0, -1.0), index=df.index)
    base = summarize(engine.run(df, target, WIN, daytrade=True))
    double = summarize(engine.run(df, target, WIN, daytrade=True, cost_mult=2))
    assert double["total_cost"] == pytest.approx(2 * base["total_cost"])


def test_lookahead_check_catches_peeking():
    peek = Strategy("peek", "uses tomorrow's close", "D1", False,
                    lambda df: np.sign(df["close"].shift(-1) - df["close"]).fillna(0.0), params={})
    assert validation.lookahead_check(peek, daily(), {})


@pytest.mark.parametrize("name,data", [("ma_cross", daily), ("opening_range_breakout", intraday)])
def test_baseline_strategies_are_causal(name, data):
    s = load(name)
    assert validation.lookahead_check(s, data(), s.params) == []


def test_psr_and_dsr_behave():
    assert validation.probabilistic_sharpe(0.1, 500, 0, 3) > 0.95
    assert validation.probabilistic_sharpe(0.0, 500, 0, 3) == pytest.approx(0.5)
    # More trials raise the bar a lucky strategy has to clear.
    assert validation.expected_max_sharpe(1000, 0.01) > validation.expected_max_sharpe(10, 0.01) > 0


def bars_from(rows, start="2025-01-02 10:00"):
    idx = pd.date_range(start, periods=len(rows), freq="5min")
    return pd.DataFrame(rows, columns=["open", "high", "low", "close"], index=idx, dtype=float)


def bracket(df, position, stop, target):
    return pd.DataFrame({"position": position, "stop": stop, "target": target}, index=df.index)


def test_without_brackets_matches_plain_series():
    df = intraday()
    rng = np.random.default_rng(5)
    pos = pd.Series(rng.choice([-1.0, 0.0, 1.0], len(df)), index=df.index)
    plain = engine.run(df, pos, WIN, daytrade=True)
    framed = engine.run(df, bracket(df, pos, np.nan, np.nan), WIN, daytrade=True)
    assert framed.bars["pnl"].sum() == pytest.approx(plain.bars["pnl"].sum())
    assert len(framed.trades) == len(plain.trades)


def test_stop_fills_at_stop_price_and_stays_flat():
    # Long from bar 1 at 100, stop 10 below. Bar 2 trades down to 85.
    df = bars_from([[100, 101, 99, 100], [100, 102, 98, 101], [101, 101, 85, 88], [88, 120, 88, 120]])
    sig = bracket(df, 1.0, 10.0, np.nan)
    res = engine.run(df, sig, WIN, daytrade=True, cost_mult=0)
    assert res.bars["held"].tolist() == [0, 1, 1, 0]  # no re-entry on the same signal
    assert res.trades["pnl"].sum() == pytest.approx((90 - 100) * WIN.point_value)
    assert res.trades["exit_reason"].tolist() == ["stop"]


def test_stop_wins_when_both_touched_in_the_same_bar():
    df = bars_from([[100, 100, 100, 100], [100, 130, 70, 100], [100, 100, 100, 100]])
    res = engine.run(df, bracket(df, 1.0, 10.0, 10.0), WIN, daytrade=True, cost_mult=0)
    assert res.trades["exit_reason"].tolist() == ["stop_both"]
    assert res.trades["pnl"].sum() == pytest.approx(-10 * WIN.point_value)


def test_gap_through_stop_fills_at_open():
    df = daily(5)
    df.iloc[:] = 100.0
    df.iloc[3] = [80.0, 81.0, 79.0, 80.0]  # opens 20 below a stop 10 below
    res = engine.run(df, bracket(df, 1.0, 10.0, np.nan), STOCK, daytrade=False, cost_mult=0)
    assert res.trades["pnl"].iloc[0] == pytest.approx(res.capital * (80 / 100 - 1))


def test_short_target_and_reentry_after_signal_resets():
    df = bars_from([[100, 100, 100, 100], [100, 101, 94, 95], [95, 96, 94, 95], [95, 96, 94, 95], [95, 96, 94, 95]])
    pos = pd.Series([-1.0, -1.0, 0.0, -1.0, -1.0], index=df.index)
    res = engine.run(df, bracket(df, pos, 20.0, 5.0), WIN, daytrade=True, cost_mult=0)
    assert res.bars["held"].tolist() == [0, -1, 0, 0, -1]
    assert res.trades["exit_reason"].tolist() == ["target", "close"]
    assert res.trades["pnl"].iloc[0] == pytest.approx(5 * WIN.point_value)


@pytest.mark.parametrize("daytrade", [True, False])
def test_bracket_pnl_reconciles_and_costs_counted(daytrade):
    df = intraday()
    rng = np.random.default_rng(7)
    pos = pd.Series(rng.choice([-1.0, 0.0, 1.0], len(df)), index=df.index).rolling(6).max().fillna(0)
    res = engine.run(df, bracket(df, pos, 60.0, 90.0), WIN, daytrade=daytrade)
    assert res.trades["pnl"].sum() == pytest.approx(res.bars["pnl"].sum())
    assert {"target"} <= set(res.trades["exit_reason"]) and set(res.trades["exit_reason"]) & {"stop", "stop_both"}
    # Every trade pays its entry and its exit.
    assert res.bars["cost"].sum() == pytest.approx(2 * len(res.trades) * (WIN.fee_per_contract_daytrade if daytrade else WIN.fee_per_contract_swing) + 2 * len(res.trades) * WIN.slippage_ticks * WIN.tick_size * WIN.point_value)


def test_lookahead_check_handles_bracket_frames():
    peek = Strategy("peek", "stop from tomorrow", "D1", False,
                    lambda df: pd.DataFrame({"position": 1.0, "stop": (df["close"].shift(-1) - df["close"]).abs(),
                                             "target": np.nan}, index=df.index), params={})
    assert validation.lookahead_check(peek, daily(), {})
