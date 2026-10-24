# 002 · Momentum intradiário confirmado por VWAP e volume em BBAS3
- Dataset: BBAS3 M5
- Modo: daytrade
- Estado: REJEITADA

## Padrão
Quando BBAS3 se afasta bastante da abertura até o meio do dia, com o preço do mesmo lado da VWAP diária e volume acima do normal para o horário, o trecho que falta até o fechamento tende a seguir a mesma direção. É a replicação da 001 (WIN) num ativo independente, com os filtros de VWAP e volume que o usuário pediu.

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra de sinal):
- Só operar dias cuja primeira barra começa até 10:05. Isso descarta os 3 dias que abrem às 13:00 e o dia que abre às 10:15.
- `abertura_dia` = `open` da primeira barra do dia.
- Barra de sinal = a barra cujo **fechamento** acontece em `signal_time`. Para `"12:00"`, é a barra rotulada 11:55.
- `mov` = ln(`close` da barra de sinal / `abertura_dia`).
- `escala` = mediana de `|mov|` nos **20 dias anteriores**, sempre na mesma `signal_time` e excluindo o dia atual (`shift(1)`). Dias sem 20 dias de histórico não operam.
- `vw` = `vwap(df, "D")` de `strategies/_helpers.py`, lido na barra de sinal.
- `rv` = `relative_volume(df, 20)` de `strategies/_helpers.py`, lido na barra de sinal.

Entrada: posição alvo = `sinal(mov)` (+1 comprado, −1 vendido), definida no fechamento da barra de sinal, se as três condições valerem:
1. `|mov| > k × escala`;
2. `sinal(close − vw) == sinal(mov)`, ou seja, o preço está do lado da VWAP diária que confirma o movimento (estritamente acima numa alta, estritamente abaixo numa queda);
3. `rv > 1.0`, ou seja, o volume acumulado do dia está acima da mediana do mesmo horário nos 20 dias anteriores.

Se alguma condição falhar, não opera no dia. Pela convenção do motor, a execução acontece na abertura da barra seguinte. Há no máximo 1 entrada por dia, e só na barra de sinal.

Saída: mantém a posição até o fim do pregão, sem stop e sem alvo; o motor zera no fechamento (day trade). O pregão fecha às 16:50 ou às 17:50, conforme a época do ano.

Comprado e vendido, com tamanho pelo capital (padrão do motor para ações).

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| signal_time | "12:00" | ["12:00", "13:00", "14:00"] |
| k | 1.5 | [1.0, 1.5, 2.0] |

Fixos (não são parâmetros): janela de 20 dias da `escala` e do `rv`, limiar `rv > 1.0` e confirmação pela VWAP diária. Grade total: 9 combinações.

## Por que pode falhar
1. **Custos contra uma vantagem bruta minúscula (o risco principal).** Com tick de R$ 0,01 num preço de ~R$ 22, 1 tick de slippage por lado custa ~4,5 bp, e com os emolumentos (2,3 bp por lado) a ida e volta sai por ~14 bp. Na exploração, o ganho bruto médio por trade ficou entre ~6 e ~24 bp conforme a combinação. As de 13h e 14h ficaram quase todas abaixo do custo, e só as de 12h com k ≥ 1,5 e os filtros passaram com folga pequena (16 a 24 bp). Com custos 2x, é provável que quase tudo fique negativo. O resultado mais provável é REJEITADA, e isso já seria informação útil: o momentum intradiário da 001 não se transfere para uma ação com custo proporcional mais alto.
2. **Seleção na exploração e regime.** Os filtros de VWAP e de volume melhoraram as médias justamente nas combinações que eu olhei, então parte da melhora pode ser ruído selecionado. Em 2025, as combinações de 12h foram negativas ou nulas (−6 a +6 bp), e o efeito vem de 2023 (45 a 67 bp). Pode ser um regime de 2023 (ano eleitoral pós-transição, BBAS3 com notícias de governo) e não um padrão estável. 2026 tem só 0 a 3 trades.
3. **Poucos trades e cauda.** As versões mais filtradas operam 80 a 130 dias em 3 anos. Tirando os 5 melhores trades, a média bruta cai para ~8 a 11 bp, abaixo do custo. Como na 001, o lucro tende a depender de poucos dias de notícia.

Explicação econômica plausível (não obrigatória): é o mesmo canal da 001 (Gao, Han, Li e Zhou, *JFE*, 2018, sobre "market intraday momentum"), com reação lenta à informação da manhã e fluxo institucional que executa ao longo do dia usando a VWAP como referência. Um preço do lado certo da VWAP com volume alto sugere que o movimento tem participação de fluxo, e não só de ordens pequenas. Não há nota em `knowledge/` sobre isso.

## Origem
Variação da 001, por três motivos: (a) o relatório da 001 sugere replicar o momentum intradiário em outro ativo como teste independente; (b) o usuário pediu volume e VWAP nas próximas hipóteses; (c) BBAS3 não tem tentativas no registro, então o DSR parte do zero. O que mudou: os filtros de VWAP diária e de volume relativo viraram regras fixas, o `mov` passou a ser log-retorno (ação), e os horários de sinal foram para 12h, 13h e 14h. A combinação das 16h saiu porque em BBAS3 o pregão termina às 16:50 em parte do ano e a correlação ali foi negativa. A sobreposição com o ORB, que pesou na 001, aqui não é testada (não há ORB em BBAS3).

Exploração em `store.load("BBAS3", "M5")` (amostra de pesquisa 2023-01-02 → 2026-01-19), scripts `research/scratch/explore_002.py`, `explore_002b.py` e `explore_002c.py`. O que foi olhado (contar como tentativas escondidas: cerca de **75 variações** em 4 famílias de ideias):
1. `explore_002.py` (30 variações): para 5 horários (12h a 16h), correlação de `mov` com o resto do dia (0,07 a 0,11 até as 14h e −0,015 às 16h), seguir `mov` com e sem `k=1`, `rv > 1,2` e `rv < 1`, além do lado da VWAP como sinal. Médias brutas de −6 a +13 bp, todas abaixo do custo.
2. `explore_002b.py` (10 variações): momentum da primeira meia hora ou da primeira hora até o fechamento (6 a 8 bp), fade de gap de abertura (≈ 0 bp) e reversão ou continuação de desvios extremos da VWAP (z > 2 ou 3) até o fechamento. A reversão perdeu (−6 a −7 bp) e a continuação ficou em +6 a +7 bp. Tudo descartado por não pagar o custo.
3. `explore_002c.py` (27 variações): a grade proposta (3 horários × 3 valores de k), cada uma sem filtro, só com VWAP e com VWAP + `rv > 1`, com entrada na abertura da barra seguinte. A melhor foi 12h/k=2/VWAP+rv (83 trades, 24 bp brutos, 55% de acerto). Essa grade foi vista na amostra inteira antes do walk-forward, então o validador vai sair otimista.

Como a busca foi larga e a vantagem é marginal, o DSR deve ser calculado de forma conservadora, somando as ~75 variações escondidas às 9 registradas.

Relatório: reports/20261023-195314_momentum_vwap_volume_BBAS3_M5
