# momentum_vwap_bracket em VBBR3_M5

**Veredito automático: REJECTED**  
Frozen 12:00 intraday momentum confirmed by daily VWAP and relative volume, with ADR-based stop, 2x target and fixed-risk sizing · day trade · gerado em 2026-10-23T20:30:30

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ❌ Sharpe fora da amostra >= mínimo
- ✅ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ❌ Maioria dos anos positiva
- ❌ Maioria dos parâmetros vizinhos positiva
- ❌ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-04-28 → 2026-01-19 (681 dias) |
| P&L total / custos | R$ -25,842.19 / R$ 16,344.99 |
| Retorno anual acima do CDI | -10.6% |
| Sharpe / Sortino | -1.79 / -1.97 |
| Deflated Sharpe (3 tentativas no dataset) | 0.1% |
| Max drawdown | -25.8% |
| Trades / acerto / payoff | 136 / 32% / 1.22 |
| Profit factor | 0.58 |
| Exposição | 10% das barras |
| Custos / lucro bruto | 172% |
| Sharpe com custos 2x | -2.71 |

Sharpe por ano: 2023: -0.89, 2024: -1.52, 2025: -2.74, 2026: -4.58

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-04-28 → 2023-05-26 | `{'stop_mult': 0.3}` | 0.8 |
| 2023-05-29 → 2023-06-26 | `{'stop_mult': 0.5}` | -0.65 |
| 2023-06-27 → 2023-07-24 | `{'stop_mult': 0.5}` | -1.28 |
| 2023-07-25 → 2023-08-21 | `{'stop_mult': 0.5}` | -0.53 |
| 2023-08-22 → 2023-09-19 | `{'stop_mult': 0.4}` | -1.29 |
| 2023-09-20 → 2023-10-18 | `{'stop_mult': 0.4}` | -1.61 |
| 2023-10-19 → 2023-11-17 | `{'stop_mult': 0.3}` | -1.3 |
| 2023-11-20 → 2023-12-15 | `{'stop_mult': 0.3}` | -0.16 |
| 2023-12-18 → 2024-01-17 | `{'stop_mult': 0.3}` | 2.22 |
| 2024-01-18 → 2024-02-16 | `{'stop_mult': 0.3}` | 1.93 |
| 2024-02-19 → 2024-03-15 | `{'stop_mult': 0.3}` | 1.99 |
| 2024-03-18 → 2024-04-15 | `{'stop_mult': 0.3}` | 0.73 |
| 2024-04-16 → 2024-05-14 | `{'stop_mult': 0.3}` | -1.32 |
| 2024-05-15 → 2024-06-12 | `{'stop_mult': 0.3}` | -1.72 |
| 2024-06-13 → 2024-07-10 | `{'stop_mult': 0.3}` | -2.74 |
| 2024-07-11 → 2024-08-07 | `{'stop_mult': 0.3}` | -2.82 |
| 2024-08-08 → 2024-09-04 | `{'stop_mult': 0.3}` | -2.53 |
| 2024-09-05 → 2024-10-02 | `{'stop_mult': 0.5}` | -4.06 |
| 2024-10-03 → 2024-10-30 | `{'stop_mult': 0.5}` | -1.51 |
| 2024-10-31 → 2024-11-29 | `{'stop_mult': 0.5}` | -2.35 |
| 2024-12-02 → 2025-01-02 | `{'stop_mult': 0.3}` | -0.12 |
| 2025-01-03 → 2025-01-30 | `{'stop_mult': 0.3}` | -0.08 |
| 2025-01-31 → 2025-02-27 | `{'stop_mult': 0.3}` | 1.61 |
| 2025-02-28 → 2025-03-31 | `{'stop_mult': 0.3}` | 1.12 |
| 2025-04-01 → 2025-04-30 | `{'stop_mult': 0.4}` | -0.74 |
| 2025-05-02 → 2025-05-29 | `{'stop_mult': 0.4}` | -2.0 |
| 2025-05-30 → 2025-06-27 | `{'stop_mult': 0.5}` | -4.57 |
| 2025-06-30 → 2025-07-25 | `{'stop_mult': 0.5}` | -3.89 |
| 2025-07-28 → 2025-08-22 | `{'stop_mult': 0.5}` | -2.32 |
| 2025-08-25 → 2025-09-19 | `{'stop_mult': 0.4}` | 0.05 |
| 2025-09-22 → 2025-10-17 | `{'stop_mult': 0.4}` | 1.16 |
| 2025-10-20 → 2025-11-14 | `{'stop_mult': 0.4}` | -0.8 |
| 2025-11-17 → 2025-12-15 | `{'stop_mult': 0.5}` | -1.73 |
| 2025-12-16 → 2026-01-16 | `{'stop_mult': 0.5}` | -4.06 |
| 2026-01-19 → 2026-01-19 | `{'stop_mult': 0.5}` | -4.67 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'stop_mult': 0.3}` | -1.62 | 142 | -28.1% |
| `{'stop_mult': 0.4}` | -1.74 | 142 | -27.7% |
| `{'stop_mult': 0.5}` | -1.93 | 142 | -25.8% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. A estratégia falha em 6 dos 7 critérios. Só passa `no_lookahead` e o número de trades. Também falha nos dois critérios de sucesso que a própria hipótese definiu, e por larga margem. O sinal congelado de BBAS3 não se replica em VBBR3: o bruto é negativo, não só pequeno demais para pagar o custo.

Números do OOS (walk-forward, 2023-04-28 a 2026-01-19): Sharpe -1,79, DSR 0,1%, max DD -25,8% (R$ -25.842 sobre R$ 100 mil), 136 trades, acerto de 32,4%, profit factor 0,58, resultado de R$ -190 por trade.

### Pontos fortes
- **Código fiel à hipótese.** Confere a barra de sinal 11:55, o corte da primeira barra em 10:10, o k = 1,5, a confirmação pela VWAP e o `rv > 1`. `escala` e `adr` usam `shift(1)` e excluem o dia atual, o alvo é 2 × stop e o tamanho é `w = min(1, 0,008 × close / stop)`. Não achei look-ahead escondido. O `high`/`low` diário só entra no `adr` com defasagem de 1 dia, e o teste de truncamento passou.
- **O envelope de risco funciona como projetado.** As saídas por `stop` dão em média R$ -910, entre R$ -766 e R$ -976. O projetado era 0,8% (R$ 800) mais o custo de ~R$ 106 a 140, ou seja ≤ R$ 940 a 980. Não houve gap além do stop nem `stop_both` (0%). As saídas por alvo dão em média R$ +1.450 (R$ 1.600 brutos menos custos). O risco efetivo por trade bate com os ~0,8% mais custo.
- **O bracket reduz o estrago do sinal.** Na amostra inteira, com s = 0,4, os mesmos sinais segurados até o fechamento (com o mesmo `w`) perdem R$ -38.668, com pior trade de R$ -2.981. Com o bracket, a perda é de R$ -26.202 e o pior trade fica em R$ -935.

### Pontos fracos e riscos
- **O sinal tem bruto negativo.** Bruto médio por trade no OOS, por ano: 2023 = -1,0 bp, 2024 = +0,2 bp, 2025 = -28,6 bp, 2026 = -97,6 bp (1 trade). O critério da hipótese pedia > 2 × C (~28 bp) em todos os anos e falhou em todos. Sem bracket, segurando até o fechamento, o bruto fica entre -14 e -26 bp em todos os anos: o movimento depois do meio-dia vai **contra** o sinal. Com isso o `cost_to_gross` (1,72) nem tem leitura útil, porque o custo (R$ 16.345) só aumenta uma perda bruta (R$ -9.497).
- **Sem os 5 maiores trades:** o resultado vai de R$ -25.842 para R$ -33.258. O lucro não está concentrado, porque não há lucro. Critério da hipótese: falhou.
- **Saídas no OOS:** 44,9% no `close`, 43,4% no `stop`, 11,8% no `target` e 0% em `stop_both`. Entre as saídas por bracket, só 21% são alvo (16 de 75), contra um p* de ~38%. O acerto total é de 32,4%, abaixo do p* e muito abaixo dos 50% a 55% esperados.
- **Parâmetros instáveis:** o walk-forward escolheu 0,3 em 16 folds, 0,5 em 12 e 0,4 em 7, pulando entre os extremos (0,3 ↔ 0,5) sem padrão. Os Sharpes de treino ficam quase todos negativos. A grade é negativa nas 3 combinações (-1,62, -1,74 e -1,93), com o mesmo sinal, como a hipótese previa, só que do lado errado.
- **Regime:** nenhum ano é positivo (Sharpe de -0,89, -1,52, -2,74 e -4,58). A piora em 2025 coincide com a piora do bruto.
- **Capital limitado:** o pior dia é de R$ -976 (~1%). A maior sequência é de 8 perdas seguidas no OOS (R$ -5.593) e de 12 na amostra inteira com s = 0,3 (R$ -7.002, 7% do capital). O max DD começa no primeiro dia do OOS (pico em 2023-04-28) e não se recupera até o fim da amostra: são 2,7 anos debaixo d'água. Com custos 2x, o DD chega a -42%.
- **Baseline:** o `opening_range_breakout` (padrão) no mesmo período tem Sharpe -2,56 e DD de -111%. A 003 é "menos ruim", mas o motivo é ter menos trades e o bracket, não um sinal com vantagem.
- **Multiplicidade:** o DSR usa n = 3 tentativas, mas as tentativas reais em VBBR3 são ~17 (14 escondidas + 3), e a regra veio de ~84 tentativas em BBAS3. Com o Sharpe negativo isso não muda nada, mas confirma que o "padrão" de BBAS3 era ruído selecionado.

### Motor (lógica nova de brackets)
Não achei bug. Conferi que:
- a entrada sai na abertura da barra 12:00 e as distâncias são lidas da barra de sinal (`stop.shift(1)`);
- stop e alvo valem já na barra de entrada;
- um gap além do stop sai na abertura;
- o custo é cobrado uma vez na entrada e uma na saída, e o custo médio de R$ 120 por trade bate com `w` (0,80) × ~15 bp × R$ 100 mil;
- não há reentrada no mesmo dia depois do bracket;
- o `prev_held` é zero na virada do dia.

Há dois detalhes que não afetam esta estratégia:
- `stop.shift(1)` não é agrupado por dia, mas não importa porque a posição é zero na primeira barra.
- Um redimensionamento no mesmo lado não reposiciona stop e alvo.

O último fold do walk-forward tem 1 dia só (2026-01-19). É cosmético.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Encerrar a família "momentum intradiário do meio-dia em ações"**, como a própria hipótese pré-registrou ("um resultado negativo aqui fecha a família"). Não procurar outro ativo onde a mesma regra funcione: isso seria repetir a mineração de BBAS3.
2. **Não inverter o sinal** para explorar o bruto negativo (reversão ao meio-dia). Ele é pequeno (-14 a -26 bp), está na ordem do custo (~14 a 18 bp) e seria uma hipótese nova minerada sobre este resultado. Se quiser testar reversão, pré-registre com justificativa econômica e teste num terceiro ativo nunca olhado.
3. **Reaproveitar o envelope de risco** (stop por `adr`, alvo 2x, tamanho por risco de 0,8%), que se comportou exatamente como projetado: perdas de stop de R$ 766 a 976, sem `stop_both` nem gaps. Ele é um bom molde para a próxima hipótese de sinal diferente, de preferência em futuros (WIN/WDO), onde o custo relativo é menor.
