"""Local Parquet store with a frozen holdout per dataset.

The first time a dataset is saved, the date that splits off its most recent
HOLDOUT_FRACTION is written to data/holdouts.json and never moves again. Data
downloaded later is newer than that date, so it also lands in the holdout.
"""

import json

import pandas as pd

from quantlab.config import HOLDOUT_FRACTION, HOLDOUTS_FILE, RAW_DIR


def dataset_id(symbol: str, timeframe: str) -> str:
    return f"{symbol.replace('$', '_')}_{timeframe}"


def _path(symbol: str, timeframe: str):
    return RAW_DIR / f"{dataset_id(symbol, timeframe)}.parquet"


def _holdouts() -> dict:
    return json.loads(HOLDOUTS_FILE.read_text()) if HOLDOUTS_FILE.exists() else {}


def holdout_start(symbol: str, timeframe: str) -> pd.Timestamp | None:
    value = _holdouts().get(dataset_id(symbol, timeframe))
    return pd.Timestamp(value) if value else None


def save(df: pd.DataFrame, symbol: str, timeframe: str) -> pd.DataFrame:
    """Merge with what is already stored and freeze the holdout on first save."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = _path(symbol, timeframe)
    if path.exists():
        df = pd.concat([pd.read_parquet(path), df])
        df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()
    df.to_parquet(path)

    holdouts = _holdouts()
    key = dataset_id(symbol, timeframe)
    if key not in holdouts:
        # Split on a day boundary so no session is cut in half.
        days = df.index.normalize().unique()
        split_day = days[int(len(days) * (1 - HOLDOUT_FRACTION))]
        holdouts[key] = split_day.isoformat()
        HOLDOUTS_FILE.parent.mkdir(parents=True, exist_ok=True)
        HOLDOUTS_FILE.write_text(json.dumps(holdouts, indent=2))
    return df


def load(symbol: str, timeframe: str, include_holdout: bool = False) -> pd.DataFrame:
    """Research data. include_holdout=True is reserved for the final, one-shot evaluation."""
    path = _path(symbol, timeframe)
    if not path.exists():
        raise FileNotFoundError(f"{path.name} not found. Run: quantlab fetch {symbol} {timeframe} --start YYYY-MM-DD")
    df = pd.read_parquet(path)
    cut = holdout_start(symbol, timeframe)
    if cut is not None and not include_holdout:
        df = df[df.index < cut]
    return df
