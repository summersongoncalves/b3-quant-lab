# 019 · Barra de choque com esforço e resultado (Wyckoff) no WDO: seguir a barra larga, de volume alto e fechamento no extremo, por até 1 hora
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: momentum
- Estado: REJEITADA

## Padrão
Quando uma barra de 5 minutos do WDO é ao mesmo tempo **muito larga** e de **volume muito alto** para aquele horário, e fecha no extremo dela, o mercado mostrou esforço (volume) com resultado (amplitude e fechamento a favor). Pela leitura de Wyckoff, isso é sinal de força (SOS) ou de fraqueza (SOW), e não absorção. Esperamos que o dólar continue no lado do fechamento da barra na hora seguinte com mais frequência que a geometria neutra.

O que se sabe antes do teste, só por estatística descritiva sem lado: depois dessas barras, a excursão máxima do WDO em 1 hora é **~40% maior** que numa barra sorteada (0,271 contra 0,193 `adr` na mediana). O combustível existe. A pergunta do validador é se o **fechamento no extremo com volume** dá o lado, coisa que o rompimento de faixa da 018 e o de extremo da 014 não deram.

## Regras
Barras de 5 min, rotuladas pelo horário de abertura. Tudo calculado no fechamento da barra de sinal t, só com dados do WDO.

Definições:
- `rng(t)` = `high(t)` − `low(t)`.
- `rng_ref(t)` = **mediana** de `rng` no **mesmo horário (hh:mm)** nos **20 pregões anteriores** (tabela dia × horário, `rolling(20, min_periods=20).median().shift(1)`). Sem os 20, a barra não sinaliza.
- `vol_ref(t)` = idem, com a coluna `volume`.
- `rr(t)` = `rng(t)` / `rng_ref(t)`; `rv(t)` = `volume(t)` / `vol_ref(t)`.
- `clv(t)` = (`close(t)` − `low(t)`) / `rng(t)`; se `rng(t)` = 0, a barra não sinaliza.
- `adr` = média de (máxima − mínima do dia) nos 20 pregões anteriores (`shift(1)`).

Gatilho (barra de choque):
- `rr(t)` ≥ **k** **e** `rv(t)` ≥ **k**, com k = 2,5 para os dois (fixo).
- **Lado**: compra se `clv(t)` ≥ 0,75 (fechou no quarto superior); venda se `clv(t)` ≤ 0,25 (quarto inferior). Barras com fechamento no meio (0,25 < `clv` < 0,75) são esforço sem resultado e **não** sinalizam.
- Janela da barra de sinal: rotulada de **09:30 a 16:00** (inclusive). Nada nos primeiros 30 minutos (leilão e ajuste da abertura); nada depois das 16:00, para que a hora de trade termine por volta das 17:05, longe do call.
- **No máximo 1 entrada por dia**: só a primeira barra de choque do pregão. Depois de qualquer saída, o dia acabou.
- **Exclusão da rolagem** (calendário, como em `fechamento_gap.py`): não operar se `data ≥ data + BMonthEnd(0) − BDay(1)`.

Saída:
- Stop e alvo fixos (abaixo), lidos na barra de sinal.
- **Saída por tempo**: a posição volta a 0 no fechamento da **12ª barra depois da barra de entrada** (1 hora), executado na abertura da seguinte. Momentum que não andou em 1 hora acabou. A posição fica 0 até o fim do pregão.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato, tick = 0,5 ponto (R$ 5). Valores da amostra de pesquisa, sem holdout e sem P&L. Nos dias de sinal, o `adr` mediano é de 54,7 pontos (p10 42, p90 71, máximo 108). A barra de choque tem range mediano de 13,5 pontos (0,25 `adr`); as 12 barras seguintes têm range mediano de **5,5 pontos** (p90 11,5). O salto entre o fechamento da barra de sinal e a abertura seguinte é de 0 ponto na mediana e 0,5 no p95.

- **Stop loss**: `stop = s × adr`, a partir da entrada, fixo.
  - `s` = 0,20 (padrão): mediana de **~11 pontos, 22 ticks, R$ 110 por contrato**, 2× o range mediano das barras pós-sinal.
  - `s` = 0,15: ~8,2 pontos, 16 ticks, R$ 82 (1,5× o range pós-sinal). Fica no limite do ruído e entra na grade como o lado apertado; não vou abaixo disso.
- **Stop gain**: `alvo = 1,5 × stop`, fixo. Com `s` = 0,20: **~16,4 pontos, 33 ticks, R$ 164**. Com 0,15: ~12,3 pontos, 25 ticks, R$ 123.
- **Custo de ida e volta (C)**: 1 tick de slippage por lado mais 2 × R$ 1,20 de emolumentos, **C ≈ 1,24 ponto (~2,5 ticks, R$ 12,40)**. **Alvo/C ≈ 13x** (`s` = 0,20) e **~10x** (0,15). No `adr` p10, o alvo com `s` = 0,15 ainda é de 9,5 pontos, ~7,7 C.
- **Acerto de equilíbrio entre os resolvidos**, `p* = (S + C) / (T + S)`:
  - `s` = 0,20: (10,9 + 1,24) / (16,4 + 10,9) = **44,5%**.
  - `s` = 0,15: (8,2 + 1,24) / (12,3 + 8,2) = **46,1%**.
- **Geometria neutra** (descritiva, média dos dois lados, entrada na abertura seguinte, 243 sinais, horizonte de 12 barras):

  | `s` | alvo | stop | tempo | acerto neutro entre resolvidos |
  |---|---|---|---|---|
  | 0,15 | 28% | 46% | 26% | 38% |
  | 0,20 | 20% | 36% | 44% | 36% |

- **Acerto esperado**: ~46% a 48% entre os resolvidos, ou seja, ~9 p.p. acima do neutro. Digo abertamente que é uma exigência alta. O motivo para acreditar: no câmbio, a notícia é incorporada pelo fluxo de ordens ao longo de horas, e não num salto único (Evans & Lyons, 2008). Uma barra que fecha no extremo com volume 2,5× o normal do horário é a pegada de quem precisa executar agora, e o resto da ordem costuma vir fatiado nas barras seguintes. Quem está do outro lado é o market maker e o vendedor de volatilidade, que fornecem liquidez contra o choque e o reabastecem até a ordem acabar. **Se o acerto entre os resolvidos ficar abaixo de ~41%, o efeito não existe e a hipótese cai.**
- **Perda máxima por trade, custos incluídos**: típica de 10,9 + 1,24 ≈ **R$ 121 (0,12% de R$ 100 mil)** com 1 contrato. No maior `adr` da amostra (108) com `s` = 0,20: 21,7 + 1,24 ≈ R$ 229 (0,23%). O salto entre barras é pequeno (p95 de 0,5 ponto), então o risco de gap além do stop é baixo, mas as barras de choque são de notícia e o validador deve medir os stops que saíram além da distância.
- **Fração esperada de trades que chegam ao alvo em 1 hora**: ~28% com `s` = 0,15 e ~20% com 0,20 pela geometria neutra; com o efeito, ~31% e ~23%. Com 0,20, quase metade dos trades sai por tempo, e é aí que o lado tem de aparecer.
- **Entradas por dia**: no máximo 1. Nada antes das 09:30 nem com barra de sinal depois das 16:00.
- **Frequência**: **~243 sinais** (58 em 2023 desde abril, 96 em 2024, 82 em 2025, 7 em 2026), cerca de 39% dos pregões, espalhados pelo dia (de 25 a 40 por hora cheia entre 09:00 e 15:00). 116 de compra e 127 de venda.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| s (stop em `adr`; alvo = 1,5 × stop) | 0.20 | [0.15, 0.20] |
| k (limiar de `rr` e de `rv`, o mesmo para os dois) | 2.5 | [2.5] (fixo) |
| horizonte (barras até a saída por tempo) | 12 | [12] (fixo) |

São 2 combinações. O limiar de 0,75/0,25 do `clv` é a definição de fechamento no quarto do extremo e fica fixo.

## Por que pode falhar
1. **Notícia sem lado, de novo.** Esta é a sexta forma de perguntar ao WDO se um evento dá o lado (008, 012, 013, 014, 018). Em todas o acerto ficou no neutro. A barra de choque pode ser só mais um jeito de achar a hora em que o dólar anda mais, sem dizer para onde. O modo de falha mais provável é acerto entre 36% e 40%.
2. **Reversão de excesso.** Choques no câmbio muitas vezes são exagerados e voltam (atuação do BC, realização depois do dado). Entrar na abertura seguinte a uma barra que fechou no extremo é comprar o topo local; se metade dos choques reverte, o stop é acionado antes do alvo.
3. **Concentração em poucos dias.** Os maiores choques são dias de Copom, payroll, fiscal (fim de 2024). O lucro, se houver, pode vir de 10 a 20 trades. O validador deve olhar o resultado sem os 10 maiores trades e por ano.

Pré-registro para o validador (antes de qualquer resultado):
- **Acerto entre os resolvidos** com `s` = 0,20 ≥ 42%; abaixo de 41%, a hipótese cai.
- **Controle 1, esforço sem resultado**: mesmas barras largas e de volume alto, mas com `clv` entre 0,25 e 0,75, operadas no lado de `close` − `open` da barra. Se o controle for igual ou melhor por trade, o fechamento no extremo não acrescenta nada e a leitura de Wyckoff não vale.
- **Controle 2, sem volume**: `rr` ≥ 2,5 e fechamento no extremo, mas `rv` < 1,5 (são poucos dias; usar só como leitura). Se for igual, o volume não acrescenta nada.
- **Concentração**: positiva sem os 10 maiores trades e com 2024 e 2025 positivos.
- **Correlação diária** com a 018 e a 014, que também seguem eventos de expansão no WDO.

## Por que é conservadora
Uma entrada por dia, 1 contrato, stop fixo de ~R$ 121 com custos (0,12% do capital), alvo 13x o custo e saída por tempo em 1 hora, sem reentrada nem preço médio. Só o tamanho do stop varia, em 2 valores; o limiar e o horizonte são fixos e o lado vem de uma regra mecânica. Um gestor de risco aprovaria porque a perda é pequena e conhecida, o trade nunca fica esperando o fechamento, e os controles derrubam a hipótese se a peça que a justifica (volume com resultado) não fizer diferença.

## Origem
Combinação de peças publicadas, adaptada ao WDO:
- **Esforço × resultado e barra de sinal de força/fraqueza**: método Wyckoff, nas versões de Pruden, *The Three Skills of Top Trading* (2007), e Weis, *Trades About to Happen* (2013): volume alto com barra larga e fechamento no extremo é esforço com resultado e tende a continuar; volume alto com fechamento no meio é absorção. Citado de memória. Aqui a leitura do volume é o centro da hipótese, e não um *spring*/*upthrust* (primos do Turtle Soup, que falharam na 005 e na 012).
- **Barra de expansão como gatilho de momentum**: Crabel (1990), *Day Trading with Short Term Price Patterns*, sobre barras de range largo depois de range normal. Citado de memória.
- **Fluxo de ordens que incorpora a notícia ao longo de horas no câmbio**: Evans & Lyons (2008), *How is macro news transmitted to exchange rates?* (JFE); Andersen, Bollerslev, Diebold & Vega (2003), *Micro effects of macro announcements* (AER). Citados de memória.
- **Diferença em relação às anteriores do mesmo estilo no WDO**:
  - a 010 (exploração, compressão com volume) não achou expansão; aqui a excursão pós-sinal é ~40% maior que a do acaso;
  - a 018 usava rompimento de faixa de ruído em relação à abertura e a confirmação do WIN; aqui o gatilho é uma única barra, medida contra o próprio horário, e o lado vem do fechamento da barra com volume, sem nenhum dado do WIN (o sinal continua existindo no holdout do WDO);
  - é também a resposta possível, sem calendário econômico, ao "momentum de notícia" sugerido no ciclo 20261023-2230: a barra de choque é um detector causal de evento.

Exploração feita (só descritiva, sem P&L, sem retorno ou MAE/MFE por lado; script em `research/scratch/explore_019.py`):
- Contagem de sinais por ano e por hora com k ∈ {2,0; 2,5; 3,0} (431, 243 e 150 dias).
- Excursão máxima sem lado em 12 e 24 barras contra 3.000 barras sorteadas (k = 2,5: 0,271 / 0,366 `adr`; sorteadas 0,193 / 0,263).
- Geometria neutra do bracket com `s` ∈ {0,15; 0,20; 0,25} e horizontes de 12 e 24 barras; range da barra de sinal e das barras seguintes; salto entre fechamento e abertura seguinte; `adr` nos dias de sinal; contagem do controle sem volume.
- As escolhas (k = 2,5 pelo meio-termo entre frequência e expansão, horizonte de 12 barras pelo estilo, `s` sem 0,25 porque o alvo seria atingido em só 13%) foram feitas por frequência, alcance do alvo e range de barra, nunca por resultado com lado.

**Tentativas escondidas**: nenhuma com resultado com lado. Pelo critério das hipóteses anteriores, registro **2** tentativas escondidas, pela escolha entre 3 limiares e 2 horizontes olhando frequência e geometria neutra. WDO_N_M5 deve ficar perto de ~44 tentativas efetivas depois desta, ainda abaixo de ~50, mas perto do limite: a iteração 3 deste ciclo deveria ser de 1 combinação.

## Notas de implementação
- `rng_ref` e `vol_ref`: tabela dia × horário (`pivot_table(index=dia, columns=hhmm)`), `rolling(20, min_periods=20).median().shift(1)`, depois de volta ao índice das barras por (dia, hhmm). Horário sem os 20 pregões não sinaliza.
- Coluna de volume: `volume` do Parquet.
- Saída por tempo: a posição fica no lado do sinal nas barras t..t+11 e vale 0 a partir de t+12 no mesmo pregão. Com entrada na abertura de t+1 e saída na abertura de t+13, o trade dura 12 barras. Stop e alvo ficam constantes nas barras em que a posição está ligada e NaN depois.
- Contagem esperada: ~243 entradas (igual à exploração), antes do motor tirar os dias sem barra seguinte.
Relatório: reports/20261023-234200_choque_esforco_resultado_WDO_N_M5
