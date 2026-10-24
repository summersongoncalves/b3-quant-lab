# 012 · Falha de extensão do balanço inicial (IB) no WDO: vender o rompimento que volta para dentro, alvo no outro lado do IB
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: price_action
- Estado: REJEITADA

## Padrão
No mini dólar, quando o preço estende além da máxima (ou mínima) da primeira hora do pregão, o *initial balance* (IB) de Dalton, e uma barra de 5 min fecha de volta dentro do IB, a extensão falhou. Os participantes "responsivos" do câmbio (exportador vendendo alta, importador comprando queda, BC) rejeitaram o preço novo. O preço tende a rodar até o outro lado do IB com mais frequência do que volta a romper o extremo que falhou.

## Regras
Barras de 5 min rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra atual.

Definições:
- Só operar dias cuja primeira barra começa até **09:05**.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam.
- `IBH` / `IBL` = máxima e mínima das barras rotuladas de **09:00 a 09:55** (a primeira hora). Se o dia não tiver pelo menos 11 barras nessa faixa, não opera. Os dois níveis ficam fixos a partir da barra 09:55.
- `max_hoje` / `min_hoje` = máxima e mínima acumuladas do dia até a barra atual, incluindo ela (`cummax` do `high` e `cummin` do `low` por dia).
- Janela de sinal: barras rotuladas de **10:00 a 13:55**. Fora dela não há sinal.

A regra não usa nenhum nível do dia anterior nem nada entre pregões. Por isso a rolagem mensal da série contínua WDO$N não a afeta, ao contrário do que acontece com os extremos do dia anterior.

Entrada (no máximo 1 por dia):
- **Vendido** na primeira barra da janela em que `max_hoje ≥ IBH + e × adr` **e** `IBL < close < IBH` (a extensão de alta de pelo menos `e` adr falhou e a barra fechou de volta dentro do IB).
- **Comprado** na primeira barra da janela em que `min_hoje ≤ IBL − e × adr` **e** `IBL < close < IBH`.
- Se as duas condições valerem na mesma barra (o dia já estendeu para os dois lados), o dia não opera e não há sinal depois.
- Se a distância até o alvo (abaixo) for menor que **3,72 pontos** (3 × C), o sinal é descartado e o dia não opera (~0,3% dos sinais).
- A execução é na abertura da barra seguinte, pela convenção do motor. Posição alvo = `lado` (1 contrato), mantida do sinal até o fim do pregão, para o motor não reentrar depois de uma saída por stop ou alvo.
- Não há segunda entrada no dia.

Saída:
- Stop loss e stop gain fixos (abaixo), lidos na barra de sinal.
- Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato, e o tick vale 0,5 ponto (R$ 5). Os valores típicos abaixo são da combinação padrão (`e` = 0,10, `b` = 0,05), medidos na amostra de pesquisa (687 dias válidos, 361 sinais).

- **Stop loss** (atrás da estrutura que falhou): o nível fica além do extremo da extensão, `max_hoje + b × adr` no vendido e `min_hoje − b × adr` no comprado.
  - Distância passada ao motor: `stop = max(|extremo − close| + b × adr, 0,15 × adr)`, com o `close` da barra de sinal. O piso de 0,15 adr (~8,6 pontos, ~1,7 range de barra) é fixo e quase nunca é usado.
  - Mediana de **15,6 pontos, ou ~31 ticks e ~R$ 156 por contrato**. São ~3 ranges medianos de barra M5 entre 10:00 e 13:55 (5,0 pontos).
  - p10 de 9,7 pontos (R$ 97), p90 de 28,5 pontos (R$ 285), máximo de 53,6 pontos (R$ 536).
- **Stop gain** (próximo nível): o outro lado do IB. A distância é `alvo = close − IBL` no vendido e `IBH − close` no comprado.
  - Mediana de **23,0 pontos, ou ~46 ticks e ~R$ 230 por contrato**.
  - p10 de 12,0 pontos e p90 de 45,0 pontos. Alvo/stop mediano de 1,47.
  - O alvo no meio do IB foi considerado e descartado pela geometria (mediana de ~10,8 pontos contra stop de ~12, com p* de ~58%). Essa escolha foi descritiva, sem P&L (ver Origem).
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) mais emolumentos de 2 × R$ 1,20 (0,24 ponto). Dá **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**.
  - **Alvo/C ≈ 18,5x** na mediana. O custo é ~8% do stop mediano.
- **Acerto de equilíbrio** do bracket, com medianas: `p* = (S + C) / (T + S) = (15,6 + 1,24) / (23,0 + 15,6) ≈ 44%`. Esse p* só vale para os trades que terminam em stop ou alvo; os que saem no fechamento entram pelo resultado líquido.
- **Taxa de acerto esperada**: ~46 a 50% dos trades resolvidos no alvo, contra 36% de um passeio aleatório com a mesma geometria (S/(S+T)). Os motivos:
  - na 008, a continuação da excursão da manhã no WDO teve bruto negativo (Sharpe −0,49 sem bracket). Isso sugere que o dólar em M5 é mais um mercado de balanço do que de tendência;
  - no câmbio existe um lado "responsivo" estrutural (fluxo comercial que vende alta e compra queda, atuação do BC), que é exatamente o participante que Dalton descreve como o que rejeita a extensão do IB;
  - com stop atrás do extremo que falhou, só se perde quando o mercado volta a romper esse extremo, que é uma confirmação de que a ideia estava errada.

  É um palpite moderado. Se a taxa ficar perto de 36 a 40%, a ideia é ruído.
- **Perda máxima por trade, custos incluídos**:
  - no stop mediano, ~R$ 168, ou **~0,17% de R$ 100 mil**;
  - no p90, ~R$ 297 (0,30%);
  - no pior stop da amostra, ~R$ 548 (0,55%).

  Um gap de barra além do stop (notícia dos EUA às 10:30, 11:00 ou 12:00, leilão do BC) pode piorar isso. O validador deve medir os gaps além do stop.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: medi só um benchmark sem lado. Com barras sorteadas da janela 10:00–13:55 e lado aleatório, usando a geometria mediana (S = 0,27 adr, T = 0,40 adr), o resultado até o fim do pregão foi de 23% no alvo, 42% no stop e 35% sem tocar nenhum dos dois. Se a hipótese tiver vantagem, espero **~25 a 32% de saídas no alvo**, ~30 a 38% no stop e ~35% no fechamento. Abaixo de 20% no alvo, o envelope repete o problema do ciclo VBBR3.
- **Entradas por dia**: no máximo 1. Ficam proibidas a primeira hora (leilão de abertura, formação do IB, dados dos EUA às 09:30 ou 10:30) e qualquer entrada depois das 13:55, quando o dólar fica parado (volume de 0,75 a 0,85 da mediana, segundo a exploração 011).

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| `e` (extensão mínima além do IB, em adr) | 0,10 | 0,05 · 0,10 · 0,15 |
| `b` (folga do stop além do extremo, em adr) | 0,05 | 0,05 · 0,10 |

**Grade total: 6 combinações.** Ficam fixos: IB = primeira hora (09:00–09:55), janela de sinal 10:00–13:55, alvo no outro lado do IB, piso do stop de 0,15 adr, descarte de alvo menor que 3 × C, `adr` de 20 pregões e 1 contrato.

Sinais por combinação (descritivo): `e` = 0,05 dá ~476; `e` = 0,10 dá ~361 (92 em 2023 desde abril, 118 em 2024, 133 em 2025 e 18 em 2026); `e` = 0,15 dá ~263. O stop mediano vai de ~12 pontos (`e` = 0,05, `b` = 0,05) a ~22 pontos (`e` = 0,15, `b` = 0,10). O alvo mediano fica em ~23 a 24 pontos em todas.

Critérios prévios de sucesso, além dos `GATES`:
1. Líquido médio por trade positivo em 2024 e em 2025, cada ano separadamente.
2. Resultado positivo sem os 10 maiores trades e também sem os 20 maiores.
3. Pelo menos 4 das 6 combinações com Sharpe positivo.
4. Saídas no alvo em pelo menos 20% dos trades.
5. Correlação diária com a 008 (sinal invertido) reportada. Se a 012 for só "a 008 ao contrário" (correlação < −0,6 com a 008 nos dias em comum), o relatório tem que dizer isso, porque aí a vantagem não vem da estrutura do IB.

## Por que pode falhar
1. **É a inversão da 008 com outro nome.** Se o que funciona for só "fade da excursão da manhã", a estrutura do IB não acrescenta nada, e a escolha do lado foi influenciada pelo resultado da 008. O critério 5 mede isso.
2. **Dias de notícia.** Uma extensão que falha às 10:30 pode virar tendência depois de um dado dos EUA às 11:00 ou de um leilão do BC. Os stops vão se concentrar nesses dias, e os ganhos podem vir de poucos dias de reversão forte (critério 2).
3. **Stop perto do ruído na combinação mais apertada.** Com `e` = 0,05 e `b` = 0,05, o stop p10 é de ~7,6 pontos (1,5 range de barra), e o custo vira ~16% do stop nesses casos. Se só a combinação de stop largo funcionar, isso é sinal de ruído (critério 3).

## Por que é conservadora
É uma entrada por dia, com 1 contrato, num nível objetivo que todo o mercado enxerga, e o stop fica logo atrás do extremo que invalida a ideia. A perda típica é de ~R$ 168 (0,17% do capital) e a pior da amostra fica em ~0,55%. Ela não opera na primeira hora nem na tarde parada, não usa nenhum nível de outro pregão (imune à rolagem) e tem só 2 parâmetros numa grade de 6.

## Origem
Combinação de estratégias conhecidas, citadas de memória:
- **Dalton, *Mind Over Markets*** (Dalton, Jones & Dalton): o *initial balance* da primeira hora, a "extensão do range" e a leitura de que uma extensão rejeitada (atividade responsiva) leva a uma rotação até o outro lado do balanço. Daqui vêm o nível, a lógica e o alvo no extremo oposto do IB.
- **Connors & Raschke (1995), *Street Smarts*, "Turtle Soup"**: entrar contra o rompimento que falha, quando o preço volta para dentro do nível, com stop logo além do extremo da perfuração. Daqui vêm o gatilho e o stop atrás da estrutura.
- **Adaptação à B3**: IB das 09:00 às 09:55 do WDO, janela de sinal até 13:55 (a tarde do dólar é parada, conforme a exploração 011) e regra só intradiária para escapar da distorção da rolagem mensal.

A família de falso rompimento já falhou em VBBR3 (005, extremo de 20 pregões) e em WIN (extremo do dia anterior, exploração não registrada). Aqui a diferença é diagnóstica: o nível é do próprio dia e o mercado é o dólar. Em WIN, a persistência da direção do dia (001, 006, 007) era o oposto do fade. No WDO, a 008 mostrou que essa persistência não existe.

**O que olhei**, só descritivo, com `store.load("WDO$N", "M5")` e sem holdout. Os scripts estão em `research/scratch/explore_012.py`, `explore_012b.py` e `explore_012c.py`:
- largura do IB: mediana de 0,47 adr (p10 0,29, p90 0,78);
- range de barra de 10:00 a 13:55: mediana de 5,0 pontos;
- contagem de sinais por ano e por lado nas 6 combinações da grade;
- distribuição das distâncias de stop e alvo, e com que frequência o piso do stop é usado;
- alvo no meio do IB contra alvo no outro lado do IB;
- benchmark de alcance com barras sorteadas e lado aleatório.

**Não calculei P&L, acerto, MAE, MFE nem frequência de saídas condicionada ao lado do sinal.**

**Tentativas escondidas: ~2.**
- 1 pela escolha do alvo (meio do IB contra o outro lado do IB), feita só pela geometria descritiva;
- 1 pela influência do resultado da 008 na escolha do lado (fade em vez de continuação).

Com as 2 linhas da 008 e as ~9 tentativas escondidas das explorações 009 a 011, WDO_N_M5 passa a ~11 + 6 + 2 ≈ **19 tentativas efetivas** depois desta validação.

## Notas de implementação
- Módulo novo `falha_balanco_inicial`, `timeframe="M5"`, params `e` e `b`, grade de 6.
- Stop e alvo em pontos do instrumento, lidos na barra de sinal. `instruments.for_symbol` já mapeia `WDO*`.
- O IB só fica definido depois do fechamento da barra 09:55. Sinal só a partir da barra 10:00, e `max_hoje`/`min_hoje` incluem a barra atual.
- Stop e alvo são níveis absolutos na hipótese, mas o motor lê distâncias: elas são calculadas no fechamento da barra de sinal a partir do `close` dela (aproximação da entrada na abertura seguinte). Distância de stop = `max(|extremo − close| + b × adr, 0,15 × adr)`; alvo = `close − IBL` (vendido) ou `IBH − close` (comprado).
- Só a primeira barra com gatilho no dia pode operar. Se nela as duas condições valem, ou o alvo é < 3,72 pontos (3 × 1,24), ou alguma distância é ≤ 0, o dia não opera e não há nova tentativa.

Relatório: reports/20261023-224139_falha_balanco_inicial_WDO_N_M5
