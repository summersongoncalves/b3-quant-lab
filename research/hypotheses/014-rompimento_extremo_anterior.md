# 014 · Rompimento da máxima ou da mínima do dia anterior no WDO (cascata de stops), stop de volta dentro do range anterior
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: price_action
- Estado: REJEITADA

## Padrão
No mini dólar, a máxima e a mínima do pregão anterior são os níveis em que mais se acumulam stops (de quem vendeu ou comprou o range de ontem) e ordens de rompimento. Quando um fechamento de 5 min passa do nível pela primeira vez no dia, essas ordens disparam e empurram o preço mais um pouco no mesmo sentido (Osler, 2005). Esperamos que o preço chegue a 1,5 vez a distância do stop, a favor do rompimento, com mais frequência do que volta para dentro do range anterior. O sinal é um **nível do dia anterior**, e não a excursão a partir da abertura (008) nem o gap (013).

## Regras
Barras de 5 min, rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra de sinal.

Definições:
- Só operar dias cuja primeira barra começa até **09:05**.
- `PDH` / `PDL` = máxima e mínima do pregão anterior (o dia anterior do dataset, `shift(1)` diário).
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam.
- **Exclusão da rolagem** (mesma regra da 013, só pelo calendário): o dia não opera se `data ≥ data + BMonthEnd(0) − BDay(1)` (os 2 últimos dias úteis do mês) **ou** se o pregão anterior do dataset cair nessa janela. No segundo caso, o `PDH`/`PDL` pode ser de outro vencimento.
- `abertura` = `open` da primeira barra do dia. O dia só opera se `PDL < abertura < PDH` (abriu dentro do range anterior). É ~82% dos dias.
- Se alguma barra rotulada de **09:00 a 09:25** fechar acima de `PDH` ou abaixo de `PDL`, o dia não opera. Nesse caso o nível já foi rompido no leilão ou na primeira meia hora, a janela mais ruidosa (~27% dos dias que abrem dentro).
- Janela de sinal: barras rotuladas de **09:30 a 12:55**.

Entrada (no máximo 1 por dia):
- **Comprado** na primeira barra da janela com `close > PDH`. **Vendido** na primeira barra da janela com `close < PDL`. Só o primeiro evento do dia conta. Depois dele não há outro sinal, nem do lado oposto.
- `over` = `|close − nível rompido|`. Se `over > 0,15 × adr`, o sinal é descartado e o dia não opera. A barra que já correu tanto além do nível é, em geral, de notícia, e o stop ficaria largo demais (~7% dos sinais, sobram ~181).
- A execução é na abertura da barra seguinte, pela convenção do motor. A posição alvo é `lado` (1 contrato), mantida do sinal até o fim do pregão (ffill por dia), para que o motor não reentre depois de uma saída por stop ou alvo.

Saída:
- Stop loss e stop gain fixos (abaixo), calculados na barra de sinal. Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato, e o tick vale 0,5 ponto (R$ 5). Os números vêm da amostra de pesquisa (626 dias válidos depois das exclusões, ~195 primeiros rompimentos na janela antes do corte de `over`). O `adr` mediano nos dias de sinal é de 56,7 pontos. O range mediano de uma barra M5 entre 09:30 e 12:55 é de 5,5 pontos (média de 6,3), e o da barra de sinal é de 9,5 pontos.

- **Stop loss** (atrás da estrutura): a ideia está errada se o preço volta para dentro do range de ontem com folga. O nível do stop é `PDH − b × adr` no comprado e `PDL + b × adr` no vendido.
  - Distância passada ao motor: `stop = max(over + b × adr, 0,20 × adr)`, com o `close` da barra de sinal. O piso de 0,20 adr (~11,3 pontos, ~2 ranges de barra) é fixo.
  - Com `b` = 0,20 (padrão): mediana de **14,5 pontos, ou ~29 ticks e ~R$ 145 por contrato** (~2,6 ranges de barra). p10 de 10,5 e p90 de 21,2 pontos. O piso quase nunca é usado.
  - Com `b` = 0,15: mediana de 12,5 pontos (25 ticks), e o piso vale em ~54% dos sinais. Com `b` = 0,25: mediana de ~17 pontos (~34 ticks).
- **Stop gain**: `alvo = 1,5 × stop`, fixo. Com `b` = 0,20: mediana de **~21,8 pontos, ou ~43 ticks e ~R$ 218 por contrato** (~0,38 adr).
  - Não há um "próximo nível" objetivo acima da máxima de ontem. Por isso o alvo é um múltiplo do risco, dimensionado pela excursão sem lado (abaixo).
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) mais emolumentos de 2 × R$ 1,20 (0,24 ponto). Dá **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**. **Alvo/C ≈ 17,5x** na mediana, e o menor alvo possível (1,5 × 0,20 adr ≈ 0,30 adr) passa de 10 C em qualquer dia da amostra.
- **Acerto de equilíbrio** do bracket: `p* = (S + C) / (T + S) = (14,5 + 1,24) / (21,8 + 14,5) ≈ 43,4%` (43,6% com `b` = 0,15 e 43,0% com `b` = 0,25). Um passeio aleatório com essa geometria daria `S/(S+T)` = 40%.
- **Taxa de acerto esperada**: ~47 a 50% dos trades resolvidos no alvo. Os motivos:
  - na mesa de câmbio, a máxima e a mínima de ontem são o nível mais olhado do dia. Os stops de quem operou o range anterior ficam logo além deles, e as ordens stop de rompimento também. Osler (2005) mostra, em dados de ordens de um banco de câmbio, que stops se acumulam além de níveis visíveis e que, quando disparados, geram cascatas rápidas no sentido do rompimento;
  - a exploração sem lado mostra que **há combustível** depois desse evento. A excursão máxima em 60 minutos, para qualquer lado, tem mediana de 0,257 adr depois do rompimento, contra 0,225 em barras sorteadas na mesma janela, e chega a 0,25 adr em 53% dos sinais, contra 42% das barras sorteadas. Isso não diz o lado. Diz só que o rompimento do extremo anterior é um momento de movimento, ao contrário da compressão da 010.

  É um palpite moderado: a folga sobre o passeio aleatório precisa ser de ~3,5 pontos percentuais só para empatar. Se a taxa ficar perto de 40%, a ideia é ruído, como nas 008, 012 e 013.
- **Perda máxima por trade, custos incluídos**:
  - no stop mediano (`b` = 0,20), ~R$ 157, ou **~0,16% de R$ 100 mil**;
  - no p90, ~R$ 224 (0,22%);
  - no pior caso permitido pelo corte de `over` (0,15 adr) com `adr` de ~100 pontos e `b` = 0,25, o stop fica em ~40 pontos, ~R$ 412 (0,41%).

  Uma barra que abre além do stop sai na abertura e pode piorar a perda. O trade pode atravessar as divulgações dos EUA às 09:30/10:30 e a janela da PTAX, e o validador deve medir os gaps além do stop.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: medi só um benchmark com **lado sorteado**, nos mesmos dias de sinal, com as mesmas distâncias e entrada na abertura da barra seguinte, até o fim do pregão: ~34 a 40% no alvo, ~46 a 59% no stop e ~7 a 14% sem tocar nenhum dos dois. A geometria se resolve quase sempre dentro do pregão, então o problema do ciclo VBBR3 (alvo inatingível) não se aplica. Se houver vantagem, espero **~42 a 47% de saídas no alvo**, ~45% no stop e ~10% no fechamento.
- **Entradas por dia**: no máximo 1, entre 09:35 e 13:00 (execução na barra seguinte às de 09:30 a 12:55). Ficam proibidos o leilão e a primeira meia hora (não há sinal antes das 09:30) e a tarde inteira, quando o dólar fica parado (ciclo 2245). Nenhuma entrada perto do call de fechamento.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| `b` (folga do stop dentro do range anterior, em adr) | 0,20 | 0,15 · 0,20 · 0,25 |
| `k` (alvo em múltiplos do stop) | 1,5 | fixo |
| `over_max` (corte do quanto a barra já passou do nível, em adr) | 0,15 | fixo |

**Grade total: 3 combinações.** Ficam fixos também: janela de sinal de 09:30 a 12:55, piso do stop de 0,20 adr, `adr` de 20 pregões, exclusão da rolagem pelo calendário, abertura dentro do range anterior e 1 contrato.

Sinais (descritivo, antes do corte de `over`): ~195, sendo 47 em 2023 (desde abril), 64 em 2024, 75 em 2025 e 9 em 2026. São ~40% de rompimentos de alta e ~60% de baixa. O horário mediano do sinal é 10:25 (quartis de 09:50 e 11:20).

Critérios prévios de sucesso, além dos `GATES`:
1. Líquido médio por trade positivo em 2024 e em 2025, cada ano separadamente.
2. Resultado positivo sem os 10 maiores trades e também sem os 20 maiores.
3. As 3 combinações com Sharpe do mesmo sinal, e pelo menos 2 positivas.
4. Acerto entre trades resolvidos acima do benchmark de lado aleatório com a mesma geometria (40%) por pelo menos 5 pontos percentuais.
5. Resultado separado entre rompimentos de alta e de baixa. Se todo o lucro vier de um lado só (o dólar subiu ou caiu muito num ano), isso precisa aparecer.
6. Correlação diária com a 008 e a 012 nos dias em comum reportada. Um rompimento do `PDH` pode coincidir com a extensão do IB que a 012 vendia.

## Por que pode falhar
- **O dólar em M5 é ruído também nos níveis do dia anterior.** As 008, 009, 012 e 013 deram acerto no nível do lado aleatório. O combustível medido sem lado pode ser só volatilidade (os rompimentos acontecem em barras maiores, de 9,5 pontos contra 5,5), e volatilidade sem direção paga o stop tanto quanto o alvo.
- **Falso rompimento.** O mesmo nível que junta stops atrai quem vende o rompimento (Turtle Soup de Connors & Raschke). Se os responsivos do câmbio (exportador na alta, importador na baixa, BC) dominarem, o preço volta para dentro e o stop é atingido. O corte de 0,20 adr de folga pode ficar dentro desse vaivém.
- **Poucos trades e um ano direcional.** São ~180 trades em três anos, e 60% dos rompimentos são de baixa. Se o resultado vier só de um ano de dólar em tendência, ele é o viés do período, e não o efeito do nível.

## Por que é conservadora
Cada trade tem perda definida antes da entrada, atrás de uma estrutura objetiva (a volta para dentro do range de ontem), de ~0,16% do capital na mediana e menos de ~0,45% no pior caso, com 1 contrato e 1 entrada por dia. Ficam fora o leilão, a primeira meia hora, a tarde parada, os dias de rolagem e as barras que já correram demais. O alvo é atingível dentro do pregão na quase totalidade dos trades, e a grade tem só 3 combinações, variando só o tamanho do stop.

## Origem
Estratégia conhecida, adaptada ao WDO:
- **Rompimento da máxima e da mínima do dia anterior**: setup clássico de day trade de futuros. Crabel (1990), *Day Trading with Short Term Price Patterns*, usa o range anterior como referência de rompimento. Dalton, *Mind Over Markets*, trata a saída do range anterior como atividade "iniciativa". Citados de memória.
- **Mecanismo**: Osler (2005), *Stop-loss orders and price cascades in currency markets* (Journal of International Money and Finance), sobre a concentração de stops além de níveis visíveis e as cascatas no câmbio. Osler (2003) é a referência dos números redondos, testados descritivamente na exploração 009. Citados de memória.
- **Contraparte**: Connors & Raschke (1995), *Street Smarts* (Turtle Soup), a leitura oposta, citada só como risco.
- **Peças reaproveitadas** do laboratório: exclusão da rolagem pelo calendário, da 013, e stop atrás da estrutura com piso em adr, da 012 e da 013.

O ciclo 2210 descartou os extremos do dia anterior no WDO por dois motivos. O primeiro é a rolagem, que a regra de calendário da 013 resolve, aqui reforçada pela exclusão do dia seguinte. O segundo é que esses extremos "já falharam em WIN e VBBR3". O registro não tem nenhum teste de máxima ou mínima do dia anterior: a 005 usou o extremo de 20 pregões em VBBR3, e a 006 o reteste da abertura em WIN. Esta é a primeira hipótese do laboratório com esse nível.

Exploração descritiva, sem P&L com o lado do sinal (`research/scratch/explore_014.py`, `explore_014b.py`, `explore_014c.py`):
- **Primeira ideia, descartada antes de escrever:** NR4 e inside day de Crabel com rompimento do range anterior. Depois de um dia NR4 ou inside day, o range do dia seguinte tem mediana de 0,86 adr, **menor** que o dos outros dias (0,91). No dólar a compressão diária continua, como a intradiária na 010. Só sobravam ~68 sinais.
- Para o rompimento do extremo anterior, olhei a frequência e o horário dos sinais, o `over`, a distância do nível até a abertura (mediana de 0,30 adr), o range das barras e a excursão máxima sem lado em 60 e 120 minutos, comparada com barras sorteadas.
- Rodei também o benchmark de lado sorteado, para 3 valores de `b`, com `k` = 1,5, só para medir se o alvo é atingível. Ele não usa o lado do sinal.

Tentativas escondidas: **~3**, a olhada no NR4/ID (descartada pela descritiva, sem lado) e a escolha de `k` = 1,5 e da grade de `b` pela geometria do benchmark sorteado. Nada calculou resultado com o lado do rompimento. Somadas às ~22 efetivas de WDO_N_M5, o dataset chega a ~25 antes desta validação.

## Notas de implementação
- `stop = max(over + b × adr, 0,20 × adr)` e `alvo = k × stop` em pontos, com o `close` da barra de sinal. Sem aproximações além disso.
- `over` usa `|close − nível|` do lado rompido (PDH se `close > PDH`, senão PDL).
- "Pregão anterior na janela de rolagem" usa a coluna diária do dataset deslocada em 1 (passado). O primeiro dia do dataset não opera.
- Se o primeiro evento do dia tiver `over > over_max × adr`, o dia não opera (sem novo sinal depois).
- Dias com barra rotulada 09:00 a 09:25 fechando além de PDH/PDL não operam; só olha barras até 09:25.
- `k` e `over_max` ficam em `params` mas fora da `grid` (fixos).
Relatório: reports/20261023-225813_rompimento_extremo_anterior_WDO_N_M5
