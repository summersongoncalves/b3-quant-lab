# momentum_vwap_volume em BBAS3_M5

**Veredito automático: PROMISING**  
Intraday momentum from the open confirmed by daily VWAP and relative volume, flat at the close · day trade · gerado em 2026-10-23T19:53:14

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
| P&L total / custos | R$ 4,561.50 / R$ 13,599.93 |
| Retorno anual acima do CDI | 0.4% |
| Sharpe / Sortino | 0.07 / 0.04 |
| Deflated Sharpe (9 tentativas no dataset) | 15.6% |
| Max drawdown | -7.7% |
| Trades / acerto / payoff | 103 / 44% / 1.46 |
| Profit factor | 1.14 |
| Exposição | 10% das barras |
| Custos / lucro bruto | 75% |
| Sharpe com custos 2x | -0.72 |

Sharpe por ano: 2023: 0.25, 2024: -0.53, 2025: 0.29, 2026: 0.0

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-04-28 → 2023-05-26 | `{'signal_time': '12:00', 'k': 2.0}` | 1.4 |
| 2023-05-29 → 2023-06-26 | `{'signal_time': '12:00', 'k': 2.0}` | 2.04 |
| 2023-06-27 → 2023-07-24 | `{'signal_time': '13:00', 'k': 1.5}` | 1.86 |
| 2023-07-25 → 2023-08-21 | `{'signal_time': '14:00', 'k': 2.0}` | 2.01 |
| 2023-08-22 → 2023-09-19 | `{'signal_time': '14:00', 'k': 2.0}` | 0.31 |
| 2023-09-20 → 2023-10-18 | `{'signal_time': '12:00', 'k': 1.0}` | -2.27 |
| 2023-10-19 → 2023-11-17 | `{'signal_time': '12:00', 'k': 2.0}` | 1.22 |
| 2023-11-20 → 2023-12-15 | `{'signal_time': '13:00', 'k': 2.0}` | 3.58 |
| 2023-12-18 → 2024-01-17 | `{'signal_time': '14:00', 'k': 2.0}` | 3.6 |
| 2024-01-18 → 2024-02-16 | `{'signal_time': '12:00', 'k': 1.5}` | 3.0 |
| 2024-02-19 → 2024-03-15 | `{'signal_time': '12:00', 'k': 1.5}` | 2.89 |
| 2024-03-18 → 2024-04-15 | `{'signal_time': '14:00', 'k': 1.0}` | 1.01 |
| 2024-04-16 → 2024-05-14 | `{'signal_time': '14:00', 'k': 2.0}` | -1.12 |
| 2024-05-15 → 2024-06-12 | `{'signal_time': '14:00', 'k': 2.0}` | -2.73 |
| 2024-06-13 → 2024-07-10 | `{'signal_time': '12:00', 'k': 2.0}` | -0.92 |
| 2024-07-11 → 2024-08-07 | `{'signal_time': '12:00', 'k': 1.0}` | 0.97 |
| 2024-08-08 → 2024-09-04 | `{'signal_time': '12:00', 'k': 2.0}` | 1.73 |
| 2024-09-05 → 2024-10-02 | `{'signal_time': '12:00', 'k': 2.0}` | 2.22 |
| 2024-10-03 → 2024-10-30 | `{'signal_time': '12:00', 'k': 2.0}` | 4.0 |
| 2024-10-31 → 2024-11-29 | `{'signal_time': '12:00', 'k': 2.0}` | 3.54 |
| 2024-12-02 → 2025-01-02 | `{'signal_time': '13:00', 'k': 2.0}` | 1.33 |
| 2025-01-03 → 2025-01-30 | `{'signal_time': '12:00', 'k': 2.0}` | 1.41 |
| 2025-01-31 → 2025-02-27 | `{'signal_time': '12:00', 'k': 2.0}` | 1.8 |
| 2025-02-28 → 2025-03-31 | `{'signal_time': '12:00', 'k': 1.5}` | 2.13 |
| 2025-04-01 → 2025-04-30 | `{'signal_time': '12:00', 'k': 2.0}` | 1.29 |
| 2025-05-02 → 2025-05-29 | `{'signal_time': '14:00', 'k': 2.0}` | -0.67 |
| 2025-05-30 → 2025-06-27 | `{'signal_time': '14:00', 'k': 1.5}` | -0.55 |
| 2025-06-30 → 2025-07-25 | `{'signal_time': '13:00', 'k': 2.0}` | 2.42 |
| 2025-07-28 → 2025-08-22 | `{'signal_time': '12:00', 'k': 1.0}` | 1.28 |
| 2025-08-25 → 2025-09-19 | `{'signal_time': '13:00', 'k': 2.0}` | 1.84 |
| 2025-09-22 → 2025-10-17 | `{'signal_time': '13:00', 'k': 2.0}` | 1.54 |
| 2025-10-20 → 2025-11-14 | `{'signal_time': '13:00', 'k': 2.0}` | 2.7 |
| 2025-11-17 → 2025-12-15 | `{'signal_time': '14:00', 'k': 2.0}` | -1.43 |
| 2025-12-16 → 2026-01-16 | `{'signal_time': '14:00', 'k': 2.0}` | 1.07 |
| 2026-01-19 → 2026-01-19 | `{'signal_time': '14:00', 'k': 2.0}` | 0.81 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'signal_time': '12:00', 'k': 1.0}` | -0.09 | 186 | -6.9% |
| `{'signal_time': '12:00', 'k': 1.5}` | 0.25 | 150 | -5.8% |
| `{'signal_time': '12:00', 'k': 2.0}` | 0.34 | 95 | -7.1% |
| `{'signal_time': '13:00', 'k': 1.0}` | -0.94 | 179 | -17.7% |
| `{'signal_time': '13:00', 'k': 1.5}` | -0.56 | 127 | -12.4% |
| `{'signal_time': '13:00', 'k': 2.0}` | -0.19 | 86 | -8.1% |
| `{'signal_time': '14:00', 'k': 1.0}` | -0.62 | 177 | -15.7% |
| `{'signal_time': '14:00', 'k': 1.5}` | -0.17 | 136 | -9.9% |
| `{'signal_time': '14:00', 'k': 2.0}` | 0.28 | 102 | -8.0% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Não. O PROMISING automático só aparece porque o Sharpe OOS é maior que zero (0,07). Seis dos sete critérios substantivos falham, e o lucro OOS inteiro depende de um único trade. Sou mais rígido aqui: não há o que promover.

### Revisão do código
- O código segue a hipótese: sinal na barra rotulada `signal_time − 5 min`, `escala` = mediana dos 20 `|mov|` anteriores com `shift(1)`, VWAP diária e `rv` causais, 1 entrada por dia e posição mantida até o motor zerar no fechamento. O look-ahead check passou e eu não achei look-ahead manual. A VWAP usa o `high`/`low` da barra de sinal, mas eles já são conhecidos no fechamento dela.
- Há uma divergência pequena com a hipótese. O filtro "primeira barra até 10:05" também descarta 11 dias que abrem às 10:10, e a hipótese só cita os 3 dias de 13:00 e o de 10:15. São 15 dias excluídos, e não 4. O efeito no resultado é desprezível.
- Para os horários de 13h e 14h, a `escala` inclui os 3 dias que abriram às 13:00, com `mov` de apenas 1 hora. O efeito também é desprezível.
- Motor: não achei bug. Observação menor: o último fold do walk-forward tem só 1 dia (2026-01-19).

### Pontos fortes
- Não há look-ahead, e o código é limpo e fiel à hipótese.
- O drawdown OOS é contido (−7,7%) porque a exposição é baixa (10% das barras).
- Fica muito acima do baseline `opening_range_breakout` (parâmetros padrão) em BBAS3 M5 no mesmo período OOS: Sharpe −1,77, 515 trades, R$ −40,7 mil e DD −49%. Esse baseline, porém, é fraco nesse ativo e não serve de referência exigente. Rodei a comparação em memória, sem `validate`, para não inflar o registro de BBAS3.
- O sinal de 12h tem bruto consistente na amostra inteira: 16 a 23 bp por trade para k = 1,0 a 2,0.

### Pontos fracos e riscos
- **Sem vantagem líquida.** O Sharpe OOS é 0,07, e o PSR contra zero é de só 54%. O bruto OOS dá 17,6 bp por trade, e o custo come 13,2 bp, ou 75% do bruto. Com custos 2x, o Sharpe vai a −0,72 (R$ −9,0 mil).
- **DSR.** Fica em 15,6% com as 9 tentativas registradas. Somando as ~75 variações escondidas (84 no total), cai para **4,4%**. O mínimo é 95%.
- **Concentração extrema.** O lucro líquido OOS é R$ 4.562. O maior trade sozinho (2025-12-05, vendido às 14h) rendeu R$ 5.092: sem ele, o OOS fica negativo (R$ −531). Sem os 5 maiores, fica em R$ −10.351. A assimetria (101 trades com resultado médio negativo e uma cauda que paga tudo) também aparece na curtose diária de 57,6 e no skew de 2,9.
- **Parâmetros instáveis.** O walk-forward pula entre os 3 horários (12h em 18 folds, 13h em 7, 14h em 10) e usa k = 1,0, 1,5 e 2,0. No OOS por horário de entrada, as janelas de 12h somaram R$ +11,8 mil, as de 13h R$ −8,1 mil e as de 14h R$ +0,8 mil. O seletor escolhe 13h por ruído de treino e perde.
- **Grade frágil.** Só 3 das 9 combinações têm Sharpe > 0 na amostra inteira (12h/k=1,5: 0,25; 12h/k=2,0: 0,34; 14h/k=2,0: 0,28), e as de 13h são todas negativas. Mesmo essas 3 vêm de uma grade que o estrategista viu antes, então o número é otimista.
- **Regime.** O Sharpe OOS por ano é 2023: 0,25, 2024: −0,53, 2025: 0,29. Com parâmetros fixos, as combinações de 12h perdem em 2025 (k=2,0: R$ −2,3 mil; k=1,5: ≈0), e o ganho vem de 2023–2024. Isso confirma o que a própria hipótese suspeitava: a 12h é um efeito de 2023, não um padrão estável.
- **Execução.** A liquidez não é problema: a barra de entrada movimenta em mediana R$ 4,3 milhões, contra R$ 100 mil de posição. A saída no fechamento depende do leilão de fechamento, e o custo modelado (1 tick + emolumentos ≈ 14 bp ida e volta) é otimista para quem não usa ordem a mercado no leilão. O custo real tende a ser maior, o que piora um quadro que já é negativo com 2x.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Pare de minerar BBAS3 com essa família.** Com 84 tentativas efetivas e DSR de 4,4%, qualquer nova variação aqui parte com desvantagem. O momentum intradiário não se transfere para uma ação com custo proporcional de ~14 bp.
2. Se quiser testar a ideia de forma independente, **fixe a regra antes** (12h, k = 1,5, VWAP + rv, sem grade) e rode-a numa cesta de ações líquidas de tick relativo menor ou preço maior (ex.: VALE3, ITUB4, PETR4). O critério de sucesso deve ser o bruto por trade acima de 2x o custo em cada ativo e em cada ano, não o Sharpe agregado.
3. Para atacar o custo, que é o problema central, só faz sentido voltar ao tema em instrumento de custo proporcional baixo (WIN/WDO). Ali, a pergunta útil é se os filtros de VWAP e volume melhoram a 001 fora da amostra, com registro.
4. Qualquer versão nova precisa reportar o resultado sem os 5 maiores trades. Se ele ficar negativo, a estratégia deve ser descartada.
