"""Project paths and global research settings."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
HOLDOUTS_FILE = DATA_DIR / "holdouts.json"
RESEARCH_DIR = ROOT / "research"
REGISTRY_FILE = RESEARCH_DIR / "registry.jsonl"
REPORTS_DIR = ROOT / "reports"

# Share of each dataset (the most recent part) frozen as holdout the first time
# it is downloaded. The agent loop never sees it; see docs/conceitos-avaliacao.md.
HOLDOUT_FRACTION = 0.20

# Annual risk-free rate used in Sharpe. Brazil's CDI is high, so a strategy with
# a positive Sharpe at rf=0 can still lose to a fixed-income fund. Update as needed.
RISK_FREE_ANNUAL = 0.14

TRADING_DAYS = 252
