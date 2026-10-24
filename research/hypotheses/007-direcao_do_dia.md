# 007 · Direção do dia: seguir a excursão da manhã às 10:30, com stop atrás da abertura
- Dataset: WIN$N M5
- Modo: daytrade
- Estilo: direcional
- Estado: PROMISSORA

## Padrão
Quando o WIN já se afastou pelo menos 0,3 `adr` da abertura para um lado só até as 10:30, e continua desse lado, o pregão tende a fechar desse mesmo lado. O lado do dia é decidido pela excursão da manhã. A entrada é às 10:30, a favor desse lado, e a posição fica até o fechamento, a menos que o preço atravesse a abertura (ideia errada) ou complete um `adr` inteiro a partir dela (dia esgotado).

Esta hipótese é **pré-registrada**. A regra, o horário, o stop e o alvo foram fixados antes de qualquer conta nova. A única exploração feita depois disso foi descritiva (distâncias e frequência de saídas, sem P&L; ver Origem). Não há grade.

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra de sinal):
- Só operar dias cuja primeira barra começa até **09:30** (mesmo corte da 001 e da 006).
- `abertura` = `open` da primeira barra do dia.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam. Não usa nada entre pregões, então não é afetado pelos saltos de rolagem da série contínua.
- Barra de sinal = a barra rotulada **10:25**, que fecha às 10:30. Se o dia não tiver essa barra, não opera.
- `max_m` / `min_m` = máxima e mínima do dia até a barra de sinal, **incluindo** ela.
- `exc_alta` = `max_m − abertura ≥ 0,3 × adr`. `exc_baixa` = `abertura − min_m ≥ 0,3 × adr`.
- `lado` = +1 se `exc_alta` e não `exc_baixa`; −1 se `exc_baixa` e não `exc_alta`; 0 nos outros casos. Os dias com excursão para os dois lados (27 dos 694) não têm lado definido e não operam.
- Filtro "o lado ainda vale": só operar se `(close − abertura) × lado ≥ 0,1 × adr`, com o `close` da barra de sinal. Se às 10:30 o preço já voltou para perto da abertura, o lado do dia não está mais definido. O filtro também evita stops dentro do ruído de uma barra (ver Risco).

Entrada:
- Posição alvo = `lado` (1 contrato), definida no fechamento da barra 10:25 e executada na abertura da barra 10:30, pela convenção do motor.
- A posição alvo fica igual a `lado` do sinal até o fim do pregão, para que o motor não reentre depois de uma saída por stop ou alvo.
- No máximo 1 entrada por dia. Não há entrada em nenhum outro horário.

Saída:
- Stop loss e stop gain fixos (abaixo), lidos na barra de sinal.
- Sem saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Descritivas da amostra de pesquisa (694 dias válidos, sem P&L): `adr` mediano de ~1.770 pontos; range médio de uma barra de M5 nas 12 barras antes do sinal de ~200 pontos; 456 dias com lado definido às 10:30, dos quais **376 passam no filtro** (~130 por ano, ~54% dos pregões); `|close − abertura|` mediano de 0,32 `adr` nos dias de sinal.

- **Stop loss** (atrás da estrutura): o nível é `abertura − 0,1 × adr` no comprado e `abertura + 0,1 × adr` no vendido. Se o preço atravessa a abertura com folga de 0,1 `adr`, o dia trocou de lado e a ideia está errada. A distância passada ao motor é `stop = (close − abertura) × lado + 0,1 × adr`. Pelo filtro, ela é de no mínimo 0,2 `adr` (~350 pontos). Valores com o filtro: mediana de **~830 pontos, ou ~166 ticks, ~R$ 166 por contrato** (~4,3 ranges de barra), p90 de ~1.410 pontos (~R$ 283) e máximo de ~2.850 pontos (~R$ 571). O pior caso fica em ~1,4 range de barra, mas é raro; a mediana está bem fora do ruído.
- **Stop gain** (dia esgotado): o nível é `abertura + 1,0 × adr` no comprado e `abertura − 1,0 × adr` no vendido. É o ponto em que o dia já andou, a partir da abertura, um range diário médio inteiro. A distância passada ao motor é `alvo = abertura + lado × adr − close`, multiplicada por `lado`. Mediana de **~1.110 pontos, ou ~222 ticks, ~R$ 222 por contrato**. Sinais com alvo ≤ 0 (o dia já passou de 1 `adr` às 10:30) são descartados.
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 5 pontos) mais emolumentos de 2 × R$ 0,25 (= 2,5 pontos). Dá C ≈ **12,5 pontos ≈ 2,5 ticks ≈ R$ 2,50**. **Alvo/C ≈ 89x** na mediana. O custo é ~1,5% do stop e não é o problema.
- **Acerto de equilíbrio** do bracket, com valores medianos: `p* = (S + C) / (T + S) = (830 + 12,5) / (1.110 + 830) ≈ 43%`. Esse p* só vale para os trades que terminam em stop ou alvo. Como ~40% dos trades devem sair no fechamento, a conta que importa é a expectativa: com as frequências descritivas abaixo e as distâncias medianas, os brackets sozinhos dão ~0,29 × 1.110 − 0,30 × 830 ≈ +70 pontos por trade, antes das saídas no fechamento e dos custos. Isso é uma conta de medianas, não um resultado de backtest.
- **Taxa de acerto esperada**: ~55% de trades positivos. O argumento: o validador da 006 mediu que, nos dias de excursão de um lado só, o pregão fecha do lado da excursão em ~61% das vezes. O stop atrás da abertura corta justamente os dias em que essa leitura falhou (nos dias de reteste da abertura, a regra ingênua perdeu em média R$ 40). Quem está do outro lado do trade é quem fez o fade da excursão da manhã e quem precisa ajustar hedge e posição ao longo do dia, o canal de *intraday momentum* de Gao, Han, Li e Zhou (*JFE*, 2018), já citado na 001.
- **Perda máxima por trade, custos incluídos**: no stop mediano, ~R$ 169, ou **~0,17% de R$ 100 mil**. No p90, ~R$ 286 (0,29%). No pior stop da amostra, ~R$ 574 (0,57%). Um gap de barra além do stop pode piorar isso, mas às 10:30 em diante, longe dos leilões, gaps de barra no WIN são raros (nenhum gap além do stop no OOS da 006). Tudo abaixo de 1% do capital.
- **Fração esperada de saídas** (descritiva, com a regra já fixada, contando só quem tocou o quê primeiro): **~29% no alvo, ~30% no stop e ~41% no fechamento**. O alvo de 1 `adr` a partir da abertura é atingível, porque o dia já andou ~0,3 a 0,5 `adr` e ainda tem ~7h30 de pregão. Mas o alvo foi posto de propósito longe, porque o efeito é de direção do dia e o lucro vem de segurar. Ele só corta os dias de tendência extrema, para reduzir a dependência de cauda. **Atenção: em 2023, sem o filtro, 52% dos sinais bateram o stop**, contra ~35% em 2024 e 2025. 2023 deve ser fraco de novo.
- **Entradas por dia**: no máximo 1, só na abertura da barra 10:30. Ficam fora a primeira 1h30 do pregão (o leilão, a abertura do à vista às 10h e a formação da excursão) e qualquer entrada à tarde. A saída no fechamento é a do motor (última barra), por construção da hipótese.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| (nenhum) | | |

Fixos (não são parâmetros e não podem ir para a grade): barra de sinal 10:25, excursão mínima de 0,3 `adr` de um lado só, filtro de 0,1 `adr` do lado certo da abertura, `adr` de 20 pregões, stop em `abertura ∓ 0,1 adr`, alvo em `abertura ± 1,0 adr`, corte de abertura em 09:30, 1 contrato. **Grade total: 1 combinação.** O walk-forward só mede a estabilidade no tempo, sem escolher nada.

Critérios prévios de sucesso, além dos `GATES`:
1. Líquido médio por trade positivo em 2024 e 2025 separadamente. 2026 tem poucos dias e não conta.
2. Resultado sem os 10 maiores trades positivo, e sem os 20 maiores também positivo (a 006 falhou neste último).
3. **Comparação obrigatória com a mesma entrada sem stop e sem alvo**, segurada até o fechamento (é a regra ingênua do validador da 006, mais o filtro de 0,1 `adr`). Se o bracket piorar o Sharpe em mais de 0,3, o stop está cortando os dias errados e isso tem que ser registrado no relatório. A hipótese não vira "sem stop" por causa disso: segurar sem stop viola a regra de risco da mesa.
4. Medir a correlação diária com a 001 (`signal_time` 12:00 e `k` 0,0, e também os parâmetros do walk-forward da 001) e com a 006. Se a correlação com a 001 em 12:00 / k 0,0 passar de ~0,7, as duas são a mesma ideia e só uma deve seguir.

## Por que pode falhar
1. **O stop atrás da abertura corta o efeito.** O diagnóstico ingênuo (Sharpe 1,81) não tinha stop. ~30% dos trades devem bater o stop, e parte desses dias voltaria para o lado da excursão até o fechamento (é exatamente o que a 006 explora). Se for assim, o stop transforma uma vantagem de direção do dia num bracket com acerto perto do p* e Sharpe abaixo de 1. 2023, com 52% de stops sem o filtro, é o lugar mais provável de dar errado.
2. **O DSR não passa mesmo se o efeito for real.** WIN_N_M5 tem ~55 tentativas efetivas contando esta. O Sharpe OOS exigido para DSR ≥ 95% está em ~1,8. O número de 1,81 da regra ingênua é o melhor caso, visto sem stop, sem walk-forward e depois de outras ~50 tentativas. Qualquer degradação deixa a hipótese em PROMISSORA.
3. **É a 001 com outro horário.** A 001 em 12:00 com k = 0 entra do lado do movimento da manhã e segura até o fechamento, e o ORB compra o rompimento da faixa de abertura. Se a 007 não tiver correlação moderada com essas duas, ótimo. Se tiver correlação alta, não é ideia nova, só um reempacotamento do mesmo efeito com risco definido. Ainda assim, isso seria útil como versão com stop da 001.

## Por que é conservadora
Uma entrada por dia, num horário fixo e longe dos dois leilões, com 1 contrato e sem parâmetro livre. O stop fica num nível objetivo (a abertura, com folga de 0,1 `adr`), a ~4 ranges de barra na mediana, e custa ~R$ 169 (0,17% do capital). O pior caso observado fica abaixo de 0,6%. O alvo é ~89× o custo e corta os dias extremos, o que reduz a dependência da cauda. Um gestor de risco aprovaria porque a regra foi escrita antes de olhar o resultado, a perda por trade é conhecida e não há preço médio nem reentrada.

## Origem
Recomendação do ciclo `reports/ciclos/20261023-2107_WIN_N_M5.md` (próximo passo 1) e do validador da 006 (`reports/20261023-210154_reteste_abertura_WIN_N_M5/report.md`, "O que testar a seguir", item 1). É parente direto da 001 (mesmo efeito, *intraday momentum*) e da 006 (mesma excursão de 0,3 `adr` e o mesmo stop atrás da abertura). O que muda: o horário é fixo e cedo (10:30, não 12h a 16h), o lado vem da excursão em `adr` e não da mediana de 20 dias do movimento, e há stop por estrutura e alvo de esgotamento, que a 001 não tinha.

Escolhas e tentativas escondidas:
1. **Diagnóstico do validador da 006** (regra ingênua às 10:30 e às 11:00, sem stop, sem walk-forward, Sharpe OOS 1,81 e 1,78). Isso conta como **2 tentativas**, e foi esse resultado que motivou esta hipótese. O horário de 10:30 foi escolhido por ser o primeiro dos dois, antes de olhar qualquer outro.
2. **O stop (0,1 `adr` atrás da abertura) e o alvo (1,0 `adr` a partir da abertura) foram fixados antes de rodar qualquer conta**, por argumento de estrutura (a abertura como nível de invalidação, um `adr` inteiro como esgotamento), e não por MAE/MFE.
3. **Descritivas** (`desc007.py`, no scratchpad da sessão, com `store.load("WIN$N", "M5")` e sem holdout): `adr`, range de barra, distância do `close` das 10:30 até a abertura, distribuição de stop e alvo e a frequência de saídas (alvo, stop, fechamento) por ano. Não calculei P&L. A primeira rodada mostrou 21 sinais com stop ≤ 0 (o preço já tinha atravessado o nível do stop) e 39% de stops. Por isso adicionei o filtro de 0,1 `adr` do lado certo, que também garante stop ≥ 0,2 `adr`. Essa escolha veio depois de ver frequências de saída (não retorno), com e sem filtro. Conto **2 tentativas** por conservadorismo.

Total desta hipótese: ~4 tentativas escondidas mais 1 registrada. Somadas às ~52 efetivas do dataset (que já incluem 1 do diagnóstico), WIN_N_M5 fica em **~56 tentativas efetivas**. Com esse n, o Sharpe OOS mínimo para DSR ≥ 95% fica em ~1,8. **Expectativa honesta: PROMISSORA, e não candidata ao holdout**, a menos que o stop quase não custe nada em relação à regra ingênua. Esta deve ser a última família testada em WIN_N_M5 antes de mudar de dataset (WDO$N M5, sem tentativas).

## Notas de implementação
- Stop e alvo são níveis absolutos na hipótese (abertura ∓ 0,1 adr e abertura ± 1,0 adr), mas o motor recebe distâncias fixas a partir da entrada. As distâncias são calculadas no fechamento da barra 10:25 a partir do `close` dela (`stop = (close − abertura) × lado + 0,1 adr`; `alvo = (abertura + lado × adr − close) × lado`). A entrada real é na abertura da barra 10:30, então os níveis efetivos diferem dos teóricos pelo gap entre o close das 10:25 e a abertura das 10:30.
- Não entra se stop ≤ 0 ou alvo ≤ 0, ou se o filtro `(close − abertura) × lado ≥ 0,1 adr` falha.
- `params={}` e `grid={}`: 1 combinação.

Relatório: reports/20261023-213418_direcao_do_dia_WIN_N_M5
