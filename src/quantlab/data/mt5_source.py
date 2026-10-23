"""Download OHLCV bars from a running MetaTrader 5 terminal.

The terminal must be open and logged in to the broker account. The Python
package attaches to it; no credentials go through this code.

B3 symbol conventions in MT5 (check yours with `quantlab symbols WIN`):
  - Stocks: PETR4, VALE3, ...
  - Futures, current contract: WINZ26, WDOZ26 (letter = month, digits = year)
  - Futures, continuous series: usually WIN$ / WIN$N and WDO$ / WDO$N.
    Continuous series splice contracts at each roll; the jump at the roll is
    not a real price move, so check how your broker builds it.
"""

from datetime import datetime

import MetaTrader5 as mt5
import pandas as pd

TIMEFRAMES = {
    "M1": mt5.TIMEFRAME_M1,
    "M5": mt5.TIMEFRAME_M5,
    "M15": mt5.TIMEFRAME_M15,
    "M30": mt5.TIMEFRAME_M30,
    "H1": mt5.TIMEFRAME_H1,
    "D1": mt5.TIMEFRAME_D1,
}

TERMINAL_PATH = r"C:\Program Files\Clear Investimentos MT5 Terminal\terminal64.exe"


def connect() -> None:
    if not mt5.initialize(path=TERMINAL_PATH):
        raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}. Is the terminal open and logged in?")


def list_symbols(pattern: str) -> list[str]:
    connect()
    try:
        return sorted(s.name for s in (mt5.symbols_get(f"*{pattern}*") or []))
    finally:
        mt5.shutdown()


def fetch(symbol: str, timeframe: str, start: datetime, end: datetime) -> pd.DataFrame:
    """Return bars indexed by bar open time (broker server time, B3 local time)."""
    connect()
    try:
        if not mt5.symbol_select(symbol, True):
            raise ValueError(f"Symbol {symbol} not available: {mt5.last_error()}")
        # copy_rates_range fails with "Invalid params" when the range holds more
        # bars than the terminal's "Max bars in chart" setting, so take the most
        # recent bars allowed and filter by date afterwards. Asking for exactly
        # maxbars also fails, hence the -1.
        rates = mt5.copy_rates_from_pos(symbol, TIMEFRAMES[timeframe], 0, mt5.terminal_info().maxbars - 1)
        if rates is None or len(rates) == 0:
            raise ValueError(f"No bars for {symbol} {timeframe}: {mt5.last_error()}")
    finally:
        mt5.shutdown()

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.set_index("time").rename(columns={"tick_volume": "ticks", "real_volume": "volume"})
    df = df[(df.index >= start) & (df.index <= end)]
    return df[["open", "high", "low", "close", "volume", "ticks", "spread"]]
