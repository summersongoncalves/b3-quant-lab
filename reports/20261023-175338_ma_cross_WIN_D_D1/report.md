# ma_cross em WIN_D_D1

**Veredito automático: REJECTED**  
Moving average crossover (baseline swing) · swing · gerado em 2026-10-23T17:53:38

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ❌ Sharpe fora da amostra >= mínimo
- ❌ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ✅ Maioria dos anos positiva
- ❌ Maioria dos parâmetros vizinhos positiva
- ✅ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-10-31 → 2025-10-21 (494 dias) |
| P&L total / custos | R$ 18.95 / R$ 13.05 |
| Retorno anual acima do CDI | 0.0% |
| Sharpe / Sortino | 0.00 / 0.00 |
| Deflated Sharpe (9 tentativas no dataset) | 37.3% |
| Max drawdown | -3.7% |
| Trades / acerto / payoff | 5 / 20% / 4.05 |
| Profit factor | 1.01 |
| Exposição | 49% das barras |
| Custos / lucro bruto | 41% |
| Sharpe com custos 2x | 0.00 |

Sharpe por ano: 2023: 3.59, 2024: -1.25, 2025: 0.48

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-10-31 → 2024-02-01 | `{'fast': 10, 'slow': 100, 'allow_short': False}` | -0.48 |
| 2024-02-02 → 2024-05-06 | `{'fast': 10, 'slow': 100, 'allow_short': False}` | -0.15 |
| 2024-05-07 → 2024-08-02 | `{'fast': 10, 'slow': 100, 'allow_short': False}` | -0.16 |
| 2024-08-05 → 2024-10-30 | `{'fast': 10, 'slow': 100, 'allow_short': False}` | -0.01 |
| 2024-10-31 → 2025-02-04 | `{'fast': 10, 'slow': 100, 'allow_short': False}` | -0.17 |
| 2025-02-05 → 2025-05-09 | `{'fast': 10, 'slow': 200, 'allow_short': False}` | -0.4 |
| 2025-05-12 → 2025-08-07 | `{'fast': 20, 'slow': 100, 'allow_short': False}` | -0.31 |
| 2025-08-08 → 2025-10-21 | `{'fast': 10, 'slow': 200, 'allow_short': False}` | -0.38 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'fast': 10, 'slow': 100, 'allow_short': False}` | -0.31 | 9 | -6.7% |
| `{'fast': 10, 'slow': 150, 'allow_short': False}` | -0.38 | 8 | -6.1% |
| `{'fast': 10, 'slow': 200, 'allow_short': False}` | -0.35 | 7 | -5.7% |
| `{'fast': 20, 'slow': 100, 'allow_short': False}` | -0.4 | 7 | -8.2% |
| `{'fast': 20, 'slow': 150, 'allow_short': False}` | -0.27 | 5 | -6.2% |
| `{'fast': 20, 'slow': 200, 'allow_short': False}` | -0.62 | 6 | -8.7% |
| `{'fast': 50, 'slow': 100, 'allow_short': False}` | -0.51 | 7 | -10.5% |
| `{'fast': 50, 'slow': 150, 'allow_short': False}` | -0.64 | 6 | -9.9% |
| `{'fast': 50, 'slow': 200, 'allow_short': False}` | -0.19 | 4 | -5.2% |
