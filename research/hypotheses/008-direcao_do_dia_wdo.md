# 008 · Direção do dia no WDO: replicação pré-registrada da 007, sem mudança de regra
- Dataset: WDO$N M5
- Modo: daytrade
- Estilo: direcional
- Estado: REJEITADA

## Padrão
Na 007, quando o WIN se afasta pelo menos 0,3 `adr` da abertura para um lado só até as 10:30 e continua desse lado, o pregão tende a fechar desse mesmo lado. Esta hipótese testa se o mesmo efeito, "a excursão da manhã decide a direção do dia", **generaliza para o mini dólar (WDO$N)**. A regra é a da 007, sem nenhuma mudança.

É uma **replicação pré-registrada**. O módulo a validar é o mesmo `direcao_do_dia` (`src/quantlab/strategies/direcao_do_dia.py`), **sem nenhuma mudança de código**: o implementador não escreve módulo novo. Só muda o dataset. Todas as regras, limiares, horários, stop e alvo foram herdados da 007 antes de qualquer conta no WDO. A única exploração feita no WDO foi descritiva, sem P&L (ver Origem). Não há grade.

## Regras
São as mesmas da 007, copiadas aqui para o pré-registro ficar completo. Barras de 5 min são rotuladas pelo horário de abertura, e tudo é calculado no fechamento da barra de sinal.
- Só operar dias cuja primeira barra começa até **09:30**.
- `abertura` = `open` da primeira barra do dia.
- `adr` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam. A regra não usa nada entre pregões, então os saltos de rolagem mensal da série contínua WDO$N não a afetam.
- Barra de sinal = a barra rotulada **10:25**, que fecha às 10:30. Se o dia não tiver essa barra, não opera.
- `max_m` / `min_m` = máxima e mínima do dia até a barra de sinal, incluindo ela.
- `exc_alta` = `max_m − abertura ≥ 0,3 × adr`. `exc_baixa` = `abertura − min_m ≥ 0,3 × adr`.
- `lado` = +1 se `exc_alta` e não `exc_baixa`; −1 se `exc_baixa` e não `exc_alta`; 0 nos outros casos (não opera).
- Filtro "o lado ainda vale": `(close − abertura) × lado ≥ 0,1 × adr`, com o `close` da barra de sinal.

Entrada:
- Posição alvo = `lado` (1 contrato), definida no fechamento da barra 10:25 e executada na abertura da barra 10:30, pela convenção do motor.
- A posição alvo fica igual a `lado` até o fim do pregão, para que o motor não reentre depois de uma saída por stop ou alvo.
- No máximo 1 entrada por dia, e nenhuma em outro horário.

Saída:
- Stop loss e stop gain fixos (abaixo), lidos na barra de sinal. Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão, zerado pelo motor.

## Risco e saída
**A regra se aplica ao WDO sem adaptação.** As descritivas abaixo vêm da amostra de pesquisa (05/04/2023 a 05/02/2026, 709 pregões, sem holdout e sem P&L):
- O WDO abre às **09:00**, como o WIN. A primeira barra é das 09:00 em 703 dias e das 09:05 em 3. Em 3 dias ela começa às 12:00 ou 13:00, entre eles o primeiro dia da série (05/04/2023, que começa às 12:00); esses 3 são excluídos pelo corte de 09:30.
- A barra 10:25 existe em 706 dos 709 dias. Ela fecha 1h30 depois da abertura, a mesma distância do leilão que na 007.
- A última barra é das 18:25 em 561 dias e das 17:55 em 145 dias (mudança de grade horária). A saída no fechamento é a do motor nos dois casos.
- 687 dias são válidos: têm a barra 10:25, abertura até 09:30 e 20 pregões de histórico. Em 39 deles a excursão foi para os dois lados, e 485 têm lado definido.
- **396 sinais passam no filtro**, ~56% dos dias válidos (na 007 eram 54%). Por ano: 97 em 2023 (desde abril), 149 em 2024, 134 em 2025 e 16 em 2026. São 197 compras e 199 vendas.
- `adr` mediano de **57,3 pontos** (p10 42,3, p90 75,8). O preço mediano é de ~5.396 pontos.
- Range de uma barra de M5 entre 09:25 e 10:20: mediana de 6,5 pontos, média de 7,6.
- `|close − abertura|` mediano de 0,36 `adr` nos dias de sinal (0,32 no WIN).

Unidades do WDO: 1 ponto = R$ 10 por contrato, e o tick vale 0,5 ponto (R$ 5).

- **Stop loss** (atrás da estrutura): o nível é `abertura − 0,1 × adr` no comprado e `abertura + 0,1 × adr` no vendido. A distância passada ao motor é `stop = (close − abertura) × lado + 0,1 × adr`, de no mínimo 0,2 `adr` pelo filtro.
  - Mediana de **26,6 pontos, ou ~53 ticks e ~R$ 266 por contrato**, cerca de 3,5 ranges médios de barra (4,3 no WIN).
  - p10 de 13,6 pontos (R$ 136), p90 de 48,4 pontos (R$ 484), máximo de 90,4 pontos (R$ 904).
  - Ponto de atenção: 58 sinais (15%) têm stop abaixo de 15 pontos (~2 ranges de barra), e o mínimo é 7,3 pontos (~1 range de barra). Nesses dias o stop fica perto do ruído. Isso não foi corrigido, porque a regra é replicada intacta.
- **Stop gain** (dia esgotado): o nível é `abertura ± 1,0 × adr`. A distância é `alvo = (abertura + lado × adr − close) × lado`.
  - Mediana de **34,9 pontos, ou ~70 ticks e ~R$ 349 por contrato**.
  - p10 de 16,0 pontos e p90 de 52,6 pontos.
  - Ponto de atenção: 3 sinais têm alvo abaixo de 3 × C (mínimo de 0,9 ponto) e 15 têm alvo abaixo de 7,5 pontos. É a mesma regra da 007: só são descartados alvos ≤ 0. Esses sinais ficam na amostra, porque a replicação não muda nada.
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) mais emolumentos de 2 × R$ 1,20 (= 0,24 ponto). Dá **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**.
  - **Alvo/C ≈ 28x** na mediana.
  - O custo é ~4,7% do stop mediano, contra ~1,5% no WIN: em relação ao movimento, o WDO é ~3x mais caro que o WIN. Ainda assim, isso não deve ser o que decide o resultado.
- **Acerto de equilíbrio** do bracket, com medianas: `p* = (S + C) / (T + S) = (26,6 + 1,24) / (34,9 + 26,6) ≈ 45%`, contra 43% na 007. Como na 007, esse p* só vale para os trades que terminam em stop ou alvo. A expectativa também depende das ~40% de saídas no fechamento.
- **Taxa de acerto esperada**: ~53 a 56% de trades positivos, **se** o efeito generalizar. A 007 teve 56% em WIN. Stop e alvo estão em unidades de `adr`, então a geometria do bracket é a mesma nos dois mercados.
  - O argumento econômico para o dólar é plausível, mas diferente do WIN. O fluxo do dia (exportadores e importadores, tesouraria de bancos, ajuste de hedge e operações de estrangeiros) tende a se revelar cedo e a persistir. Quem está do outro lado é quem faz o fade da excursão da manhã.
  - O contra-argumento: no câmbio o Banco Central intervém (leilões de swap e de linha), e isso pode reverter os dias de excursão forte. Não há expectativa de que o WDO seja melhor que o WIN. O teste é justamente esse.
- **Perda máxima por trade, custos incluídos**:
  - no stop mediano, ~R$ 278, ou **~0,28% de R$ 100 mil**;
  - no p90, ~R$ 496 (0,50%);
  - no pior stop da amostra, ~R$ 916 (0,92%).
  
  Tudo fica abaixo de 1%, mas o pior caso fica mais perto do limite do que no WIN (0,57%). Um gap de barra além do stop pode piorar isso, e no dólar os gaps intradiários por notícia (BC, dados dos EUA às 09:30 ou 10:00 de Brasília, fala de autoridade) são mais prováveis que no WIN. Esse é um ponto a medir no relatório.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: estimativa *a priori* de **~25 a 30%**, tirada da 007 (29% no alvo, 30% no stop, 41% no fechamento), porque o alvo está na mesma posição em unidades de `adr` e o pregão restante (~8h) é parecido. **Não medi a frequência de saídas no WDO**, de propósito: ela é praticamente uma conta de resultado e seria uma tentativa escondida. O validador deve comparar a frequência realizada com 29/30/41.
- **Entradas por dia**: no máximo 1, só na abertura da barra 10:30. Ficam fora a primeira 1h30 (leilão, divulgações das 09:30 e 10:00, formação da excursão) e qualquer entrada à tarde.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| (nenhum) | | |

São fixos, herdados da 007 e fora de qualquer grade: barra de sinal 10:25, excursão de 0,3 `adr` de um lado só, filtro de 0,1 `adr`, `adr` de 20 pregões, stop em `abertura ∓ 0,1 adr`, alvo em `abertura ± 1,0 adr`, corte de abertura em 09:30 e 1 contrato. **Grade total: 1 combinação.** O walk-forward só mede a estabilidade no tempo.

Critérios prévios de sucesso, além dos `GATES` (os mesmos da 007):
1. Líquido médio por trade positivo em 2024 e em 2025, cada ano separadamente. 2023 (desde abril) é reportado, mas não conta; 2026 tem 16 sinais e também não conta.
2. Resultado positivo sem os 10 maiores trades, e também sem os 20 maiores. A 007 falhou neste critério em WIN (−R$ 81 sem os 20 maiores). Se o WDO falhar igual, isso confirma que o efeito depende de cauda nos dois mercados.
3. **Comparação obrigatória com a mesma entrada sem stop e sem alvo**, segurada até o fechamento, com o mesmo filtro. Se o bracket piorar o Sharpe em mais de 0,3, isso tem que ser registrado. A hipótese não vira "sem stop" por causa disso.
4. **Correlação diária com a 007 em WIN** (P&L diário nos dias em comum e em todos os dias). Uma correlação alta (> ~0,5) indica que os dois mercados respondem ao mesmo fator macro do dia (risco Brasil), e aí operar os dois não diversifica. Uma correlação baixa com resultado positivo é a evidência mais forte de que o efeito é estrutural.
5. Leitura da replicação: o efeito **generaliza** se o critério 1 passar e o Sharpe OOS for positivo e da mesma ordem que o da 007 (≥ ~0,7). Se o Sharpe OOS ficar ≤ 0, o efeito é específico do WIN, e isso tem que constar no relatório da 007 como ressalva.

## Por que pode falhar
1. **O efeito é do WIN, não da microestrutura geral.** O *intraday momentum* do índice pode vir do fluxo de hedge do mercado à vista e de ETFs, que não existe do mesmo jeito no dólar. No câmbio, as intervenções do BC e a arbitragem com o dólar à vista e o cupom podem reverter as excursões da manhã. Se for assim, o acerto fica perto do p* de 45% e o Sharpe perto de zero.
2. **Dependência de cauda, de novo.** Na 007, o resultado sumia sem os 20 maiores trades. No dólar, os dias de tendência forte se concentram em choques (fiscal, eleição, Copom, *payroll*). Um resultado positivo pode vir de ~10 dias de notícia, o que é exatamente o que um trader conservador não quer.
3. **Stop no ruído e custo relativo maior.** 15% dos sinais têm stop abaixo de ~2 ranges de barra, e o custo pesa ~3x mais em relação ao stop do que no WIN. Gaps de notícia além do stop são mais prováveis no dólar. Juntos, esses fatores podem tirar ~0,1 a 0,2 de Sharpe, o que a 007 em WIN não sofria.

## Por que é conservadora
Uma entrada por dia, num horário fixo, longe dos leilões, com 1 contrato e sem nenhum parâmetro livre. A regra foi escrita em outro mercado antes de qualquer conta neste, então o teste é tão limpo quanto possível: n = 1 tentativa num dataset virgem. O stop fica num nível objetivo (a abertura com folga de 0,1 `adr`) e custa ~R$ 278 (0,28% do capital) na mediana. O pior caso da amostra fica em 0,92%, dentro do limite de 1%. Não há preço médio nem reentrada.

## Origem
Replicação da 007 (`research/hypotheses/007-direcao_do_dia.md`, relatório `reports/20261023-213418_direcao_do_dia_WIN_N_M5`). É a recomendação do ciclo `reports/ciclos/20261023-2138_WIN_N_M5.md` (próximos passos, item 1). Não muda nada na regra: só o dataset muda, de WIN$N para WDO$N.

Tentativas escondidas no WDO_N_M5:
1. **Descritivas sem P&L** (`desc008.py`, no scratchpad da sessão, com `store.load("WDO$N", "M5")` e sem holdout):
   - horário da primeira e da última barra;
   - existência da barra 10:25;
   - `adr` e range de barra;
   - contagem de sinais por ano e por lado;
   - distribuição das distâncias de stop e alvo, e contagem de stops e alvos pequenos.

   **Não calculei retorno, acerto, MAE, MFE nem frequência de saídas (alvo, stop, fechamento).** Nada nas descritivas mudou a regra, e nenhuma escolha foi feita a partir delas.
2. Total: **~0 tentativas escondidas e 1 registrada.** WDO_N_M5 não tinha nenhuma tentativa antes desta. Com n = 1, o DSR é praticamente o PSR, e um Sharpe OOS da ordem de ~1,0 a 1,2 já deve bastar para DSR ≥ 95%, dependendo do número de trades e da assimetria.
3. A escolha do WDO como mercado de replicação e da 007 como regra a replicar foi feita pelo ciclo anterior, por causa do resultado da 007 em WIN. Isso é seleção pelo resultado em outro dataset, e não neste. Mesmo assim, se a 008 passar, o relatório deve dizer que a regra replicada foi a melhor de ~56 tentativas efetivas em WIN.

## Notas de implementação
- **Nenhum código novo.** Validar o módulo existente `direcao_do_dia` com o dataset WDO$N M5. `params={}` e `grid={}`: 1 combinação.
- `instruments.for_symbol` já mapeia `WDO*` para o instrumento WDO (tick de 0,5, R$ 10 por ponto, R$ 1,20 por contrato por lado, 1 tick de slippage).
- O módulo declara `timeframe="M5"` e usa só horários (09:30 e 10:25) e o `adr` em pontos do próprio instrumento. Nada nele é específico do WIN.

Relatório: reports/20261023-215505_direcao_do_dia_WDO_N_M5
