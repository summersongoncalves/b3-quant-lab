---
name: ciclo
description: Roda o ciclo de pesquisa estrategista → implementador → validador por N iterações num dataset e gera um resumo. Use quando o usuário pedir para rodar o ciclo, buscar estratégias ou "/ciclo SÍMBOLO TF N".
---

# Ciclo de pesquisa

Argumentos esperados: `SÍMBOLO TIMEFRAME [N=3] [daytrade|swing]`. Ex.: `/ciclo WIN$N M5 3 daytrade`.

## Antes de começar
1. Confirme que o dataset existe: `uv run quantlab info <SÍMBOLO> <TF>`. Se não existir, pare e diga ao usuário qual `quantlab fetch` rodar (exige o MT5 aberto e logado).
2. Rode `uv run pytest -q`. Se falhar, pare: não se pesquisa com o motor quebrado.

## Cada iteração (em sequência, nunca em paralelo: cada uma aprende com a anterior)
1. **estrategista** (Agent, subagent_type `estrategista`): passe dataset, timeframe, modo e o número da iteração. Recebe o caminho da hipótese.
2. **implementador** (Agent, subagent_type `implementador`): passe o caminho da hipótese, o símbolo e o timeframe. Se ele não conseguir eliminar o look-ahead, marque a hipótese como `Estado: abandonada (look-ahead)` e vá para a próxima iteração.
3. **validador** (Agent, subagent_type `validador`): passe o nome do módulo, a hipótese e o símbolo. Recebe veredito e sugestões.
4. Anote numa linha o resultado da iteração e siga.

## Parada antecipada
- Se 3 iterações seguidas forem REJEITADAS pelo mesmo motivo (ex.: custos), diga isso ao estrategista na próxima rodada e peça uma mudança de direção (outro timeframe, outro tipo de padrão).
- Pare se surgir um bug no motor apontado pelo validador.

## No fim
Escreva `reports/ciclos/AAAAMMDD-HHMM_<SÍMBOLO>_<TF>.md` com:
- tabela: iteração, hipótese, veredito, Sharpe OOS, DSR, trades, link do relatório;
- número total de tentativas no dataset (`research/registry.jsonl`) e o que isso significa para o DSR;
- o que o ciclo aprendeu (padrões que se repetem nas falhas);
- candidatas ao holdout, se houver, com o comando exato `uv run quantlab holdout ...` para o **usuário** decidir rodar.

Mostre ao usuário a tabela e as conclusões. Nunca rode o holdout por conta própria.
