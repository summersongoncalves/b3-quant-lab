---
name: ciclo
description: Roda o ciclo de pesquisa estrategista → implementador → validador por N iterações num dataset e gera um resumo. Use quando o usuário pedir para rodar o ciclo, buscar estratégias ou "/ciclo SÍMBOLO TF N [modo] [estilo]".
---

# Ciclo de pesquisa

Argumentos esperados: `SÍMBOLO TIMEFRAME [N=3] [daytrade|swing] [direcional|momentum|price_action]`. Ex.: `/ciclo WIN$N M5 3 daytrade price_action`.

**Estilo do estrategista:** se o usuário passar um estilo, use-o em todas as iterações. Se não passar, alterne na ordem direcional → momentum → price_action, começando pelo estilo seguinte ao da última hipótese do mesmo dataset (veja o campo `Estilo:` em `research/hypotheses/`; sem histórico, comece por direcional).

## Antes de começar
1. Confirme que o dataset existe: `uv run quantlab info <SÍMBOLO> <TF>`. Se não existir, pare e diga ao usuário qual `quantlab fetch` rodar (exige o MT5 aberto e logado).
2. Rode `uv run pytest -q`. Se falhar, pare: não se pesquisa com o motor quebrado.
3. O estrategista atual é só de day trade. Se o modo for `swing`, pare e diga ao usuário que ainda não existe estrategista de swing.

## Cada iteração (em sequência, nunca em paralelo: cada uma aprende com a anterior)
1. **estrategista** (Agent, subagent_type `estrategista`): passe dataset, timeframe, modo, **estilo**, o número da iteração e um resumo de uma linha de cada iteração anterior do ciclo. Recebe o caminho da hipótese. Não sugira recusa na chamada: o trabalho dele é propor. Se ele recusar mesmo assim, só vale por bloqueio objetivo (ver "Quando não propor" no prompt dele); nesse caso encerre o ciclo e registre a justificativa no resumo.
2. **implementador** (Agent, subagent_type `implementador`): passe o caminho da hipótese, o símbolo e o timeframe. Se ele não conseguir eliminar o look-ahead, marque a hipótese como `Estado: abandonada (look-ahead)` e vá para a próxima iteração.
3. **validador** (Agent, subagent_type `validador`): passe o nome do módulo, a hipótese e o símbolo. Recebe veredito e sugestões.
4. Anote numa linha o resultado da iteração e siga.

## Refinamento
Quando o validador der **PROMISSORA** (ou CANDIDATA AO HOLDOUT, se ele achar que ainda dá para melhorar), as próximas iterações do ciclo passam a ser de **refinamento** dessa estratégia, em vez de ideias novas:
- Na chamada do estrategista, diga `modo: refinamento da NNN (versão k)` e passe o relatório e as sugestões do validador da versão anterior, mais a tabela das versões já feitas (Sharpe OOS, DSR, trades, resultado sem os 10/20 maiores).
- Cada versão é uma hipótese nova (`NNN-<nome>_v2.md`, módulo `<nome>_v2`) e passa pelo implementador e pelo validador como qualquer outra. Cada versão conta como iteração do ciclo e como tentativa no registro.
- Passe ao validador o módulo da versão anterior, para ele comparar as duas no mesmo período.
- O refinamento termina quando o estrategista declarar `refinamento encerrado` (com o motivo), quando o validador recomendar parar, ou quando as iterações do ciclo acabarem. Depois disso, se ainda houver iterações, o ciclo volta a ideias novas.
- No resumo do ciclo, inclua a tabela de versões e diga qual é a **melhor versão** e por quê. A melhor versão é a mais robusta, não necessariamente a de maior Sharpe.

## Parada antecipada
- Se 3 iterações seguidas forem REJEITADAS pelo mesmo motivo (ex.: custos), diga isso ao estrategista na próxima rodada e peça uma mudança de direção (outro timeframe, outro tipo de padrão).
- Pare se surgir um bug no motor apontado pelo validador.

## No fim
Escreva `reports/ciclos/AAAAMMDD-HHMM_<SÍMBOLO>_<TF>.md` com:
- tabela: iteração, estilo, hipótese (com a versão, se for refinamento), veredito, Sharpe OOS, DSR, trades, link do relatório;
- número total de tentativas no dataset (`research/registry.jsonl`) e o que isso significa para o DSR;
- o que o ciclo aprendeu (padrões que se repetem nas falhas);
- candidatas ao holdout, se houver, com o comando exato `uv run quantlab holdout ...` para o **usuário** decidir rodar.

Mostre ao usuário a tabela e as conclusões. Nunca rode o holdout por conta própria.
