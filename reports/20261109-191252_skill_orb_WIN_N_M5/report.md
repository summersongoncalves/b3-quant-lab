# skill_orb em WIN_N_M5

**Veredito automático: REJECTED**  
day-trader-skill ORB ported to B3: 15-min range, long on close above, stop at range mid, target in R · day trade · gerado em 2026-11-09T19:12:52

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
| Período | 2023-07-20 → 2026-02-04 (636 dias) |
| P&L total / custos | R$ -2,914.50 / R$ 1,162.50 |
| Retorno anual acima do CDI | -1.2% |
| Sharpe / Sortino | -0.91 / -2.39 |
| Deflated Sharpe (26 tentativas no dataset) | 0.0% |
| Max drawdown | -4.9% |
| Trades / acerto / payoff | 465 / 38% / 1.42 |
| Profit factor | 0.86 |
| Exposição | 12% das barras |
| Custos / lucro bruto | 66% |
| Sharpe com custos 2x | -1.27 |

Sharpe por ano: 2023: -3.74, 2024: -2.11, 2025: 0.11, 2026: 3.6

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-07-20 → 2023-08-16 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.9 |
| 2023-08-17 → 2023-09-14 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -4.03 |
| 2023-09-15 → 2023-10-13 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -2.58 |
| 2023-10-16 → 2023-11-13 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -3.44 |
| 2023-11-14 → 2023-12-12 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -3.23 |
| 2023-12-13 → 2024-01-12 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.17 |
| 2024-01-15 → 2024-02-09 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.12 |
| 2024-02-14 → 2024-03-12 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -0.73 |
| 2024-03-13 → 2024-04-10 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -2.06 |
| 2024-04-11 → 2024-05-09 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.18 |
| 2024-05-10 → 2024-06-07 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.22 |
| 2024-06-10 → 2024-07-05 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.37 |
| 2024-07-08 → 2024-08-02 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.24 |
| 2024-08-05 → 2024-08-30 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -2.02 |
| 2024-09-02 → 2024-09-27 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.05 |
| 2024-09-30 → 2024-10-25 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.8 |
| 2024-10-28 → 2024-11-26 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.07 |
| 2024-11-27 → 2024-12-26 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.54 |
| 2024-12-27 → 2025-01-27 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -3.64 |
| 2025-01-28 → 2025-02-24 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.81 |
| 2025-02-25 → 2025-03-26 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 0.74 |
| 2025-03-27 → 2025-04-25 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 1.05 |
| 2025-04-28 → 2025-05-26 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.2 |
| 2025-05-27 → 2025-06-24 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -2.63 |
| 2025-06-25 → 2025-07-22 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -4.48 |
| 2025-07-23 → 2025-08-19 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -3.69 |
| 2025-08-20 → 2025-09-16 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -1.17 |
| 2025-09-17 → 2025-10-14 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.18 |
| 2025-10-15 → 2025-11-11 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 0.62 |
| 2025-11-12 → 2025-12-10 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 1.04 |
| 2025-12-11 → 2026-01-13 | `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | 0.27 |
| 2026-01-14 → 2026-02-04 | `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | 2.04 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'range_bars': 3, 'target_r': 1.0, 'no_entry_last_min': 30}` | -1.31 | 526 | -5.9% |
| `{'range_bars': 3, 'target_r': 2.0, 'no_entry_last_min': 30}` | -0.92 | 526 | -5.7% |
