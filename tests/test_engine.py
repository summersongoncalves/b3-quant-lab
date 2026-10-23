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
