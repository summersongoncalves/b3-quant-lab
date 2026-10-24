# 015 · Recuo à VWAP a favor da tendência da semana no WDO ("Holy Grail" intradiário com viés semanal)
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: direcional
- Estado: REJEITADA

## Padrão
Quando o dólar vem de uma semana com tendência clara (variação de 5 pregões de pelo menos ~1,1 adr, ajustada pela rolagem), o primeiro recuo da manhã até a VWAP do dia que é rejeitado a favor da tendência é uma entrada barata do lado da semana. Esperamos que, a partir desse toque, o preço chegue a 1,5 vez a distância do stop a favor da semana com mais frequência do que a geometria neutra (~39% entre os resolvidos).

A diferença em relação a tudo que já foi testado no WDO M5 (008, 012, 013, 014) é a **fonte do lado**. Lá o lado vinha de dentro do próprio pregão (excursão da manhã, gap, extensão do IB, extremo de ontem), e o acerto ficou no nível do sorteio. Aqui o lado vem de uma escala maior, a semana, e o intradiário só escolhe o preço de entrada.

## Regras
Barras de 5 min, rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra de sinal.

Definições diárias (só pregões passados):
- Só operar dias cuja primeira barra começa até **09:05**.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`).
- **Janela de rolagem** (só calendário, como na 013/014): `roll(d)` = `d ≥ d + BMonthEnd(0) − BDay(1)` (os 2 últimos dias úteis do mês). Dias com `roll(d)` **não operam**.
- **Variação diária ajustada pela rolagem**: `delta(d) = close(d) − close(d−1)` (fechamento = `close` da última barra do pregão), **exceto** quando `roll(d)` ou `roll(d−1)` for verdadeiro; nesses dias usa-se só a parte intradiária, `delta(d) = close(d) − open(d)`. Assim o salto de contrato da série contínua (gap médio de +7,4 pontos nesses dias contra −0,5 nos demais) não entra na tendência.
- `T5(d)` = soma de `delta` dos **5 pregões anteriores** (d−5 a d−1), dividida por `adr(d)`.
- **Viés do dia**: `vies = +1` se `T5 ≥ z0 × √5` e `vies = −1` se `T5 ≤ −z0 × √5`; caso contrário o dia não opera. Com `z0` = 0,5, o limiar é **1,118 adr**. Dias sem 5 `delta` válidos ou sem `adr` não operam.

Definições intradiárias:
- `vwap` = VWAP do pregão desde a primeira barra: soma acumulada de `(high + low + close)/3 × volume` dividida pela soma acumulada de `volume`, até a barra atual inclusive.
- Janela de sinal: barras rotuladas de **10:00 a 12:55**.

Entrada (no máximo 1 por dia):
- **Comprado** (só se `vies = +1`): primeira barra da janela com `close[t−1] > vwap[t−1]`, `low[t] ≤ vwap[t]` e `close[t] > vwap[t]` (o preço vinha acima da VWAP, recuou até ela e fechou de volta acima).
- **Vendido** (só se `vies = −1`): primeira barra da janela com `close[t−1] < vwap[t−1]`, `high[t] ≥ vwap[t]` e `close[t] < vwap[t]`.
- `t−1` é a barra anterior **do mesmo pregão** (a primeira barra do dia nunca é `t−1` válido de outro dia).
- Execução na abertura da barra seguinte, pela convenção do motor. A posição alvo é `vies` (1 contrato), mantida do sinal até o fim do pregão (ffill por dia), para que o motor não reentre depois de uma saída por stop ou alvo. Só o primeiro toque do dia conta.

Saída:
- Stop loss e stop gain fixos (abaixo), calculados na barra de sinal. Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato; tick = 0,5 ponto (R$ 5). Números da amostra de pesquisa (626 dias válidos, sem holdout, sem P&L): nos dias de sinal o `adr` mediano é **56,6 pontos** (p90 73,6, máximo 108,3); o range mediano de uma barra M5 entre 10:00 e 12:55 é **5,5 pontos** (média 6,1) e o da barra de sinal, 6,5 pontos. O `|close − vwap|` mediano na barra de sinal é de 2,1 pontos, ou seja, a entrada fica colada na VWAP.

- **Stop loss**: `stop = s × adr`, a partir do preço de entrada, fixo.
  - `s` = 0,25 (padrão): mediana de **14,2 pontos, ~28 ticks, ~R$ 142 por contrato**, ~2,6 ranges de barra. Como a entrada fica a ~2 pontos da VWAP, o stop fica ~12 pontos do outro lado dela: a ideia está errada quando o preço **aceita** o lado oposto da VWAP com folga, e não quando só a encosta.
  - `s` = 0,20: 11,3 pontos (~23 ticks, ~2 ranges de barra, o mínimo aceitável). `s` = 0,30: 17,0 pontos (~34 ticks).
- **Stop gain**: `alvo = 1,5 × stop`, fixo. Com `s` = 0,25: mediana de **21,2 pontos, ~42 ticks, ~R$ 212 por contrato** (0,375 adr).
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) + emolumentos 2 × R$ 1,20 (0,24 ponto) = **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**. **Alvo/C ≈ 17x** com `s` = 0,25 (≈ 14x com 0,20; ≈ 21x com 0,30). Todos bem acima de 3x.
- **Acerto de equilíbrio**: `p* = (S + C)/(T + S)`:
  - `s` = 0,20: (11,3 + 1,24)/28,3 ≈ **44,3%**;
  - `s` = 0,25: (14,2 + 1,24)/35,4 ≈ **43,6%**;
  - `s` = 0,30: (17,0 + 1,24)/42,5 ≈ **42,9%**.
  
  A geometria neutra (média dos dois lados, mesmos dias e distâncias) dá ~38 a 39% de alvo entre os resolvidos. Para empatar, o viés da semana precisa acrescentar ~5 pontos percentuais.
- **Taxa de acerto esperada**: ~46 a 48% entre os resolvidos. É um palpite moderado, com três argumentos:
  - **Momentum de câmbio em escala de dias/semanas** está documentado (Menkhoff, Sarno, Schmeling & Schrimpf, 2012; Moskowitz, Ooi & Pedersen, 2012), e no dólar-real ele tem fonte conhecida: fluxo de estrangeiros na bolsa e na renda fixa, desmonte de carry e hedge de empresas, que se espalham por vários dias.
  - **Ordens grandes são fatiadas e executadas por algoritmos de VWAP ao longo de dias** (Lillo & Farmer, 2004, memória longa do fluxo de ordens). Quem ainda tem lote a executar do lado da semana volta a agir quando o preço chega à VWAP do dia, que é a régua do próprio algoritmo. A contraparte é o market maker e o scalper intradiário, que vendem o pico da manhã e devolvem na VWAP.
  - **Holy Grail** (Connors & Raschke): em tendência forte, o recuo à média é comprado. A regra só troca a EMA 20 por VWAP e o ADX pela tendência de 5 pregões.
  
  Se o acerto ficar perto de 39%, o viés semanal também é ruído no WDO intradiário, e isso é informação nova para o laboratório.
- **Perda máxima por trade, custos incluídos**: no stop mediano (`s` = 0,25), ~R$ 155, ou **~0,15% de R$ 100 mil**; no pior caso da amostra (`s` = 0,30, `adr` = 108), ~32,5 pontos, **~R$ 337 (0,34%)**. Uma barra que abre além do stop sai na abertura e pode piorar a perda (divulgações dos EUA às 10:00 e 10:30, janelas da PTAX). O validador deve medir os gaps além do stop.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: medi só a geometria **neutra** (os dois lados, nos mesmos dias e com as mesmas distâncias, entrada na abertura da barra seguinte ao toque, até o fim do pregão), sem o lado do sinal:

  | `s` | alvo | stop | fechamento |
  |---|---|---|---|
  | 0,20 | 36% | 59% | 5% |
  | 0,25 | 34% | 54% | 12% |
  | 0,30 | 29% | 48% | 23% |

  Com a vantagem esperada, ~38 a 41% de saídas no alvo com `s` = 0,25. O alvo é atingível dentro do pregão (o problema do ciclo VBBR3 não se repete): a entrada é cedo (sinal mediano às 10:30, quartis 10:10 e 11:15), com ~7 horas pela frente.
- **Entradas por dia**: no máximo 1, com execução entre 10:05 e 13:00. Ficam proibidos o leilão e a primeira hora (09:00 a 10:00, quando a VWAP ainda é instável e saem os dados dos EUA das 09:30), a tarde inteira para entradas (dólar parado, ciclo 2245) e os dias da janela de rolagem.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| `s` (stop em fração do adr) | 0,25 | 0,20 · 0,25 · 0,30 |
| `k` (alvo em múltiplos do stop) | 1,5 | fixo |
| `z0` (força mínima da tendência de 5 pregões, em adr·√5) | 0,5 | fixo |

**Grade total: 3 combinações**, variando só o tamanho do stop. Ficam fixos também: tendência de 5 pregões (a semana), `adr` de 20 pregões, janela de sinal 10:00 a 12:55, VWAP desde a primeira barra, ajuste e exclusão da rolagem pelo calendário e 1 contrato.

Sinais (descritivo): 284 dias com viés forte, **170 sinais** (60% desses dias têm o toque na janela): 48 em 2023 (desde abril), 55 em 2024, 61 em 2025 e 6 em 2026. 46% comprados e 54% vendidos.

Critérios prévios de sucesso, além dos `GATES`:
1. Líquido médio por trade positivo em 2024 e em 2025, cada ano separadamente.
2. Resultado positivo sem os 10 maiores trades e também sem os 20 maiores.
3. As 3 combinações com Sharpe do mesmo sinal, e pelo menos 2 positivas.
4. Acerto entre trades resolvidos pelo menos 5 pontos percentuais acima da geometria neutra (~39% com `s` = 0,25).
5. **Diagnóstico do viés**: o mesmo toque na VWAP operado **sem** o filtro de tendência (lado = lado de onde o preço veio, todos os dias com toque) tem de ser reportado. Se ele der o mesmo resultado, o lucro não vem da semana, e a hipótese cai mesmo que passe nos `GATES`.
6. Resultado separado entre comprados e vendidos, e por ano. Se todo o lucro vier de um único período de dólar em tendência (ex.: alta do fim de 2024), isso precisa aparecer.
7. Correlação diária com a 008 e a 014 nos dias em comum.

## Por que pode falhar
- **A semana não passa para o intradiário.** O momentum de câmbio documentado é de semanas a meses e inclui o overnight. Dentro do pregão do WDO o lado pode continuar sendo sorteio, como nas 008, 012, 013 e 014, e o viés semanal ser forte demais no papel e fraco demais por trade (alguns décimos de ponto) para pagar 1,24 ponto.
- **Poucos trades e dependência de regime.** São ~170 trades em menos de três anos, com 54% de vendas. Um ou dois períodos de tendência longa (alta do dólar no fim de 2024, queda em 2025) podem responder por todo o resultado, e aí é o regime, não a regra.
- **O stop fica no vaivém da VWAP.** A VWAP é justamente onde o preço oscila mais na manhã. Com `s` = 0,20, o stop fica ~9 pontos do outro lado dela, menos de 2 ranges de barra, e pode ser pego pelo ruído mesmo com o viés certo.

## Por que é conservadora
A perda é fixa e conhecida antes da entrada, ~0,15% do capital na mediana e no máximo ~0,34%, com 1 contrato e 1 entrada por dia, sempre do lado da tendência maior e nunca contra ela. Entra-se num recuo (preço justo do dia), e não em rompimento esticado, e ficam fora o leilão, a primeira hora, a tarde, a rolagem e as semanas sem tendência clara. A grade tem só 3 combinações e o alvo se resolve dentro do pregão em ~88% dos trades.

## Origem
Estratégia conhecida, adaptada e combinada (todas as fontes citadas de memória):
- **Entrada**: Connors & Raschke (1995), *Street Smarts*, setup "Holy Grail" (tendência forte por ADX, recuo até a EMA 20, entrada na retomada). Aqui a média é a VWAP do dia e a tendência é a de 5 pregões.
- **Viés de escala maior**: momentum de séries temporais e de moedas, Moskowitz, Ooi & Pedersen (2012), *Time series momentum*; Menkhoff, Sarno, Schmeling & Schrimpf (2012), *Currency momentum strategies*. O limiar em `adr·√5` normaliza a variação de 5 dias pela volatilidade, como um z-score.
- **VWAP como nível de quem está no controle**: Zarattini, Aziz & Barbon (2024), *Beat the market*, que usa a VWAP como referência e stop do momentum intradiário; e Lillo & Farmer (2004), *The long memory of the efficient market*, sobre o fatiamento de ordens grandes ao longo de dias.
- **Peças do laboratório**: exclusão da rolagem pelo calendário (013 e 014), aqui estendida ao ajuste da variação diária; geometria `alvo = 1,5 × stop` e grade só no stop (014).

É a primeira hipótese do laboratório com viés de vários dias. Não é inversão de nenhuma regra anterior: o lado não depende do que o preço fez no próprio pregão.

Exploração descritiva, sem P&L com o lado do sinal (`research/scratch/explore_015.py`):
- gap médio nos dias de rolagem e no seguinte (+7,4 pontos, contra −0,5 nos demais), para justificar o ajuste da variação diária;
- distribuição de `T5` e `T20` em adr (mediana ~0, 48% positivos), frequência de toques na VWAP com `N` = 5 e `N` = 20 sem limiar (384 e 389 sinais) e com `z0` = 0,5 para `N` = 5 (170 sinais), horário dos sinais, `adr`, range das barras e distância à VWAP;
- geometria neutra (os dois lados, mesmos dias e distâncias) para 3 valores de `s` com `k` = 1,5, só para medir se o alvo é atingível.

Tentativas escondidas: **~3**. A escolha de `N` = 5 (em vez de 20 ou de ambos na grade) e de `z0` = 0,5 foi feita olhando só frequência de sinais; a grade de `s` e `k` = 1,5 foi escolhida pela geometria neutra. Nada calculou resultado com o lado do viés. Somadas às ~26 efetivas de WDO_N_M5, o dataset chega a ~29 antes desta validação.

## Notas de implementação
- Fechamento do dia = `close` da última barra do pregão; `open(d)` = `open` da primeira barra.
- `roll(d)` só pelo calendário (`BMonthEnd(0)`, `BDay(1)`), como `_rollover_days` em `fechamento_gap.py`. O primeiro dia do dataset tem `roll(d−1)` tratado como verdadeiro.
- `T5` usa `delta` de d−5 a d−1 (`rolling(5).sum().shift(1)`), dividido pelo `adr` do dia d.
- A VWAP reinicia a cada pregão. Se o volume acumulado for 0, a barra não gera sinal.
- `stop = s × adr` e `alvo = k × stop`, em pontos, constantes no dia.
- `k` e `z0` ficam em `params`, fora da `grid`.

Relatório: reports/20261023-230646_recuo_vwap_tendencia_semanal_WDO_N_M5
