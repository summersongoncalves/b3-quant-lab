"""Performance metrics. All ratios are computed on DAILY P&L, even for intraday
strategies, so that strategies on different timeframes are comparable."""

import numpy as np
import pandas as pd
from scipy import stats

from quantlab.backtest.engine import BacktestResult
from quantlab.config import RISK_FREE_ANNUAL, TRADING_DAYS


def daily_excess_returns(result: BacktestResult) -> pd.Series:
    """Daily return on capital minus the risk-free rate the capital gave up.

    Futures only need margin, and the margin itself can sit in CDI-earning
    bonds, so their P&L is already an excess return. A stock position uses the
    cash, so it is charged the CDI for the share of the day it was invested.
    """
    bars = result.bars
    by_day = bars.groupby(bars.index.normalize())
    ret = by_day["pnl"].sum() / result.capital
    if result.instrument.kind == "stock":
        rf_daily = (1 + RISK_FREE_ANNUAL) ** (1 / TRADING_DAYS) - 1
        ret = ret - rf_daily * by_day["held"].apply(lambda h: h.abs().mean())
    return ret


def sharpe(daily: pd.Series) -> float:
    sd = daily.std()
    return float(daily.mean() / sd * np.sqrt(TRADING_DAYS)) if sd > 0 else 0.0


def max_drawdown(daily_pnl: pd.Series, capital: float) -> float:
    equity = capital + daily_pnl.cumsum()
    return float((equity / equity.cummax() - 1).min())


def summarize(result: BacktestResult) -> dict:
    bars, trades = result.bars, result.trades
    daily = daily_excess_returns(result)
    daily_pnl = bars.groupby(bars.index.normalize())["pnl"].sum()
    downside = daily[daily < 0].std()
    wins = trades["pnl"][trades["pnl"] > 0]
    losses = trades["pnl"][trades["pnl"] < 0]
    ann_return = float(daily.mean() * TRADING_DAYS)
    mdd = max_drawdown(daily_pnl, result.capital)

    return {
        "start": str(bars.index[0]),
        "end": str(bars.index[-1]),
        "days": int(len(daily)),
        "total_pnl": round(float(bars["pnl"].sum()), 2),
        "total_cost": round(float(bars["cost"].sum()), 2),
        "annual_excess_return": ann_return,
        "annual_vol": float(daily.std() * np.sqrt(TRADING_DAYS)),
        "sharpe": sharpe(daily),
        "sortino": float(daily.mean() / downside * np.sqrt(TRADING_DAYS)) if downside > 0 else 0.0,
        "max_drawdown": mdd,
        "calmar": ann_return / abs(mdd) if mdd < 0 else 0.0,
        "trades": int(len(trades)),
        "win_rate": float(len(wins) / len(trades)) if len(trades) else 0.0,
        "profit_factor": float(wins.sum() / -losses.sum()) if len(losses) else float("inf"),
        "avg_trade": float(trades["pnl"].mean()) if len(trades) else 0.0,
        "payoff": float(wins.mean() / -losses.mean()) if len(wins) and len(losses) else 0.0,
        "exposure": float((bars["held"] != 0).mean()),
        # Share of the gross edge eaten by costs; above ~0.5 the edge is fragile.
        "cost_to_gross": float(bars["cost"].sum() / abs(bars["pnl_gross"].sum())) if bars["pnl_gross"].sum() else float("inf"),
        # Inputs for PSR / DSR (non-annualized daily Sharpe, Pearson kurtosis).
        "sharpe_daily": float(daily.mean() / daily.std()) if daily.std() > 0 else 0.0,
        "skew": float(stats.skew(daily)) if len(daily) > 2 else 0.0,
        "kurtosis": float(stats.kurtosis(daily, fisher=False)) if len(daily) > 3 else 3.0,
        "sharpe_by_year": {str(y): round(sharpe(d), 2) for y, d in daily.groupby(daily.index.year)},
    }
