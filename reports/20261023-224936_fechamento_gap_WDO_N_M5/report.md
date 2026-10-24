# fechamento_gap em WDO_N_M5

**Veredito automático: REJECTED**  
Fade the WDO opening gap at 09:15; stop behind the first-15-minute range, target at the previous close · day trade · gerado em 2026-10-23T22:49:36

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
| Período | 2023-08-01 → 2026-02-05 (629 dias) |
| P&L total / custos | R$ -4,438.26 / R$ 2,132.80 |
| Retorno anual acima do CDI | -1.8% |
| Sharpe / Sortino | -1.22 / -2.01 |
| Deflated Sharpe (11 tentativas no dataset) | 0.1% |
| Max drawdown | -5.4% |
| Trades / acerto / payoff | 172 / 40% / 1.08 |
| Profit factor | 0.72 |
| Exposição | 5% das barras |
| Custos / lucro bruto | 93% |
| Sharpe com custos 2x | -1.80 |

Sharpe por ano: 2023: -0.51, 2024: -1.72, 2025: -1.06, 2026: -1.59

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | -0.43 |
| 2023-08-29 → 2023-09-26 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 2.38 |
| 2023-09-27 → 2023-10-25 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 0.94 |
| 2023-10-26 → 2023-11-24 | `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | 0.21 |
| 2023-11-27 → 2023-12-22 | `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | -1.09 |
| 2023-12-26 → 2024-01-24 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | -0.46 |
| 2024-01-25 → 2024-02-23 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -1.2 |
| 2024-02-26 → 2024-03-22 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -1.28 |
| 2024-03-25 → 2024-04-22 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | -0.56 |
| 2024-04-23 → 2024-05-21 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 1.2 |
| 2024-05-22 → 2024-06-19 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 0.88 |
| 2024-06-20 → 2024-07-17 | `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | 2.51 |
| 2024-07-18 → 2024-08-14 | `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | 0.3 |
| 2024-08-15 → 2024-09-11 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | -0.33 |
| 2024-09-12 → 2024-10-09 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -2.31 |
| 2024-10-10 → 2024-11-06 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | 0.42 |
| 2024-11-07 → 2024-12-06 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 0.53 |
| 2024-12-09 → 2025-01-09 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 0.88 |
| 2025-01-10 → 2025-02-06 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -1.17 |
| 2025-02-07 → 2025-03-10 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | 0.18 |
| 2025-03-11 → 2025-04-07 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | 1.61 |
| 2025-04-08 → 2025-05-08 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | 1.39 |
| 2025-05-09 → 2025-06-05 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | 2.42 |
| 2025-06-06 → 2025-07-04 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | 1.31 |
| 2025-07-07 → 2025-08-01 | `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | 0.92 |
| 2025-08-04 → 2025-08-29 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -5.18 |
| 2025-09-01 → 2025-09-26 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | -2.83 |
| 2025-09-29 → 2025-10-24 | `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | -1.67 |
| 2025-10-27 → 2025-11-24 | `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | -1.12 |
| 2025-11-25 → 2025-12-22 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | -1.97 |
| 2025-12-23 → 2026-01-23 | `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | -2.19 |
| 2026-01-26 → 2026-02-05 | `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -0.12 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'g_min': 0.15, 'b': 0.1, 'g_max': 0.8}` | -1.11 | 248 | -5.1% |
| `{'g_min': 0.15, 'b': 0.15, 'g_max': 0.8}` | -0.91 | 248 | -4.7% |
| `{'g_min': 0.25, 'b': 0.1, 'g_max': 0.8}` | -0.74 | 134 | -3.2% |
| `{'g_min': 0.25, 'b': 0.15, 'g_max': 0.8}` | -0.6 | 134 | -2.7% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Falham 5 dos 7 gates e todos os critérios prévios da hipótese que dependem de resultado (1 a 4). O resultado é negativo **antes dos custos**: na combinação padrão, o bruto é de R$ −1.760 e o líquido, de R$ −4.835. Não existe borda para os custos comerem.

Conferência do código: implementa a hipótese. `pc` = último `close` do pregão anterior, `adr` de 20 pregões com `shift(1)`, faixa só das barras 09:00–09:10, sinal no `close` das 09:10 e piso de 0,20 adr. Não achei look-ahead além do que o teste automático cobre. A exclusão da rolagem por calendário funciona, com 1 vazamento (detalhes abaixo). Nenhum bug no motor.

### Pontos fortes
- **Risco bem definido e cumprido.** Nas 141 saídas por stop, nenhuma perdeu mais de R$ 20 além do projetado (distância × R$ 10 + custos). A maior perda foi de R$ 341 (0,34% de R$ 100 mil), num stop projetado de 32,9 pontos. Não houve gap de barra relevante além do stop, nem nas barras de dado dos EUA. `stop_both` aparece em só 1 de 248 saídas (0,4%), então o resultado não depende da suposição do motor sobre a ordem dentro da barra.
- **A geometria se resolveu como previsto.** Nas saídas, foram 140 stops, 98 alvos, 9 fechamentos e 1 `stop_both`. Só 3,6% dos trades chegaram ao fim do pregão.
- **Correlação baixa com as outras.** A correlação diária foi de +0,04 com a 008 (`direcao_do_dia`, 136 dias em comum) e de −0,07 com a 012 (`falha_balanco_inicial`, 135 dias em comum). O sinal de gap é mesmo uma informação diferente, mas isso não basta quando não há borda.
- **A rolagem está bem tratada.** No conjunto dos dias excluídos, o gap médio é de +11,7 pontos (63 dias), contra −0,55 nos incluídos (646 dias). O carrego fica quase todo no último pregão do mês: gap médio de +9,8 a +35 pontos por ano, contra ~0 no penúltimo. A regra de calendário pega esses dias. A única falha é 29/05/2024: o feriado de Corpus Christi deslocou a janela, o dia teve gap de +12,5 pontos e gerou 1 trade (stop, R$ −99). É irrelevante para o veredito.

### Pontos fracos e riscos
- **A taxa de acerto fica abaixo do passeio aleatório.** Entre os trades resolvidos (stop ou alvo), a taxa de acerto é de 41,0% na combinação padrão. O benchmark de lado aleatório, S/(S+T) com as medianas, dá 42,0%, e o p* com custos é de 46,0%. A folga sobre o aleatório é de **−1,0 p.p.**, quando a hipótese pedia +6 a +8 p.p. para empatar e o critério 4 pedia pelo menos +5. O mesmo acontece em toda a grade:

  | combinação | acerto resolvidos | S/(S+T) | p* |
  |---|---|---|---|
  | g 0,15 / b 0,10 | 41,0% | 42,0% | 46,0% |
  | g 0,15 / b 0,15 | 44,9% | 45,5% | 49,3% |
  | g 0,25 / b 0,10 | 38,1% | 38,4% | 42,0% |
  | g 0,25 / b 0,15 | 41,1% | 42,2% | 45,6% |

  É ruído puro com custo, o cenário "o gap no dólar é informação" que a própria hipótese listou.
- **Critério 1 falhou.** O líquido médio por trade foi de R$ −23,4 em 2024 e de R$ −14,8 em 2025, e todos os anos ficaram negativos em todas as combinações.
- **Critério 2 falhou.** Sem os 10 maiores trades, o resultado vai a R$ −8.356; sem os 20 maiores, a R$ −10.847.
- **Critério 3 falhou.** As 4 combinações têm Sharpe negativo, de −0,60 a −1,11. No walk-forward, os parâmetros escolhidos pulam entre as 4 combinações e o Sharpe de treino oscila de −5,2 a +2,5.
- **Critério 5:**
  - Os dois lados perdem: R$ −1.374 nos gaps de alta (110 trades) e R$ −3.461 nos de baixa (138 trades).
  - Montei um proxy de dia de notícia: barra das 09:30 ou das 10:30 com range acima de 2,5× a mediana de 6 pontos. Os 35 trades desses dias somam R$ +396, com 48,6% de acerto. Os 213 demais somam R$ −5.231, com 39,7% de acerto.
  - O único bolsão positivo está, então, nos dias de notícia, que são ~14% dos trades. A hipótese apontava esses dias como risco, e não como fonte de lucro. Com n = 35 e um proxy definido depois de ver os dados, isso é anedótico.
- **Sem o bracket, a mesma entrada não salva a ideia.** Segurando até o fechamento, os 248 trades têm 50% de acerto e líquido de R$ −710. O resultado só fica perto de zero por causa de 2025 (R$ +7.179); 2023 (R$ −2.785), 2024 (R$ −3.438) e 2026 (R$ −1.667) são negativos. É um só ano bom, e não uma borda.
- **Risco para capital limitado:**
  - No backtest da amostra inteira, o max drawdown é de R$ −5.109 (−5,1%) e vai do pico de 19/05/2023 até 15/12/2025. O pico nunca foi recuperado, ou seja, ~2,5 anos sangrando.
  - A maior sequência é de 12 perdas, a pior sequência acumulada é de R$ −1.992 e o pior dia, de R$ −341 (02/12/2024).
  - No walk-forward (OOS), o max DD é de −5,4% e o Sharpe, de −1,22.
- **Comparação com o baseline.** Na amostra inteira, o `opening_range_breakout` também perde (Sharpe −0,35, R$ −5.215 em 671 trades). A 013 fica pior em Sharpe (−1,11).
- **Custos:** 93% do bruto OOS em valor absoluto, mas o bruto já é negativo.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Encerrar a linha "gap/abertura" no WDO M5.** A 008, a 012 e a 013 mostram que nem a excursão da manhã nem o gap da noite têm direção explorável no WDO M5. Com ~22 tentativas efetivas no dataset (o DSR do registro conta só 11), qualquer nova variante de abertura nesse ativo precisa de um motivo estrutural novo, e não de mais um parâmetro.
2. A hipótese levantou a ideia de usar o **ajuste (~16:00) como referência**, no lugar do último negócio das 18:25. É a única variante com motivação independente, mas é um teste novo, com custo de multiplicidade. Antes de qualquer P&L com lado, faça um teste descritivo de frequência: com que frequência o preço toca o ajuste antes de romper a faixa de 15 minutos, comparado com o lado sorteado.
3. Não explorar o bolsão dos "dias de notícia" (n = 35, proxy definido depois de ver os resultados). Seria ajuste à amostra.
4. Se o laboratório continuar no WDO, mudar de horizonte (swing em D1, carrego ou cupom cambial) ou de ativo. Mais regras de abertura em M5 não são o caminho.
