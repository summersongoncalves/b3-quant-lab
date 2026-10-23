"""Writes report.json (for the future Vue front end), report.md (for people and
agents) and equity.png."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from quantlab.backtest.engine import BacktestResult

CHECK_LABELS = {
    "no_lookahead": "Sem look-ahead (sinal não usa dados futuros)",
    "oos_sharpe": "Sharpe fora da amostra >= mínimo",
    "oos_trades": "Trades suficientes fora da amostra",
    "deflated_sharpe": "Deflated Sharpe (descontando nº de tentativas)",
    "stable_years": "Maioria dos anos positiva",
    "robust_grid": "Maioria dos parâmetros vizinhos positiva",
    "survives_2x_costs": "Continua positiva com custos 2x",
}


def write(out_dir: Path, result: dict, oos: BacktestResult) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    full = {**result, **series(oos)}
    (out_dir / "report.json").write_text(json.dumps(full, indent=2, default=str), encoding="utf-8")
    _equity_chart(out_dir / "equity.png", oos, result)
    (out_dir / "report.md").write_text(_markdown(result), encoding="utf-8")


def series(oos: BacktestResult) -> dict:
    """Daily equity/drawdown and per-trade P&L, for interactive charts."""
    cum = oos.bars.groupby(oos.bars.index.normalize())["pnl"].sum().cumsum()
    return {
        "equity": {
            "dates": [d.strftime("%Y-%m-%d") for d in cum.index],
            "pnl": cum.round(2).tolist(),
            "drawdown": (cum - cum.cummax()).round(2).tolist(),
        },
        "trade_pnls": oos.trades["pnl"].round(2).tolist(),
    }


def _equity_chart(path: Path, oos: BacktestResult, result: dict) -> None:
    daily = oos.bars.groupby(oos.bars.index.normalize())["pnl"].sum().cumsum()
    drawdown = daily - daily.cummax()
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True, height_ratios=[3, 1])
    ax1.plot(daily.index, daily.values, color="#2563eb", linewidth=1.2)
    ax1.set_title(f"{result['strategy']} | {result['dataset']} | walk-forward fora da amostra")
    ax1.set_ylabel("P&L acumulado (R$)")
    ax1.grid(alpha=0.3)
    ax2.fill_between(drawdown.index, drawdown.values, 0, color="#dc2626", alpha=0.4)
    ax2.set_ylabel("Drawdown (R$)")
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def _markdown(r: dict) -> str:
    o = r["oos"]
    lines = [
        f"# {r['strategy']} em {r['dataset']}",
        "",
        f"**Veredito automático: {r['verdict']}**  ",
        f"{r['description']} · {'day trade' if r['daytrade'] else 'swing'} · gerado em {r['created']}",
        "",
        "## Critérios (definidos antes do teste)",
        "",
        *[f"- {'✅' if ok else '❌'} {CHECK_LABELS[k]}" for k, ok in r["checks"].items()],
        "",
        "## Resultado fora da amostra (walk-forward)",
        "",
        "| Métrica | Valor |",
        "|---|---|",
        f"| Período | {o['start'][:10]} → {o['end'][:10]} ({o['days']} dias) |",
        f"| P&L total / custos | R$ {o['total_pnl']:,.2f} / R$ {o['total_cost']:,.2f} |",
        f"| Retorno anual acima do CDI | {o['annual_excess_return']:.1%} |",
        f"| Sharpe / Sortino | {o['sharpe']:.2f} / {o['sortino']:.2f} |",
        f"| Deflated Sharpe ({r['trials_on_dataset']} tentativas no dataset) | {r['deflated_sharpe']:.1%} |",
        f"| Max drawdown | {o['max_drawdown']:.1%} |",
        f"| Trades / acerto / payoff | {o['trades']} / {o['win_rate']:.0%} / {o['payoff']:.2f} |",
        f"| Profit factor | {o['profit_factor']:.2f} |",
        f"| Exposição | {o['exposure']:.0%} das barras |",
        f"| Custos / lucro bruto | {o['cost_to_gross']:.0%} |",
        f"| Sharpe com custos 2x | {r['oos_2x_costs']['sharpe']:.2f} |",
        "",
        "Sharpe por ano: " + ", ".join(f"{y}: {s}" for y, s in o["sharpe_by_year"].items()),
        "",
        "![equity](equity.png)",
        "",
        "## Parâmetros escolhidos em cada janela",
        "",
        "| Teste | Parâmetros | Sharpe no treino |",
        "|---|---|---|",
        *[f"| {f['test_start']} → {f['test_end']} | `{f['params']}` | {f['train_sharpe']} |" for f in r["walk_forward"]["folds"]],
        "",
        "## Grade completa (amostra de pesquisa inteira, só para ver robustez)",
        "",
        "| Parâmetros | Sharpe | Trades | Max DD |",
        "|---|---|---|---|",
        *[f"| `{g['params']}` | {g['sharpe']} | {g['trades']} | {g['max_drawdown']:.1%} |" for g in r["grid"]],
    ]
    if r["lookahead_problems"]:
        lines += ["", "## ⚠️ Look-ahead detectado", "", *[f"- {p}" for p in r["lookahead_problems"]]]
    return "\n".join(lines) + "\n"
