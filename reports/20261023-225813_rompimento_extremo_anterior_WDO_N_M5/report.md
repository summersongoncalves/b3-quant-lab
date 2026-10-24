# rompimento_extremo_anterior em WDO_N_M5

**Veredito automático: PROMISING**  
WDO: first M5 close beyond the previous day's high/low (09:30-12:55); stop back inside the old range, target 1.5x stop · day trade · gerado em 2026-10-23T22:58:13

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
| P&L total / custos | R$ 106.12 / R$ 1,909.60 |
| Retorno anual acima do CDI | 0.0% |
| Sharpe / Sortino | 0.03 / 0.05 |
| Deflated Sharpe (14 tentativas no dataset) | 4.6% |
| Max drawdown | -1.8% |
| Trades / acerto / payoff | 154 / 46% / 1.18 |
| Profit factor | 1.01 |
| Exposição | 7% das barras |
| Custos / lucro bruto | 95% |
| Sharpe com custos 2x | -0.55 |

Sharpe por ano: 2023: -1.61, 2024: 0.53, 2025: 0.5, 2026: -4.69

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | -1.52 |
| 2023-08-29 → 2023-09-26 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | -1.25 |
| 2023-09-27 → 2023-10-25 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | 1.24 |
| 2023-10-26 → 2023-11-24 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 1.26 |
| 2023-11-27 → 2023-12-22 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 1.37 |
| 2023-12-26 → 2024-01-24 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | -1.87 |
| 2024-01-25 → 2024-02-23 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | -1.32 |
| 2024-02-26 → 2024-03-22 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 0.03 |
| 2024-03-25 → 2024-04-22 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 0.93 |
| 2024-04-23 → 2024-05-21 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 0.71 |
| 2024-05-22 → 2024-06-19 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | -1.66 |
| 2024-06-20 → 2024-07-17 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | -0.46 |
| 2024-07-18 → 2024-08-14 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 0.93 |
| 2024-08-15 → 2024-09-11 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 1.31 |
| 2024-09-12 → 2024-10-09 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 0.41 |
| 2024-10-10 → 2024-11-06 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 0.71 |
| 2024-11-07 → 2024-12-06 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | -0.42 |
| 2024-12-09 → 2025-01-09 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 2.86 |
| 2025-01-10 → 2025-02-06 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 2.31 |
| 2025-02-07 → 2025-03-10 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 2.26 |
| 2025-03-11 → 2025-04-07 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | -1.4 |
| 2025-04-08 → 2025-05-08 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | -1.06 |
| 2025-05-09 → 2025-06-05 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | -1.36 |
| 2025-06-06 → 2025-07-04 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 3.05 |
| 2025-07-07 → 2025-08-01 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 2.97 |
| 2025-08-04 → 2025-08-29 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | 3.11 |
| 2025-09-01 → 2025-09-26 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | -1.55 |
| 2025-09-29 → 2025-10-24 | `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | -0.81 |
| 2025-10-27 → 2025-11-24 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | 0.78 |
| 2025-11-25 → 2025-12-22 | `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | 3.87 |
| 2025-12-23 → 2026-01-23 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | 4.0 |
| 2026-01-26 → 2026-02-05 | `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | 1.21 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'b': 0.15, 'k': 1.5, 'over_max': 0.15}` | -0.01 | 173 | -2.0% |
| `{'b': 0.2, 'k': 1.5, 'over_max': 0.15}` | 0.01 | 173 | -2.1% |
| `{'b': 0.25, 'k': 1.5, 'over_max': 0.15}` | -0.06 | 173 | -2.1% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Não. O PROMISING automático só aparece porque o Sharpe OOS (0,03) é estritamente positivo. Seis dos sete gates falham (Sharpe OOS, DSR 4,6%, anos, grade, custos 2x), e o DSR usa 14 tentativas, quando o dataset tem ~25 efetivas. Com 25 o DSR cai ainda mais. Dos 6 critérios prévios da hipótese, 4 falham (2, 3, 4 e 5). O resultado é indistinguível de zero.

Código conferido: implementa a hipótese (PDH/PDL e `adr` com `shift(1)`, rolagem pelo calendário mais exclusão do dia seguinte, filtro 09:00-09:25 só com barras já fechadas, 1º evento na janela, corte de `over`). Não encontrei look-ahead. Detalhe sem efeito prático: o motor aplica as distâncias a partir da abertura de t+1, e não do close do sinal. O desvio abertura−close na entrada tem mediana de 0 e p90 de 0,5 ponto. **Nenhum bug no motor.**

Números da amostra de pesquisa inteira (b = 0,20, 173 trades, backtest direto):
- **Saídas:** stop 84 (49%), alvo 63 (36%), fechamento 26 (15%), stop_both 0. O stop não fica dentro do ruído de uma barra.
- **Critério 4:** acerto entre resolvidos de **42,9%** (63/147). Fica abaixo do p* médio de **43,6%** e não chega aos 45% exigidos (40% + 5 p.p.). O benchmark de lado sorteado (200 sorteios, mesmas distâncias) dá 38,2% ± 3,8 p.p. A estratégia fica ~1,2 desvio acima, e 11% dos sorteios têm P&L ≥ ao real. **Falha.**
- **Direção ou volatilidade:** com alvo = stop (k = 1), +S vem antes de −S em 54,0% dos 163 resolvidos (erro-padrão de ~3,9 p.p., ~1 EP acima de 50%). O lado oposto (Turtle Soup) com a mesma geometria acerta 34,6%, e o lado aleatório 38,2%. Há uma assimetria fraca a favor do rompimento, de ~4 p.p. Ela é pequena demais para pagar os custos e não é estatisticamente distinguível de ruído. O "combustível" medido na descritiva é, na maior parte, volatilidade.
- **Critério 1 (anos):** médio líquido por trade de R$ -27,1 em 2023, +11,9 em 2024, +16,7 em 2025 e -63,5 em 2026 (9 trades). Passa formalmente em 2024 e 2025, mas com R$ 12-17 por trade contra um stop de ~R$ 157. Isso é ruído.
- **Critério 2 (concentração):** total de **R$ +26**. Sem os 10 maiores, **R$ -2.992**. Sem os 20 maiores, **R$ -5.284**. **Falha.**
- **Critério 3 (grade):** Sharpe de -0,01, +0,01 e -0,06 para b = 0,15, 0,20 e 0,25. Só 1 positiva e sinais mistos. **Falha.** O walk-forward pula entre os extremos 0,15 e 0,25 em 26 de 32 janelas.
- **Critério 5 (lado):** vendido 104 trades, R$ +1.576 (acerto resolvido de 48,2%). Comprado 69 trades, R$ -1.550 (35,5%). Todo o lucro vem das vendas de 2024-2025 (R$ +2.301). As compras perdem em todos os anos. É o padrão "lucro de um lado só" que a hipótese pediu para expor. **Falha.**
- **Critério 6 (correlação diária, dias em comum):** com a 008 (`direcao_do_dia`, Sharpe -1,27), ρ = **+0,40** em 91 dias em comum. Com a 012 (`falha_balanco_inicial`, Sharpe -1,86), ρ = **-0,22** em 91 dias. Com o baseline ORB, ρ = +0,23 em 172 dias. A 014 é, em parte, a 008 com outro gatilho e, em parte, o espelho da 012.
- **Custos:** R$ 2.145 de custos contra R$ 2.171 de bruto (**99%**, ou 95% no OOS). Com custos 2x, o Sharpe OOS vai a -0,55.
- **Risco (R$ 100 mil, 1 contrato):** maior perda de R$ 288 (0,29%), exatamente o stop mais custo. Não há gaps além do stop (excesso de R$ 0 em todas as 84 perdas). Maior sequência de 5 perdas (R$ -784). Pior dia de R$ -288. Max DD de R$ -2.125 (-2,1%), com pico em 2023-05-12, vale em 2024-06-05 e **recuperação só em 2025-11-05, ~2,5 anos submerso**.
- **Baseline:** o ORB no mesmo dataset dá Sharpe de -0,35. A 014 "bate" o baseline apenas por estar em zero.
- **Mesma entrada sem bracket** (até o fechamento): Sharpe de 0,46 in-sample, R$ +3.420, acerto de 50,3% e Sharpe de 0,17 com custos 2x. Mas cai a **R$ -5.366 sem os 10 maiores** (top 5: R$ 1.448, 1.243, 1.163, 828 e 758) e a R$ -9.427 sem os 20. 2023 dá R$ -1.268 e 2024-2025 dão R$ +4.710. É cauda de poucos dias de tendência, não vantagem por trade. O bracket corta exatamente essa cauda, o que explica o resultado nulo da versão com bracket.
- **Amostra:** 173 trades (154 OOS) e só 9 em 2026. Com ~150 resolvidos, o erro-padrão do acerto é de ~4 p.p., o mesmo tamanho da folga exigida sobre o aleatório. Mesmo um acerto de 45% não seria distinguível de 40% com folga. Um P&L médio de R$ 0,15 por trade, com desvio de ~R$ 175, exigiria milhares de trades para ser detectado. A amostra limita a inferência a "não há efeito grande". Um efeito pequeno não pode ser descartado nem confirmado.

### Pontos fortes
- Implementação limpa, sem look-ahead, e risco por trade bem definido: perda máxima de 0,29% do capital, sem gap além do stop e com 0 stop_both.
- A geometria se resolve dentro do pregão (85% das saídas em stop ou alvo).
- Há uma assimetria descritiva fraca a favor do rompimento (54% em k = 1, contra 34,6% do lado oposto), coerente, em sinal, com a cascata de stops.

### Pontos fracos e riscos
- Acerto abaixo de p*, e P&L de R$ +26 em 173 trades: os custos comem 99% do bruto.
- Lucro todo nas vendas de 2024-2025. As compras perdem sempre. Isso é viés do período (o dólar caiu em 2025), não efeito do nível.
- Some sem os 10 maiores trades, com ou sem bracket.
- Drawdown de ~2,5 anos para recuperar, inaceitável para capital próprio.
- ρ = +0,40 com a 008, que é rejeitada: a informação é parcialmente redundante.
- Com ~25 tentativas efetivas em WDO_N_M5, um Sharpe de 0,03 está completamente dentro do esperado pelo acaso.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Parar com os níveis intradiários e diários do WDO em M5 como gatilho de direção.** 008, 009, 012, 013 e 014 deram acerto no nível do lado aleatório. O dataset já tem ~26 tentativas, e qualquer nova variante aqui precisa de um Sharpe muito alto para passar no DSR.
- Não refinar a versão sem bracket: o Sharpe de 0,46 vem de 5 a 10 dias de tendência. Escolhê-la agora seria data-snooping (contaria como mais uma tentativa) e ela não sobrevive sem os maiores trades.
- Se quiser explorar a assimetria de ~4 p.p., faça só descritivamente e num dataset diferente (por exemplo, o DOL cheio ou o WDO em M15 ou M1, se existirem), com um teste pré-registrado de "+S antes de −S" sem P&L. Uma vantagem que pague custos exige ~8-10 p.p. com esta geometria.
- Trocar de família: o dólar em M5 parece ter informação mais na volatilidade (quando há movimento) que na direção. Hipóteses que lucrem com volatilidade sem lado não cabem no motor de futuros direcional. Isso vale registrar como conclusão do ciclo WDO.
