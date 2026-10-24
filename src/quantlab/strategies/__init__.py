"""Strategy contract.

Each strategy is a module in this package exposing `STRATEGY = Strategy(...)`.
`signal_fn(df, **params)` returns the TARGET position for each bar, in [-1, 1],
using only data up to that bar's close. The engine executes it on the next bar.

For a stop loss / take profit, return a DataFrame with columns `position`,
`stop` and `target` instead: the two distances (price units, from the entry
fill) are read at the signal bar and fixed for the trade. See backtest/engine.py.
"""

import importlib
import itertools
import pkgutil
from dataclasses import dataclass, field
from typing import Callable

import pandas as pd


@dataclass
class Strategy:
    name: str
    description: str
    timeframe: str
    daytrade: bool
    signal_fn: Callable[..., pd.Series]
    params: dict
    # Values to search in validation. Every combination counts as a trial.
    grid: dict[str, list] = field(default_factory=dict)
    # Shown in the web UI, so written in Portuguese: a friendly name, a one-line
    # plain-language rule, and what each parameter means.
    title: str = ""
    summary: str = ""
    param_help: dict[str, str] = field(default_factory=dict)

    def signals(self, df: pd.DataFrame, **overrides) -> pd.Series:
        return self.signal_fn(df, **{**self.params, **overrides})

    def grid_combinations(self) -> list[dict]:
        if not self.grid:
            return [dict(self.params)]
        keys = list(self.grid)
        return [{**self.params, **dict(zip(keys, values))} for values in itertools.product(*self.grid.values())]


def load(name: str) -> Strategy:
    return importlib.import_module(f"quantlab.strategies.{name}").STRATEGY


def available() -> list[str]:
    return sorted(m.name for m in pkgutil.iter_modules(__path__) if not m.name.startswith("_"))
