"""Read-only HTTP API over the research files, for the Vue front end in web/.

Everything is read from disk on each request: reports/, research/ and data/
are the single source of truth, written by the CLI and the agents.
"""

import json
import re
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from quantlab import strategies
from quantlab.config import HOLDOUTS_FILE, RAW_DIR, REGISTRY_FILE, REPORTS_DIR, RESEARCH_DIR, ROOT

app = FastAPI(title="quantlab")
HYPOTHESES_DIR = RESEARCH_DIR / "hypotheses"
CYCLES_DIR = REPORTS_DIR / "ciclos"
# Files the markdown documents link to, viewable from the UI. Market data stays out.
VIEWABLE_DIRS = ("docs", "knowledge/notas", "research", "reports", "src/quantlab", ".claude/agents", ".claude/skills")
VIEWABLE_FILES = ("CLAUDE.md", "README.md")
VIEWABLE_SUFFIXES = (".md", ".py", ".json", ".jsonl", ".txt")
MAX_FILE_BYTES = 2_000_000


def _report_dirs() -> dict[str, Path]:
    if not REPORTS_DIR.exists():
        return {}
    return {d.name: d for d in REPORTS_DIR.iterdir() if (d / "report.json").exists()}


def _report_dir(report_id: str) -> Path:
    # Look the id up instead of joining it into a path, so "../" can't escape.
    d = _report_dirs().get(report_id)
    if d is None:
        raise HTTPException(404, f"report {report_id} not found")
    return d


def _validator_section(md: str) -> str | None:
    """The validator agent appends its analysis to report.md under this heading."""
    _, sep, rest = md.partition("## Análise do validador")
    return (sep + rest).strip() if sep else None


def _validator_verdict(section: str | None) -> str | None:
    match = re.search(r"\*\*Veredito final:\*\*\s*([^\n]+)", section or "")
    return match.group(1).strip() if match else None


def _strategy_labels(name: str) -> dict:
    """Portuguese display fields from the strategy module, so old reports get them too."""
    try:
        s = strategies.load(name)
    except ImportError:
        return {"title": name, "summary": "", "param_help": {}}
    return {"title": s.title or name, "summary": s.summary, "param_help": s.param_help}


def _md_files(folder: Path) -> dict[str, Path]:
    return {p.stem: p for p in sorted(folder.glob("*.md"))} if folder.exists() else {}


def _field(md: str, name: str) -> str | None:
    match = re.search(rf"^- {name}:\s*(.+)$", md, re.MULTILINE)
    return match.group(1).strip() if match else None


@app.get("/api/reports")
def list_reports():
    out = []
    for report_id, d in _report_dirs().items():
        r = json.loads((d / "report.json").read_text(encoding="utf-8"))
        analysis = _validator_section((d / "report.md").read_text(encoding="utf-8"))
        o = r["oos"]
        out.append({
            "id": report_id,
            "strategy": r["strategy"],
            "title": _strategy_labels(r["strategy"])["title"],
            "dataset": r["dataset"],
            "daytrade": r["daytrade"],
            "created": r["created"],
            "verdict": r["verdict"],
            "validator_verdict": _validator_verdict(analysis),
            "sharpe": o["sharpe"],
            "deflated_sharpe": r["deflated_sharpe"],
            "trades": o["trades"],
            "max_drawdown": o["max_drawdown"],
            "total_pnl": o["total_pnl"],
        })
    return sorted(out, key=lambda r: r["created"], reverse=True)


@app.get("/api/reports/{report_id}")
def get_report(report_id: str):
    d = _report_dir(report_id)
    r = json.loads((d / "report.json").read_text(encoding="utf-8"))
    r["id"] = report_id
    r.update(_strategy_labels(r["strategy"]))
    r["validator_analysis"] = _validator_section((d / "report.md").read_text(encoding="utf-8"))
    r["has_png"] = (d / "equity.png").exists()
    return r


@app.get("/api/reports/{report_id}/equity.png")
def report_png(report_id: str):
    path = _report_dir(report_id) / "equity.png"
    if not path.exists():
        raise HTTPException(404)
    return FileResponse(path)


@app.get("/api/hypotheses")
def list_hypotheses():
    out = []
    for name, path in _md_files(HYPOTHESES_DIR).items():
        md = path.read_text(encoding="utf-8")
        title = md.splitlines()[0].lstrip("# ").strip() if md else name
        out.append({"id": name, "title": title, "dataset": _field(md, "Dataset"),
                    "mode": _field(md, "Modo"), "state": _field(md, "Estado")})
    return out


@app.get("/api/hypotheses/{hypothesis_id}")
def get_hypothesis(hypothesis_id: str):
    path = _md_files(HYPOTHESES_DIR).get(hypothesis_id)
    if path is None:
        raise HTTPException(404)
    return {"id": hypothesis_id, "markdown": path.read_text(encoding="utf-8")}


@app.get("/api/cycles")
def list_cycles():
    return [{"id": name} for name in sorted(_md_files(CYCLES_DIR), reverse=True)]


@app.get("/api/cycles/{cycle_id}")
def get_cycle(cycle_id: str):
    path = _md_files(CYCLES_DIR).get(cycle_id)
    if path is None:
        raise HTTPException(404)
    return {"id": cycle_id, "markdown": path.read_text(encoding="utf-8")}


@app.get("/api/datasets")
def list_datasets():
    holdouts = json.loads(HOLDOUTS_FILE.read_text()) if HOLDOUTS_FILE.exists() else {}
    trials: dict[str, int] = {}
    if REGISTRY_FILE.exists():
        for line in REGISTRY_FILE.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e["phase"] == "search":
                trials[e["dataset"]] = trials.get(e["dataset"], 0) + 1
    out = []
    for path in sorted(RAW_DIR.glob("*.parquet")) if RAW_DIR.exists() else []:
        index = pd.read_parquet(path, columns=[]).index
        out.append({"id": path.stem, "bars": len(index), "start": str(index.min()), "end": str(index.max()),
                    "holdout_start": holdouts.get(path.stem), "trials": trials.get(path.stem, 0)})
    return out


@app.get("/api/strategies")
def list_strategies():
    out = []
    for name in strategies.available():
        s = strategies.load(name)
        out.append({"name": name, "description": s.description, "timeframe": s.timeframe,
                    "daytrade": s.daytrade, "params": s.params, "grid": s.grid,
                    **_strategy_labels(name)})
    return out


@app.get("/api/files/{path:path}")
def get_file(path: str):
    """Any viewable text file by its repo-relative path, for links inside the markdown docs."""
    target = (ROOT / path).resolve()
    try:
        rel = target.relative_to(ROOT).as_posix()
    except ValueError:
        raise HTTPException(404)
    allowed = rel in VIEWABLE_FILES or any(rel.startswith(d + "/") for d in VIEWABLE_DIRS)
    if not allowed or target.suffix not in VIEWABLE_SUFFIXES or not target.is_file():
        raise HTTPException(404, f"{path} not found or not viewable")
    if target.stat().st_size > MAX_FILE_BYTES:
        raise HTTPException(413, f"{path} is too large to view")
    return {"path": rel, "kind": "markdown" if target.suffix == ".md" else "text",
            "content": target.read_text(encoding="utf-8", errors="replace")}
