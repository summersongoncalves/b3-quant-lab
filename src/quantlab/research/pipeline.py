"""Full validation of one strategy on one dataset, with a pass/fail verdict.

The gates are fixed BEFORE looking at results. Changing them after seeing a
report to let a strategy pass defeats their purpose.
"""

import json
from collections import Counter
from datetime import datetime

import numpy as np

from quantlab.backtest import engine
from quantlab.backtest.instruments import for_symbol
from quantlab.backtest.metrics import summarize
from quantlab.config import REPORTS_DIR
from quantlab.data import store
from quantlab.research import registry, report, validation
from quantlab.strategies import load

GATES = {
    "min_oos_sharpe": 0.5,
    "min_oos_trades": 30,
    "min_dsr": 0.95,
    "min_share_positive_years": 0.6,
    "min_share_positive_grid": 0.5,
    "min_sharpe_2x_costs": 0.0,
}


def validate(strategy_name: str, symbol: str, timeframe: str | None = None,
             train_days: int | None = None, test_days: int | None = None) -> dict:
    strategy = load(strategy_name)
    timeframe = timeframe or strategy.timeframe
    dataset = store.dataset_id(symbol, timeframe)
    instrument = for_symbol(symbol)
    df = store.load(symbol, timeframe)
    # Defaults: daily strategies train on ~2 years and trade the next quarter;
    # intraday ones have less history available, so ~4 months / 1 month.
    if train_days is None:
        train_days, test_days = (504, 63) if timeframe == "D1" else (80, 20)

    lookahead = validation.lookahead_check(strategy, df, strategy.params)

    grid = validation.grid_search(strategy, df, instrument)
    for params, s in grid:
        registry.record(strategy.name, dataset, params, s, phase="search")
    grid_sharpes = [s["sharpe"] for _, s in grid]

    oos, folds, target = validation.walk_forward(strategy, df, instrument, train_days, test_days)
    oos_summary = summarize(oos)
    registry.record(strategy.name, dataset, {"walk_forward": True}, oos_summary, phase="walkforward")
    stressed = summarize(engine.run(df.loc[target.index], target, instrument, strategy.daytrade, cost_mult=2.0))

    n_trials, var_sharpe = registry.trials(dataset)
    dsr = validation.deflated_sharpe(oos_summary, n_trials, var_sharpe)
    years = oos_summary["sharpe_by_year"]

    checks = {
        "no_lookahead": not lookahead,
        "oos_sharpe": oos_summary["sharpe"] >= GATES["min_oos_sharpe"],
        "oos_trades": oos_summary["trades"] >= GATES["min_oos_trades"],
        "deflated_sharpe": dsr >= GATES["min_dsr"],
        "stable_years": np.mean([v > 0 for v in years.values()]) >= GATES["min_share_positive_years"],
        "robust_grid": np.mean([s > 0 for s in grid_sharpes]) >= GATES["min_share_positive_grid"],
        "survives_2x_costs": stressed["sharpe"] > GATES["min_sharpe_2x_costs"],
    }
    if not checks["no_lookahead"] or oos_summary["sharpe"] <= 0 or not checks["oos_trades"]:
        verdict = "REJECTED"
    elif all(checks.values()):
        verdict = "HOLDOUT_CANDIDATE"
    else:
        verdict = "PROMISING"

    param_votes = Counter(json.dumps(f["params"], sort_keys=True) for f in folds)
    result = {
        "strategy": strategy.name,
        "description": strategy.description,
        "dataset": dataset,
        "daytrade": strategy.daytrade,
        "created": datetime.now().isoformat(timespec="seconds"),
        "verdict": verdict,
        "checks": {k: bool(v) for k, v in checks.items()},
        "gates": GATES,
        "lookahead_problems": lookahead[:5],
        "oos": oos_summary,
        "oos_2x_costs": {k: stressed[k] for k in ("sharpe", "total_pnl", "max_drawdown")},
        "deflated_sharpe": dsr,
        "trials_on_dataset": n_trials,
        "walk_forward": {"train_days": train_days, "test_days": test_days, "folds": folds},
        "most_chosen_params": json.loads(param_votes.most_common(1)[0][0]),
        "grid": [{"params": p, "sharpe": round(s["sharpe"], 2), "trades": s["trades"],
                  "max_drawdown": round(s["max_drawdown"], 3)} for p, s in grid],
    }
    out_dir = REPORTS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}_{strategy.name}_{dataset}"
    report.write(out_dir, result, oos)
    result["report_dir"] = str(out_dir)
    return result


def holdout(strategy_name: str, symbol: str, params: dict, timeframe: str | None = None, force: bool = False) -> dict:
    """One-shot test on the frozen holdout. Each strategy gets one attempt per
    dataset: if it is tweaked and retried, the holdout becomes training data."""
    strategy = load(strategy_name)
    timeframe = timeframe or strategy.timeframe
    dataset = store.dataset_id(symbol, timeframe)
    log = REPORTS_DIR.parent / "research" / "holdout_log.jsonl"
    previous = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()] if log.exists() else []
    if any(e["strategy"] == strategy.name and e["dataset"] == dataset for e in previous) and not force:
        raise RuntimeError(f"{strategy.name} already used the holdout of {dataset}. See {log}.")

    df = store.load(symbol, timeframe, include_holdout=True)
    cut = store.holdout_start(symbol, timeframe)
    # Signals see earlier data for indicator warm-up; only holdout bars are traded.
    target = strategy.signals(df, **{**strategy.params, **params})[df.index >= cut]
    summary = summarize(engine.run(df.loc[target.index], target, for_symbol(symbol), strategy.daytrade))

    entry = {"ts": datetime.now().isoformat(timespec="seconds"), "strategy": strategy.name,
             "dataset": dataset, "params": params, "summary": summary}
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")
    return entry
