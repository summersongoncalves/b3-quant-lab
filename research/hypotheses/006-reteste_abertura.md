# 006 · Reteste da abertura depois de uma excursão da manhã no WIN
- Dataset: WIN$N M5
- Modo: daytrade
- Estilo: price_action
- Estado: PROMISSORA

## Padrão
Quando o WIN se afasta pelo menos 0,3 `adr` da abertura do dia para um lado, volta para testar o preço de abertura e uma barra de 5 min fecha de volta do lado da excursão, o nível da abertura segurou. O preço tende a voltar até o extremo da manhã (ou ficar do lado da excursão até o fechamento) com mais frequência do que atravessa a abertura com força.

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra atual):
- Só operar dias cuja primeira barra começa até **09:30** (mesmo corte da 001).
- `abertura` = `open` da primeira barra do dia.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam. O `adr` só usa máxima e mínima dentro de cada pregão, então não é afetado pelos saltos de rolagem da série contínua. A regra também não usa nenhum nível do dia anterior.
- `max_ant` = máxima do dia até a barra **anterior** (`cummax` do `high` com `shift(1)` dentro do dia). `min_ant` = mínima do dia até a barra anterior.
- `exc_alta` = `max_ant − abertura ≥ 0,3 × adr`. `exc_baixa` = `abertura − min_ant ≥ 0,3 × adr`.
- Janela de sinal: barras rotuladas de **10:30 a 14:55**. Fora dela não há sinal.

Entrada (no máximo 1 por dia):
- **Comprado** na primeira barra da janela em que `exc_alta` **e não** `exc_baixa` **e** `low ≤ abertura` **e** `close > abertura` (o dia subiu, voltou a tocar a abertura e a barra fechou de volta acima dela).
- **Vendido** na primeira barra da janela em que `exc_baixa` **e não** `exc_alta` **e** `high ≥ abertura` **e** `close < abertura`.
- Os dias que já se afastaram 0,3 `adr` para os dois lados antes do sinal não operam: são dias sem lado definido.
- Se as duas condições aparecerem na mesma barra, o dia não opera. Pela definição isso não pode acontecer, porque cada lado exige que o outro não tenha excursão.
- A execução é na abertura da barra seguinte, pela convenção do motor. Posição alvo = `lado` (1 contrato), mantida igual do sinal até o fim do pregão, para que o motor não reentre depois de um bracket.
- Não há segunda entrada no dia, mesmo depois de uma saída por stop ou alvo.

Saída:
- Stop loss e stop gain fixos (ver abaixo), lidos na barra de sinal.
- Sem saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Valores típicos da amostra de pesquisa: `adr` mediano de ~1.740 pontos; range médio de uma barra de M5 nas 12 barras antes do sinal de ~220 pontos (das 10h às 11h, horário da maioria dos sinais); `close − abertura` na barra de sinal de ~70 pontos (mediana).

- **Stop loss** (atrás da estrutura): o nível do stop é `abertura − s × adr` para comprado e `abertura + s × adr` para vendido. A distância passada ao motor é `stop = (close − abertura) × lado + s × adr`, com o `close` da barra de sinal. Se o preço atravessa a abertura em s `adr`, a ideia "a abertura segurou" está errada. Com s = 0,25 (padrão), a distância típica é de **~520 pontos, ou ~104 ticks**, e vale ~R$ 104 por contrato (~2,4 ranges de barra). Com s = 0,2: ~420 pontos, ~84 ticks, ~R$ 84. Com s = 0,3: ~590 pontos, ~118 ticks, ~R$ 118.
- **Stop gain** (próximo nível): o extremo da manhã. A distância passada ao motor é `alvo = (max_dia − close)` para comprado e `(close − min_dia)` para vendido, com `max_dia` e `min_dia` acumulados até a barra de sinal, **incluindo** ela. A mediana é de **~670 pontos, ou ~134 ticks**, e vale ~R$ 134 por contrato (~0,39 `adr`). O mínimo observado foi de ~250 pontos (~50 ticks), porque a excursão mínima é de 0,3 `adr`. O alvo não depende de s.
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 5 pontos) mais emolumentos de 2 × R$ 0,25 (= 2,5 pontos). Dá C ≈ **12,5 pontos ≈ 2,5 ticks ≈ R$ 2,50 por contrato**. **Alvo/C ≈ 54x** na mediana e ≥ 20x no pior caso. O custo não é o problema aqui.
- **Acerto de equilíbrio** do bracket, com valores medianos: `p* = (S + C) / (T + S)`. s = 0,2: (420 + 12,5) / (670 + 420) ≈ **40%**. s = 0,25: (520 + 12,5) / (670 + 520) ≈ **45%**. s = 0,3: (590 + 12,5) / (670 + 590) ≈ **48%**.
- **Taxa de acerto esperada**: ~50% a 55% de trades positivos, contando as saídas no fechamento. Na exploração (in-sample, ver Origem), com s = 0,25, o acerto foi de 56%: um terço dos trades bateu o alvo, um terço o stop, e um terço saiu no fechamento, a maioria no positivo. O argumento para ficar acima do p* tem duas partes. Primeiro, quem empurrou o preço 0,3 `adr` na manhã ainda carrega posição, e a abertura é o nível em que a operação do dia volta a zero para eles. Segundo, o alvo é um nível que o próprio dia já negociou, e não um múltiplo arbitrário do stop. **Expectativa honesta: provavelmente PROMISSORA no máximo, e não aprovada.** O resultado bruto in-sample (~80 pontos por trade) é negativo em 2023, e sem os 10 melhores trades cai para ~23 pontos líquidos.
- **Perda máxima por trade, custos incluídos**: no stop, ~R$ 106 com s = 0,25, ou **~0,11% de R$ 100 mil**. Num stop largo (`adr` alto e `close` longe da abertura), fica em ~R$ 170. A exceção é um gap de barra além do stop: na exploração, o pior trade foi de −845 pontos (~R$ 171). Tudo isso fica muito abaixo de 1% do capital de referência.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: ~30% a 35% (31% / 35% / 36% na exploração, de s = 0,15 a 0,35). O alvo mediano é de 0,39 `adr`, e os sinais saem em média perto das 11h, com ~7 horas de pregão pela frente. Isso é bem mais atingível que os alvos de 0,8 a 1,0 `adr` da 003 a 005. Outros ~30% devem sair no fechamento, e a hipótese depende de essas saídas serem positivas em média.
- **Entradas por dia**: no máximo 1. Sinal só em barras rotuladas de 10:30 a 14:55. Fica proibida a primeira 1h30 do pregão: o leilão, a abertura do mercado à vista às 10h e a excursão que a regra exige. Também ficam proibidas as últimas ~3 horas antes do call, para dar tempo de o alvo ser atingido. Os sinais saem principalmente às 10h e às 11h (87 e 66 de 218).

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| stop_mult (s) | 0.25 | [0.2, 0.25, 0.3] |

Fixos (não são parâmetros e não podem ir para a grade): excursão mínima de 0,3 `adr`, `adr` de 20 pregões, janela de sinal de 10:30 a 14:55, corte de abertura em 09:30, alvo no extremo do dia e 1 contrato. Grade total: **3 combinações**, todas com o mesmo sinal e o mesmo alvo. Se só uma funcionar, é ruído.

Critério prévio de sucesso, além dos `GATES`: o líquido médio por trade precisa ser positivo em 2024 e 2025 separadamente, e o resultado sem os 10 maiores trades precisa ser positivo. 2026 tem só 4 sinais e não conta.

## Por que pode falhar
1. **2023 negativo e cauda.** Na exploração, o bracket perdeu em 2023 nos três tamanhos de stop (−8 a −54 pontos brutos por trade). O líquido sem os 10 melhores trades cai de ~68 para ~23 pontos. Com ~220 sinais em 2,9 anos, ou ~150 no walk-forward, a diferença entre "padrão" e "três meses bons de 2024 e 2025" é pequena. O retorno sem bracket, segurando até o fechamento, foi positivo em todos os anos (~96 pontos brutos). Se o bracket só atrapalha, o sinal é "direção do dia" disfarçada de price action.
2. **Sobreposição com o ORB e com a 001.** Um dia que se afastou 0,3 `adr` da abertura antes das 10h30 provavelmente rompeu a faixa de abertura, e o ORB entrou do mesmo lado. A 006 compra o reteste desse rompimento. Com a 001 a sobreposição deve ser menor, porque no sinal o `close` está perto da abertura (`mov` ≈ 0), e a 001 com k ≥ 0,5 não dispara nesse ponto. O validador deve medir a correlação diária com os dois. Se for alta, a 006 é o ORB com outra entrada, e não uma ideia nova.
3. **Mineração escondida.** Esta é a terceira família de price action olhada nesta iteração. As duas anteriores (fade e reteste dos extremos do dia anterior) deram bruto negativo, e a escolha desta foi feita depois de ver o retorno dela. Os três tamanhos de stop também foram vistos in-sample. Com ~13 tentativas escondidas somadas às ~33 já existentes em WIN_N_M5, o DSR desta grade deve ser lido como otimista.

Explicação econômica plausível (não demonstrada): a abertura é o preço de referência do dia para quem opera intraday ("estou ganhando ou perdendo hoje?"). Depois de uma excursão forte, quem perdeu o movimento ou quer aumentar a posição tende a deixar ordens perto desse nível. Quem apostou na reversão costuma ter o stop logo do outro lado da abertura. O reteste que segura reflete fluxo informado da manhã que ainda não terminou (o mesmo canal do *intraday momentum* de Gao, Han, Li e Zhou, 2018, citado na 001). Do outro lado do trade está quem fez o fade da excursão e precisa sair. A ideia de "teste da abertura" é clássica em price action (Al Brooks, *Trading Price Action: Trends*, 2012, sobre o preço de abertura como suporte ou resistência). Não há nota em `knowledge/` (`knowledge/notas` está vazia).

## Por que é conservadora
Uma entrada por dia, em ~30% dos pregões, longe dos dois leilões, com 1 contrato. O stop fica atrás de um nível objetivo, a abertura, a ~2,4 ranges de barra da entrada, e o alvo é um preço que o próprio dia já negociou, a ~54× o custo. Um stop custa ~R$ 106, ~0,11% do capital de referência. Mesmo 15 stops seguidos custariam menos de 2%. Um gestor de risco aprovaria porque a perda por trade é conhecida e pequena, o alvo é atingível no tempo que resta e não há preço médio nem reentrada.

## Origem
Primeira ideia de price action em WIN_N_M5. Não é variação de uma hipótese anterior, mas é parente da família "intraday momentum" da 001: usa a excursão da manhã como viés e entra no reteste da abertura.

Scripts em `research/scratch/` (todos com `store.load("WIN$N", "M5")`, sem holdout). Tentativas escondidas:
1. Inspeção básica: range de barra por hora, range diário e gaps de abertura (para achar os saltos de rolagem). **1 tentativa.**
2. `explore_006.py`: fade do falso rompimento da máxima ou da mínima do dia anterior, de 10:00 a 14:55. Testei stop atrás do extremo do dia com alvo de 1R, alvo no meio do range anterior e segurar até o fechamento. São **3 variações**, com bruto de −21, −32 e −16 pontos por trade em 362 trades. Descartado. Repete em WIN o resultado ruim da 005b em VBBR3. Não propus o lado inverso.
3. `explore_006b.py`: rompimento aceito do extremo do dia anterior (≥ 0,1 `adr`) seguido de reteste que segura. Testei alvo de 1,5R e segurar até o fechamento. São **2 variações**, com bruto de −33 e +36 pontos (2023: −95). Descartado.
4. `explore_006c.py`, `explore_006d.py` (este com bug de sinal no stop do vendido) e `explore_006e.py`: a regra desta hipótese. Testei stop em 0,1 `adr` além da abertura, 3 tamanhos de stop (0,15 / 0,25 / 0,35) com o alvo no extremo e segurar até o fechamento. Conto **7 variações**, por conservadorismo. A grade final (0,2 / 0,25 / 0,3) interpola os valores vistos e foi escolhida para manter o stop em ≥ 2 ranges de barra. O 0,15 ficava em ~1,5 range, dentro do ruído.

Total desta iteração: **~13 tentativas escondidas** mais as 3 da grade. Somadas às 18 registradas e às ~15 escondidas da 001, WIN_N_M5 chega a **~49 tentativas efetivas**. Com esse n, um Sharpe OOS de ~1,3 (o que a exploração sugere: ~68 pontos líquidos por trade, ~75 trades por ano) dificilmente passa no DSR de 95%.

## Notas de implementação
- Stop e alvo são distâncias medidas a partir do `close` da barra de sinal, como a hipótese define; o motor as aplica a partir da abertura seguinte (aproximação: o preço de entrada difere do close).
- Sinais com alvo ≤ 0 (close no extremo do dia) ou stop ≤ 0 são descartados antes de escolher a primeira entrada do dia; a próxima barra válida da janela pode então ser a entrada.
- Posição mantida (com stop/alvo fixos via ffill) até o fim do pregão; sem segunda entrada no dia.

Relatório: reports/20261023-210154_reteste_abertura_WIN_N_M5
