# direcao_do_dia em WDO_N_M5

**Veredito automático: REJECTED**  
Follow the morning excursion (>= 0.3 ADR from the open, one side) at 10:30; stop at open -/+ 0.1 ADR, target at open +/- 1 ADR · day trade · gerado em 2026-10-23T21:55:05

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
| P&L total / custos | R$ -7,987.40 / R$ 4,464.00 |
| Retorno anual acima do CDI | -3.2% |
| Sharpe / Sortino | -1.17 / -1.74 |
| Deflated Sharpe (1 tentativas no dataset) | 3.3% |
| Max drawdown | -8.1% |
| Trades / acerto / payoff | 360 / 45% / 0.96 |
| Profit factor | 0.79 |
| Exposição | 29% das barras |
| Custos / lucro bruto | 127% |
| Sharpe com custos 2x | -1.82 |

Sharpe por ano: 2023: -1.79, 2024: -0.88, 2025: -1.22, 2026: -1.81

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{}` | -2.39 |
| 2023-08-29 → 2023-09-26 | `{}` | -3.4 |
| 2023-09-27 → 2023-10-25 | `{}` | -3.52 |
| 2023-10-26 → 2023-11-24 | `{}` | -1.9 |
| 2023-11-27 → 2023-12-22 | `{}` | -1.45 |
| 2023-12-26 → 2024-01-24 | `{}` | -0.47 |
| 2024-01-25 → 2024-02-23 | `{}` | -1.2 |
| 2024-02-26 → 2024-03-22 | `{}` | 0.34 |
| 2024-03-25 → 2024-04-22 | `{}` | 0.44 |
| 2024-04-23 → 2024-05-21 | `{}` | 1.26 |
| 2024-05-22 → 2024-06-19 | `{}` | -1.41 |
| 2024-06-20 → 2024-07-17 | `{}` | -2.81 |
| 2024-07-18 → 2024-08-14 | `{}` | -4.41 |
| 2024-08-15 → 2024-09-11 | `{}` | -2.92 |
| 2024-09-12 → 2024-10-09 | `{}` | -0.89 |
| 2024-10-10 → 2024-11-06 | `{}` | 0.94 |
| 2024-11-07 → 2024-12-06 | `{}` | 0.94 |
| 2024-12-09 → 2025-01-09 | `{}` | -0.65 |
| 2025-01-10 → 2025-02-06 | `{}` | -1.55 |
| 2025-02-07 → 2025-03-10 | `{}` | -2.57 |
| 2025-03-11 → 2025-04-07 | `{}` | -2.59 |
| 2025-04-08 → 2025-05-08 | `{}` | -1.71 |
| 2025-05-09 → 2025-06-05 | `{}` | -1.18 |
| 2025-06-06 → 2025-07-04 | `{}` | 0.98 |
| 2025-07-07 → 2025-08-01 | `{}` | 0.82 |
| 2025-08-04 → 2025-08-29 | `{}` | 0.58 |
| 2025-09-01 → 2025-09-26 | `{}` | -0.25 |
| 2025-09-29 → 2025-10-24 | `{}` | -0.92 |
| 2025-10-27 → 2025-11-24 | `{}` | 1.12 |
| 2025-11-25 → 2025-12-22 | `{}` | -1.02 |
| 2025-12-23 → 2026-01-23 | `{}` | -1.71 |
| 2026-01-26 → 2026-02-05 | `{}` | -2.43 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{}` | -1.27 | 396 | -9.6% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. A replicação pré-registrada (n = 1 no WDO_N_M5, regra da 007 intacta) falha em todos os gates, exceto look-ahead e número de trades. Sharpe OOS de −1,17, DSR de 3,3%, todos os anos negativos e P&L **bruto** negativo. Pelo critério 5 da hipótese, o efeito é **específico do WIN**.

Conferência do código: o módulo implementa a regra da hipótese. O `adr` usa `shift(1)` sobre pregões, `max_m`/`min_m` vão até a barra 10:25 inclusive, a decisão sai no fechamento da 10:25 e a execução na abertura da 10:30, e nenhuma estatística usa a série inteira. Não achei look-ahead.

Números da amostra de pesquisa inteira (backtest direto, 05/04/2023 a 05/02/2026, 396 trades, sem holdout):

| Item | Previsto (hipótese) | Realizado |
|---|---|---|
| Saídas fechamento / stop / alvo | ~41 / 30 / 29% | 41,7 / 35,1 / 23,2% (165 / 139 / 92) |
| `stop_both` | — | 0 |
| Acerto | 53 a 56% se generalizar; p* ≈ 45% | **44,7%** (abaixo do p*) |
| P&L líquido | — | −R$ 9.548 (média de −R$ 24,1 por trade) |
| P&L bruto (custo zero) | — | **−R$ 4.638**, Sharpe −0,62 |
| Custos | ~4,7% do stop | R$ 4.910 (R$ 12,40 por trade) |
| Maior perda | ≤ R$ 916 | R$ 527,2 (stop de 51,5 pts, 07/11/2024), igual ao projetado |

Por tipo de saída: stop, 139 trades com média de −R$ 237,5 (−R$ 33.014); alvo, 92 com +R$ 230,5 (+R$ 21.207); fechamento, 165 com +R$ 13,7 (+R$ 2.259). O alvo bate em menos dias do que o stop, e a ida até o fechamento quase não rende.

Critérios prévios:
1. **2024 e 2025 positivos? Falhou.** Média por trade de −R$ 17,5 em 2024 (149 trades, 48% de acerto) e de −R$ 23,7 em 2025 (134 trades, 45%). 2023 dá −R$ 33,6 e 2026 dá −R$ 31,0. O Sharpe OOS por ano é negativo em todos: −1,79, −0,88, −1,22 e −1,81.
2. **Sem os 10 e sem os 20 maiores? Falhou**, e o resultado já é negativo com eles: −R$ 14.449 sem os 10 maiores e −R$ 18.676 sem os 20. Não há cauda que salve.
3. **Bracket vs. mesma entrada sem stop/alvo:** o Sharpe diário simples vai de −1,27 com bracket para −0,49 sem ele (P&L de −R$ 5.375 e acerto de 46,5%). **O bracket piora o Sharpe em 0,78, acima do limite de 0,3**, e isso fica registrado. Sem bracket, 2024 fica levemente positivo (+R$ 12 por trade) e 2025 fica negativo (−R$ 11,8): também não passa no critério 1.
4. **Correlação diária com a 007 em WIN** (backtest direto do WIN, sem validate): 0,08 em todos os dias e 0,13 nos 220 dias com trade nos dois. O lado é o mesmo em só 23% dos dias em comum, o que é coerente com a correlação negativa entre Ibovespa e dólar. Diversificaria, mas não há o que diversificar.
5. **Leitura da replicação:** Sharpe OOS de −1,17 ≤ 0, então o **efeito é específico do WIN**. Pelo pré-registro, isso tem que constar como ressalva no relatório da 007.

### Pontos fortes
- O teste é limpo: regra congelada, 1 combinação, dataset sem tentativas anteriores e nenhuma frequência de saída medida antes. É exatamente o tipo de teste que pode derrubar uma hipótese, e derrubou.
- A execução é fiel ao projetado. Em 139 stops, a perda realizada é igual à distância do stop mais R$ 12,40, sem nenhum gap além do stop, e `stop_both` = 0. A maior perda (R$ 527, 0,53% de R$ 100 mil) ficou abaixo do pior caso projetado (R$ 916). O stop do WDO não está "no ruído" no sentido do motor.

### Pontos fracos e riscos
- **Não há borda nem antes dos custos.** O bruto é negativo (Sharpe −0,62 sem custo), então o problema não é o custo 3x maior em relação ao stop. Os custos só aprofundam a perda (de −0,62 para −1,27).
- O acerto (44,7%) fica abaixo do p* (~45%), como previa o item 1 de "Por que pode falhar" (intervenções do BC e fade das excursões).
- Stops curtos (< 15 pts, 58 sinais): acerto de 33%, 64% saem no stop e média de −R$ 14 por trade. Os stops ≥ 15 pts dão média pior (−R$ 25,8), então o ponto de atenção do estrategista não explica a perda. A regra perde nos dois grupos.
- Risco para capital limitado: maior sequência de 9 perdas seguidas (−R$ 1.624, 1,6% do capital), pior dia de −R$ 527 e drawdown de −R$ 9.578 (−9,6%) desde o pico de 05/06/2023. **A estratégia fica 665 pregões debaixo d'água e não se recupera até o fim da amostra.**
- Seleção: a regra foi a melhor de ~56 tentativas efetivas em WIN. O DSR do WDO com n = 1 é honesto para este dataset, mas a escolha da regra veio de um processo de busca no outro mercado. Quando uma regra escolhida assim falha num mercado novo, isso é o que se espera se boa parte do Sharpe de 1,34 da 007 vier de seleção, e não de efeito estrutural. Esta falha **enfraquece a 007**: o efeito não generaliza, e a 007 já dependia de cauda (negativa sem os 20 maiores).

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Não inverter a regra no WDO** ("fade da excursão"). Seria uma tentativa escolhida pelo resultado desta. O bruto invertido seria no máximo ~+0,6 de Sharpe antes dos custos, e o bracket não é simétrico. Se for proposto, tem de ser registrado como tentativa nova, com argumento econômico próprio (intervenção do BC) e escrito antes de qualquer conta.
2. **Rebaixar a 007** e anotar a ressalva no relatório dela: o efeito não replica fora do WIN e depende de cauda. Antes de qualquer holdout, a 007 precisaria de outra replicação limpa: WIN em outro timeframe com a mesma regra em horas, ou o mesmo ativo em outro período fora dos ~56 testes.
3. Se a família "excursão da manhã" continuar, tratar índice e dólar como mercados com microestrutura diferente. Nada do WIN deve ser reaproveitado no WDO sem uma hipótese própria.

Observação sobre o relatório (não é bug do motor): "Custos / lucro bruto = 127%" não tem leitura útil quando o bruto é negativo. Sugiro mostrar "n/a" nesse caso em `research/report.py`.
