# reversao_esticamento_vwap em VBBR3_M5

**Veredito automático: REJECTED**  
Fade of a >0.5 adr stretch from the daily VWAP in the mid-session, with ADR-based stop, 1.5x target and fixed-risk sizing · day trade · gerado em 2026-10-23T20:38:18

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
| P&L total / custos | R$ -7,240.41 / R$ 15,650.75 |
| Retorno anual acima do CDI | -3.3% |
| Sharpe / Sortino | -0.59 / -0.77 |
| Deflated Sharpe (6 tentativas no dataset) | 0.4% |
| Max drawdown | -11.1% |
| Trades / acerto / payoff | 129 / 46% / 1.02 |
| Profit factor | 0.86 |
| Exposição | 7% das barras |
| Custos / lucro bruto | 186% |
| Sharpe com custos 2x | -1.58 |

Sharpe por ano: 2023: -1.41, 2024: -0.48, 2025: -0.01, 2026: 0.0

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-04-28 → 2023-05-26 | `{'stop_mult': 0.35}` | 4.08 |
| 2023-05-29 → 2023-06-26 | `{'stop_mult': 0.25}` | 1.48 |
| 2023-06-27 → 2023-07-24 | `{'stop_mult': 0.25}` | 0.84 |
| 2023-07-25 → 2023-08-21 | `{'stop_mult': 0.25}` | 0.3 |
| 2023-08-22 → 2023-09-19 | `{'stop_mult': 0.25}` | -1.54 |
| 2023-09-20 → 2023-10-18 | `{'stop_mult': 0.25}` | -2.41 |
| 2023-10-19 → 2023-11-17 | `{'stop_mult': 0.25}` | -2.43 |
| 2023-11-20 → 2023-12-15 | `{'stop_mult': 0.25}` | -0.18 |
| 2023-12-18 → 2024-01-17 | `{'stop_mult': 0.35}` | 0.71 |
| 2024-01-18 → 2024-02-16 | `{'stop_mult': 0.5}` | 1.07 |
| 2024-02-19 → 2024-03-15 | `{'stop_mult': 0.5}` | -0.1 |
| 2024-03-18 → 2024-04-15 | `{'stop_mult': 0.5}` | 0.41 |
| 2024-04-16 → 2024-05-14 | `{'stop_mult': 0.5}` | 0.41 |
| 2024-05-15 → 2024-06-12 | `{'stop_mult': 0.5}` | 0.86 |
| 2024-06-13 → 2024-07-10 | `{'stop_mult': 0.5}` | 1.87 |
| 2024-07-11 → 2024-08-07 | `{'stop_mult': 0.5}` | 2.81 |
| 2024-08-08 → 2024-09-04 | `{'stop_mult': 0.5}` | 1.46 |
| 2024-09-05 → 2024-10-02 | `{'stop_mult': 0.25}` | -0.34 |
| 2024-10-03 → 2024-10-30 | `{'stop_mult': 0.25}` | -0.82 |
| 2024-10-31 → 2024-11-29 | `{'stop_mult': 0.35}` | -1.23 |
| 2024-12-02 → 2025-01-02 | `{'stop_mult': 0.5}` | -1.81 |
| 2025-01-03 → 2025-01-30 | `{'stop_mult': 0.5}` | -0.38 |
| 2025-01-31 → 2025-02-27 | `{'stop_mult': 0.5}` | -1.43 |
| 2025-02-28 → 2025-03-31 | `{'stop_mult': 0.5}` | 0.26 |
| 2025-04-01 → 2025-04-30 | `{'stop_mult': 0.5}` | -0.7 |
| 2025-05-02 → 2025-05-29 | `{'stop_mult': 0.35}` | 1.16 |
| 2025-05-30 → 2025-06-27 | `{'stop_mult': 0.35}` | 1.78 |
| 2025-06-30 → 2025-07-25 | `{'stop_mult': 0.35}` | 1.78 |
| 2025-07-28 → 2025-08-22 | `{'stop_mult': 0.35}` | -0.87 |
| 2025-08-25 → 2025-09-19 | `{'stop_mult': 0.25}` | -0.51 |
| 2025-09-22 → 2025-10-17 | `{'stop_mult': 0.5}` | -1.38 |
| 2025-10-20 → 2025-11-14 | `{'stop_mult': 0.35}` | 0.98 |
| 2025-11-17 → 2025-12-15 | `{'stop_mult': 0.35}` | 1.45 |
| 2025-12-16 → 2026-01-16 | `{'stop_mult': 0.35}` | 0.86 |
| 2026-01-19 → 2026-01-19 | `{'stop_mult': 0.35}` | 0.04 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'stop_mult': 0.25}` | -0.58 | 136 | -14.2% |
| `{'stop_mult': 0.35}` | -0.11 | 136 | -9.0% |
| `{'stop_mult': 0.5}` | -0.28 | 136 | -8.5% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. A estratégia falha em 5 de 7 critérios automáticos e também nos dois critérios de sucesso que a própria hipótese definiu. O DSR foi calculado com 6 tentativas no registro, mas o número efetivo em VBBR3 M5 é de ~37. Com um Sharpe OOS negativo, o DSR fica em ~0% com qualquer n, então a multiplicidade só reforça a rejeição.

Números do walk-forward (OOS, 2023-04-28 a 2026-01-19): Sharpe −0,59, DSR 0,4%, max DD −11,1%, 129 trades, P&L de R$ −7.240 com R$ 15.651 de custos (custo/bruto = 186%), acerto de 45,7% (abaixo do p* de 46,1% para s = 0,35) e Sharpe −1,58 com custos 2x. A análise abaixo usa backtests na amostra de pesquisa inteira, um por valor da grade (136 trades cada).

### Pontos fortes
- **Código fiel à hipótese e sem look-ahead escondido.** `adr` usa o range dos 20 pregões anteriores com `shift(1)`. `dev` usa o `close` e a VWAP acumulada até a barra atual, ambos conhecidos no fechamento. A janela 11:00–15:25, o corte de 10:10, a regra de 1 entrada por dia (primeira ocorrência), o alvo de 1,5 × stop e w = min(1; 0,008 × close / stop) batem com o texto.
- **O envelope de risco funcionou exatamente como projetado.** Nenhuma saída `stop_both` (0% nas três grades), então o resultado não depende da suposição do motor dentro da barra. Também não houve gap além do stop. As perdas no stop ficaram na média em R$ 919 e no pior caso em R$ 956 com s = 0,35 (projeção: ≤ ~R$ 940–980). Com s = 0,25, o pior trade foi de R$ −1.017 (1,02% do capital), em 2023, quando o C era de 18 bp. O risco efetivo por stop foi de 0,84% a 0,92% do capital, perto dos ~0,8% + custo. O pior dia é igual ao pior trade (≤ R$ 1.017).
- **O bracket melhorou o bruto.** Com s = 0,35, o bruto médio foi de ~17 bp por trade, contra 12,6 bp segurando até o fechamento na exploração. Foi melhor que o baseline: `opening_range_breakout` padrão no mesmo dataset deu 603 trades, R$ −135 mil e Sharpe ≈ −2,3.

### Pontos fracos e riscos
- **O bruto não paga 2 × C em nenhum ano (critério 1 da hipótese reprovado).** Bruto contra custo médio por trade, em bp, com s = 0,35: 2023 18,1 vs 17,8; 2024 10,7 vs 14,0; 2025 21,2 vs 14,5. O 2 × C exigido (~28–36 bp) não foi atingido em nenhum ano e em nenhuma grade. Com s = 0,25, 2024 teve só 3,3 bp; com s = 0,5, 2023 teve 5,5 bp.
- **Sem os 5 maiores trades, o resultado é negativo (critério 2 reprovado).** Com s = 0,35, o P&L líquido na amostra inteira é de R$ −4 (zero), e sem os 5 maiores trades vai a R$ −5.445. Com s = 0,25: R$ −13.374. Com s = 0,5: R$ −8.016. Os 5 maiores trades são todos alvos de ~R$ 1.000–1.100, ou seja, a concentração vem do teto do bracket e não de caudas raras. Mesmo assim, o líquido não sobrevive sem eles.
- **Os parâmetros são instáveis.** O walk-forward passa pelos três valores da grade: 0,25 em 2023, 0,5 em quase todo 2024 e no começo de 2025, e 0,35 no fim de 2025. Os três valores dão resultado líquido negativo na amostra inteira (Sharpe −0,58, −0,11 e −0,28). O "melhor" valor (0,35, com P&L ≈ 0) é o padrão, escolhido depois da exploração.
- **Regime.** 2023 foi negativo (Sharpe OOS −1,41) e 2024 também (−0,48). 2025 ficou no zero (−0,01). Não há nenhum ano claramente positivo.
- **Acerto contra p\*.** O acerto OOS foi de 45,7%, contra p* = 46,1%. Na amostra inteira, com s = 0,35, foi de 49,3%. Fica muito pouco acima do p*, mas 35% das saídas são no fechamento, com ganho menor que o alvo, e o payoff realizado é de ~1,0. As saídas com s = 0,35 foram 36% `stop`, 29% `target` e 35% `close`.
- **Sobreposição com a 003 invertida.** Nos 54 dias em que as duas operam (40% dos 136 trades da 004 e 38% dos 142 da 003), a 004 fica do lado oposto da 003 em 92,6% dos casos. A correlação do P&L diário é de −0,49 nos dias em que as duas operam e de −0,24 em todos os dias. A correlação de posição barra a barra é de −0,34. Parte do bruto positivo da 004 é só o espelho do bruto negativo da 003. Na prática, isso é mineração da inversão, que o validador da 003 pediu para evitar.
- **Risco para capital limitado.** A maior sequência de perdas foi de 8 trades (R$ −5.218, ou −5,2% do capital, com s = 0,35). O max DD na amostra inteira foi de R$ −9.546, com pico em 28/04/2023, e **nunca foi recuperado** até 19/01/2026. São ~2,7 anos debaixo d'água.
- **Custos.** O custo come 186% do bruto no OOS. A execução seria viável: a liquidez de VBBR3 no miolo do pregão é suficiente para R$ 100 mil e o horário fica longe dos leilões. O problema não é executar, é que a margem não existe.

### Bug no motor
Não encontrei bug. O `_brackets` fixa o stop e o alvo a partir da abertura da barra de entrada, com as distâncias da barra de sinal (`shift(1)`). Ele cobra o custo cheio na saída por bracket, trata o gap além do stop e bloqueia a reentrada no mesmo dia. As perdas observadas (stop + ~14–18 bp × w) batem com isso.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Encerrar o day trade em VBBR3 M5**, como a própria hipótese recomenda. São 8 famílias e ~37 tentativas efetivas, e nenhuma chega a 2 × C. O tick de R$ 0,01 num papel de ~R$ 21 (~14 bp de ida e volta) é uma barreira estrutural. Mais tentativas aqui só inflam a multiplicidade.
2. Se a ideia de reversão à VWAP for retomada, que seja num **ativo de preço alto ou num futuro com custo por trade bem menor em bp** (ex.: WIN/WDO, ou uma ação acima de R$ 60), nunca olhado antes. O limiar (0,5 adr), a janela e o bracket devem ficar congelados exatamente como aqui, sem nova exploração. Critério prévio: bruto > 2 × C em cada ano.
3. Não testar variações de alvo, limiar ou janela em VBBR3: qualquer ajuste agora seria calibração sobre os números deste relatório.
