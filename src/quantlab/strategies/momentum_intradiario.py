"""Intraday momentum: the move from the open to `signal_time` continues until the close.

On the signal bar (the bar whose close happens at `signal_time`, i.e. labelled
signal_time - 5 min) compute mov = close - open of the day's first bar. If
|mov| > k * scale, go long (mov > 0) or short (mov < 0) and hold until the
engine flattens at the close. scale is the median |mov| of the previous 20
valid days (current day excluded). Days whose first bar starts after 09:30, or
with fewer than 20 days of history, are not traded. One entry per day.
"""

import pandas as pd

from quantlab.strategies import Strategy

HISTORY_DAYS = 20
LATEST_OPEN = "09:30"
BAR_MINUTES = 5


def signals(df: pd.DataFrame, signal_time: str, k: float) -> pd.Series:
    day = df.index.normalize()
    day_open = df["open"].groupby(day).transform("first")
    first_time = df.index.to_series().groupby(day).transform("first").dt.time
    valid_day = first_time <= pd.Timestamp(LATEST_OPEN).time()

    label = (pd.Timestamp(signal_time) - pd.Timedelta(minutes=BAR_MINUTES)).time()
    is_signal_bar = (df.index.time == label) & valid_day.to_numpy()

    mov = (df["close"] - day_open)[is_signal_bar]
    mov.index = mov.index.normalize()  # one value per day
    # Past days only: rolling over the 20 previous days, shifted so today is excluded.
    scale = mov.abs().rolling(HISTORY_DAYS).median().shift(1)

    scale_bar = scale.reindex(mov.index).to_numpy()
    take = (mov.abs().to_numpy() > k * scale_bar)  # NaN scale -> False
    side = pd.Series(mov.apply(lambda x: 1.0 if x > 0 else -1.0 if x < 0 else 0.0).to_numpy(), index=df.index[is_signal_bar])
    entry = pd.Series(float("nan"), index=df.index)
    entry[side.index] = side.where(take, 0.0)

    # Position starts at the signal bar and is held for the rest of the day.
    return entry.groupby(day).ffill().fillna(0.0)


STRATEGY = Strategy(
    name="momentum_intradiario",
    description="Intraday momentum: open-to-signal_time move continues to the close",
    timeframe="M5",
    daytrade=True,
    signal_fn=signals,
    params={"signal_time": "14:00", "k": 0.5},
    grid={"signal_time": ["12:00", "14:00", "16:00"], "k": [0.0, 0.5, 1.0]},
    title="Tendência do dia até o fechamento",
    summary="Se o preço andou forte da abertura até o horário do sinal, entra na mesma direção e segura até o fim do pregão.",
    param_help={
        "signal_time": "Horário em que o movimento do dia é medido e a entrada é decidida.",
        "k": "Filtro de força: só opera se o movimento for maior que k vezes o movimento típico dos últimos 20 dias. k=0 opera todo dia.",
    },
)
