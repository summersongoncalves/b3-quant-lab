"""Checks that separate a real edge from luck and bugs.

References:
  - Bailey & Lopez de Prado (2012), "The Sharpe Ratio Efficient Frontier" (PSR)
  - Bailey & Lopez de Prado (2014), "The Deflated Sharpe Ratio"
  - Lopez de Prado (2018), "Advances in Financial Machine Learning", ch. 7, 11-14
"""

import numpy as np
import pandas as pd
from scipy.stats import norm

from quantlab.backtest import engine
from quantlab.backtest.instruments import Instrument
from quantlab.backtest.metrics import summarize
from quantlab.strategies import Strategy

EULER_GAMMA = 0.5772156649


def lookahead_check(strategy: Strategy, df: pd.DataFrame, params: dict, checks: int = 25) -> list[str]:
    """Recompute signals on truncated data. A causal strategy gives the same
    signal at bar k whether or not it can see bars after k."""
    full = strategy.signals(df, **params)
    problems = []
    start = min(len(df) // 4, 500)
    for k in np.linspace(start, len(df) - 1, checks, dtype=int):
        truncated = strategy.signals(df.iloc[: k + 1], **params)
        if not np.isclose(truncated.iloc[-1], full.iloc[k], equal_nan=True):
            problems.append(f"bar {df.index[k]}: {truncated.iloc[-1]} with data up to k vs {full.iloc[k]} with full data")
    return problems


def probabilistic_sharpe(sr: float, n: int, skew: float, kurt: float, benchmark: float = 0.0) -> float:
    """Probability that the true (daily) Sharpe is above `benchmark`, given the
    sample length and the non-normality of returns."""
    if n < 2:
        return 0.0
    denom = np.sqrt(max(1 - skew * sr + (kurt - 1) / 4 * sr**2, 1e-12))
    return float(norm.cdf((sr - benchmark) * np.sqrt(n - 1) / denom))


def expected_max_sharpe(n_trials: int, var_sharpe: float) -> float:
    """Daily Sharpe the best of `n_trials` skill-less strategies would show by chance."""
    if n_trials < 2 or var_sharpe <= 0:
        return 0.0
    return float(np.sqrt(var_sharpe) * (
        (1 - EULER_GAMMA) * norm.ppf(1 - 1 / n_trials) + EULER_GAMMA * norm.ppf(1 - 1 / (n_trials * np.e))
    ))


def deflated_sharpe(summary: dict, n_trials: int, var_sharpe: float) -> float:
    return probabilistic_sharpe(
        summary["sharpe_daily"], summary["days"], summary["skew"], summary["kurtosis"],
        benchmark=expected_max_sharpe(n_trials, var_sharpe),
    )


def grid_search(strategy: Strategy, df: pd.DataFrame, instrument: Instrument) -> list[tuple[dict, dict]]:
    out = []
    for params in strategy.grid_combinations():
        result = engine.run(df, strategy.signals(df, **params), instrument, strategy.daytrade)
        out.append((params, summarize(result)))
    return out


def walk_forward(strategy: Strategy, df: pd.DataFrame, instrument: Instrument,
                 train_days: int, test_days: int) -> tuple[engine.BacktestResult, list[dict], pd.Series]:
    """Pick the best params on each train window, trade them on the next test window.

    Signals are computed on train+test together so indicators are warmed up,
    but P&L is only taken from the test window. The stitched test windows are
    the out-of-sample (OOS) result.
    """
    days = df.index.normalize().unique()
    folds, oos_parts = [], []
    for i in range(train_days, len(days), test_days):
        train_days_idx = days[i - train_days: i]
        test_days_idx = days[i: i + test_days]
        window = df[(df.index >= train_days_idx[0]) & (df.index < (test_days_idx[-1] + pd.Timedelta(days=1)))]
        is_test = window.index >= test_days_idx[0]

        best_params, best_sharpe = None, -np.inf
        for params in strategy.grid_combinations():
            sig = strategy.signals(window, **params)
            res = engine.run(window[~is_test], sig[~is_test], instrument, strategy.daytrade)
            s = summarize(res)["sharpe"]
            if s > best_sharpe:
                best_params, best_sharpe = params, s

        # Signals see the train window for warm-up, but only test bars are traded.
        oos_parts.append(strategy.signals(window, **best_params)[is_test])
        folds.append({"test_start": str(test_days_idx[0].date()), "test_end": str(test_days_idx[-1].date()),
                      "params": best_params, "train_sharpe": round(best_sharpe, 2)})

    if not oos_parts:
        raise ValueError(f"Not enough data: {len(days)} days for train={train_days} + test={test_days}")
    # One run over the stitched test windows, so a position switching params
    # between folds pays its exit/entry costs like it would in real life.
    target = pd.concat(oos_parts)
    oos = engine.run(df.loc[target.index], target, instrument, strategy.daytrade)
    return oos, folds, target
