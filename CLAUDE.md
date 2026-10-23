# b3-quant-lab

Laboratório acadêmico de pesquisa quantitativa em day trade e swing trade na B3. Não é sistema de execução de ordens e não faz recomendação de investimento.

## Comandos
- `uv run pytest -q`: testes do motor (rodar depois de mexer em `backtest/` ou `research/`)
- `uv run quantlab symbols WIN`: busca símbolos no MT5 (terminal aberto e logado)
- `uv run quantlab fetch WIN$N M5 --start 2025-01-01`: baixa barras para `data/raw/`
- `uv run quantlab info|list|backtest|validate|holdout ...`: ver `src/quantlab/cli.py`
- `/ciclo SÍMBOLO TF N modo`: ciclo de agentes (`.claude/skills/ciclo/SKILL.md`)
- Front end: `uv run quantlab serve` (API somente leitura em :8000, `src/quantlab/api.py`) + `npm --prefix web run dev` (Vue em :5173, proxy de `/api`). O front lê `report.json`; se mudar o formato em `research/report.py`/`pipeline.py`, atualize `web/src/api.ts`.

`uv` foi instalado via winget. Se um shell antigo não o encontrar, use o caminho completo
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\astral-sh.uv_Microsoft.Winget.Source_8wekyb3d8bbwe\uv.exe`.

## Regras invioláveis
1. **Holdout**: `store.load(..., include_holdout=True)` e `quantlab holdout` só a pedido explícito do usuário. Os agentes nunca os usam.
2. **Timing**: sinal calculado no fechamento da barra t, executado na abertura de t+1 (`backtest/engine.py`). Não mude essa convenção.
3. **Registro**: toda avaliação de pesquisa passa por `quantlab validate`, que grava em `research/registry.jsonl`. Nunca apague linhas desse arquivo: elas alimentam o Deflated Sharpe.
4. **Critérios** (`GATES` em `research/pipeline.py`) não mudam para fazer uma estratégia passar.
5. Custos em `backtest/instruments.py` são aproximados. Calibrar com nota de corretagem real.

## Estrutura
- `src/quantlab/data`: MT5 → Parquet com holdout congelado (`data/holdouts.json`)
- `src/quantlab/backtest`: motor vetorizado, instrumentos/custos, métricas
- `src/quantlab/research`: validação (look-ahead, walk-forward, PSR/DSR), registro, relatórios
- `src/quantlab/strategies`: uma estratégia por módulo, contrato em `__init__.py`
- `research/hypotheses`: hipóteses do estrategista; `reports/`: relatórios gerados
- `docs/`: conceitos de avaliação e funcionamento dos agentes (em português)
- Código e README em inglês; docs, hipóteses e relatórios em português.
