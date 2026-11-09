# skill_orb em WDO_N_M5

**Veredito automático: REJECTED**  
day-trader-skill ORB ported to B3: 15-min range, long on close above, stop at range mid, target in R · day trade · gerado em 2026-11-09T19:13:07

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
| P&L total / custos | R$ -4,484.40 / R$ 5,654.40 |
| Retorno anual acima do CDI | -1.8% |
| Sharpe / Sortino | -0.89 / -1.84 |
| Deflated Sharpe (31 tentativas no dataset) | 0.0% |
| Max drawdown | -5.6% |
| Trades / acerto / payoff | 456 / 45% / 1.04 |
| Profit factor | 0.86 |
| Exposição | 9% das barras |
| Custos / lucro bruto | 483% |
| Sharpe com custos 2x | -2.00 |

Sharpe por ano: 2023: -0.75, 2024: -0.38, 2025: -1.68, 2026: -0.93

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.49 |
| 2023-08-29 → 2023-09-26 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.05 |
| 2023-09-27 → 2023-10-25 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.17 |
| 2023-10-26 → 2023-11-24 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.81 |
| 2023-11-27 → 2023-12-22 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.08 |
| 2023-12-26 → 2024-01-24 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.87 |
| 2024-01-25 → 2024-02-23 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 0.2 |
| 2024-02-26 → 2024-03-22 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 1.02 |
| 2024-03-25 → 2024-04-22 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -2.12 |
| 2024-04-23 → 2024-05-21 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 1.49 |
| 2024-05-22 → 2024-06-19 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 0.62 |
| 2024-06-20 → 2024-07-17 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 1.31 |
| 2024-07-18 → 2024-08-14 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 2.03 |
| 2024-08-15 → 2024-09-11 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 0.55 |
| 2024-09-12 → 2024-10-09 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 0.99 |
| 2024-10-10 → 2024-11-06 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.24 |
| 2024-11-07 → 2024-12-06 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.28 |
| 2024-12-09 → 2025-01-09 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.34 |
| 2025-01-10 → 2025-02-06 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.53 |
| 2025-02-07 → 2025-03-10 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.44 |
| 2025-03-11 → 2025-04-07 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.55 |
| 2025-04-08 → 2025-05-08 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.59 |
| 2025-05-09 → 2025-06-05 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.71 |
| 2025-06-06 → 2025-07-04 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 0.44 |
| 2025-07-07 → 2025-08-01 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 1.05 |
| 2025-08-04 → 2025-08-29 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.58 |
| 2025-09-01 → 2025-09-26 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -3.48 |
| 2025-09-29 → 2025-10-24 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -3.98 |
| 2025-10-27 → 2025-11-24 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -3.89 |
| 2025-11-25 → 2025-12-22 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -3.84 |
| 2025-12-23 → 2026-01-23 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.02 |
| 2026-01-26 → 2026-02-05 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.41 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.8 | 517 | -4.9% |
| `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.2 | 517 | -9.0% |
