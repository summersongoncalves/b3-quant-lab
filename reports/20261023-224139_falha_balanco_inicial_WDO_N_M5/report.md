# falha_balanco_inicial em WDO_N_M5

**Veredito automático: REJECTED**  
Fade a failed extension of the first-hour range (IB) in WDO; stop behind the failed extreme, target at the opposite IB side · day trade · gerado em 2026-10-23T22:41:39

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
| P&L total / custos | R$ -6,692.95 / R$ 3,633.20 |
| Retorno anual acima do CDI | -2.7% |
| Sharpe / Sortino | -1.31 / -2.06 |
| Deflated Sharpe (7 tentativas no dataset) | 0.2% |
| Max drawdown | -7.6% |
| Trades / acerto / payoff | 293 / 44% / 0.96 |
| Profit factor | 0.75 |
| Exposição | 15% das barras |
| Custos / lucro bruto | 119% |
| Sharpe com custos 2x | -2.01 |

Sharpe por ano: 2023: -2.44, 2024: -1.98, 2025: -0.41, 2026: 1.4

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'e': 0.1, 'b': 0.1}` | -0.82 |
| 2023-08-29 → 2023-09-26 | `{'e': 0.1, 'b': 0.1}` | 0.0 |
| 2023-09-27 → 2023-10-25 | `{'e': 0.15, 'b': 0.1}` | -2.06 |
| 2023-10-26 → 2023-11-24 | `{'e': 0.15, 'b': 0.1}` | -1.86 |
| 2023-11-27 → 2023-12-22 | `{'e': 0.15, 'b': 0.05}` | -0.15 |
| 2023-12-26 → 2024-01-24 | `{'e': 0.05, 'b': 0.05}` | -0.07 |
| 2024-01-25 → 2024-02-23 | `{'e': 0.05, 'b': 0.05}` | -0.31 |
| 2024-02-26 → 2024-03-22 | `{'e': 0.1, 'b': 0.1}` | -1.46 |
| 2024-03-25 → 2024-04-22 | `{'e': 0.15, 'b': 0.1}` | -3.09 |
| 2024-04-23 → 2024-05-21 | `{'e': 0.15, 'b': 0.1}` | -3.34 |
| 2024-05-22 → 2024-06-19 | `{'e': 0.05, 'b': 0.1}` | -1.79 |
| 2024-06-20 → 2024-07-17 | `{'e': 0.05, 'b': 0.05}` | -2.5 |
| 2024-07-18 → 2024-08-14 | `{'e': 0.15, 'b': 0.05}` | -1.29 |
| 2024-08-15 → 2024-09-11 | `{'e': 0.05, 'b': 0.05}` | -2.09 |
| 2024-09-12 → 2024-10-09 | `{'e': 0.15, 'b': 0.05}` | -0.01 |
| 2024-10-10 → 2024-11-06 | `{'e': 0.15, 'b': 0.05}` | -0.42 |
| 2024-11-07 → 2024-12-06 | `{'e': 0.15, 'b': 0.05}` | 0.13 |
| 2024-12-09 → 2025-01-09 | `{'e': 0.15, 'b': 0.05}` | 1.15 |
| 2025-01-10 → 2025-02-06 | `{'e': 0.15, 'b': 0.1}` | 1.02 |
| 2025-02-07 → 2025-03-10 | `{'e': 0.05, 'b': 0.1}` | 0.55 |
| 2025-03-11 → 2025-04-07 | `{'e': 0.15, 'b': 0.1}` | -0.44 |
| 2025-04-08 → 2025-05-08 | `{'e': 0.05, 'b': 0.1}` | 0.16 |
| 2025-05-09 → 2025-06-05 | `{'e': 0.15, 'b': 0.05}` | 1.11 |
| 2025-06-06 → 2025-07-04 | `{'e': 0.15, 'b': 0.05}` | -0.86 |
| 2025-07-07 → 2025-08-01 | `{'e': 0.15, 'b': 0.05}` | -1.21 |
| 2025-08-04 → 2025-08-29 | `{'e': 0.15, 'b': 0.05}` | 0.2 |
| 2025-09-01 → 2025-09-26 | `{'e': 0.15, 'b': 0.05}` | 0.39 |
| 2025-09-29 → 2025-10-24 | `{'e': 0.15, 'b': 0.05}` | -0.41 |
| 2025-10-27 → 2025-11-24 | `{'e': 0.15, 'b': 0.05}` | -0.94 |
| 2025-11-25 → 2025-12-22 | `{'e': 0.15, 'b': 0.05}` | 0.18 |
| 2025-12-23 → 2026-01-23 | `{'e': 0.15, 'b': 0.05}` | 2.57 |
| 2026-01-26 → 2026-02-05 | `{'e': 0.15, 'b': 0.1}` | 1.43 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'e': 0.05, 'b': 0.05}` | -1.71 | 476 | -11.3% |
| `{'e': 0.05, 'b': 0.1}` | -1.63 | 476 | -11.4% |
| `{'e': 0.1, 'b': 0.05}` | -1.86 | 360 | -12.3% |
| `{'e': 0.1, 'b': 0.1}` | -1.62 | 360 | -11.3% |
| `{'e': 0.15, 'b': 0.05}` | -0.9 | 262 | -5.9% |
| `{'e': 0.15, 'b': 0.1}` | -0.81 | 262 | -5.5% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Falha em 5 dos 7 GATES (Sharpe OOS −1,31, DSR 0,2%, anos, grade, custos 2x) e em 3 dos 5 critérios prévios da própria hipótese. O DSR usa 7 tentativas registradas; com as ~19 tentativas efetivas declaradas para WDO_N_M5, seria ainda menor. Não há nada a resgatar: o bruto já é negativo.

Números abaixo: backtest direto na amostra de pesquisa (2023-04-05 a 2026-02-05, sem holdout), combinação padrão `e`=0,10, `b`=0,05, salvo indicação.

### Conferência do código
- Implementa o que a hipótese descreve: IB 09:00–09:55 com ≥ 11 barras, `adr` de 20 pregões com `shift(1)`, `cummax`/`cummin` incluindo a barra atual, janela 10:00–13:55, só o primeiro evento do dia (descartado se os dois lados valem ou se o alvo < 3,72 pontos), stop `max(|extremo − close| + b·adr, 0,15·adr)` e alvo no outro lado do IB, medidos do close da barra de sinal.
- Não achei look-ahead além do que o teste automático pega. `IBH`/`IBL` são `transform` sobre o dia inteiro, mas só incluem barras até 09:55 e só são usados a partir de 10:00.
- Ressalva pequena: as distâncias são medidas do close do sinal, e a entrada é na abertura seguinte. Os níveis absolutos andam junto com o gap de 1 barra. O efeito é irrelevante perto do tamanho do prejuízo.
- Motor: sem bug encontrado. A perda realizada nos stops bate exatamente com a distância planejada × R$ 10 + R$ 12,40 (mediana −R$ 155 nos dois).

### Critérios prévios da hipótese
| # | Critério | Resultado | |
|---|---|---|---|
| 1 | Líquido médio > 0 em 2024 e em 2025 | 2024: −R$ 45,1/trade; 2025: −R$ 29,0/trade (2023: −28,1; 2026: +68,9 em 18 trades) | ❌ |
| 2 | Positivo sem os 10 e sem os 20 maiores | Total −R$ 10.497; sem top 10: −R$ 14.903; sem top 20: −R$ 17.874 | ❌ |
| 3 | ≥ 4 de 6 combinações com Sharpe > 0 | 0 de 6 (de −0,81 a −1,86) | ❌ |
| 4 | Saídas no alvo ≥ 20% | 26,4% (95/360) | ✅ (mas ver abaixo) |
| 5 | Correlação diária com a 008 | −0,50 nos 198 dias em comum; −0,22 em todos os dias. 87% dos dias em comum têm lado oposto ao da 008 | reportado; fica abaixo do limiar de −0,6, mas por pouco |

### Stop e alvo
- Saídas: stop 48,6% (175), alvo 26,4% (95), fechamento 25,0% (90), **stop_both 0%**. O stop (~3 ranges de barra) não está dentro do ruído de 1 barra, e o resultado não depende da suposição do motor.
- O alvo dentro da faixa prevista (25–32%) engana: o stop ficou em 49%, contra 30–38% previstos, e roubou a fatia do fechamento (25% contra ~35%).
- **Acerto entre os resolvidos: 35,2%** (95 / 270). A hipótese esperava 46–50%. O p* com custos é ~44%, e o **benchmark de lado aleatório é 36%**. A própria hipótese disse que "perto de 36 a 40% a ideia é ruído": é exatamente isso, um pouco abaixo do aleatório.
- Médias: alvo +R$ 188, stop −R$ 168, fechamento +R$ 11. O bruto total é **−R$ 6.033** e os custos somam R$ 4.464: a estratégia perde antes dos custos.
- Na melhor combinação (`e`=0,15, `b`=0,05), o acerto entre resolvidos sobe para 42,8%, ainda abaixo do p*. Resultado: −R$ 4.769, com bruto −R$ 1.520.
- Gaps além do stop: **nenhum**. O excesso sobre a perda planejada foi R$ 0 em todos os stops. A maior perda (−R$ 427) é um stop largo planejado, perto do p90 + custos da hipótese (R$ 297 no p90, R$ 548 no pior caso).

### Inversão da 008 (critério 5)
- A 012 opera no lado oposto ao da 008 em 87% dos dias em comum. A correlação do P&L diário nesses dias é −0,50 (−0,56 com `e`=0,15). O sinal é em grande parte a 008 invertida, embora a correlação não cruze −0,6, porque os brackets e os horários são diferentes.
- Ponto decisivo: **as duas perdem**. A 008 deu −R$ 9.548 e a 012 deu −R$ 5.500 nos dias em comum com ela, e −R$ 4.997 nos outros dias. Nem a continuação nem o fade da excursão da manhã têm vantagem no WDO M5. A estrutura do IB não acrescenta nada, e a inversão também não.

### Sem bracket (mesma entrada, segurar até o fechamento)
- `e`=0,10: −R$ 10.984, bruto −R$ 6.520, Sharpe diário −1,25.
- `e`=0,15: −R$ 8.909, Sharpe −1,29.
- O bracket não é o problema. A entrada não tem direção.

### Risco para capital limitado (R$ 100 mil, 1 contrato)
- Perda máxima por trade: R$ 427 (0,43%). Pior dia: −R$ 427.
- Maior sequência: 8 perdas seguidas, somando −R$ 1.793 (1,8%).
- Max DD na amostra inteira: −R$ 12.326 (12,3%). No walk-forward: −7,6%.
- **Debaixo d'água por 683 pregões**: o pico é praticamente o início, e a curva termina no fundo.
- Comparação: o baseline `opening_range_breakout` no mesmo dataset também perde (−R$ 5.215, Sharpe −0,35), mas perde menos que a 012 (−R$ 10.497, Sharpe −1,86). A 012 não bate o baseline.

### Estabilidade de parâmetros
- O walk-forward pula entre os extremos da grade até o fim de 2024, com Sharpe de treino negativo em quase todas as janelas. Depois se fixa em `e`=0,15, a extensão maior, que é a que faz menos trades e portanto perde menos.
- O único ano positivo, 2026, tem 18 trades (5 semanas). Não serve de evidência.

### Pontos fortes
- Implementação limpa, sem look-ahead e imune à rolagem.
- Stops respeitados, sem gap nem stop_both. O risco por trade ficou como projetado (mediana R$ 155–168).
- A hipótese definiu benchmarks (36% aleatório, p* 44%) que permitiram rejeitar sem ambiguidade.

### Pontos fracos e riscos
- O bruto é negativo em todas as 6 combinações. O acerto entre resolvidos (35%) é igual ao de um lado aleatório.
- O sinal é ~87% a 008 invertida. A 008 e a 012 perdem juntas, o que indica que a excursão da manhã no WDO M5 não carrega informação direcional, em nenhum dos dois sentidos.
- Os custos ainda comem 119% do lucro bruto OOS.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Parar a família "excursão/extensão da manhã" no WDO M5** (continuação 008, fade 012). Com ~19 tentativas efetivas no dataset, mais variações de nível (IB de 30 min, meio do IB, `e` maior) são data-mining. A melhora de `e`=0,15 vem de operar menos, não de uma vantagem.
- Se o WDO continuar como alvo, mudar o tipo de informação, não o nível. Exemplos: um condicionante exógeno medido antes do sinal (dia com ou sem dado dos EUA, ou com ou sem leilão do BC, calendário conhecido de véspera), ou a relação com DI/índice do dólar, se houver dado. Exigir antes, só de forma descritiva, que o acerto entre resolvidos se afaste do benchmark aleatório.
- Alternativa: trocar de dataset ou de timeframe (WDO M15/H1 ou swing), em vez de gastar mais tentativas em WDO_N_M5.
