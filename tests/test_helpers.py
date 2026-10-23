import numpy as np
import pandas as pd
import pytest

from quantlab.strategies._helpers import relative_volume, vwap
from test_engine import intraday


def with_volume(df, seed=2):
    rng = np.random.default_rng(seed)
    return df.assign(volume=rng.integers(100, 1000, len(df)))


@pytest.mark.parametrize("period", ["D", "W"])
def test_vwap_is_causal_and_resets(period):
    df = with_volume(intraday(days=20))
    full = vwap(df, period)
    cut = df.index[len(df) // 2]
    assert full.loc[:cut].equals(vwap(df.loc[:cut], period))
    # First bar of each period: VWAP is that bar's typical price.
    typical = (df["high"] + df["low"] + df["close"]) / 3
    day = df.index.normalize()
    key = day if period == "D" else day - pd.to_timedelta(df.index.day_of_week, unit="D")
    first = ~pd.Series(key, index=df.index).duplicated()
    assert np.allclose(full[first.to_numpy()], typical[first.to_numpy()])


def test_vwap_matches_hand_computation():
    idx = pd.DatetimeIndex(["2025-01-02 09:00", "2025-01-02 09:05", "2025-01-03 09:00"])
    df = pd.DataFrame({"high": [11, 21, 31], "low": [9, 19, 29], "close": [10, 20, 30],
                       "volume": [1, 3, 5]}, index=idx)
    assert vwap(df, "D").tolist() == [10, (10 * 1 + 20 * 3) / 4, 30]
    assert vwap(df, "W").tolist() == [10, 17.5, (10 + 60 + 150) / 9]


def test_relative_volume_uses_only_past_days():
    df = with_volume(intraday(days=30))
    full = relative_volume(df, days=5)
    cut = df.index[len(df) // 2]
    pd.testing.assert_series_equal(full.loc[:cut], relative_volume(df.loc[:cut], days=5))
    assert full.loc[: df.index[5 * 20 - 1]].isna().all()  # first 5 days have no history
    assert full.dropna().gt(0).all()
