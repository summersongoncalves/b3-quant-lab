# falso_rompimento_20d em VBBR3_M5

**Veredito automático: REJECTED**  
Fade of a failed breakout of the previous 20-session low/high on M5, with ADR-based stop, 2x target and fixed-risk sizing · day trade · gerado em 2026-10-23T20:45:33

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
| P&L total / custos | R$ -10,472.52 / R$ 11,956.21 |
| Retorno anual acima do CDI | -4.7% |
| Sharpe / Sortino | -1.04 / -0.82 |
| Deflated Sharpe (9 tentativas no dataset) | 0.1% |
| Max drawdown | -12.9% |
| Trades / acerto / payoff | 104 / 44% / 0.90 |
| Profit factor | 0.71 |
| Exposição | 9% das barras |
| Custos / lucro bruto | 806% |
| Sharpe com custos 2x | -1.95 |

Sharpe por ano: 2023: -1.13, 2024: -0.77, 2025: -1.42, 2026: -2.5

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-04-28 → 2023-05-26 | `{'stop_mult': 0.5}` | -3.08 |
| 2023-05-29 → 2023-06-26 | `{'stop_mult': 0.4}` | -1.29 |
| 2023-06-27 → 2023-07-24 | `{'stop_mult': 0.4}` | -1.29 |
| 2023-07-25 → 2023-08-21 | `{'stop_mult': 0.4}` | -1.17 |
| 2023-08-22 → 2023-09-19 | `{'stop_mult': 0.5}` | -0.19 |
| 2023-09-20 → 2023-10-18 | `{'stop_mult': 0.4}` | 1.38 |
| 2023-10-19 → 2023-11-17 | `{'stop_mult': 0.3}` | 1.39 |
| 2023-11-20 → 2023-12-15 | `{'stop_mult': 0.3}` | 2.86 |
| 2023-12-18 → 2024-01-17 | `{'stop_mult': 0.3}` | -0.35 |
| 2024-01-18 → 2024-02-16 | `{'stop_mult': 0.5}` | -0.41 |
| 2024-02-19 → 2024-03-15 | `{'stop_mult': 0.5}` | -2.45 |
| 2024-03-18 → 2024-04-15 | `{'stop_mult': 0.5}` | -3.7 |
| 2024-04-16 → 2024-05-14 | `{'stop_mult': 0.5}` | -3.63 |
| 2024-05-15 → 2024-06-12 | `{'stop_mult': 0.3}` | -2.06 |
| 2024-06-13 → 2024-07-10 | `{'stop_mult': 0.3}` | -1.36 |
| 2024-07-11 → 2024-08-07 | `{'stop_mult': 0.3}` | -1.67 |
| 2024-08-08 → 2024-09-04 | `{'stop_mult': 0.3}` | -2.65 |
| 2024-09-05 → 2024-10-02 | `{'stop_mult': 0.4}` | -0.02 |
| 2024-10-03 → 2024-10-30 | `{'stop_mult': 0.4}` | 2.84 |
| 2024-10-31 → 2024-11-29 | `{'stop_mult': 0.3}` | 3.56 |
| 2024-12-02 → 2025-01-02 | `{'stop_mult': 0.4}` | 2.97 |
| 2025-01-03 → 2025-01-30 | `{'stop_mult': 0.4}` | 2.11 |
| 2025-01-31 → 2025-02-27 | `{'stop_mult': 0.4}` | 2.15 |
| 2025-02-28 → 2025-03-31 | `{'stop_mult': 0.3}` | 0.54 |
| 2025-04-01 → 2025-04-30 | `{'stop_mult': 0.3}` | 0.31 |
| 2025-05-02 → 2025-05-29 | `{'stop_mult': 0.5}` | -2.63 |
| 2025-05-30 → 2025-06-27 | `{'stop_mult': 0.5}` | -3.1 |
| 2025-06-30 → 2025-07-25 | `{'stop_mult': 0.3}` | -1.18 |
| 2025-07-28 → 2025-08-22 | `{'stop_mult': 0.3}` | 0.05 |
| 2025-08-25 → 2025-09-19 | `{'stop_mult': 0.3}` | 0.96 |
| 2025-09-22 → 2025-10-17 | `{'stop_mult': 0.3}` | -2.37 |
| 2025-10-20 → 2025-11-14 | `{'stop_mult': 0.5}` | 0.59 |
| 2025-11-17 → 2025-12-15 | `{'stop_mult': 0.5}` | 0.59 |
| 2025-12-16 → 2026-01-16 | `{'stop_mult': 0.5}` | 0.55 |
| 2026-01-19 → 2026-01-19 | `{'stop_mult': 0.4}` | -0.56 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'stop_mult': 0.3}` | -0.98 | 108 | -17.2% |
| `{'stop_mult': 0.4}` | -0.77 | 108 | -13.8% |
| `{'stop_mult': 0.5}` | -0.97 | 108 | -12.3% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Falham 5 dos 7 critérios (Sharpe OOS -1,04; DSR 0,1%; 0 de 4 anos positivos; 0 de 3 pontos da grade positivos; Sharpe -1,95 com custos 2x). Os dois critérios prévios da própria hipótese também falham: o bruto médio por trade fica longe de 2×C (~30 bp) em todos os anos, e o resultado sem os 5 maiores trades é ainda mais negativo.

Conferência do código: implementa o que a hipótese descreve. `L20`, `H20` e `adr` usam `shift(1)` no nível diário. `min_hoje`/`max_hoje` são `cummin`/`cummax` até a barra atual, inclusive, o que é legítimo com o sinal no fechamento. O tamanho usa o `close` da barra de sinal, o stop é `s × adr` em R$ e o alvo é 2× o stop. Não achei look-ahead que o teste automático deixe passar. O motor aplica o stop a partir da abertura de entrada (`o[t] - side*stop`), como a hipótese supõe. Não achei bug no motor.

Números (backtest em Python sobre a amostra de pesquisa; nenhum uso de holdout):

| | s=0,3 | s=0,4 | s=0,5 | OOS (WF) |
|---|---|---|---|---|
| Trades | 108 | 108 | 108 | 104 |
| Bruto/trade 2023 (bp) | -12,7 | -4,6 | -9,9 | -0,5 |
| Bruto/trade 2024 (bp) | +6,1 | +11,1 | +5,3 | +3,8 |
| Bruto/trade 2025 (bp) | +6,7 | -2,4 | +1,0 | +1,1 |
| Bruto/trade total (bp) | +1,4 | +3,5 | -0,5 | +1,9 |
| Custo/trade (bp) | 15,3 | 15,3 | 15,3 | 15,2 |
| Saídas stop / alvo / fechamento | 46/17/45 | 34/10/64 | 29/5/74 | 33/9/62 |
| P&L líquido (R$) | -12.707 | -8.390 | -9.365 | -10.473 |
| Sem os 5 maiores trades (R$) | -20.028 | -15.894 | -16.999 | -17.882 |

### Pontos fortes
- O envelope de risco funcionou exatamente como projetado. Não houve nenhum `stop_both` (0 de 104) nem gap além do stop: a maior perda OOS foi de R$ 945 (0,95% do capital), igual ao stop (~R$ 900) mais custos. Pior dia: R$ -945.
- Amostra OOS suficiente para o GATE: 104 trades contra o mínimo de 30, já que o OOS cobre quase todo o período (começa em 28/04/2023). Mesmo assim, com ~35 trades por ano, o erro-padrão do bruto por trade é da ordem de ±10 a 15 bp por ano. Mas o resultado não é ambíguo: o bruto fica perto de zero em toda a grade e em todos os anos.
- Bate o baseline `opening_range_breakout` no mesmo dataset (Sharpe -2,71 na amostra inteira, 603 trades), mas só por ser menos negativa. Os dois perdem dinheiro.

### Pontos fracos e riscos
- **A tese central não aparece nos dados.** A hipótese esperava uma volta de 0,5 a 1 `adr`. Só 9 de 104 trades OOS (8,7%) chegaram ao alvo de 0,8 `adr`, e 60% saíram no fechamento com média de +R$ 113. A taxa de acerto (44%) fica acima do p* de 37,7%, mas o payoff realizado é de 0,90, contra os ~1,5 projetados. Por isso o p* do bracket não descreve a estratégia: ela vira, na prática, um "segura até o fechamento" com stop.
- **O bruto ainda é ~0, como o do parente de 1 pregão** (+0,7 a +3,6 bp). O nível de 20 pregões não concentrou reversões maiores. O bruto total (+1,9 bp OOS) é 1/8 do custo (custos/bruto = 806%).
- **Viés de lado.** Os 63 vendidos OOS somam R$ -11.038 (média de -175), e os 41 comprados somam R$ +566 (média de +14). O fade de máximas perdeu num papel que subiu de R$ 15 para R$ 25. Mesmo o lado comprado não paga 2×C, e selecioná-lo agora seria mineração de subconjunto.
- **Estabilidade de parâmetros.** O walk-forward pula entre os três pontos da grade (0,3 / 0,4 / 0,5 aparecem em blocos alternados) com Sharpe de treino entre -3,7 e +3,6. Isso é ruído: não existe ótimo.
- **Risco para capital limitado.** O max drawdown OOS foi de -12,9% (R$ ~13 mil) e **nunca se recuperou**: o pico é de 03/05/2023, o vale de 12/08/2024, e o fim da amostra ainda está abaixo do pico. A maior sequência foi de 6 perdas, somando R$ -5.453 (-5,5%). Com s = 0,3, foram 8 perdas seguidas (R$ -7.653).
- **Multiplicidade.** O DSR usa 9 tentativas registradas, mas o número efetivo declarado é de ~46, e a escolha de 20 pregões veio depois de ver a regra parente. Com o n correto, o DSR ficaria ainda menor (já está em 0,1%). Isso não muda o veredito.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Parar de iterar em VBBR3 M5.** São ~46 tentativas e 10 famílias, todas com bruto entre -19 e +17 bp contra ~15 bp de custo. Não proponha a versão "só comprado" nem a mudança de 20 para 10 ou 50 pregões: seriam mineração sobre este mesmo resultado.
- Se a ideia de falso rompimento de extremo multissemanal continuar interessante, testar a regra **exatamente igual** (pré-registrada, sem mudar parâmetro) em outro ativo mais líquido e com custo relativo menor (ex.: WIN$N, ou uma ação de preço/liquidez maior), contando como uma tentativa nova nesse dataset.
- Antes de qualquer nova hipótese de day trade em ações de ~R$ 20, calibrar o custo real (nota de corretagem e slippage medido). Com C ~15 bp, um bruto de 3 bp por trade nunca vai passar.
