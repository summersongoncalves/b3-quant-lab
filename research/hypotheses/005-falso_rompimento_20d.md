# 005 · Falso rompimento do extremo de 20 pregões em VBBR3 ("Turtle Soup" intradiário), com bracket largo
- Dataset: VBBR3 M5
- Modo: daytrade
- Estado: REJEITADA

## Padrão
Quando VBBR3 fura, durante o pregão, a mínima (ou a máxima) dos 20 pregões anteriores e volta a fechar uma barra de 5 min do lado de dentro desse nível, o rompimento falhou. Os stops acumulados abaixo da mínima (ou acima da máxima) de várias semanas já foram executados, e o preço tende a voltar para dentro do range com um movimento grande, de ~0,5 a 1 `adr`, no resto do dia. É um evento raro (~108 dias em 3 anos) e de amplitude grande, que permite um alvo muito acima de 2×C.

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra atual):
- Só operar dias cuja primeira barra começa até **10:10** (mesmo corte da 003 e da 004).
- `adr` = média de (máxima do dia − mínima do dia), em R$, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam.
- `L20` = menor mínima diária dos **20 pregões anteriores** (`shift(1)`, sem o dia atual). `H20` = maior máxima diária dos 20 pregões anteriores. Os dois ficam constantes durante o dia.
- `min_hoje` = mínima acumulada do dia até a barra atual, incluindo a barra atual (`cummin` do `low` por dia). `max_hoje` = máxima acumulada (`cummax` do `high`).
- Janela de sinal: barras rotuladas de **10:30 a 14:55** (fechamento entre 10:35 e 15:00). Fora dela não há sinal.

Entrada (no máximo 1 por dia):
- **Comprado** na primeira barra da janela em que `min_hoje < L20` **e** `close > L20` (o dia furou a mínima de 20 pregões e a barra atual fechou de volta acima dela). A perfuração pode ter ocorrido antes das 10:30 ou na própria barra.
- **Vendido** na primeira barra da janela em que `max_hoje > H20` **e** `close < H20`.
- Se as duas condições aparecerem no mesmo dia, vale a que aparecer primeiro. Se aparecerem na mesma barra, o dia não opera (na exploração de frequência isso não aconteceu nenhuma vez).
- A execução é na abertura da barra seguinte, pela convenção do motor.
- Não há segunda entrada no dia, mesmo depois de uma saída por stop ou alvo.

Tamanho (risco fixo por trade, igual à 003 e à 004):
- `stop_dist` = `s × adr` (R$ por ação), lido na barra de sinal.
- `w` = min(1, 0,008 × `close` / `stop_dist`), com o `close` da barra de sinal.
- Posição alvo = `lado × w`, mantida igual do sinal até o fim do pregão, para que o motor não reentre depois de um bracket.

Saída:
- Stop loss e stop gain fixos a partir do preço de entrada (ver abaixo), lidos na barra de sinal.
- Sem saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Valores típicos com preço mediano de ~R$ 19,8 e `adr` mediano de ~281 bp (~R$ 0,56). O range mediano de uma barra de M5 é de ~24 bp, ou ~5 ticks.

- **Stop loss**: `s × adr`. Com s = 0,4 (padrão), dá ~R$ 0,22, ou seja **~22 ticks** e ~112 bp. Com s = 0,3: ~17 ticks (~84 bp). Com s = 0,5: ~28 ticks (~140 bp). O menor stop fica a ~3,5 ranges de barra da entrada, fora do ruído de uma barra. Para uma posição cheia de R$ 100 mil, o stop valeria R$ 840 / 1.120 / 1.400. Com o ajuste de tamanho `w` (0,95 / 0,71 / 0,57), a perda no stop fica limitada a ~R$ 800.
- **Stop gain**: `2 × stop` (**fixo**). Com s = 0,4: **~44 ticks** e ~225 bp (0,8 `adr`). Com s = 0,3: ~34 ticks (~169 bp, 0,6 `adr`). Com s = 0,5: ~56 ticks (~281 bp, 1,0 `adr`). A relação de 2x (contra 1,5x da 004) é a escolha deliberada desta iteração: o problema recorrente em VBBR3 foi bruto pequeno, e um falso rompimento de extremo de várias semanas é justamente o tipo de evento que pode andar um `adr` inteiro de volta para dentro do range.
- **Custo de ida e volta (C)**: emolumentos de 2 × 2,3 bp mais 1 tick de slippage por lado (2 × R$ 0,01 / preço). Dá ~14,7 bp com R$ 19,8 (~15 bp na média dos sinais; ~18 bp em 2023 com R$ 15), ou ~R$ 150 por R$ 100 mil cheios (~R$ 105 com w = 0,71). Em ticks, C ≈ 3 ticks. **Alvo/C**: ~11x (s = 0,3), **~15x** (s = 0,4) e ~19x (s = 0,5). Todos muito acima do mínimo de 3x.
- **Acerto de equilíbrio, só para o bracket**: `p* = (S + C) / (T + S)`. s = 0,3: (84 + 15) / (169 + 84) = **39,1%**. s = 0,4: (112 + 15) / (225 + 112) = **37,7%**. s = 0,5: (140 + 15) / (281 + 140) = **36,8%**.
- **Taxa de acerto esperada**: 40% a 45% de trades positivos, com payoff realizado de ~1,5 (uma parte relevante sairá no fechamento sem bater o alvo, com ganho menor que 2× o stop). O argumento para ficar acima do p* é estrutural: no falso rompimento, o stop natural (o novo extremo do dia) fica perto e o alvo natural (o meio do range de 20 dias) fica longe, então a assimetria é do próprio evento, e não de calibração. **Expectativa honesta: provavelmente REJEITADA.** O parente mais próximo que olhei (falso rompimento da mínima/máxima do dia anterior, ver Origem) deu só +0,7 a +3,6 bp brutos por trade. A aposta aqui é que o nível de 20 pregões, mais raro e mais visível, concentra mais stops e produz reversões maiores. Isso não está demonstrado: não olhei o retorno da regra de 20 pregões. Critério prévio de sucesso, como na 003 e na 004: **bruto médio por trade acima de 2 × C (~30 bp) em cada ano** e resultado sem os 5 maiores trades positivo.
- **Perda máxima por trade, custos incluídos**: ~0,8% do capital no stop mais ~0,15% × `w` de custo, ou seja ≤ ~R$ 910 com s = 0,4 (0,91% de R$ 100 mil) e ≤ ~R$ 940 com s = 0,3 (w ≈ 0,95). Em 2023, com C de ~18 bp, fica em ~R$ 970. A exceção é o gap dentro do pregão (barra de notícia abrindo além do stop), que sai na abertura dessa barra e pode passar de 1%. Note que comprar uma mínima de 20 dias é, por construção, comprar um papel que está caindo; o risco de notícia é o mesmo de quem vende o movimento na 004.
- **Entradas por dia**: no máximo 1. Sinal só entre 10:35 e 15:00 (fechamento da barra). Ficam proibidos os primeiros 30 minutos depois do leilão de abertura (spread largo e extremos do leilão que não são rompimentos "reais") e as últimas ~2 horas antes do call de fechamento, para dar tempo de o alvo ser atingido.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| stop_mult (s) | 0.4 | [0.3, 0.4, 0.5] |

Fixos (não são parâmetros e não podem ir para a grade): janela de 20 pregões para `L20`/`H20` e para o `adr`, alvo = 2 × stop, janela de sinal de 10:30 a 14:55, corte de abertura em 10:10, risco de 0,8% por trade e ausência de filtro de "idade" do extremo. Grade total: **3 combinações**, todas com o mesmo sinal. Se só uma funcionar, é ruído.

## Por que pode falhar
1. **Poucos trades e cauda.** São ~108 sinais na amostra de pesquisa inteira (33 / 41 / 32 em 2023 / 24 / 25), o que dá ~80 no walk-forward, perto do mínimo de 30 e com muito erro de estimação. Com alvo de 2× o stop, o resultado depende de ~30 a 40 alvos; cinco trades a mais ou a menos mudam o veredito. O critério "sem os 5 maiores trades positivo" é especialmente duro aqui.
2. **O parente próximo já não pagou o custo.** O falso rompimento do extremo do dia anterior deu bruto de +0,7 bp (com bracket) e +3,6 bp (até o fechamento), com 2023 negativo. Se o efeito de "caça aos stops" fosse forte em VBBR3, deveria ter aparecido ali. Se a diferença entre 1 e 20 pregões não for real, o resultado será o mesmo: bruto ~0 contra C de ~15 bp.
3. **Rompimentos de 20 dias são, muitas vezes, notícia.** Uma mínima de 20 pregões costuma ser furada por um motivo (reajuste de combustível, Petrobras, resultado). Nesses dias o "falso rompimento" de uma barra pode ser só uma pausa, e a tendência retoma, batendo o stop. A regra de entrar no primeiro fechamento de volta dentro do nível, sem confirmação, é a mais exposta a isso. Há ainda viés de lado: 64 dos 108 sinais são vendidos (fades de máxima), num período em que o papel subiu de ~R$ 15 para ~R$ 25.

## Por que é conservadora
Uma entrada por dia, em menos de 15% dos pregões, longe dos dois leilões, com stop proporcional à volatilidade já conhecida (`adr` de 20 dias) e tamanho calculado para que um stop custe ~0,8% do capital (≤ ~0,95% com custos), o mesmo envelope que nas hipóteses 003 e 004 entregou perdas de stop de R$ 766 a R$ 1.017, sem `stop_both` e sem gap além do stop. O alvo de ~15×C é o primeiro desenho neste ativo em que o custo não come a vantagem por construção. Um gestor de risco aprovaria porque o pior dia normal é conhecido de antemão e a frequência baixa limita a sequência de perdas.

## Origem
Fonte: Connors e Raschke, *Street Smarts* (1995), padrão "Turtle Soup", que faz o fade da quebra de uma mínima/máxima de 20 dias quando o preço volta para dentro do nível. Aqui o padrão foi adaptado ao intradiário (sinal na barra de 5 min que fecha de volta dentro do nível, saída obrigatória no mesmo pregão) e **sem** o filtro original de "o extremo anterior ter pelo menos 4 dias de idade", que deixava só 28 sinais em 3 anos. Não há nota em `knowledge/` (a pasta `knowledge/notas` está vazia). A explicação econômica é plausível, mas não está demonstrada. Abaixo de uma mínima de várias semanas ficam stops de quem está comprado e ordens de entrada de quem segue rompimento. Quando esse fluxo se esgota sem continuação, quem está do outro lado (quem forneceu liquidez aos stops) é recompensado pela volta. Isso é provisão de liquidez a fluxo forçado, como na 004, mas o gatilho é um nível de preço multissemanal, e não a VWAP do dia. Não reaproveita sinal de VWAP nem de momentum do meio-dia, nem a inversão deles.

A ideia nasceu de uma exploração que **falhou** e, portanto, está contaminada. Tentativas escondidas nesta iteração (todas em `store.load("VBBR3", "M5")`, amostra de pesquisa até 19/01/2026):
1. `research/scratch/explore_005.py`: rompimento da máxima/mínima do dia anterior depois de um dia NR7 (Crabel), na janela 10:30–14:55, segurado até o fechamento e com bracket de 0,5/1,0 `adr`. São **2 variações**, com bruto de −18,7 e −17,0 bp em 98 trades, negativo em todos os anos. Descartado. Não propus o lado inverso (+18,7 bp brutos) porque seria mineração da inversão e, mesmo assim, ficaria abaixo de 2×C.
2. `research/scratch/explore_005b.py`: falso rompimento do extremo do dia anterior (furou em ≥ 0,1 `adr` e fechou de volta dentro), até o fechamento e com bracket de 0,4/0,8 `adr`. São **2 variações**, com bruto de +3,6 e +0,7 bp em 359 trades e 2023 negativo. Descartado. A 005 é uma variação dessa regra (nível de 20 pregões em vez de 1), e isso deve ser lido como seleção depois de ver o resultado.
3. `research/scratch/explore_005c.py`: **só contagem de frequência**, sem olhar retorno, do gatilho de 20 pregões em 4 configurações (20 ou 10 pregões; com ou sem filtro de idade ≥ 3). A escolha (20 pregões, sem filtro de idade, 108 sinais) foi feita pela frequência mínima para passar no critério de trades. Conto como **2** tentativas, por conservadorismo.

Total desta iteração: **6 tentativas escondidas** mais as 3 da grade. Somadas às ~37 anteriores, VBBR3 M5 chega a **~46 tentativas efetivas**. O DSR deve ser lido com esse n.

**Nota para o orquestrador:** reforço a recomendação da 004. Agora são 10 famílias olhadas em VBBR3 M5, e a única direção que dá bruto positivo de forma consistente (reversão / provisão de liquidez) fica entre 0 e ~17 bp por trade, contra ~15 bp de custo. Esta hipótese é o desenho com maior alvo/C possível nessa direção. Se for rejeitada, as iterações 4 e 5 em VBBR3 só aumentam a mineração.

Relatório: reports/20261023-204533_falso_rompimento_20d_VBBR3_M5
