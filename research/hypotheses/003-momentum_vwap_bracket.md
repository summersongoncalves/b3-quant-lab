# 003 · Replicação pré-registrada do momentum + VWAP + volume em VBBR3, com stop, alvo e risco fixo por trade
- Dataset: VBBR3 M5
- Modo: daytrade
- Estado: REJEITADA

## Padrão
Quando VBBR3 se afasta bastante da abertura até as 12h, com o preço do lado certo da VWAP diária e volume acima do normal para o horário, o resto do dia tende a seguir a mesma direção. É o teste independente que o ciclo da 002 pediu: a regra de BBAS3 fica congelada e é aplicada sem grade de sinal num ativo novo. A única coisa que muda é o envelope de risco (stop, alvo e tamanho da posição).

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra de sinal):
- Só operar dias cuja primeira barra começa até **10:10**. Isso descarta os 2 dias que abrem às 10:15 e os 2 que abrem às 13:05. Na 002 o corte era 10:05, e o validador apontou que ele excluía, sem motivo, os dias que abrem às 10:10.
- `abertura_dia` = `open` da primeira barra do dia.
- Barra de sinal = a barra rotulada **11:55**, cujo fechamento acontece às 12:00. **Fixo, não é parâmetro.**
- `mov` = ln(`close` da barra de sinal / `abertura_dia`).
- `escala` = mediana de `|mov|` nos 20 dias anteriores, na mesma barra de sinal e excluindo o dia atual (`shift(1)`). Dias sem 20 dias de histórico não operam.
- `vw` = `vwap(df, "D")` e `rv` = `relative_volume(df, 20)`, ambos de `strategies/_helpers.py` e lidos na barra de sinal.
- `adr` = média de (máxima do dia − mínima do dia), em R$, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam.

Entrada (no máximo 1 por dia, só na barra de sinal). O lado é `sinal(mov)` (+ comprado, − vendido) se as três condições valerem:
1. `|mov| > 1.5 × escala` (k = 1,5, **fixo**);
2. `sinal(close − vw) == sinal(mov)`, com o preço estritamente do lado da VWAP que confirma o movimento;
3. `rv > 1.0`.

Se alguma falhar, não opera no dia. A execução é na abertura da barra 12:00, pela convenção do motor.

Tamanho (risco fixo por trade):
- `stop_dist` = `s × adr` (R$ por ação).
- `w` = min(1, 0,008 × `close` / `stop_dist`), em que `close` é o da barra de sinal.
- Posição alvo = `sinal(mov) × w`, mantida igual do sinal até o fim do pregão. Assim, uma perda no stop custa no máximo ~0,8% de R$ 100 mil antes dos custos. O stop nunca é apertado para caber no risco: quando ele é largo, quem diminui é a posição.

Saída:
- Stop loss e stop gain fixos a partir do preço de entrada (ver abaixo), lidos na barra de sinal. Depois de uma saída por bracket, a posição alvo continua com o mesmo sinal até o fim do dia, então o motor não reentra.
- O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor. A saída fica no fechamento, e não às 16:30, porque o canal econômico (Gao et al., 2018) é justamente o fluxo da última meia hora, e a 002 também saía no fechamento. Mexer na saída seria uma segunda variável.

## Risco e saída
Valores típicos com preço de ~R$ 21 e `adr` de ~R$ 0,55, que é cerca de 265 bp. As medianas por ano de `adr` foram R$ 0,50 a 0,57, ou 204 a 329 bp do preço.

- **Stop loss**: `s × adr`. Com s = 0,4, dá R$ 0,22, ou seja 22 ticks e ~105 bp. Com s = 0,3, são 16 ou 17 ticks (~79 bp). Com s = 0,5, são 27 ou 28 ticks (~131 bp). O range mediano de uma barra de M5 é de ~23 bp, ou 4 a 5 ticks, então mesmo o menor stop fica a ~3,4 barras de distância, fora do ruído de uma barra. Para uma posição cheia de R$ 100 mil, o stop vale R$ 790, R$ 1.050 ou R$ 1.310. Depois do ajuste de tamanho `w`, a perda no stop fica limitada a ~R$ 800.
- **Stop gain**: `2 × stop`. Com s = 0,4, são 44 ticks e ~210 bp. Com s = 0,3, são 33 ticks (~157 bp). Com s = 0,5, são 55 ticks (~262 bp). A partir do meio-dia, o alvo pede 0,6 a 1,0 `adr` e será atingido em poucos dias. A maioria dos trades deve sair por stop ou no fechamento. O alvo existe para travar os dias de continuação forte, que são a própria tese, e para não devolver o lucro no call.
- **Custo de ida e volta (C)**: emolumentos de 2 × 2,3 bp mais 1 tick de slippage por lado (2 × R$ 0,01 / preço). Isso dá ~14 bp com R$ 21 (2024 e 2025), ~18 bp com R$ 15 (2023) e ~12,4 bp com R$ 25,5 (2026). Para R$ 100 mil cheios, são ~R$ 140. Alvo/C: ~11x (s = 0,3), ~15x (s = 0,4) e ~19x (s = 0,5), com folga muito acima do mínimo de 3x.
- **Acerto de equilíbrio, só para o bracket**: `p* = (S + C) / (T + S)`. Dá (79 + 14) / (157 + 79) = 39,4% com s = 0,3, (105 + 14) / 315 = 37,8% com s = 0,4 e (131 + 14) / 393 = 36,9% com s = 0,5. Em 2023, com C de 18 bp e `adr` maior, p* fica parecido (~38%). Como boa parte dos trades sai no fechamento, o critério que vale na prática é: **bruto médio por trade acima de 2 × C (~28 bp) em cada ano**, e o resultado sem os 5 maiores trades precisa continuar positivo. Esses foram os critérios de sucesso definidos no ciclo da 002.
- **Taxa de acerto esperada**: 50% a 55% dos trades positivos, contando as saídas no fechamento, contra o p* de ~38% do bracket puro. Essa expectativa vem só da 002 (BBAS3, melhor combinação: 55% de acerto e 24 bp brutos, número otimista porque foi minerado). Não olhei o momentum em VBBR3. O motivo para esperar algo melhor que em BBAS3 é o custo relativo: VBBR3 oscila de 30% a 50% a mais por dia (`adr` de ~265 bp contra ~180 bp), com custo quase igual, então o custo come uma fração menor do movimento típico. Minha expectativa honesta é de rejeição. Mesmo assim, o teste vale a pena: é a forma mais barata, em tentativas, de saber se o padrão existe fora de BBAS3.
- **Perda máxima por trade, custos incluídos**: ~0,8% do capital de stop mais ~0,14% × `w` de custo, ou seja ≤ ~R$ 940 (0,94% de R$ 100 mil). Em 2023, com C de 18 bp, fica em ~R$ 980. A exceção é o gap dentro do pregão (uma barra que abre além do stop, como numa notícia ao meio-dia). Nesse caso a saída é na abertura da barra e a perda pode passar de 1%.
- **Entradas por dia**: no máximo 1, só às 12:00. Não há entrada no leilão de abertura, nem na primeira hora, nem perto do call. A saída no fechamento é intencional (ver Regras).

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| stop_mult (s) | 0.4 | [0.3, 0.4, 0.5] |

Fixos (não são parâmetros e não podem ir para a grade): sinal às 12:00, k = 1,5, `rv > 1.0`, confirmação pela VWAP diária, janelas de 20 dias, alvo = 2 × stop e risco de 0,8% por trade no ajuste de tamanho. Grade total: **3 combinações**. Como a regra de sinal está congelada, a grade só move o envelope de risco, e as três combinações devem dar o mesmo sinal de resultado. Se só uma funcionar, é ruído.

## Por que pode falhar
1. **Herda a mineração de BBAS3.** A regra de 12h com k = 1,5, VWAP e volume saiu de ~84 variações em BBAS3, e mesmo lá o OOS foi zero sem um único trade (05/12/2025). Se o padrão era ruído selecionado, ele não vai aparecer em VBBR3. Essa é exatamente a pergunta do teste, e um resultado negativo aqui fecha a família "momentum intradiário em ações".
2. **Custo ainda alto e poucos trades.** Com C de 12 a 18 bp e os três filtros, devem sair só ~80 a 130 trades em 3 anos, poucos para um DSR alto. Em 2023, com a ação a R$ 15, o custo é o maior da amostra. Se o bruto ficar abaixo de ~28 bp num ano, a hipótese falha no critério de estabilidade.
3. **Cauda e notícia.** VBBR3 se mexe com petróleo, Petrobras e política de preços de combustível. Dias de notícia (anúncio de reajuste, resultado) podem concentrar o lucro. O stop e o tamanho por risco limitam o estrago nos dias ruins, mas não criam vantagem nos normais. O `stop_both` deve ser raro, porque o stop está a 3 ou mais barras de range. Se passar de ~5% das saídas, o resultado está otimista ou pessimista por causa da hipótese do motor sobre a ordem dos toques.

## Por que é conservadora
Uma entrada por dia, no meio do pregão, longe dos leilões. O stop é proporcional à volatilidade já conhecida, e o tamanho da posição é calculado para que um stop custe ~0,8% do capital, somando no máximo ~0,95% com os custos. A regra de sinal é congelada antes de olhar o ativo, com só 3 tentativas no registro. Um gestor de risco aprovaria porque o pior dia normal é conhecido de antemão e porque a pesquisa não está ajustando o sinal ao ativo.

## Origem
Variação pré-registrada da 002, seguindo os "Próximos passos" 2 e 5 de `reports/ciclos/20261023-1955_BBAS3_M5.md`: congelar a regra (12h, k = 1,5, VWAP + volume relativo) e rodá-la num ativo líquido independente, com o critério de bruto acima de 2x o custo em cada ano e o resultado sem os 5 maiores trades positivo. O que mudou em relação à 002:
- ativo (VBBR3);
- corte de primeira barra em 10:10, corrigindo a nota do validador;
- stop e alvo proporcionais a `adr`, pedidos pelo perfil de risco;
- tamanho da posição por risco fixo;
- grade só no stop.

Não há nota em `knowledge/` (a pasta `knowledge/notas` está vazia). A referência econômica é a mesma da 001 e da 002 (Gao, Han, Li e Zhou, *JFE*, 2018).

Tentativas escondidas em VBBR3, **antes** de escolher esta ideia. Nenhuma delas olhou o momentum do meio-dia em VBBR3:
1. `research/scratch/explore_003.py`: rompimento do range da primeira hora (10:00–11:00) com stop `s × adr` e alvo de 1,5x, `s` ∈ {0,25; 0,35; 0,5}, com e sem `rv > 1`. São **6 variações**, todas com bruto de ~0 bp e líquido de −11 a −19 bp por trade. Descartado.
2. `research/scratch/explore_003b.py`: gap de abertura em 7 faixas de z contra o retorno de 10:30 a 16:25. São **7 variações**, não monotônicas (z < −3: +70 bp em 40 dias; vizinho: −29 bp), o que é ruído. Descartado.
3. Estatísticas de volatilidade e custo por ano (`adr`, range por barra e C em VBBR3 e BBAS3), usadas para calibrar o stop. Conta como **1** tentativa.

Total: **~14 tentativas escondidas em VBBR3**, mais as 3 da grade. A regra de sinal vem de ~84 tentativas em BBAS3, que não entram no DSR de VBBR3 mas devem pesar na leitura qualitativa.

Relatório: reports/20261023-203030_momentum_vwap_bracket_VBBR3_M5
