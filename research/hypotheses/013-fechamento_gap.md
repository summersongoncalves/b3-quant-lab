# 013 · Fechamento do gap de abertura no WDO: vender o gap de alta (comprar o de baixa) às 09:15, stop atrás da faixa dos 15 primeiros minutos, alvo no fechamento anterior
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: price_action
- Estado: REJEITADA

## Padrão
No mini dólar, quando o pregão abre afastado do fechamento do pregão anterior por um gap moderado (de 0,15 a 0,8 `adr`), o preço tende a voltar até o fechamento anterior, o nível de referência mais próximo, com mais frequência do que rompe a faixa dos primeiros 15 minutos no sentido do gap. O sinal é o **gap de abertura**, uma informação da noite, e não a excursão da manhã: ele fica definido antes da primeira negociação e não depende do que o preço faz depois da abertura.

## Regras
Barras de 5 min rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra de sinal.

Definições:
- Só operar dias cuja primeira barra é a das **09:00** e que têm as barras 09:00, 09:05 e 09:10.
- `pc` (fechamento anterior) = `close` da última barra do pregão anterior.
- `abertura` = `open` da primeira barra do dia.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico ou sem pregão anterior não operam.
- `g` = (`abertura` − `pc`) / `adr`.
- **Exclusão da rolagem**: não operar nos **2 últimos dias úteis (segunda a sexta) de cada mês**, calculados só pelo calendário: o dia é excluído se `data ≥ BMonthEnd(data) − 1 BDay` (pandas `offsets.BMonthEnd(0)` e `offsets.BDay(1)`). É nessa janela que a série contínua WDO$N troca de vencimento. Na amostra, o gap médio nesses dias é de +11,7 pontos (o carrego de ~1 mês), contra −0,6 nos demais, então o "gap" ali é artificial. A regra não usa feriados nem dados futuros.
- `OR_max` / `OR_min` = máxima e mínima das barras 09:00, 09:05 e 09:10 (os 15 primeiros minutos).
- Barra de sinal = a barra rotulada **09:10** (fecha às 09:15).

Entrada (no máximo 1 por dia, só nesta barra):
- Condição de gap: `g_min ≤ |g| ≤ 0,8`.
- `lado` = −1 (vendido) se `g > 0`; +1 (comprado) se `g < 0`.
- `alvo_dist` = (`pc` − `close`) × `lado`, com o `close` da barra 09:10. Se `alvo_dist < 0,10 × adr` (o gap já fechou, ou falta quase nada), o dia não opera.
- Posição alvo = `lado` (1 contrato), definida no fechamento da barra 09:10 e executada na abertura da barra 09:15, pela convenção do motor. A posição alvo fica igual a `lado` até o fim do pregão, para o motor não reentrar depois de uma saída por stop ou alvo.
- Nenhuma entrada em outro horário.

Saída:
- Stop loss e stop gain fixos (abaixo), calculados na barra de sinal.
- Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato, e o tick vale 0,5 ponto (R$ 5). Os valores típicos abaixo são da combinação padrão (`g_min` = 0,15, `b` = 0,10), medidos na amostra de pesquisa (248 sinais). O range mediano de uma barra M5 entre 09:15 e 12:00 é de 6,0 pontos, e entre 09:00 e 09:10 é de 9,5.

- **Stop loss** (atrás da estrutura que invalida a ideia): se o preço passa do extremo dos 15 primeiros minutos no sentido do gap, o mercado está fazendo "gap and go", e não fechamento de gap.
  - Nível: `OR_max + b × adr` no vendido e `OR_min − b × adr` no comprado.
  - Distância passada ao motor: `stop = max(|nível − close|, 0,20 × adr)`, com o `close` da barra 09:10. O piso de 0,20 adr (~11,5 pontos, ~2 ranges de barra) é fixo e protege contra o stop dentro do ruído; ele vale em ~46% dos sinais com `b` = 0,10 e ~19% com `b` = 0,15.
  - Mediana de **13,0 pontos, ou ~26 ticks e ~R$ 130 por contrato** (~2,2 ranges de barra). p10 de 8,6 pontos, p90 de 20,9, máximo de ~39,6.
  - Com `b` = 0,15, a mediana vai a 15,0 pontos (30 ticks, R$ 150).
- **Stop gain** (próximo nível): o fechamento do pregão anterior. Distância `alvo = alvo_dist = |pc − close|`.
  - Mediana de **18,0 pontos, ou ~36 ticks e ~R$ 180 por contrato**. p10 de 8,5 e p90 de 34,7 pontos. Alvo/stop mediano de 1,39.
  - Com `g_min` = 0,25, o alvo mediano sobe para 21,2 pontos (42 ticks).
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) mais emolumentos de 2 × R$ 1,20 (0,24 ponto). Dá **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**.
  - **Alvo/C ≈ 14,5x** na mediana; nenhum sinal tem alvo menor que 3 × C (o corte de 0,10 adr ≈ 5,7 pontos ≈ 4,6 C garante isso).
- **Acerto de equilíbrio** do bracket, com medianas: `p* = (S + C) / (T + S) = (13,0 + 1,24) / (18,0 + 13,0) ≈ 46%`. Nas outras combinações, p* vai de 42% (`g_min` 0,25, `b` 0,10) a 49% (`g_min` 0,15, `b` 0,15).
- **Taxa de acerto esperada**: ~48 a 52% dos trades resolvidos no alvo, contra ~40% de um passeio aleatório com a mesma geometria (S/(S+T) = 0,40 na combinação padrão). Os motivos:
  - o leilão de abertura do WDO concentra numa só cruzada as ordens da noite (reação ao DXY e ao câmbio de emergentes, stops, ordens a mercado de quem não opera fora do horário). Esse é um choque de liquidez, e não só de informação: os provedores de liquidez locais (tesourarias, exportadores vendendo a alta, importadores comprando a queda) absorvem o desequilíbrio e são pagos com a reversão parcial (Grossman & Miller, 1988);
  - o fechamento anterior é o nível onde ficou o último consenso de preço e para onde muitos alvos de quem opera gap apontam;
  - a 008 e a 012 mostraram que, *depois* da abertura, o dólar M5 não tem persistência nem reversão da excursão. O gap é um tipo de informação diferente, anterior à abertura, e é o único do repertório clássico ainda não testado no laboratório.

  É um palpite moderado: a folga sobre o passeio aleatório precisa ser de ~6 a 8 pontos percentuais só para empatar. Se a taxa ficar perto de 40%, a ideia é ruído.
- **Perda máxima por trade, custos incluídos**:
  - no stop mediano, ~R$ 143, ou **~0,14% de R$ 100 mil**;
  - no p90, ~R$ 222 (0,22%);
  - no pior stop da amostra, ~R$ 408 (0,41%); com `b` = 0,15, ~R$ 446.

  O trade atravessa a janela de dados dos EUA às 09:30 (horário de verão americano) ou 10:30. Uma barra que abre além do stop sai na abertura e pode piorar a perda. O validador deve medir os gaps além do stop e a fração das perdas nessas barras.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: medi só um benchmark sem lado: nos mesmos dias de sinal, com lado sorteado, as mesmas distâncias e entrada na abertura das 09:15, o resultado até o fim do pregão foi de ~45% no alvo, ~52% no stop e ~4% sem tocar nenhum dos dois (combinação padrão). A geometria se resolve quase sempre dentro do pregão, então o problema do ciclo VBBR3 (alvo inatingível, tudo saindo no fechamento) não se aplica aqui. Se houver vantagem, espero **~45 a 52% de saídas no alvo**, ~45% no stop e ~4% no fechamento. Abaixo de 40% no alvo, não há efeito.
- **Entradas por dia**: no máximo 1, só às 09:15. A entrada fica depois do leilão de abertura e das três primeiras barras, as mais largas do dia (9,5 pontos de range mediano). Não há entrada à tarde nem perto do call de fechamento.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| `g_min` (gap mínimo, em adr) | 0,15 | 0,15 · 0,25 |
| `b` (folga do stop além da faixa dos 15 min, em adr) | 0,10 | 0,10 · 0,15 |
| `g_max` (gap máximo, em adr) | 0,8 | fixo |

**Grade total: 4 combinações.** Ficam fixos: `g_max` = 0,8 (gaps maiores são de notícia e tendem a seguir; são ~2% dos dias), barra de sinal 09:10, faixa dos 15 primeiros minutos, alvo no fechamento anterior, piso do stop de 0,20 adr, corte de alvo menor que 0,10 adr, exclusão dos 2 últimos dias úteis do mês, `adr` de 20 pregões e 1 contrato.

Sinais por combinação (descritivo): `g_min` = 0,15 dá ~248 (54 em 2023 desde abril, 93 em 2024, 92 em 2025, 9 em 2026); `g_min` = 0,25 dá ~134 (33, 52, 48, 1). Os lados são os do gap, que na amostra é simétrico (gap mediano de −0,25 ponto fora da rolagem).

Critérios prévios de sucesso, além dos `GATES`:
1. Líquido médio por trade positivo em 2024 e em 2025, cada ano separadamente.
2. Resultado positivo sem os 10 maiores trades e também sem os 20 maiores.
3. Pelo menos 3 das 4 combinações com Sharpe positivo.
4. Acerto entre trades resolvidos acima do benchmark de lado aleatório com a mesma geometria (S/(S+T)) por pelo menos 5 pontos percentuais.
5. Resultado reportado separado entre gaps de alta e de baixa, e entre dias com e sem divulgação dos EUA às 09:30/10:30, se o validador conseguir montar esse corte. Se todo o lucro vier de um lado só, ou só de dias de notícia, isso precisa aparecer no relatório.
6. Correlação diária com a 008 e a 012 nos dias em comum reportada.

## Por que pode falhar
- **O gap no dólar é informação, não desequilíbrio.** O WDO abre depois de uma noite em que o DXY e o câmbio de emergentes já andaram. Se o gap só incorpora esse preço "justo", não há o que fechar, e a ideia vira um passeio aleatório com custo, como as 008 a 012.
- **Stop curto na janela mais volátil.** O stop mediano de ~2 barras e a entrada antes das 09:30 deixam o trade exposto às divulgações americanas e ao ruído da primeira hora. O piso de 0,20 adr ajuda, mas os stops podem virar moeda ao ar e haver gaps de barra além do stop.
- **Poucos trades e um fechamento anterior frágil.** São ~250 sinais na melhor combinação e ~130 na outra, e 2026 quase não tem sinais. O último `close` do pregão anterior (18:25) é de um horário de liquidez baixa, e o nível que o mercado realmente olha pode ser o ajuste (~16:00). Se o efeito existir no ajuste e não no último negócio, esta regra o mede mal.

## Por que é conservadora
Cada trade tem perda definida antes da entrada, atrás de uma estrutura objetiva (a faixa dos 15 minutos), de ~0,14% do capital na mediana e menos de 0,5% no pior caso da amostra, com 1 contrato e 1 entrada por dia. O alvo é um nível conhecido e próximo, que a geometria mostra ser atingível dentro do pregão em quase todos os trades. Os dias de rolagem e os gaps de notícia (acima de 0,8 adr) ficam fora, e a grade tem só 4 combinações.

## Origem
Estratégia conhecida, adaptada ao WDO:
- **Gap fill / fade do gap**: literatura de varejo de futuros de índice e de câmbio (citada de memória), em que gaps pequenos e moderados tendem a voltar ao fechamento anterior e gaps grandes tendem a seguir.
- **Base acadêmica da reversão depois da abertura**, citada de memória: Grossman & Miller (1988), *Liquidity and market structure* (provisão de liquidez paga pela reversão de choques de fluxo); Berkman, Koch, Tuttle & Zhang (2012), *Paying attention: overnight returns and the hidden cost of buying at the open*; Lou, Polk & Skouras (2019), *A tug of war: overnight versus intraday expected returns*. As duas últimas mostram que o retorno da noite e o do pregão tendem a ter sinais opostos.
- **Stop atrás da faixa de abertura**: peça do *opening range* de Crabel (1990), usada aqui como invalidação (o rompimento da faixa no sentido do gap é o "gap and go"), e não como gatilho. A tipologia de abertura em relação ao valor anterior vem de Dalton, *Mind Over Markets* (de memória).

É a primeira hipótese de gap do laboratório. O ciclo 2210 do WDO descartou o "fade do gap" como "a inversão da 008 com outro nome". Não concordo: a 008 mede a excursão a partir da abertura, das 09:00 às 10:30, e o gap é o movimento anterior à abertura. O sinal desta hipótese fica definido antes do primeiro negócio, e o critério 6 pede a correlação com a 008 e a 012 para checar isso. O ciclo também apontou que a rolagem distorce os níveis do dia anterior. A exploração confirmou que a rolagem da série WDO$N cai no fim do mês, e não no 1º dia útil, e a regra exclui essa janela só pelo calendário.

Exploração descritiva, sem P&L com o lado do sinal (`research/scratch/explore_013.py` e `explore_013b.py`):
- distribuição de |g|: mediana de 0,157 adr, p90 de 0,43 e p95 de 0,57; maiores gaps em 05/08/2024 (1,9 adr) e 06/11/2024 (1,6 adr), dias de notícia;
- localização da rolagem: gap médio de +21,6 pontos no último dia útil do mês e |g| mediano de 0,44 nesse dia, contra ~0,15 nos outros;
- range das barras por horário, frequência de sinais por ano, distâncias de stop e alvo e uso do piso para 6 combinações (`g_min` 0,15/0,20/0,25 × `b` 0,05/0,10 e depois 0,10/0,15);
- benchmark de lado sorteado, nos mesmos dias e com as mesmas distâncias, para medir se o alvo é atingível. Ele mistura os dois lados e não revela o resultado do lado do sinal.

Tentativas escondidas: **~2**. O piso do stop passou de 0,15 para 0,20 adr e a grade de `b` passou de {0,05; 0,10} para {0,10; 0,15}, porque com os valores iniciais o stop mediano ficava em ~1,7 range de barra. As duas escolhas foram feitas pela geometria, sem resultado com lado, mas o benchmark de lado sorteado usou os dias de sinal. Somando com as ~19 efetivas de WDO_N_M5, o dataset chega a ~21 antes desta validação.

## Notas de implementação
- Stop e alvo são níveis absolutos na hipótese; o motor pede distâncias a partir da entrada. Foram passadas como distâncias calculadas no `close` da barra 09:10 (aproximação: a entrada real é a abertura das 09:15, que pode diferir do `close`).
- Stop = `max(|nível − close|, 0,20 × adr)` e alvo = `(pc − close) × lado`; se alguma distância for ≤ 0 (ou o alvo < 0,10 adr), o dia não opera.
- `pc` = `close` da última barra do dia anterior (shift diário); `adr` = média de (máx − mín) dos 20 pregões anteriores (shift diário).
- Exclusão dos 2 últimos dias úteis do mês: `data >= data + BMonthEnd(0) − BDay(1)`, só pelo calendário de dias de semana (sem feriados e sem olhar datas do dataset). Em meses cujo último dia útil real é feriado, a janela pode deslocar um dia.
- A posição fica igual a `lado` até o fim do pregão (ffill por dia) para o motor não reentrar após stop ou alvo.

Relatório: reports/20261023-224936_fechamento_gap_WDO_N_M5
