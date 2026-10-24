# direcao_do_dia em WIN_N_M5

**Veredito automático: PROMISING**  
Follow the morning excursion (>= 0.3 ADR from the open, one side) at 10:30; stop at open -/+ 0.1 ADR, target at open +/- 1 ADR · day trade · gerado em 2026-10-23T21:34:18

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
| P&L total / custos | R$ 5,670.20 / R$ 845.00 |
| Retorno anual acima do CDI | 2.2% |
| Sharpe / Sortino | 1.34 / 2.19 |
| Deflated Sharpe (22 tentativas no dataset) | 86.8% |
| Max drawdown | -1.2% |
| Trades / acerto / payoff | 338 / 56% / 1.02 |
| Profit factor | 1.31 |
| Exposição | 26% das barras |
| Custos / lucro bruto | 13% |
| Sharpe com custos 2x | 1.14 |

Sharpe por ano: 2023: 0.51, 2024: 1.26, 2025: 1.53, 2026: 2.92

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-07-20 → 2023-08-16 | `{}` | -2.48 |
| 2023-08-17 → 2023-09-14 | `{}` | -0.99 |
| 2023-09-15 → 2023-10-13 | `{}` | 1.66 |
| 2023-10-16 → 2023-11-13 | `{}` | 1.36 |
| 2023-11-14 → 2023-12-12 | `{}` | 2.75 |
| 2023-12-13 → 2024-01-12 | `{}` | -0.33 |
| 2024-01-15 → 2024-02-09 | `{}` | -0.57 |
| 2024-02-14 → 2024-03-12 | `{}` | 0.5 |
| 2024-03-13 → 2024-04-10 | `{}` | 2.84 |
| 2024-04-11 → 2024-05-09 | `{}` | 3.96 |
| 2024-05-10 → 2024-06-07 | `{}` | -0.06 |
| 2024-06-10 → 2024-07-05 | `{}` | -0.53 |
| 2024-07-08 → 2024-08-02 | `{}` | -1.21 |
| 2024-08-05 → 2024-08-30 | `{}` | -0.32 |
| 2024-09-02 → 2024-09-27 | `{}` | 0.17 |
| 2024-09-30 → 2024-10-25 | `{}` | -0.38 |
| 2024-10-28 → 2024-11-26 | `{}` | -0.34 |
| 2024-11-27 → 2024-12-26 | `{}` | 0.92 |
| 2024-12-27 → 2025-01-27 | `{}` | 2.78 |
| 2025-01-28 → 2025-02-24 | `{}` | 2.96 |
| 2025-02-25 → 2025-03-26 | `{}` | 0.48 |
| 2025-03-27 → 2025-04-25 | `{}` | 0.61 |
| 2025-04-28 → 2025-05-26 | `{}` | 2.26 |
| 2025-05-27 → 2025-06-24 | `{}` | 3.94 |
| 2025-06-25 → 2025-07-22 | `{}` | 2.99 |
| 2025-07-23 → 2025-08-19 | `{}` | 2.86 |
| 2025-08-20 → 2025-09-16 | `{}` | 0.99 |
| 2025-09-17 → 2025-10-14 | `{}` | 1.35 |
| 2025-10-15 → 2025-11-11 | `{}` | 0.66 |
| 2025-11-12 → 2025-12-10 | `{}` | -0.37 |
| 2025-12-11 → 2026-01-13 | `{}` | -0.51 |
| 2026-01-14 → 2026-02-04 | `{}` | -0.02 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{}` | 0.95 | 370 | -1.4% |

## Análise do validador
**Veredito final:** PROMISSORA

**Concorda com o veredito automático?** Sim, e por dois motivos independentes. (a) O DSR falha: 86,8% com as 22 tentativas do registro e **82,1% com as ~56 tentativas efetivas** declaradas na hipótese. O Sharpe OOS exigido para DSR ≥ 95% é 1,67 (n = 22) ou **1,79 (n = 56)**, e o OOS deu 1,34. (b) Um critério prévio da própria hipótese falha: **sem os 20 maiores trades o resultado fica em −R$ 81**. Não há motivo para ser mais frouxo. Também não rejeito: o efeito existe nos três anos, o stop quase não custa nada, e a correlação com a 001 é baixa.

Conferência do código: implementa a hipótese. O `adr` usa `shift(1)` sobre os ranges diários, `max_m`/`min_m` vão até a barra 10:25 inclusive, e a decisão sai no fechamento dela (10:30). As distâncias de stop e alvo são medidas do `close` das 10:25, como dizem as Notas de implementação: stop mediano de 825 pts (p90 1.372, máx. 2.855) e alvo mediano de 1.107 pts, batendo com as descritivas (830 / 1.410 / 2.850 / 1.110). As 338 entradas são todas às 10:30, no máximo 1 por dia, sem reentrada depois do stop. Não achei look-ahead e não achei bug no motor. Um detalhe sem efeito prático: os dias com abertura depois de 09:30 entram no cálculo do `adr`, o que puxa o `adr` um pouco para baixo.

### Critérios prévios da hipótese
| # | Critério | Resultado | Passa? |
|---|---|---|---|
| 1 | Líquido médio por trade > 0 em 2024 e em 2025 | 2024: +R$ 13,20 (132 trades); 2025: +R$ 20,19 (141) | sim |
| 2 | Positiva sem os 10 e sem os 20 maiores | total R$ 5.670; sem top 5: R$ 3.953; sem top 10: R$ 2.457; **sem top 20: −R$ 81** | **não** |
| 3 | Bracket × mesma entrada sem stop/alvo (diferença de Sharpe ≤ 0,3) | ingênua: Sharpe 1,38, P&L R$ 7.872, max DD −2,4%; bracket: 1,34, R$ 5.670, −1,2%. Diferença de **−0,04** | sim |
| 4 | Correlação do P&L diário < ~0,7 com a 001 em 12:00/k=0 | 0,27 (0,39 nos dias em que as duas operam); 001 com params do WF: 0,26 (0,36); 006 WF: 0,08 (0,36) | sim |

Sobre o critério 3: nos 100 dias em que o bracket stopou, a regra ingênua perdeu em média R$ 144 por trade, contra R$ 147 com o stop. **O stop corta os dias certos**, e o "Por que pode falhar" nº 1 não se confirmou. O custo do bracket está no alvo: nos 98 dias de alvo, segurar até o fechamento renderia R$ 18.343 contra R$ 16.464. Isso explica a diferença de P&L, mas o bracket corta o max DD pela metade. Sem os 20 maiores, a regra ingênua também fica negativa (−R$ 1.310). A dependência de cauda vem do efeito em si, não do stop.

### Pontos fortes
- **Stop e alvo se comportam como projetado.** Saídas: 41,4% no fechamento, 29,6% no stop, 29,0% no alvo, contra 41/30/29 previstos. **0% de `stop_both`**. Toda saída por stop custou exatamente a distância projetada mais R$ 2,50, sem nenhum gap além do stop no OOS. Maior perda: R$ 291 (stop de R$ 289 + custo), ou 0,29% de R$ 100 mil.
- **Acerto acima do equilíbrio.** Nos trades que terminam em bracket, 49,5% bateram o alvo, contra p* = 42,8% com as distâncias medianas. Acerto total de 56% (previsto ~55%). Média por saída: alvo +R$ 168, stop −R$ 147, fechamento +R$ 28.
- **Risco baixo para capital limitado.** Max DD de R$ 1.236 (1,2%), pior dia de −R$ 291, maior sequência de 6 perdas somando −R$ 760 (0,76%). Custos de R$ 845 são 13% do bruto. Com custos 2x o Sharpe fica em 1,14.
- **Positiva em todos os anos.** 2023: 0,51; 2024: 1,26; 2025: 1,53; 2026: 2,92. O 2023 fraco era a previsão: 42% de stops (o estrategista previu ~52% sem o filtro, e o filtro trouxe a fração para 42%), e mesmo assim +R$ 6,91 por trade.
- **Bate os baselines.** Melhor que o ORB (Sharpe OOS 1,07, max DD −4,0%) e que a 006 (1,20). Fica abaixo da 001 (1,61), mas com risco definido e só 0,27 de correlação.

### Pontos fracos e riscos
- **DSR insuficiente.** Com n = 56 seria preciso Sharpe OOS de ~1,79. Faltam ~0,45 de Sharpe, o que não se resolve mexendo em parâmetro.
- **Dependência de cauda (critério 2 falhou).** Os 20 maiores trades (6% dos 338, todos perto do alvo, entre R$ 300 e R$ 370) somam R$ 5.750, mais que o lucro total. A expectativa por trade sem eles é ~0. É o mesmo padrão que derrubou a 006.
- **Tempo debaixo d'água longo.** Do pico de 19/04/2024 ao vale de 24/10/2024 e à recuperação em 23/12/2024 são ~8 meses. A maior sequência debaixo d'água é de **171 pregões**. Para quem opera o próprio dinheiro, isso pesa mais do que o Sharpe de 1,34 sugere. Na tabela de treino do walk-forward, de 06/2024 a 11/2024 quase todas as janelas são negativas.
- **2026 infla o número.** 15 trades a +R$ 49 de média e Sharpe 2,92. Sem 2026, o Sharpe OOS cai para 1,25.
- **Sobreposição com o ORB.** A correlação diária com o baseline ORB é **0,44** (0,64 nos dias em que os dois operam). Parte do efeito é "seguir o rompimento da manhã", que o baseline já captura. A correlação com a 001 é baixa (0,27), então não é a 001 com outro horário.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Não mexer nesta hipótese.** Ela é pré-registrada, e qualquer variação de alvo, horário ou filtro em WIN_N_M5 só soma tentativas num dataset onde o DSR já exige Sharpe ~1,8. Como sugere a própria hipótese, a próxima família deve ir para um **dataset novo**: WDO$N M5 (zero tentativas), com esta mesma regra intacta como primeira tentativa. Isso testa se o efeito generaliza, e com n pequeno o DSR fica alcançável.
2. Se o humano quiser confirmar a 007, o caminho honesto é o holdout de WIN$N, por decisão dele. Antes disso, é preciso aceitar que o critério 2 falhou e registrar que o holdout vai testar um efeito de cauda (~20 dias bons por ano).
3. Uma análise descritiva, sem P&L e sem registro, que ajudaria: medir se os 20 maiores trades se concentram em dias de evento (Copom, payroll, CPI). Se sim, o efeito é de notícia, não de *intraday momentum*.

## Ressalva posterior (orquestrador, 23/10/2026)
Esta seção foi acrescentada depois da análise acima, a partir de dois testes que o pré-registro previa.

**Replicação em WDO$N M5 ([hipótese 008](../../research/hypotheses/008-direcao_do_dia_wdo.md)): REJEITADA.**
- **A regra falhou no outro mercado.** Com a regra intacta e o mesmo módulo, o Sharpe OOS foi de −1,17 e o DSR de 3,3%, com n = 1. Todos os anos ficaram negativos, e o resultado já é negativo antes dos custos.
- **Leitura pelo critério 5:** o efeito é específico do WIN.
- **O que isso sugere:** a regra foi a melhor de ~56 tentativas em WIN. Se ela falha num mercado limpo, parte do Sharpe de 1,34 provavelmente vem da seleção. Relatório: [reports/20261023-215505_direcao_do_dia_WDO_N_M5](../20261023-215505_direcao_do_dia_WDO_N_M5/report.md).

**Eventos macro ([anexo do ciclo](../ciclos/20261023-2138_WIN_N_M5.md)):**
- Os trades em dias de payroll, CPI, FOMC ou no pregão seguinte ao Copom são 14% do total e trazem 68% do P&L.
- Nos dias sem evento, a média é de R$ 4,5 por trade.

**Situação:** a 007 continua PROMISSORA pelos critérios automáticos, mas rebaixada na leitura qualitativa. Não deve ir ao holdout antes de outra replicação limpa, por exemplo a mesma regra em WIN noutro timeframe.
