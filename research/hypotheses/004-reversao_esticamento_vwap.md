# 004 · Reversão de esticamento em relação à VWAP diária em VBBR3, com bracket e risco fixo por trade
- Dataset: VBBR3 M5
- Modo: daytrade
- Estado: REJEITADA

## Padrão
Quando VBBR3 se afasta muito da VWAP diária no miolo do pregão (mais de meio `adr` de distância), o preço tende a devolver parte do afastamento antes do fechamento. É uma família nova em VBBR3: provisão de liquidez contra um impacto de preço temporário, e não continuação de tendência.

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra atual):
- Só operar dias cuja primeira barra começa até **10:10** (mesmo corte da 003).
- `vw` = `vwap(df, "D")` de `strategies/_helpers.py`, lido na barra atual.
- `adr` = média de (máxima do dia − mínima do dia), em R$, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam.
- `dev` = (`close` − `vw`) / `adr`, na barra atual (adimensional).
- Janela de sinal: barras rotuladas de **11:00 a 15:25** (fechamento entre 11:05 e 15:30). Fora dela não há sinal.

Entrada (no máximo 1 por dia):
- Na **primeira** barra do dia, dentro da janela, em que `|dev| > 0,5` (**fixo**), o lado é `−sinal(dev)`: vendido se o preço está acima da VWAP, comprado se está abaixo.
- A execução é na abertura da barra seguinte, pela convenção do motor.
- Se essa primeira ocorrência não gerar trade (ex.: dia sem `adr`), o dia não opera. Não há segunda entrada, mesmo depois de uma saída por stop ou alvo.

Tamanho (risco fixo por trade, igual à 003):
- `stop_dist` = `s × adr` (R$ por ação).
- `w` = min(1, 0,008 × `close` / `stop_dist`), com o `close` da barra de sinal.
- Posição alvo = `−sinal(dev) × w`, mantida igual do sinal até o fim do pregão, para que o motor não reentre depois de um bracket.

Saída:
- Stop loss e stop gain fixos a partir do preço de entrada (ver abaixo), lidos na barra de sinal.
- Sem saída por sinal: a posição não é zerada quando o preço volta à VWAP. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Valores típicos com preço de ~R$ 21 e `adr` de ~R$ 0,55 (~265 bp; medianas por ano de R$ 0,50 a 0,57). O range mediano de uma barra de M5 é de ~24 bp, ou 5 ticks.

- **Stop loss**: `s × adr`. Com s = 0,35, dá R$ 0,19, ou seja **19 ticks** e ~92 bp. Com s = 0,25, são 14 ticks (~66 bp). Com s = 0,5, são 27 ou 28 ticks (~131 bp). Mesmo o menor stop fica a ~3 ranges de barra da entrada, fora do ruído de uma barra. Para uma posição cheia de R$ 100 mil, o stop vale R$ 660, R$ 920 ou R$ 1.310. Depois do ajuste de tamanho `w`, a perda no stop fica limitada a ~R$ 800.
- **Stop gain**: `1,5 × stop` (**fixo**). Com s = 0,35, são **29 ticks** e ~138 bp. Com s = 0,25, são 21 ticks (~98 bp). Com s = 0,5, são 41 ticks (~196 bp). A relação caiu de 2x (003) para 1,5x porque na 003 só 12% das saídas foram no alvo. Aqui o alvo pede 0,37 a 0,75 `adr`, ou seja, devolver de ~75% a ~150% do afastamento mínimo de 0,5 `adr`. É compatível com um horizonte de 1 a 4 horas.
- **Custo de ida e volta (C)**: emolumentos de 2 × 2,3 bp mais 1 tick de slippage por lado (2 × R$ 0,01 / preço). Isso dá ~14 bp com R$ 21, ~18 bp com R$ 15 (2023) e ~12,4 bp com R$ 25,5 (2026), ou ~R$ 140 para R$ 100 mil cheios. Em ticks, C equivale a ~3 ticks. Alvo/C: ~7x (s = 0,25), ~10x (s = 0,35) e ~14x (s = 0,5). Todos acima do mínimo de 3x.
- **Acerto de equilíbrio, só para o bracket**: `p* = (S + C) / (T + S)`. Dá (66 + 14) / (98 + 66) = 48,8% com s = 0,25, (92 + 14) / (138 + 92) = 46,1% com s = 0,35 e (131 + 14) / (196 + 131) = 44,3% com s = 0,5. Como parte dos trades sai no fechamento, o critério que vale na prática é o mesmo da 003: **bruto médio por trade acima de 2 × C (~28 bp) em cada ano**, e resultado sem os 5 maiores trades positivo.
- **Taxa de acerto esperada**: 50% a 53%, que fica só um pouco acima do p*. Ela vem da exploração (ver Origem): segurando até o fechamento, 51% dos trades foram positivos, com bruto médio de 12,6 bp, positivo nos três anos (9,7, 13,1 e 15,4 bp). Esse bruto está **abaixo** de 2 × C, e quase todo ele vem de poucos trades (sem os 5 maiores, cai para 0,5 bp). **Minha expectativa honesta é REJEITADA.** O que pode mudar o quadro é o bracket cortar as perdas grandes (MAE mediana de −69 bp até o fechamento) sem cortar os ganhos (MFE mediana de +93 bp). Mas isso não está demonstrado, e calibrar o bracket nesses números seria mineração. Por isso o múltiplo do alvo e o limiar ficaram fixos.
- **Perda máxima por trade, custos incluídos**: ~0,8% do capital de stop mais ~0,14% × `w` de custo, ou seja ≤ ~R$ 940 (0,94% de R$ 100 mil). Em 2023, com C de 18 bp, fica em ~R$ 980. A exceção é o gap dentro do pregão: uma barra de notícia (reajuste de combustível, Petrobras) que abre além do stop sai na abertura dessa barra, e a perda pode passar de 1%. Esse é o risco típico de quem vende o movimento.
- **Entradas por dia**: no máximo 1, entre 11:05 e 15:30. Ficam proibidos a primeira hora depois do leilão (a VWAP ainda tem pouco volume e o `dev` é instável) e a última hora e meia antes do call de fechamento.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| stop_mult (s) | 0.35 | [0.25, 0.35, 0.5] |

Fixos (não são parâmetros e não podem ir para a grade): limiar `|dev| > 0,5`, janela de 11:00 a 15:25, alvo = 1,5 × stop, janela de 20 dias do `adr`, corte de abertura em 10:10 e risco de 0,8% por trade. Grade total: **3 combinações**. Como o sinal é o mesmo nas três, elas devem dar o mesmo sinal de resultado. Se só uma funcionar, é ruído.

## Por que pode falhar
1. **O bruto não paga o custo (o risco principal).** Na exploração, o bruto até o fechamento foi de 12,6 bp contra um C de ~14 bp. É a mesma armadilha de BBAS3: em VBBR3, um tick de R$ 0,01 mais emolumentos custa ~14 bp, e nenhuma das sete famílias que olhei neste ativo passou de ~13 bp brutos. Se o bracket não melhorar muito a relação entre ganho e perda, o resultado é negativo, e com custos 2x fica certamente negativo.
2. **Cauda e notícia.** Sem os 5 maiores trades, o bruto vai a ~0,5 bp. O lucro bruto vem de poucos dias de reversão forte, e as perdas grandes vêm dos dias de tendência (notícia de preço de combustível), justamente quando vender o movimento é mais perigoso. Os resultados de 2026 são pouquíssimos dias e não contam.
3. **Sobreposição com a 003 invertida e evidência contrária em BBAS3.** No meio-dia, um preço longe da VWAP é parecido com o sinal da 003 com o lado trocado, e o validador pediu para não minerar a inversão. A diferença é que aqui o gatilho é a distância até a VWAP, em qualquer horário entre 11h e 15h30, e não o movimento desde a abertura às 12h. Mesmo assim a correlação entre os dois sinais deve ser alta, e o validador deve medi-la. Além disso, em BBAS3 (`explore_002b.py`) a reversão de desvios extremos da VWAP segurada até o fechamento **perdeu** (−6 a −7 bp). Se o efeito existisse de forma geral, deveria aparecer lá também.

## Por que é conservadora
Uma entrada por dia, no miolo do pregão, longe dos leilões. O stop é proporcional à volatilidade já conhecida (`adr` de 20 dias), e o tamanho é calculado para que um stop custe ~0,8% do capital, ou no máximo ~0,95% com os custos. Esse é o mesmo envelope que, na 003, entregou perdas de stop de R$ 766 a 976, sem `stop_both` e sem gap além do stop. A grade só mexe no envelope de risco, com 3 tentativas, e o sinal está congelado. Um gestor de risco aprovaria porque o pior dia normal é conhecido de antemão. Ele só deve exigir atenção ao risco de gap de notícia, que é inerente a quem vende o movimento.

## Origem
Primeira ideia da família "reversão à VWAP / provisão de liquidez" em VBBR3. A explicação econômica é plausível, mas não está demonstrada. Quem empurra o preço para longe da VWAP é, em geral, uma ordem grande e impaciente, que paga impacto. O impacto temporário tende a ser devolvido (Kyle, 1985; Hendershott e Menkveld, 2014, sobre "price pressures"). Do outro lado ficam os algoritmos de execução institucionais com referência na VWAP, que compram abaixo e vendem acima dela durante o resto do dia. Não há nota em `knowledge/` (a pasta `knowledge/notas` está vazia).

Ela não segue a sugestão 2 do validador da 003 ("testar reversão num terceiro ativo nunca olhado"), porque o orquestrador pediu VBBR3. Por isso a sobreposição com a 003 invertida está declarada acima.

Tentativas escondidas nesta iteração (todas em `store.load("VBBR3", "M5")`, amostra de pesquisa até 19/01/2026):
1. `research/scratch/explore_004.py`: fade de choques de liquidez numa barra (|retorno da barra| > z × mediana do horário, com e sem volume da barra > 2x a mediana do horário), com saída em 30 ou 60 min. São **8 variações**, com bruto de −1,4 a +6,7 bp, todas abaixo do custo. A melhor (z > 4, volume > 2x, 60 min) foi positiva em todos os anos, mas com metade do custo. Descartado.
2. `research/scratch/explore_004b.py`: reversão de `|dev| > 0,35` ou `> 0,5` `adr` em relação à VWAP diária, com saída em 60 min ou no fechamento. São **4 variações**, com bruto de 3,4 a 12,6 bp. A escolhida é `0,5` até o fechamento, que foi a melhor das quatro (viés de seleção).
3. `research/scratch/explore_004c.py`: reversão diária do retorno do dia anterior (|z| > 1, 1,5 ou 2), operada das 10:30 ao fechamento. São **3 variações**, com bruto de −0,6 a 6,8 bp e 2023 muito negativo. Descartado.
4. `research/scratch/explore_004d.py`: pullback à VWAP diária a favor da tendência da VWAP semanal, com saída em 60 min ou no fechamento. São **2 variações**, com bruto de −0,1 e −8,6 bp. Descartado.

Total desta iteração: **17 tentativas escondidas**. Somadas às ~14 escondidas e às 3 registradas da 003, VBBR3 M5 chega a **~34 tentativas efetivas** mais as 3 desta grade, ou seja ~37. O DSR deve ser lido com esse n.

**Nota para o orquestrador:** nenhuma das sete famílias olhadas em VBBR3 M5 (ORB, gap, momentum do meio-dia, choque de barra, reversão à VWAP, reversão diária, pullback com VWAP semanal) passou de ~13 bp brutos por trade, contra um custo de ~14 bp. Se esta hipótese for rejeitada, recomendo **encerrar o day trade em VBBR3 M5** em vez de gastar as iterações 3 a 5 do ciclo. O custo de um tick de R$ 0,01 num ativo de ~R$ 21 é uma barreira estrutural, e cada nova tentativa só aumenta a mineração.

Relatório: reports/20261023-203818_reversao_esticamento_vwap_VBBR3_M5
