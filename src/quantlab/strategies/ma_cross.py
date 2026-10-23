"""Baseline swing strategy: long when the fast moving average is above the slow one.

Not expected to be good. It exists to check the pipeline end to end and to be
the bar every new idea has to beat.
"""

import pandas as pd

from quantlab.strategies import Strategy


def signals(df: pd.DataFrame, fast: int, slow: int, allow_short: bool) -> pd.Series:
    fast_ma = df["close"].rolling(fast).mean()
    slow_ma = df["close"].rolling(slow).mean()
    position = (fast_ma > slow_ma).astype(float)
    if allow_short:
        position = position.where(fast_ma > slow_ma, -1.0)
    return position.where(slow_ma.notna(), 0.0)


STRATEGY = Strategy(
    name="ma_cross",
    description="Moving average crossover (baseline swing)",
    timeframe="D1",
    daytrade=False,
    signal_fn=signals,
    params={"fast": 20, "slow": 100, "allow_short": False},
    grid={"fast": [10, 20, 50], "slow": [100, 150, 200]},
    title="Cruzamento de médias móveis",
    summary="Fica comprado enquanto a média curta do preço está acima da média longa.",
    param_help={
        "fast": "Tamanho da média curta, em dias.",
        "slow": "Tamanho da média longa, em dias.",
        "allow_short": "Se verdadeiro, fica vendido quando a média curta está abaixo da longa.",
    },
)
