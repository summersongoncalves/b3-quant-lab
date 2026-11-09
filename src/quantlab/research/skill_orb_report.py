"""Relatório da regra da day-trader-skill na B3, no mesmo formato do "History" do trader-timemachine.

    uv run python -m quantlab.research.skill_orb_report WIN_N            # alvo 2R (padrão da skill)
    uv run python -m quantlab.research.skill_orb_report BBAS3 --target-r 1
    uv run python -m quantlab.research.skill_orb_report --all            # os 4 ativos, 1R e 2R

Usa só a parte de pesquisa dos dados (o holdout do laboratório fica guardado), com custos da B3
(emolumentos aproximados + 1 tick de derrapagem por lado). Estudo acadêmico: não é recomendação.
"""

import argparse
import sys

import pandas as pd

from quantlab import strategies
from quantlab.backtest import engine
from quantlab.backtest.instruments import for_symbol
from quantlab.data import store

SYMBOLS = ["WIN_N", "WDO_N", "BBAS3", "VBBR3"]
CAPITAL = 100_000.0


def verdict(target: int, stop: int, r: float) -> str:
    """Mesma régua da skill: compara 'alvo primeiro' com o ponto de equilíbrio 1/(1+R)."""
    decided = target + stop
    if decided == 0:
        return "Sem trades decididos."
    p = target / decided
    need = 1 / (1 + r)
    diff = (p - need) * 100
    if abs(diff) < 5:
        return "Perto de cara ou coroa" if r == 1 else "Perto do empate (break-even)"
    side = "do alvo" if diff > 0 else "do stop"
    return ("Puxa para o lado " if abs(diff) < 15 else "Fortemente para o lado ") + side


def run(symbol: str, target_r: float) -> dict:
    s = strategies.load("skill_orb")
    df = store.load(symbol, "M5")
    sig = s.signals(df, target_r=target_r)
    inst = for_symbol(symbol)
    res = engine.run(df, sig, inst, s.daytrade, capital=CAPITAL)
    tr = res.trades.copy()
    if tr.empty:
        return {"symbol": symbol, "target_r": target_r, "trades": 0}

    stop_d = sig["stop"].reindex(tr["entry"]).to_numpy()
    entry_px = df["open"].reindex(tr["entry"]).to_numpy()
    if inst.kind == "future":
        risk_brl = stop_d * inst.point_value
    else:
        risk_brl = CAPITAL * stop_d / entry_px
    tr["R"] = tr["pnl"] / risk_brl
    # mesmos trades sem custo nenhum: mostra quanto da perda é a regra e quanto são os custos
    gross = engine.run(df, sig, inst, s.daytrade, capital=CAPITAL, cost_mult=0.0).trades
    tr["R_bruto"] = gross["pnl"].to_numpy() / risk_brl

    kind = tr["exit_reason"].replace({"stop_both": "stop", "signal": "neither", "close": "neither"})
    n_target = int((kind == "target").sum())
    n_stop = int((kind == "stop").sum())
    n_neither = int((kind == "neither").sum())
    sessions = df.index.normalize().nunique()
    return {
        "symbol": symbol,
        "target_r": target_r,
        "start": df.index[0].date(),
        "end": df.index[-1].date(),
        "sessions": sessions,
        "trades": len(tr),
        "target": n_target,
        "stop": n_stop,
        "neither": n_neither,
        "avg_R": tr["R"].mean(),
        "avg_R_gross": tr["R_bruto"].mean(),
        "total_R": tr["R"].sum(),
        "pnl": tr["pnl"].sum(),
        "costs": res.bars["cost"].sum(),
        "verdict": verdict(n_target, n_stop, target_r),
        "trades_df": tr,
    }


def show(r: dict) -> None:
    if not r["trades"]:
        print(f"{r['symbol']}: nenhum disparo.")
        return
    decided = r["target"] + r["stop"]
    p = r["target"] / decided * 100 if decided else 0
    unit = "1 contrato" if r["symbol"].startswith(("WIN", "WDO")) else f"R$ {CAPITAL:,.0f} por trade"
    print(f"\n=== {r['symbol']} · alvo {r['target_r']:g}R · {r['start']} a {r['end']} ({r['sessions']} pregões) ===")
    print(f"A regra disparou {r['trades']} vezes: {r['target']} alvo, {r['stop']} stop, {r['neither']} zerou no fechamento.")
    print(f"Alvo primeiro em {p:.1f}% dos que decidiram (precisa de {100 / (1 + r['target_r']):.1f}% para empatar).")
    print(f"R médio por trade: {r['avg_R_gross']:+.3f} sem custos  →  {r['avg_R']:+.3f} com custos  ·  R total: {r['total_R']:+.1f}")
    print(f"Resultado líquido ({unit}): R$ {r['pnl']:+,.2f}  ·  custos pagos: R$ {r['costs']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    print(f"Veredito: {r['verdict']}.")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol", nargs="?")
    p.add_argument("--target-r", type=float, default=2.0)
    p.add_argument("--all", action="store_true", help="todos os ativos, 1R e 2R, e uma tabela resumo")
    p.add_argument("--csv", help="salva os trades neste arquivo CSV")
    a = p.parse_args()

    if a.all:
        rows = []
        for sym in SYMBOLS:
            for r_mult in (1.0, 2.0):
                r = run(sym, r_mult)
                show(r)
                if r["trades"]:
                    rows.append({k: r[k] for k in ("symbol", "target_r", "trades", "target", "stop", "neither", "avg_R_gross", "avg_R", "verdict")})
        print("\n=== Resumo ===")
        print(pd.DataFrame(rows).to_string(index=False, float_format=lambda x: f"{x:+.3f}"))
        return
    if not a.symbol:
        p.error("informe o ativo (ex. WIN_N) ou use --all")
    r = run(a.symbol, a.target_r)
    show(r)
    if a.csv and r["trades"]:
        r["trades_df"].to_csv(a.csv, index=False)
        print(f"Trades salvos em {a.csv}")


if __name__ == "__main__":
    main()
