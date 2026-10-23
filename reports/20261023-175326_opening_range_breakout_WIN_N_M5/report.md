# opening_range_breakout em WIN_N_M5

**Veredito automático: PROMISING**  
Opening range breakout, flat at the close (baseline day trade) · day trade · gerado em 2026-10-23T17:53:26

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ✅ Sharpe fora da amostra >= mínimo
- ✅ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ✅ Maioria dos anos positiva
- ✅ Maioria dos parâmetros vizinhos positiva
- ✅ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-07-20 → 2026-02-04 (636 dias) |
| P&L total / custos | R$ 8,802.50 / R$ 1,442.50 |
| Retorno anual acima do CDI | 3.5% |
| Sharpe / Sortino | 1.07 / 1.47 |
| Deflated Sharpe (9 tentativas no dataset) | 83.5% |
| Max drawdown | -4.0% |
| Trades / acerto / payoff | 577 / 55% / 1.01 |
| Profit factor | 1.21 |
| Exposição | 79% das barras |
| Custos / lucro bruto | 14% |
| Sharpe com custos 2x | 0.90 |

Sharpe por ano: 2023: 0.78, 2024: 1.23, 2025: 0.27, 2026: 7.17

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-07-20 → 2023-08-16 | `{'range_bars': 12, 'last_entry': '11:00'}` | -1.63 |
| 2023-08-17 → 2023-09-14 | `{'range_bars': 3, 'last_entry': '11:00'}` | -1.6 |
| 2023-09-15 → 2023-10-13 | `{'range_bars': 12, 'last_entry': '11:00'}` | 0.08 |
| 2023-10-16 → 2023-11-13 | `{'range_bars': 12, 'last_entry': '12:00'}` | 0.32 |
| 2023-11-14 → 2023-12-12 | `{'range_bars': 3, 'last_entry': '11:00'}` | 1.74 |
| 2023-12-13 → 2024-01-12 | `{'range_bars': 12, 'last_entry': '11:00'}` | 1.96 |
| 2024-01-15 → 2024-02-09 | `{'range_bars': 12, 'last_entry': '11:00'}` | 2.5 |
| 2024-02-14 → 2024-03-12 | `{'range_bars': 6, 'last_entry': '11:00'}` | 3.43 |
| 2024-03-13 → 2024-04-10 | `{'range_bars': 12, 'last_entry': '11:00'}` | 2.89 |
| 2024-04-11 → 2024-05-09 | `{'range_bars': 12, 'last_entry': '11:00'}` | 2.66 |
| 2024-05-10 → 2024-06-07 | `{'range_bars': 6, 'last_entry': '11:00'}` | 1.9 |
| 2024-06-10 → 2024-07-05 | `{'range_bars': 12, 'last_entry': '14:00'}` | 2.12 |
| 2024-07-08 → 2024-08-02 | `{'range_bars': 12, 'last_entry': '14:00'}` | 1.04 |
| 2024-08-05 → 2024-08-30 | `{'range_bars': 12, 'last_entry': '14:00'}` | -1.18 |
| 2024-09-02 → 2024-09-27 | `{'range_bars': 12, 'last_entry': '14:00'}` | 0.59 |
| 2024-09-30 → 2024-10-25 | `{'range_bars': 12, 'last_entry': '11:00'}` | 1.1 |
| 2024-10-28 → 2024-11-26 | `{'range_bars': 12, 'last_entry': '11:00'}` | 0.9 |
| 2024-11-27 → 2024-12-26 | `{'range_bars': 12, 'last_entry': '11:00'}` | 2.12 |
| 2024-12-27 → 2025-01-27 | `{'range_bars': 12, 'last_entry': '12:00'}` | 3.69 |
| 2025-01-28 → 2025-02-24 | `{'range_bars': 12, 'last_entry': '12:00'}` | 2.64 |
| 2025-02-25 → 2025-03-26 | `{'range_bars': 12, 'last_entry': '12:00'}` | 4.29 |
| 2025-03-27 → 2025-04-25 | `{'range_bars': 12, 'last_entry': '12:00'}` | 4.8 |
| 2025-04-28 → 2025-05-26 | `{'range_bars': 3, 'last_entry': '12:00'}` | 2.07 |
| 2025-05-27 → 2025-06-24 | `{'range_bars': 3, 'last_entry': '12:00'}` | 2.52 |
| 2025-06-25 → 2025-07-22 | `{'range_bars': 3, 'last_entry': '12:00'}` | 2.29 |
| 2025-07-23 → 2025-08-19 | `{'range_bars': 6, 'last_entry': '11:00'}` | 3.52 |
| 2025-08-20 → 2025-09-16 | `{'range_bars': 6, 'last_entry': '11:00'}` | 3.61 |
| 2025-09-17 → 2025-10-14 | `{'range_bars': 6, 'last_entry': '11:00'}` | 4.04 |
| 2025-10-15 → 2025-11-11 | `{'range_bars': 12, 'last_entry': '11:00'}` | 4.52 |
| 2025-11-12 → 2025-12-10 | `{'range_bars': 12, 'last_entry': '11:00'}` | 0.66 |
| 2025-12-11 → 2026-01-13 | `{'range_bars': 6, 'last_entry': '11:00'}` | -1.11 |
| 2026-01-14 → 2026-02-04 | `{'range_bars': 6, 'last_entry': '14:00'}` | -1.23 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'range_bars': 3, 'last_entry': '11:00'}` | 0.44 | 697 | -4.9% |
| `{'range_bars': 3, 'last_entry': '12:00'}` | 0.34 | 708 | -5.0% |
| `{'range_bars': 3, 'last_entry': '14:00'}` | 0.39 | 714 | -4.8% |
| `{'range_bars': 6, 'last_entry': '11:00'}` | 0.97 | 665 | -5.1% |
| `{'range_bars': 6, 'last_entry': '12:00'}` | 0.87 | 695 | -5.2% |
| `{'range_bars': 6, 'last_entry': '14:00'}` | 0.86 | 708 | -5.8% |
| `{'range_bars': 12, 'last_entry': '11:00'}` | 1.15 | 594 | -3.7% |
| `{'range_bars': 12, 'last_entry': '12:00'}` | 1.02 | 661 | -3.6% |
| `{'range_bars': 12, 'last_entry': '14:00'}` | 0.87 | 691 | -3.8% |
