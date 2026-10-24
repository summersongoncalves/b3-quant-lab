# reversao_rsi2_diario em WDO_N_M5

**Veredito automático: REJECTED**  
WDO: trade against a daily RSI(2) extreme (<=10 buy, >=90 sell) at 10:15, stop 0.25 adr, target 1.5x stop · day trade · gerado em 2026-10-23T23:23:32

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
| P&L total / custos | R$ -1,586.92 / R$ 1,736.00 |
| Retorno anual acima do CDI | -0.6% |
| Sharpe / Sortino | -0.42 / -0.57 |
| Deflated Sharpe (23 tentativas no dataset) | 0.2% |
| Max drawdown | -2.9% |
| Trades / acerto / payoff | 140 / 41% / 1.25 |
| Profit factor | 0.88 |
| Exposição | 7% das barras |
| Custos / lucro bruto | 1164% |
| Sharpe com custos 2x | -0.89 |

Sharpe por ano: 2023: 0.42, 2024: -0.85, 2025: -0.08, 2026: -2.67

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | 0.82 |
| 2023-08-29 → 2023-09-26 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -0.52 |
| 2023-09-27 → 2023-10-25 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -1.26 |
| 2023-10-26 → 2023-11-24 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | -1.31 |
| 2023-11-27 → 2023-12-22 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 1.77 |
| 2023-12-26 → 2024-01-24 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 3.3 |
| 2024-01-25 → 2024-02-23 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 0.9 |
| 2024-02-26 → 2024-03-22 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 0.32 |
| 2024-03-25 → 2024-04-22 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 1.46 |
| 2024-04-23 → 2024-05-21 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | 1.96 |
| 2024-05-22 → 2024-06-19 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -1.26 |
| 2024-06-20 → 2024-07-17 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -2.22 |
| 2024-07-18 → 2024-08-14 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | -1.86 |
| 2024-08-15 → 2024-09-11 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | -0.95 |
| 2024-09-12 → 2024-10-09 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | -0.0 |
| 2024-10-10 → 2024-11-06 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 0.47 |
| 2024-11-07 → 2024-12-06 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 0.14 |
| 2024-12-09 → 2025-01-09 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 0.39 |
| 2025-01-10 → 2025-02-06 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 0.41 |
| 2025-02-07 → 2025-03-10 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -0.11 |
| 2025-03-11 → 2025-04-07 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -0.48 |
| 2025-04-08 → 2025-05-08 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | 0.13 |
| 2025-05-09 → 2025-06-05 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 0.79 |
| 2025-06-06 → 2025-07-04 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 1.66 |
| 2025-07-07 → 2025-08-01 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 0.0 |
| 2025-08-04 → 2025-08-29 | `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | 0.61 |
| 2025-09-01 → 2025-09-26 | `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | 0.71 |
| 2025-09-29 → 2025-10-24 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | -1.59 |
| 2025-10-27 → 2025-11-24 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | -0.33 |
| 2025-11-25 → 2025-12-22 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | -0.09 |
| 2025-12-23 → 2026-01-23 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 2.44 |
| 2026-01-26 → 2026-02-05 | `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | 1.4 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'s': 0.25, 'k': 1.5, 'lim': 10.0}` | -0.09 | 155 | -1.8% |
| `{'s': 0.3, 'k': 1.5, 'lim': 10.0}` | -0.37 | 155 | -2.9% |
| `{'s': 0.35, 'k': 1.5, 'lim': 10.0}` | -0.77 | 155 | -4.0% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Falham 5 dos 7 GATES (Sharpe OOS -0,42, DSR 0,2%, anos, grade, custos 2x) e falham também 4 dos 8 critérios prévios da hipótese (1, 2, 3 e 4). O código implementa o que a hipótese descreve. Não achei look-ahead: o `rsi_from_changes` é um EWM causal, o RSI leva `shift(1)` na série diária, o `adr` leva `shift(1)` e a rolagem vem só do calendário (`BMonthEnd`/`BDay`, sem feriados da B3, como na 015). Também não achei bug no motor.

Números da amostra de pesquisa inteira (backtest em Python, 2023-04 a 2026-02, sem holdout), com `s` = 0,25:

| item | valor |
|---|---|
| Trades / P&L líquido | 155 / R$ -328 (média de R$ -2,1 por trade); Sharpe -0,09 |
| Saídas | stop 51,6%, alvo 38,7%, fechamento 9,7%, stop_both 0% |
| Acerto entre os resolvidos | **42,9%**, abaixo do p* (43,4%) e abaixo do mínimo prévio (~44%) |
| Por ano (líquido) | 2023: R$ -22 · **2024: R$ -830** · 2025: R$ +762 · 2026: R$ -237 |
| Por lado | comprado 91 trades, R$ -21 (acerto 43,6%) · vendido 64 trades, R$ -307 (41,9%) |
| Primeiro dia vs persistente | primeiro dia 86 trades, R$ -544 · persistente 69 trades, R$ +216 |
| Sem os 10 / 20 maiores | R$ -3.150 / R$ -5.516 |
| Grade (s = 0,25/0,30/0,35) | Sharpe -0,09 / -0,37 / -0,77: mesmo sinal, mas **nenhuma positiva** |
| Controle a favor do extremo (momentum) | R$ -3.532, Sharpe -0,96, acerto 36,2% |
| Controle de lado sorteado (200 sorteios) | média de R$ -1.786 (p5 R$ -4.487, p95 R$ +1.490), acerto 39,6%. O principal fica no percentil ~79: **não é significativo** |
| Correlação diária com a 015 | -0,22 em todos os dias e -0,47 nos 80 dias em comum (lado sempre oposto, como a construção prevê) |
| Correlação diária com a 016 | 0,01 em todos os dias e 0,05 nos 38 dias em comum |
| Baseline `opening_range_breakout` (WDO) | Sharpe -0,35, 671 trades, DD -10,3% |

### Pontos fortes
- Execução limpa: 0% de stop_both. A perda máxima foi de R$ 246 (0,25% do capital), igual ao stop projetado mais o custo de R$ 12,40. Nenhum stop teve gap além do nível, e o risco por trade fica dentro do que a hipótese projetou.
- O ordenamento dos controles vai no sentido previsto: reversão (R$ -328) > sorteio (R$ -1.786) > momentum (R$ -3.532). Isso é coerente com o rastro da 015 (que tem correlação de -0,47 com esta nos dias em comum). Mas é o mesmo efeito fraco visto de outro ângulo, não um efeito novo.
- Bate o baseline em Sharpe e em drawdown, mas o baseline também é negativo, então isso não diz muito.

### Pontos fracos e riscos
- **Não há vantagem líquida.** O acerto de 42,9% fica abaixo do equilíbrio de 43,4%, e o acerto ~3 p.p. acima do sorteio vale ~0,6 erro-padrão com ~140 resolvidos. No walk-forward, os custos (R$ 1.736) equivalem a 11x o lucro bruto.
- **Dependência de um só ano.** Todo o resultado positivo vem de 2025 (R$ +762). 2024 perde R$ -830, e o critério 1 falha.
- **Cauda.** Sem os 10 maiores trades o resultado vai a R$ -3.150. O lucro não é robusto.
- **Grade monotônica para baixo.** Quanto maior o stop, pior: com s = 0,35, 31% dos trades saem no fechamento e o acerto cai a 32,7%. O sinal não sustenta um movimento maior que ~0,375 adr.
- **Drawdown sem recuperação.** O pico de equity foi em 2023-07. O fundo, de R$ -1.812 (-1,8%), veio em 2025-03, e a curva não recuperou até o fim da amostra (~19 meses debaixo d'água). A maior sequência foi de 5 perdas (R$ -811).
- O pouco que sobra vem dos extremos **persistentes** (R$ +216), e o primeiro dia de extremo perde (R$ -544). Isso contraria a leitura de "reversão depois do extremo": parece mais ruído que mecanismo.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Não refinar esta família.** A 015 (a favor da semana) e a 017 (contra o extremo de 2 dias) medem o mesmo viés de escala diária, um com o sinal trocado do outro, e nenhuma das duas passa do equilíbrio. A escala diária não dá lado ao intradiário do WDO com este bracket. Somando as tentativas, o dataset WDO_N_M5 está perto do teto (~38 a 40). Mexer no limiar (5/95), no horário ou em `k` seria data mining sobre um efeito de ~0,6 EP.
- Se o laboratório quiser testar a ideia de reversão em dias, ela deve ir para a escala em que foi documentada: **swing diário** (entrar no fechamento e sair na volta à média de 5 dias, como no Connors original), num dataset D1 novo, sem o bracket intradiário. Isso testa se a devolução acontece no overnight, que é a falha 2 prevista na hipótese e que a entrada às 10:15 não captura por construção.
- Antes de outra hipótese direcional no WDO M5, convém mudar o tipo de fonte (fluxo, PTAX, eventos) em vez de procurar mais uma fonte de lado no próprio preço do WDO.
