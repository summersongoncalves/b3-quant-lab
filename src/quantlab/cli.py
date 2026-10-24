"""Command line entry point: `uv run quantlab <command>`."""

import argparse
import json
from datetime import datetime

from quantlab import strategies
from quantlab.backtest import engine
from quantlab.backtest.instruments import for_symbol
from quantlab.backtest.metrics import summarize
from quantlab.data import store


def _parse_params(items: list[str]) -> dict:
    out = {}
    for item in items or []:
        key, value = item.split("=", 1)
        try:
            out[key] = json.loads(value)
        except json.JSONDecodeError:
            out[key] = value
    return out


def cmd_symbols(args):
    from quantlab.data import mt5_source
    print("\n".join(mt5_source.list_symbols(args.pattern)))


def _fmt(ts) -> str:
    return ts.strftime("%d/%m/%Y %H:%M") if ts.hour or ts.minute else ts.strftime("%d/%m/%Y")


def _print_split(symbol: str, timeframe: str, full, research) -> None:
    """User-facing summary (in Portuguese) of how a dataset is split between research and holdout."""
    cut = store.holdout_start(symbol, timeframe)
    days = lambda d: d.index.normalize().nunique()
    holdout = full[full.index >= cut] if cut is not None else full.iloc[:0]
    print(f"  Total:     {len(full):>7,} barras · {days(full):,} pregões · {_fmt(full.index[0])} até {_fmt(full.index[-1])}".replace(",", "."))
    if len(research):
        print(f"  Pesquisa:  {len(research):>7,} barras · {days(research):,} pregões · {_fmt(research.index[0])} até {_fmt(research.index[-1])}".replace(",", "."))
    if len(holdout):
        print(f"  Holdout:   {len(holdout):>7,} barras · {days(holdout):,} pregões · a partir de {_fmt(cut)} (trancado)".replace(",", "."))


def cmd_fetch(args):
    from quantlab.data import mt5_source
    end = datetime.fromisoformat(args.end) if args.end else datetime.now()
    first_time = store.holdout_start(args.symbol, args.timeframe) is None
    df = mt5_source.fetch(args.symbol, args.timeframe, datetime.fromisoformat(args.start), end)
    df = store.save(df, args.symbol, args.timeframe)
    print(f"OK: {args.symbol} {args.timeframe} salvo em data/raw/")
    _print_split(args.symbol, args.timeframe, df, store.load(args.symbol, args.timeframe))
    if first_time:
        print("\nO holdout foi congelado agora e nunca mais muda. Nenhum agente pode usá-lo;")
        print("ele fica guardado para a prova final, que só roda quando você pedir.")
    print(f"\nPróximo passo: /ciclo {args.symbol} {args.timeframe} 1 daytrade (ou swing)")


def cmd_info(args):
    full = store.load(args.symbol, args.timeframe, include_holdout=True)
    research = store.load(args.symbol, args.timeframe)
    print(f"{args.symbol} {args.timeframe}")
    _print_split(args.symbol, args.timeframe, full, research)


def cmd_list(args):
    for name in strategies.available():
        s = strategies.load(name)
        print(f"{name:30} {s.timeframe:4} {'daytrade' if s.daytrade else 'swing':9} {s.description}")


def cmd_backtest(args):
    """Quick single run, for smoke tests. Not registered as a trial; use `validate` for research."""
    s = strategies.load(args.strategy)
    tf = args.timeframe or s.timeframe
    df = store.load(args.symbol, tf)
    params = _parse_params(args.param)
    result = engine.run(df, s.signals(df, **params), for_symbol(args.symbol), s.daytrade)
    summary = summarize(result)
    print(json.dumps({k: v for k, v in summary.items() if k not in ("skew", "kurtosis")}, indent=2, default=str))


def cmd_validate(args):
    from quantlab.research import pipeline
    r = pipeline.validate(args.strategy, args.symbol, args.timeframe, args.train_days, args.test_days)
    o = r["oos"]
    print(f"verdict: {r['verdict']}")
    print(f"OOS sharpe {o['sharpe']:.2f} | DSR {r['deflated_sharpe']:.1%} | trades {o['trades']} | max DD {o['max_drawdown']:.1%}")
    print("checks: " + ", ".join(f"{k}={'ok' if v else 'FAIL'}" for k, v in r["checks"].items()))
    print(f"report: {r['report_dir']}")


def cmd_holdout(args):
    from quantlab.research import pipeline
    entry = pipeline.holdout(args.strategy, args.symbol, _parse_params(args.param), args.timeframe, args.force)
    print(json.dumps(entry["summary"], indent=2, default=str))


def cmd_serve(args):
    import uvicorn
    uvicorn.run("quantlab.api:app", host="127.0.0.1", port=args.port, reload=args.reload)


def main():
    p = argparse.ArgumentParser(prog="quantlab")
    sub = p.add_subparsers(required=True)

    s = sub.add_parser("symbols", help="search symbols in MT5")
    s.add_argument("pattern")
    s.set_defaults(fn=cmd_symbols)

    s = sub.add_parser("fetch", help="download bars from MT5 into data/raw")
    s.add_argument("symbol")
    s.add_argument("timeframe", choices=["M1", "M5", "M15", "M30", "H1", "D1"])
    s.add_argument("--start", required=True)
    s.add_argument("--end")
    s.set_defaults(fn=cmd_fetch)

    s = sub.add_parser("info", help="show a stored dataset")
    s.add_argument("symbol")
    s.add_argument("timeframe")
    s.set_defaults(fn=cmd_info)

    s = sub.add_parser("list", help="list strategies")
    s.set_defaults(fn=cmd_list)

    s = sub.add_parser("serve", help="read-only API for the web front end")
    s.add_argument("--port", type=int, default=8000)
    s.add_argument("--reload", action="store_true")
    s.set_defaults(fn=cmd_serve)

    for name, fn, help_ in [("backtest", cmd_backtest, "single quick run"),
                            ("validate", cmd_validate, "full validation + report"),
                            ("holdout", cmd_holdout, "one-shot final test on the holdout")]:
        s = sub.add_parser(name, help=help_)
        s.add_argument("strategy")
        s.add_argument("symbol")
        s.add_argument("--timeframe")
        if name in ("backtest", "holdout"):
            s.add_argument("--param", nargs="*", help="key=value overrides")
        if name == "validate":
            s.add_argument("--train-days", type=int)
            s.add_argument("--test-days", type=int)
        if name == "holdout":
            s.add_argument("--force", action="store_true")
        s.set_defaults(fn=fn)

    args = p.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
