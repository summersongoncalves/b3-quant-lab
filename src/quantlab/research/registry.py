"""Append-only log of every configuration ever evaluated.

This is what makes the Deflated Sharpe Ratio honest: if 300 variations were
tried on a dataset, the best one is judged against the best of 300 random
strategies, not against zero. Never delete lines from this file.
"""

import json
from datetime import datetime

import numpy as np

from quantlab.config import REGISTRY_FILE


def record(strategy: str, dataset: str, params: dict, summary: dict, phase: str) -> None:
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now().isoformat(timespec="seconds"),
        "strategy": strategy,
        "dataset": dataset,
        "phase": phase,
        "params": params,
        "sharpe_daily": summary["sharpe_daily"],
        "days": summary["days"],
    }
    with REGISTRY_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, default=str) + "\n")


def trials(dataset: str) -> tuple[int, float]:
    """Number of configurations tried on a dataset and the variance of their daily Sharpe."""
    if not REGISTRY_FILE.exists():
        return 0, 0.0
    sharpes = [
        e["sharpe_daily"]
        for e in map(json.loads, REGISTRY_FILE.read_text(encoding="utf-8").splitlines())
        if e["dataset"] == dataset and e["phase"] == "search"
    ]
    return len(sharpes), float(np.var(sharpes, ddof=1)) if len(sharpes) > 1 else 0.0
