# 018 · Rompimento conjunto da faixa de ruído: dólar e bolsa saem juntos da faixa, em lados opostos, e o WDO segue por até 2 horas
- Dataset: WDO$N M5 (com WIN$N M5 como informação auxiliar, só leitura)
- Modo: daytrade
- Estilo: momentum
- Estado: REJEITADA

## Padrão
Quando o WDO fecha uma barra fora da sua faixa de ruído intradiária (Zarattini, Aziz & Barbon, 2024) **e, na mesma barra, o WIN está fora da faixa dele no lado oposto** (dólar sobe com bolsa caindo, ou o inverso), o movimento é um choque de risco comum aos dois mercados, típico de fluxo estrangeiro, e não um fluxo isolado do câmbio. Esperamos que o WDO continue no lado do rompimento nas 2 horas seguintes com mais frequência que a geometria neutra.

O que se sabe antes do teste, só por estatística descritiva sem lado: depois desses rompimentos, a excursão do WDO em 2 horas é **~28% maior** que numa barra sorteada (0,33 contra 0,26 `adr` na mediana). O combustível existe, ao contrário da 010 (compressão), em que a excursão era igual à do acaso. A pergunta que o validador responde é se a confirmação do WIN dá o **lado**.

## Regras
Barras de 5 min, rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra de sinal, com os mesmos cálculos nos dois ativos e os dados de cada um.

Definições por ativo X ∈ {WDO, WIN}:
- `abertura_X` = `open` da primeira barra do pregão.
- `mv_X(t)` = |`close_X(t)` − `abertura_X`|, em pontos.
- `faixa_X(t)` = média de `mv_X` **no mesmo horário (hh:mm)** nos **14 pregões anteriores** (sem o dia atual; `shift(1)` na tabela dia × horário). Se faltar algum dos 14, a barra não sinaliza. 14 é o parâmetro do artigo e fica fixo.
- `rompe_X(t)` = +1 se `close_X(t)` > `abertura_X` + `faixa_X(t)`; −1 se `close_X(t)` < `abertura_X` − `faixa_X(t)`; 0 nos demais casos.
- `adr_WDO` = média de (máxima − mínima do dia) nos 20 pregões anteriores do WDO (`shift(1)`).

Usar a faixa a partir da **abertura do próprio dia** (sem o ajuste pelo fechamento anterior do artigo) evita o salto de vencimento do WDO e do WIN: nada atravessa a noite, exceto o `adr` e a faixa, que são medidas intradiárias.

Dados do WIN:
- Dentro de `signal_fn`, carregar `store.load("WIN$N", "M5")` (sem `include_holdout`), cortar em `timestamp <= última barra do df do WDO` e alinhar pelo **timestamp exato** da barra. Barra sem correspondente no WIN não sinaliza.
- O `lookahead_check` só trunca o WDO. O implementador deve garantir que, para a barra t do WDO, só barras do WIN com timestamp ≤ t entrem no cálculo, e escrever um teste que trunque os dois (como na 016).

Sinal conjunto:
- `conj(t)` = `rompe_WDO(t)` ≠ 0 **e** `rompe_WIN(t)` = −`rompe_WDO(t)`.
- **Gatilho**: `conj(t)` verdadeiro e `conj(t−1)` falso (a barra anterior do mesmo pregão, calculada sem filtro de horário). Só a transição conta, não o estado.
- Janela da barra de sinal: rotulada de **10:00 a 15:30** (inclusive). Nada antes das 10:00, para fugir do leilão de abertura e da primeira hora de ajuste; nada depois das 15:30, para que as 2 horas de trade caibam antes do call de fechamento.
- **Lado** = `rompe_WDO(t)`: compra se o dólar rompeu para cima (com a bolsa rompendo para baixo), venda no inverso.
- **No máximo 1 entrada por dia**: só o primeiro gatilho do pregão. Depois de uma saída (stop, alvo ou tempo), o dia acabou.
- **Exclusão da rolagem** (só calendário, como em `fechamento_gap.py`): não operar se `data ≥ data + BMonthEnd(0) − BDay(1)`, os 2 últimos dias úteis do mês. Dias sem 20 pregões de `adr` ou sem 14 de faixa não operam. O WIN de pesquisa termina em 04/02/2026: depois disso, não há sinal.

Saída:
- Stop e alvo fixos (abaixo), lidos na barra de sinal.
- **Saída por tempo**: a posição alvo volta a 0 no fechamento da **24ª barra depois da barra de entrada** (2 horas), executado na abertura da seguinte. Momentum que não andou em 2 horas não é momentum. A posição fica 0 até o fim do pregão.
- O que ainda estiver aberto no fim do pregão é zerado pelo motor (não deve acontecer com o corte das 15:30, salvo pregões curtos).

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato, tick = 0,5 ponto (R$ 5). Valores da amostra de pesquisa, sem holdout e sem P&L. Nos dias de sinal, o `adr` mediano é de 55 pontos (p10 41, p90 77). A barra de sinal tem range mediano de 7 pontos, e as 12 barras seguintes têm range mediano de **5,5 pontos** (p90 10,5).

- **Stop loss**: `stop = s × adr_WDO`, a partir da entrada, fixo.
  - `s` = 0,20 (padrão): mediana de **~11 pontos, 22 ticks, R$ 110 por contrato**, 2× o range mediano das barras pós-sinal.
  - `s` = 0,25: ~13,8 pontos, 28 ticks, R$ 138 (2,5× o range mediano).
  - Não uso 0,15 (8 pontos, 1,5 barra): ficaria dentro do ruído de barras que já são mais largas que o normal.
- **Stop gain**: `alvo = 1,5 × stop`, fixo. Com `s` = 0,20: **~16,5 pontos, 33 ticks, R$ 165**. Com 0,25: ~20,7 pontos, 41 ticks, R$ 207.
- **Custo de ida e volta (C)**: 1 tick de slippage por lado mais 2 × R$ 1,20 de emolumentos: **C ≈ 1,24 ponto (~2,5 ticks, R$ 12,40)**. **Alvo/C ≈ 13x** (`s` = 0,20) e **~17x** (0,25). No `adr` p10 com `s` = 0,20, o alvo ainda é de 12,4 pontos, ~10 C.
- **Acerto de equilíbrio entre os resolvidos**, `p* = (S + C) / (T + S)`:
  - `s` = 0,20: (11 + 1,24) / (16,5 + 11) = **44,5%**.
  - `s` = 0,25: (13,8 + 1,24) / (20,7 + 13,8) = **43,6%**.
- **Geometria neutra** (descritiva, média dos dois lados, entrada na abertura da barra seguinte ao gatilho, 306 sinais, horizonte de 24 barras):

  | `s` | alvo | stop | tempo | acerto neutro entre resolvidos |
  |---|---|---|---|---|
  | 0,20 | 26% | 48% | 26% | 35,5% |
  | 0,25 | 19% | 37% | 44% | 34% |

- **Acerto esperado**: ~45% a 47% entre os resolvidos com `s` = 0,20, ou seja, ~10 p.p. acima do neutro. É uma exigência alta, e digo abertamente. O motivo para acreditar: fluxo estrangeiro de realocação entra fatiado ao longo de horas (ordens grandes divididas, Kyle 1985), e quando bolsa e câmbio saem juntos da faixa, o choque é de risco-país e não de um exportador ou do BC, que tendem a ser absorvidos. A saída por tempo também ajuda: os trades que saem por tempo carregam o lado do rompimento, e se o efeito existir, eles terminam levemente a favor. **Se o acerto entre os resolvidos ficar abaixo de ~40%, o efeito não existe e a hipótese cai.**
- **Perda máxima por trade, custos incluídos**: típica de 11 + 1,24 ≈ **R$ 122 (0,12% de R$ 100 mil)** com 1 contrato. No maior `adr` da amostra (~112) com `s` = 0,25: 28 + 1,24 ≈ R$ 293 (0,29%). O risco que passa disso é o gap entre barras: a barra de sinal costuma ser de notícia, e o validador deve medir quantos stops saíram além da distância.
- **Fração esperada de trades que chegam ao alvo em 2 horas**: ~26% com `s` = 0,20 pela geometria neutra; com o efeito, ~30%. Cerca de 1/4 dos trades sai por tempo. Com 0,25, o alvo cai para ~19% e quase metade sai por tempo; por isso o padrão é 0,20.
- **Entradas por dia**: no máximo 1. Nada antes das 10:00 nem com barra de sinal depois das 15:30; a saída por tempo termina até ~17:35, antes do call.
- **Frequência**: **~306 sinais** (71 em 2023 desde abril, 113 em 2024, 111 em 2025, 11 em 2026), cerca de metade dos pregões. 58% das barras de sinal ficam na hora das 10:00, 16% na das 11:00 e o resto espalhado pela tarde.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| s (stop em `adr` do WDO; alvo = 1,5 × stop) | 0.20 | [0.20, 0.25] |
| faixa (pregões da faixa de ruído) | 14 | [14] (fixo, valor do artigo) |
| horizonte (barras até a saída por tempo) | 24 | [24] (fixo) |

São 2 combinações.

## Por que pode falhar
1. **A confirmação do WIN não acrescenta lado.** Na exploração, o rompimento do WDO **sem** o WIN fora da faixa tem a mesma excursão que o conjunto (0,255 contra 0,256 `adr` em 1 hora). O combustível vem do rompimento em si, não da confirmação. Se o lado também não vier, o acerto fica no neutro, como em 008, 012, 013, 014 e 015. É o modo de falha mais provável.
2. **Notícia sem lado.** Muitos gatilhos às 10:00 caem em dias de dado dos EUA às 8:30 ET e na janela de PTAX das 10:00. O dólar anda mais nesses dias, mas pode reverter tanto quanto seguir, e o lucro pode ficar concentrado em poucos dias de choque (ex.: fiscal no fim de 2024). Gaps além do stop são o risco de cauda.
3. **Regime de 2024.** No fiscal de 2024, dólar para cima e bolsa para baixo foi quase uma via de mão única. As compras podem carregar o resultado de um ano só. O validador deve olhar por ano e por lado.

Pré-registro para o validador (antes de qualquer resultado):
- **Acerto entre resolvidos** com `s` = 0,20 ≥ 42%; abaixo de 40%, a hipótese cai.
- **Controle 1, rompimento só do WDO**: mesma regra, mas com o gatilho `rompe_WDO(t)` ≠ 0 e `rompe_WIN(t)` = 0 (o ORB de faixa de ruído do artigo, sem confirmação). Se o controle for igual ou melhor por trade, a confirmação do WIN não serve para nada.
- **Controle 2, rompimento na mesma direção** (`rompe_WIN` = `rompe_WDO`): dias em que dólar e bolsa sobem juntos não são choque de risco. Espera-se resultado pior que o da regra.
- **Concentração**: positiva sem os 10 maiores trades e com 2024 e 2025 positivos.
- **Correlação diária** com a 016, que também usa o WIN para dar o lado do WDO.

## Por que é conservadora
Uma entrada por dia, 1 contrato, stop fixo de ~R$ 122 com custos (0,12% do capital), alvo 13x o custo e saída por tempo em 2 horas, sem reentrada. Só o tamanho do stop varia, em 2 valores; a faixa usa o parâmetro publicado e o horizonte é fixo. Um gestor de risco aprovaria porque a perda é pequena e conhecida, o trade nunca fica parado esperando o fechamento e a regra traz controles que a derrubam se a peça nova (o WIN) não acrescentar nada.

## Origem
Combinação de duas peças publicadas, adaptada ao par WDO/WIN:
- **Faixa de ruído e rompimento intradiário**: Zarattini, Aziz & Barbon (2024), *Beat the Market: An Effective Intraday Momentum Strategy for S&P500 ETF (SPY)*. A faixa é a média do afastamento absoluto em relação à abertura, no mesmo horário, nos 14 dias anteriores. Lá o rompimento é seguido com stop na VWAP ou na faixa; aqui o stop é fixo em `adr` e há saída por tempo, porque o motor exige distâncias fixas. Também segue a linha de Gao, Han, Li & Zhou (2018), *Market intraday momentum*. Citado de memória.
- **Confirmação por outro mercado via fluxo de capital**: Hau & Rey (2006), *Exchange rates, equity prices, and capital flows* (RFS): bolsa local e câmbio se movem juntos pelo rebalanceamento do investidor estrangeiro. A ideia de que fluxo informado entra fatiado e por isso persiste vem de Kyle (1985). Citado de memória.
- **Variação da 016 com diagnóstico**: a 016 foi a única hipótese do WDO acima do sorteio (45,5% contra 37,6%) e também tirava informação do WIN, mas pela **defasagem** (WDO parado). Aqui a informação vem da **concordância**: os dois romperam juntos. Os dias e o mecanismo são outros (momentum, e não convergência), e o validador da 016 desaconselhou refiná-la. Por isso esta é uma hipótese nova, não um refinamento.
- **Diferença em relação à 010**: a 010 olhava compressão com volume e não achou expansão. Aqui não há compressão, e a excursão pós-sinal é maior que a do acaso.

Exploração feita (só descritiva, sem P&L, sem retorno ou MAE/MFE por lado; script em `research/scratch/explore_018.py`):
- Contagem de sinais com janela 09:30 ou 10:00 até 15:30, gatilho por estado ou por transição, conjunto e só do WDO; distribuição por ano e por hora.
- Excursão máxima sem lado em 12 e 24 barras: conjunto 0,256 / 0,329 `adr`, só WDO 0,255 (12 barras), barras sorteadas 0,187 / 0,258.
- Geometria neutra do bracket (média dos dois lados) com `s` ∈ {0,15; 0,20; 0,25} e horizontes de 12 e 24 barras; range das barras de sinal e pós-sinal; `adr` nos dias de sinal.
- As escolhas (início às 10:00, gatilho por transição, horizonte de 24 barras, `s` sem 0,15) foram feitas por frequência, risco de leilão, alcance do alvo e range de barra, nunca por resultado com lado.

**Tentativas escondidas**: nenhuma com resultado com lado. Pelo critério das hipóteses anteriores, registro **2** tentativas escondidas, pela escolha entre 2 janelas, 2 gatilhos e 2 horizontes olhando frequência e geometria neutra. WDO_N_M5 deve ficar perto de ~40 tentativas efetivas depois desta, ainda abaixo de ~50.

## Notas de implementação
- Saída por tempo: a posição fica no lado do rompimento nas barras t..t+23 (a barra de sinal t e mais 23), e vale 0 a partir de t+24 (no mesmo pregão). Com entrada na abertura de t+1 e saída na abertura de t+25, o trade dura 24 barras. Stop e alvo ficam constantes nas barras em que a posição está ligada e NaN depois.
- Faixa: tabela dia × horário do `mv`, média móvel de 14 linhas com `shift(1)`; se qualquer um dos 14 pregões não tiver a barra daquele horário (ou o WIN não tiver a barra), a barra não sinaliza.
- Gatilho: `conj(t-1)` é a barra anterior do WDO no mesmo pregão (sem filtro de horário); barra anterior inexistente conta como falso. O primeiro gatilho do pregão é o primeiro dentro da janela 10:00 a 15:30.
- Distâncias ≤ 0 ou `adr` ausente não entram. Rolagem por calendário (BMonthEnd/BDay), como em `fechamento_gap.py`.
- Verificação: 306 entradas (igual à contagem da exploração); teste de truncamento conjunto de WDO e WIN em 25 pontos, 0 divergências.
Relatório: reports/20261023-233210_rompimento_ruido_conjunto_WDO_N_M5
