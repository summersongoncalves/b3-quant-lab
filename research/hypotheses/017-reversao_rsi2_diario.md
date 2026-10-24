# 017 · Lado do dia contra o extremo de dois pregões no WDO: RSI(2) diário de Connors como viés, entrada às 10:15 e bracket proporcional ao adr
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: direcional
- Estado: REJEITADA

## Padrão
Quando o dólar fecha dois ou três pregões seguidos esticado para um lado (RSI de 2 períodos dos fechamentos diários, ajustados pela rolagem, abaixo de 10 ou acima de 90), o pregão seguinte tende a devolver parte do esticamento. Esperamos que, comprando depois de extremos de baixa e vendendo depois de extremos de alta, com entrada às 10:15, o preço chegue a 1,5 vez a distância do stop com mais frequência do que a geometria neutra (~40% entre os resolvidos com `s` = 0,25).

A diferença em relação ao que já foi testado no WDO M5 é a **fonte e o sentido do lado**. Nas 008, 012, 013 e 014 o lado vinha do próprio pregão. Na 015 vinha da semana e era a favor da tendência. Na 016 vinha do WIN. Aqui o lado vem dos **dois ou três pregões anteriores** e é **contra** o movimento recente. É reversão de curto prazo na escala de dias, e não intradiária.

## Regras
Barras de 5 min, rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra de sinal, com dados até ela.

Definições diárias (só pregões passados):
- Só operar dias cuja primeira barra começa até **09:05**.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`).
- **Janela de rolagem** (só pelo calendário, como na 013, 014 e 015): `roll(d)` = `d ≥ d + BMonthEnd(0) − BDay(1)` (os 2 últimos dias úteis do mês). Dias com `roll(d)` **não operam**.
- **Variação diária ajustada pela rolagem** (a mesma da 015): `delta(d) = close(d) − close(d−1)`, **exceto** quando `roll(d)` ou `roll(d−1)` for verdadeiro. Nesses dias usa-se só a parte intradiária, `delta(d) = close(d) − open(d)`. O fechamento do dia é o `close` da última barra do pregão, e a abertura é o `open` da primeira. O primeiro dia do dataset tem `roll(d−1)` tratado como verdadeiro.
- **RSI(2) de Wilder sobre `delta`**: `up = max(delta, 0)`, `dn = max(−delta, 0)`; `au` e `ad` = médias exponenciais com `alpha = 1/2` (`ewm(alpha=0.5, adjust=False)`); `rsi = 100 × au / (au + ad)`. O valor usado no dia d é o do fechamento de d−1 (`shift(1)`). Os 25 primeiros pregões do dataset não operam (aquecimento do `adr` e do RSI).
- **Viés do dia**: `vies = +1` (comprado) se `rsi ≤ 10`; `vies = −1` (vendido) se `rsi ≥ 90`. Caso contrário o dia não opera.

Entrada (no máximo 1 por dia):
- Sinal no fechamento da barra rotulada **10:10**. Execução na abertura da barra **10:15**, pela convenção do motor. Se o dia não tiver a barra 10:10, não opera.
- A posição alvo é `vies` (1 contrato) da barra 10:10 até o fim do pregão (ffill por dia), para que o motor não reentre depois de uma saída por stop ou alvo.
- Não há filtro intradiário de entrada. O lado é decidido antes da abertura, e a hora fixa evita escolher o preço olhando o pregão.

Saída:
- Stop loss e stop gain fixos (abaixo), calculados na barra de sinal. Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato; tick = 0,5 ponto (R$ 5). Números da amostra de pesquisa (621 dias válidos, sem holdout, sem P&L): nos 155 dias de sinal, o `adr` mediano é **58,8 pontos** (p90 77,0; máximo 100,4), e o range mediano de uma barra M5 entre 10:15 e 16:00 é **4,5 pontos** (média 5,2).

- **Stop loss**: `stop = s × adr`, a partir do preço de entrada, fixo.
  - `s` = 0,25 (padrão): mediana de **14,7 pontos, ~29 ticks, ~R$ 147 por contrato**, ~3,3 ranges de barra.
  - `s` = 0,30: 17,6 pontos (~35 ticks, ~R$ 176). `s` = 0,35: 20,6 pontos (~41 ticks, ~R$ 206).
- **Stop gain**: `alvo = 1,5 × stop`, fixo. Com `s` = 0,25, a mediana é de **22,1 pontos, ~44 ticks, ~R$ 221 por contrato** (0,375 adr).
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) mais emolumentos de 2 × R$ 1,20 (0,24 ponto) dá **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**. **Alvo/C ≈ 18x** com `s` = 0,25 (≈ 21x com 0,30 e ≈ 25x com 0,35). Todos bem acima de 3x.
- **Acerto de equilíbrio**: `p* = (S + C)/(T + S)`:
  - `s` = 0,25: (14,7 + 1,24)/36,8 ≈ **43,4%**;
  - `s` = 0,30: (17,6 + 1,24)/44,1 ≈ **42,7%**;
  - `s` = 0,35: (20,6 + 1,24)/51,5 ≈ **42,4%**.

  A geometria neutra (os dois lados, nos mesmos dias e com as mesmas distâncias) dá **40%, 38% e 35%** de alvo entre os resolvidos. Para empatar, o viés precisa acrescentar ~3,5, ~5 e ~7,5 pontos percentuais. Por isso o padrão é `s` = 0,25.
- **Taxa de acerto esperada**: ~45 a 47% entre os resolvidos com `s` = 0,25. É um palpite moderado, com três argumentos:
  - **Contraparte natural no dólar-real.** Depois de dois ou três dias de alta forte, o exportador vende o dólar caro (internalização de receita), e o Banco Central costuma agir (leilões de swap cambial e de linha) justamente em sequências de alta. Depois de quedas fortes, o importador e quem paga dívida externa compram barato. Esses participantes são responsivos ao preço, e não ao momentum (Kohlscheen & Andrade, 2014, e Chamon, Garcia & Souza, 2017, sobre o efeito das intervenções do BCB; citados de memória).
  - **Reversão de curto prazo depois de extremos do RSI(2)** é a estratégia de Connors & Alvarez, com acerto historicamente alto em índices de ações. Em câmbio ela é menos documentada, por isso é hipótese, e não verdade.
  - **Um rastro no próprio laboratório, declarado.** Na 015, o filtro de tendência de 5 pregões (a favor da semana) deixou o acerto **abaixo** do controle (36% contra 39%). É pouco, cerca de 1 erro-padrão, e não justifica a hipótese sozinho, mas aponta para o mesmo lado: em vários dias, o dólar reverte mais do que continua.

  Se o acerto ficar perto de 40%, a escala de dias também não dá direção ao intradiário do WDO, e isso fecha a última fonte de lado "do próprio WDO" que o laboratório ainda não testou.
- **Perda máxima por trade, custos incluídos**: no stop mediano (`s` = 0,25), ~15,9 pontos, **~R$ 159, ou ~0,16% de R$ 100 mil**. No pior caso da amostra (`s` = 0,35, `adr` = 100,4), ~36,4 pontos, **~R$ 364 (0,36%)**. A entrada às 10:15 já passou dos dados americanos das 09:30 e 10:00 e da primeira janela da PTAX (10:00 a 10:10), mas ainda pegam as janelas das 11:00, 12:00 e 13:00 e os dados das 10:30. Uma barra que abre além do stop sai na abertura e pode piorar a perda, e o validador deve medir esses gaps.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: medi só a geometria **neutra** (os dois lados, entrada na abertura das 10:15, até o fim do pregão), sem o lado do sinal:

  | `s` | alvo | stop | fechamento |
  |---|---|---|---|
  | 0,25 | 36% | 55% | 9% |
  | 0,30 | 32% | 52% | 16% |
  | 0,35 | 25% | 47% | 28% |

  Com a vantagem esperada, ~39 a 42% de saídas no alvo com `s` = 0,25, e só ~9% dos trades chegam ao fechamento sem se resolver. O alvo (0,375 adr) é atingível: o movimento mediano sem sinal entre a entrada e o fechamento é de 0,30 adr, e há ~8 horas de pregão pela frente. O problema do ciclo VBBR3 não se repete.
- **Entradas por dia**: no máximo 1, sempre às 10:15. Ficam proibidos o leilão e a primeira hora e quinze (dados dos EUA das 09:30 e 10:00, primeira janela da PTAX), qualquer entrada depois das 10:15 e os dias da janela de rolagem.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| `s` (stop em fração do adr) | 0,25 | 0,25 · 0,30 · 0,35 |
| `k` (alvo em múltiplos do stop) | 1,5 | fixo |
| `lim` (limiar do RSI(2): comprado se ≤ `lim`, vendido se ≥ 100 − `lim`) | 10 | fixo |

**Grade total: 3 combinações**, variando só o tamanho do stop. O limiar 10/90 e o período 2 são os valores padrão de Connors & Alvarez, e não foram otimizados. Ficam fixos também: `adr` de 20 pregões, horário de entrada 10:15, ajuste e exclusão da rolagem pelo calendário e 1 contrato.

Sinais (descritivo): **155 dias**, sendo 45 em 2023 (desde abril), 44 em 2024, 57 em 2025 e 9 em 2026; 91 comprados (59%) e 64 vendidos. Em 45% dos dias de sinal o pregão anterior também foi sinal do mesmo lado (extremos persistentes), o que concentra parte dos trades em sequências.

Critérios prévios de sucesso, além dos `GATES`:
1. Líquido médio por trade positivo em 2024 e em 2025, cada ano separadamente.
2. Resultado positivo sem os 10 maiores trades e também sem os 20 maiores.
3. As 3 combinações com Sharpe do mesmo sinal, e pelo menos 2 positivas.
4. Acerto entre os resolvidos pelo menos 4 pontos percentuais acima da geometria neutra com `s` = 0,25 (~40%).
5. **Controles do lado**, nos mesmos 155 dias e com o mesmo bracket: (a) lado **a favor** do extremo (momentum); (b) lado sorteado. A hipótese só se sustenta se o contrário der resultado claramente pior que o principal e o sorteado ficar no meio.
6. Resultado separado entre comprados e vendidos e por ano. Se todo o lucro vier de vender o dólar, ou de um só período (ex.: a alta do fim de 2024 e a volta no começo de 2025), isso tem de aparecer.
7. Resultado separado entre o **primeiro** dia de extremo e os dias de extremo **persistente** (o pregão anterior também era sinal). Se todo o lucro vier dos persistentes, o efeito depende de poucas sequências.
8. Correlação diária com a 015 (sentido oposto, por construção, nos dias em comum) e com a 016, e o número de dias em comum.

## Por que pode falhar
- **O extremo de dois dias continua, em vez de reverter.** O momentum de câmbio documentado (Menkhoff et al., 2012) puxa para o outro lado. Em choques de risco (eleição, fiscal, tarifas), o dólar sobe vários dias seguidos e o RSI(2) fica acima de 90 durante a sequência inteira. Vender nesse regime perde várias vezes seguidas. O critério 7 existe para medir isso.
- **A reversão acontece no overnight, e não no pregão.** Se a devolução vier no gap de abertura (o exterior corrige à noite), às 10:15 ela já está no preço e sobra só ruído. A entrada fixa não captura o gap, de propósito, porque não há como operar o leilão de forma conservadora.
- **Poucos trades e dependência de regime.** São ~155 trades em menos de três anos, com 59% de compras. Alguns meses de dólar em faixa (reversão funciona) contra meses de tendência (reversão perde) podem decidir tudo. E o rastro da 015 que motiva parcialmente o sentido é de ~1 erro-padrão: pode ser só ruído.

## Por que é conservadora
O lado é decidido antes da abertura, a entrada é numa hora fixa e longe do leilão, e a perda é fixa e conhecida, ~0,16% do capital na mediana e no máximo ~0,36%, com 1 contrato e 1 entrada por dia, sem preço médio. A grade tem só 3 combinações, com todos os parâmetros de sinal nos valores padrão de mercado, e ~90% dos trades se resolvem dentro do pregão. Operar contra o extremo de dois dias tem contraparte conhecida (exportador, importador, BC), e o stop de 0,25 adr limita o dano quando a sequência continua.

## Origem
Estratégia conhecida, adaptada (fontes citadas de memória):
- **Sinal**: Connors & Alvarez (2009), *Short Term Trading Strategies That Work*, RSI(2) com limiares 10/90 nos fechamentos diários. O original é swing (entra no fechamento e sai quando o preço volta à média de 5 dias). Aqui o RSI(2) diário vira o **viés do dia** de um day trade, sem o filtro da média de 200 dias (o dólar não tem tendência secular que justifique o filtro, e ele cortaria metade dos sinais).
- **Envelope de risco e entrada em hora fixa**: geometria `alvo = 1,5 × stop` com grade só no stop (014 e 015); entrada depois da primeira hora para fugir do leilão e dos dados americanos.
- **Contexto econômico**: intervenções do BCB no câmbio (Kohlscheen & Andrade, 2014; Chamon, Garcia & Souza, 2017) e o fluxo responsivo de exportadores e importadores, a mesma contraparte invocada na 012, mas aqui na escala de dias.
- **Peças do laboratório**: variação diária ajustada pela rolagem e exclusão da rolagem pelo calendário, exatamente como na 015.

Não é refinamento da 016 e não usa o corte pós-resultado dela. A escolha do sentido contrário foi **em parte informada pelo resultado da 015** (filtro de tendência abaixo do controle), e isso conta como tentativa escondida.

Exploração descritiva, sem P&L com o lado do sinal (`research/scratch/explore_017.py`):
- distribuição do RSI(2) diário ajustado pela rolagem (mediana 44; p10 7,4; p90 90,4) e frequência de sinais com os limiares 10/90 (155), 5/95 (80) e 20/80 (280), por ano e por lado;
- fração de extremos persistentes (45%), `adr` e range das barras nos dias de sinal, movimento sem sinal da entrada ao fechamento (0,30 adr);
- geometria neutra (os dois lados) para `s` = 0,25, 0,30 e 0,35 com `k` = 1,5, só para dimensionar stop e alvo.

Tentativas escondidas: **~3**. O sentido contrário foi influenciado pela 015, o limiar 10/90 foi escolhido entre três olhando só a frequência (e é o padrão de Connors), e a grade de `s` foi escolhida pela geometria neutra. Nada calculou resultado com o lado do viés. Somadas às tentativas efetivas anteriores do WDO_N_M5 (~29 antes da 015, mais as da 015 e da 016), o dataset deve estar por volta de ~36 a 38 antes desta validação, ainda abaixo do teto de ~50.

## Notas de implementação
- Reaproveitar da 015 o cálculo de `adr`, `roll(d)` e `delta(d)` (mesmas regras, mesmos `shift`).
- RSI: `ewm(alpha=0.5, adjust=False)` sobre `up` e `dn` da série `delta` (com o primeiro valor `NaN` preenchido por 0), depois `shift(1)` por dia. Se `au + ad` = 0, o dia não opera.
- A barra de sinal é a rotulada 10:10. A posição é `vies` dessa barra até a última barra do dia e 0 antes dela.
- `stop = s × adr` e `alvo = k × stop`, em pontos, constantes no dia.
- `k` e `lim` ficam em `params`, fora da `grid`.
- Implementado em `strategies/reversao_rsi2_diario.py`; helper genérico `rsi_from_changes` em `_helpers.py`. Aquecimento: os 25 primeiros pregões (posição na série diária) não operam. Distâncias NaN ou ≤ 0 não geram entrada. O smoke test deu 155 trades, igual à contagem descritiva da hipótese.
Relatório: reports/20261023-232332_reversao_rsi2_diario_WDO_N_M5
