# b3-quant-lab

Academic research lab for day trade and swing trade strategies on B3 (Brazil's stock exchange), built around a loop of three AI agents: a **strategist** that proposes hypotheses, an **implementer** that codes them, and a **validator** that tries to break them.

Not investment advice and not an order execution system.

## What makes it more than a backtester
- **No look-ahead by construction:** signals are computed on bar close and executed on the next open; an automated check recomputes signals on truncated data to catch leaks.
- **Frozen holdout:** the last 20% of each dataset is locked on first download and can be used once per strategy.
- **Honest statistics:** every configuration ever tried is logged, and strategies are judged with walk-forward out-of-sample results and the Deflated Sharpe Ratio (Bailey & Lopez de Prado), so running the agent loop longer makes passing harder, not easier.
- **B3 specifics:** mini index (WIN) and mini dollar (WDO) contract specs, exchange fees, slippage, day trade forced flat at the close, CDI as the risk-free hurdle.

## Setup
```bash
uv sync
uv run pytest -q
uv run quantlab symbols WIN          # MetaTrader 5 terminal open and logged in
uv run quantlab fetch WIN$N M5 --start 2025-01-01
uv run quantlab validate opening_range_breakout WIN$N
```

### Dashboard
A Vue 3 + TypeScript front end over a read-only FastAPI layer: report list with filters, interactive out-of-sample equity and drawdown, pass/fail criteria, parameter-robustness heatmap, walk-forward folds, trade P&L distribution, and the agents' hypotheses and cycle summaries.
```bash
uv run quantlab serve            # API on :8000
npm --prefix web install
npm --prefix web run dev         # http://localhost:5173
```

## Layout
| Path | Content |
|---|---|
| `src/quantlab/data` | MT5 download, Parquet store, holdout freeze |
| `src/quantlab/backtest` | vectorized engine, instruments and costs, metrics |
| `src/quantlab/research` | look-ahead check, walk-forward, PSR/DSR, trial registry, reports |
| `src/quantlab/strategies` | one module per strategy |
| `src/quantlab/api.py`, `web/` | read-only API and Vue dashboard |
| `.claude/agents`, `.claude/skills/ciclo` | agent prompts and the research loop |
| `docs/` | evaluation concepts and agent design (Portuguese) |
