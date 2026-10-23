import json

import pytest

from quantlab.data import store
from quantlab.research import pipeline, registry
from test_engine import daily, intraday


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    monkeypatch.setattr(store, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(store, "HOLDOUTS_FILE", tmp_path / "holdouts.json")
    monkeypatch.setattr(registry, "REGISTRY_FILE", tmp_path / "registry.jsonl")
    monkeypatch.setattr(pipeline, "REPORTS_DIR", tmp_path / "reports")
    return tmp_path


def test_holdout_is_frozen_and_hidden(sandbox):
    df = daily(1000)
    store.save(df.iloc[:800], "PETR4", "D1")
    cut = store.holdout_start("PETR4", "D1")
    store.save(df, "PETR4", "D1")
    assert store.holdout_start("PETR4", "D1") == cut
    assert store.load("PETR4", "D1").index.max() < cut
    assert store.load("PETR4", "D1", include_holdout=True).index.max() == df.index.max()


@pytest.mark.parametrize("strategy,symbol,tf,data", [
    ("ma_cross", "PETR4", "D1", lambda: daily(1500)),
    ("opening_range_breakout", "WIN$N", "M5", lambda: intraday(days=200, bars_per_day=60)),
])
def test_validate_end_to_end(sandbox, strategy, symbol, tf, data):
    store.save(data(), symbol, tf)
    r = pipeline.validate(strategy, symbol, tf)
    assert r["verdict"] in {"REJECTED", "PROMISING", "HOLDOUT_CANDIDATE"}
    report = json.loads((sandbox / "reports").glob("*/report.json").__next__().read_text(encoding="utf-8"))
    assert report["checks"]["no_lookahead"]
    assert registry.trials(store.dataset_id(symbol, tf))[0] == 9
