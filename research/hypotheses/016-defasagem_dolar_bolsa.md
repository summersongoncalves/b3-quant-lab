# 016 · Defasagem do dólar em relação à bolsa: quando o WIN define o lado da manhã e o WDO ainda não acompanhou, operar o WDO no lado oposto ao do WIN
- Dataset: WDO$N M5 (com WIN$N M5 como informação auxiliar, só leitura)
- Modo: daytrade
- Estilo: direcional
- Estado: REJEITADA

## Padrão
O dólar e a bolsa brasileira reagem ao mesmo fator de risco (fluxo estrangeiro, risco-país, apetite global), com correlação de −0,49 entre os movimentos da manhã (abertura até 11:00, em `adr`) e de −0,55 no dia inteiro, na amostra de pesquisa. Quando o WIN anda bem para um lado até as 11:30 e o WDO ainda **não** andou o que essa relação sugere, esperamos que o WDO recupere a defasagem no resto do pregão. Entramos no WDO do lado oposto ao do WIN, e esperamos que o preço chegue a 1,5 vez a distância do stop com mais frequência que a geometria neutra (~38% entre os trades resolvidos).

O que muda em relação a tudo que já se testou no WDO M5 é a **fonte do lado**. Nas hipóteses 008, 012, 013, 014 e 015, o lado vinha do próprio dólar: excursão da manhã, extensão do IB, gap, extremos de ontem, tendência de 5 pregões. Em todas o acerto ficou no nível do sorteio. Aqui o lado vem de **outro mercado**. O filtro ainda exige que o próprio WDO **não** tenha andado a favor, o que separa esta regra da 008, em que o sinal era o WDO já ter andado.

## Regras
Barras de 5 min, rotuladas pelo horário de abertura. Tudo é calculado no fechamento da barra de sinal. Os dois ativos usam as mesmas definições, cada um com os próprios dados.

Dados do WIN:
- Dentro de `signal_fn`, carregar `store.load("WIN$N", "M5")` (sem `include_holdout`) e alinhar ao índice do `df` do WDO pelo **timestamp exato da barra**. Do WIN, só se usam a barra rotulada 11:25 do mesmo dia e os pregões **anteriores** (para o `adr`).
- **Causalidade**: o `lookahead_check` do motor só trunca o `df` do WDO, então não detecta vazamento vindo do WIN. Por isso o implementador deve garantir duas coisas. (1) Para cada barra t do WDO, só barras do WIN com timestamp ≤ t entram no cálculo. (2) Só dias presentes no `df` recebido são sinalizados. Um teste próprio que trunque também o WIN no mesmo ponto é bem-vindo.
- O WIN de pesquisa termina em 04/02/2026 (o holdout dele começa em 05/02). Dias sem a barra 11:25 do WIN não operam.

Definições diárias (para cada ativo X ∈ {WDO, WIN}):
- Só operar dias em que a primeira barra dos **dois** ativos começa até **09:05**.
- `abertura_X` = `open` da primeira barra do dia.
- `adr_X` = média de (máxima do dia − mínima do dia), em pontos, nos **20 pregões anteriores** do próprio ativo (`shift(1)`, sem o dia atual). Dias sem 20 pregões de histórico não operam.
- **Exclusão da rolagem** (só pelo calendário, como na 013/014/015): não operar se `data ≥ data + BMonthEnd(0) − BDay(1)`, ou seja, nos 2 últimos dias úteis do mês. A regra não usa nada entre pregões além do `adr`, que é um range intradiário e não sofre com o salto de vencimento. Os vencimentos bimestrais do WIN (quarta-feira mais próxima do dia 15 dos meses pares) também não afetam nada, porque só se usa `close − abertura` do mesmo dia.

Barra de sinal = a barra rotulada **11:25** (fecha às 11:30), nos dois ativos. Se faltar em algum dos dois, o dia não opera.
- `z_win` = (`close_WIN(11:25)` − `abertura_WIN`) / `adr_WIN`.
- `z_wdo` = (`close_WDO(11:25)` − `abertura_WDO`) / `adr_WDO`.
- `lado` = −sinal(`z_win`): comprar dólar quando a bolsa cai, vender quando a bolsa sobe.

Entrada (no máximo 1 por dia, só nesta barra):
- Condição da bolsa: `|z_win| ≥ k` (padrão 0,30). O WIN andou pelo menos 0,3 do seu range médio e continua desse lado às 11:30.
- Condição de defasagem: `z_wdo × lado ≤ m` (fixo em 0,20). O WDO andou no máximo 0,2 `adr` a favor do lado esperado, ou ficou parado, ou andou contra.
- Posição alvo = `lado` (1 contrato), definida no fechamento da barra 11:25 e executada na abertura da barra 11:30, pela convenção do motor. A posição alvo fica igual a `lado` até o fim do pregão (ffill por dia), para o motor não reentrar depois de uma saída por stop ou alvo.
- Nenhuma entrada em outro horário. A entrada às 11:30 fica longe do leilão de abertura, depois da janela de PTAX das 11:00 às 11:10 e muito antes do call de fechamento.

Saída:
- Stop loss e stop gain fixos (abaixo), lidos na barra de sinal. Não há saída por sinal. O que não bater stop nem alvo sai no fechamento do pregão (18:25 em 561 dias e 17:55 em 145, conforme a grade horária), zerado pelo motor.

## Risco e saída
Unidades do WDO: 1 ponto = R$ 10 por contrato, e o tick vale 0,5 ponto (R$ 5). Os números vêm da amostra de pesquisa, sem holdout e sem P&L. O `adr` mediano é de 57,3 pontos (p10 42,3, p90 75,8, máximo 112,1). O range mediano de uma barra M5 entre 11:30 e 17:30 é de **3,5 pontos** (p90 7,5).

- **Stop loss**: `stop = s × adr_WDO`, a partir do preço de entrada, fixo.
  - `s` = 0,25 (padrão): mediana de **14,3 pontos, ~29 ticks, ~R$ 143 por contrato**. São ~4 ranges medianos de barra da tarde, então `stop_both` deve ser raro (0 na 015, com geometria parecida).
  - `s` = 0,20: ~11,5 pontos (~23 ticks, R$ 115). `s` = 0,30: ~17,2 pontos (~34 ticks, R$ 172).
  - A ideia está errada quando o dólar anda ~1/4 do range médio **contra** o lado da bolsa: aí quem manda no dólar é um fluxo próprio (BC, exportador, fiscal), e não a defasagem.
- **Stop gain**: `alvo = 1,5 × stop`, fixo. Com `s` = 0,25, a mediana é de **~21,5 pontos, ~43 ticks, ~R$ 215 por contrato** (~0,375 `adr`).
- **Custo de ida e volta (C)**: 1 tick de slippage por lado (2 × 0,5 ponto) mais emolumentos de 2 × R$ 1,20, o que dá **C ≈ 1,24 ponto ≈ 2,5 ticks ≈ R$ 12,40**. **Alvo/C ≈ 17x** na mediana. Mesmo no menor caso (`s` = 0,20 com `adr` no p10), o alvo de ~12,7 pontos passa de 10 C.
- **Acerto de equilíbrio**: `p* = (S + C) / (T + S)`.
  - `s` = 0,25: (14,3 + 1,24) / (21,5 + 14,3) = **43,4%**.
  - `s` = 0,20: (11,5 + 1,24) / (28,7) = 44,3%.
  - `s` = 0,30: (17,2 + 1,24) / (43,0) = 42,9%.
- **Geometria neutra** (descritiva, sem lado). Entrada na abertura da barra 11:30, em todos os dias válidos, com os dois lados sorteados igualmente:

  | `s` | alvo | stop | fechamento | acerto neutro entre resolvidos |
  |---|---|---|---|---|
  | 0,20 | 36% | 54% | 10% | 39,9% |
  | 0,25 | 29% | 49% | 22% | 37,6% |
  | 0,30 | 24% | 43% | 33% | 35,9% |

- **Acerto esperado**: ~44% a 46% entre os resolvidos com `s` = 0,25, ou seja, 6 a 8 p.p. acima do neutro, só se a defasagem for real. O porquê: com correlação de −0,5, um movimento de 0,3+ `adr` do WIN "pede" ~0,15 a 0,25 `adr` do WDO, e a regra só entra quando esse ajuste ainda não aconteceu. **Se o acerto entre os resolvidos ficar abaixo de ~40%, o efeito não existe, e a hipótese cai.** A margem sobre p* é pequena (1 a 3 p.p.), e digo isso abertamente: é um teste de existência da defasagem, não uma aposta de alto acerto.
- **Perda máxima por trade, custos incluídos**: típica de 14,3 + 1,24 ≈ 15,5 pontos, ou **R$ 155 (0,16% de R$ 100 mil)**. No pior `adr` da amostra (112) com `s` = 0,30: 33,6 + 1,24 ≈ R$ 349 (0,35%). Só um gap intradiário além do stop (notícia) passa disso, e a 015 não teve nenhum com geometria igual.
- **Fração esperada de trades que chegam ao alvo antes do fechamento**: pela geometria neutra, **~29% com `s` = 0,25** (36% com 0,20 e 24% com 0,30). Se o efeito existir, algo como 32% a 35%. Cerca de 22% dos trades devem sair no fechamento com `s` = 0,25. O alvo é atingível: são 7 horas de pregão para andar ~0,375 `adr`.
- **Entradas por dia**: no máximo 1, só às 11:30. Não há entradas antes das 11:30 nem perto do call de fechamento.
- **Frequência**: com `k` = 0,30 e `m` = 0,20, são **~136 sinais** na amostra (33 em 2023 desde abril, 43 em 2024, 52 em 2025 e 8 em 2026), com 74 compras e 62 vendas. O mínimo dos `GATES` é de 30 trades OOS. O walk-forward começa em ~08/2023, então devem sobrar ~115 trades OOS.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| s (stop em `adr` do WDO; alvo = 1,5 × stop) | 0.25 | [0.20, 0.25, 0.30] |
| k (movimento mínimo do WIN em `adr` do WIN) | 0.30 | [0.30] (fixo) |
| m (movimento máximo do WDO a favor, em `adr` do WDO) | 0.20 | [0.20] (fixo) |

São 3 combinações. `k` e `m` ficam fixos e não entram na grade.

## Por que pode falhar
1. **A correlação é contemporânea, não defasada.** Os dois mercados reagem juntos à notícia, e um WDO que "não acompanhou" pode ter informação própria: intervenção do BC, fluxo de exportador, notícia fiscal, PTAX. Nesse caso a divergência é informação do dólar, e não atraso, e o acerto fica no nível do neutro, como em todas as anteriores. É o modo de falha mais provável.
2. **Poucos trades e a margem fina sobre p\*.** Com ~115 trades OOS, o erro-padrão do acerto é de ~4,6 p.p. Uma vantagem de 6 p.p. sobre o neutro mal se distingue do acaso, e o DSR deve ser exigente.
3. **Regime.** Em 2024 o dólar subiu por motivo doméstico (fiscal), com a bolsa caindo junto. Os sinais de "comprar dólar porque a bolsa cai" podem concentrar o lucro (ou a perda) num só semestre. O validador deve olhar o resultado por ano e por lado.

Pré-registro para o validador (antes de qualquer resultado):
- **Acerto entre resolvidos.** Com `s` = 0,25, deve ficar ≥ 42%. Abaixo de 40% (o neutro), a hipótese cai.
- **Controle 1, sem defasagem.** Mesmo lado (−sinal de `z_win`), todos os dias com `|z_win| ≥ 0,30`, sem a condição de `m`. Se o controle for igual ou melhor por trade, a "defasagem" não acrescenta nada, e o sinal seria só "dólar contra a bolsa".
- **Controle 2, lado do próprio WDO.** Nos mesmos dias de sinal, lado = sinal(`z_wdo`). Serve para conferir que o resultado não é a 008 disfarçada.
- **Concentração.** O resultado deve continuar positivo sem os 10 maiores trades.
- **Correlação diária** com 008 e 015 nos dias em comum.

## Por que é conservadora
Uma entrada por dia, 1 contrato, stop fixo definido na entrada (~R$ 155 com custos, 0,16% do capital de referência), alvo 17x o custo e nenhuma reentrada. A entrada às 11:30 evita o leilão de abertura, a primeira hora e o call de fechamento. A grade só varia o stop (3 combinações), e os dois limiares de sinal ficam fixos. Um gestor de risco aprovaria porque a perda por trade é pequena e conhecida, e porque a regra se derruba sozinha com critérios declarados antes do teste.

## Origem
Combinação de três ideias conhecidas, adaptada ao par WIN/WDO:
- **Lead-lag entre mercados**: Lo & MacKinlay (1990), *When are contrarian profits due to stock market overreaction?*, sobre autocorrelação cruzada; Hou (2007), *Industry information diffusion and the lead-lag effect in stock returns*. A informação chega primeiro ao mercado mais líquido ou mais exposto ao fator, e os outros acompanham com atraso. Citado de memória.
- **Ligação entre câmbio e bolsa via fluxo de capital**: Hau & Rey (2006), *Exchange rates, equity prices, and capital flows* (RFS). O retorno da bolsa local e o câmbio se movem juntos pelo rebalanceamento de investidores estrangeiros, e no Brasil isso aparece como bolsa para baixo e dólar para cima. Citado de memória.
- **Convergência de pares**: Gatev, Goetzmann & Rouwenhorst (2006), *Pairs trading*. Entrar no ativo que ficou para trás quando o par diverge. Aqui só a perna do WDO é operada (day trade, 1 contrato), sem hedge no WIN.
- O **horário da decisão**, um ponto fixo depois da manhã segurado até o fechamento, vem da família de momentum intradiário: Gao, Han, Li & Zhou (2018), *Market intraday momentum*, e a 001 do laboratório (WIN).

Quem está do outro lado: participantes do dólar que ainda não ajustaram ao movimento de risco da bolsa, como exportadores e importadores com ordens em níveis, tesourarias que operam em torno das janelas de PTAX e o market maker que fornece liquidez parado. O risco é que eles saibam algo que a bolsa não sabe (ver "Por que pode falhar", item 1).

Exploração feita (só descritiva, sem P&L, sem retorno condicionado ao lado, sem MAE/MFE por lado):
- Correlação contemporânea de `close − abertura` em `adr` entre WDO e WIN: −0,44 até 10:30, −0,49 até 11:00 e −0,55 no dia inteiro (625 dias válidos).
- Contagem de sinais para barras de sinal 10:25, 10:55 e 11:25, `k` ∈ {0,25; 0,3; 0,4; 0,5} e `m` ∈ {0; 0,1; 0,2; 0,3}. Escolhi 11:25 / 0,30 / 0,20 porque dá ~136 sinais (o bastante para os `GATES`), porque a entrada fica depois da janela de PTAX das 11:00 e porque 0,30 `adr` é o limiar de excursão já usado na 007/008. Foi uma escolha só por frequência, e a declaro aqui.
- Geometria neutra do bracket a partir das 11:30 (tabela acima), nos dois lados, em todos os dias válidos.
- Range de barra M5 da tarde, distribuição do `adr`, horário da última barra, cobertura dos dados do WIN (até 04/02/2026).

**Tentativas escondidas**: nenhuma baseada em resultado. As escolhas de horário, `k` e `m` usaram só contagem de sinais. Contando o mesmo critério das hipóteses anteriores, registro **1** tentativa escondida, pela escolha entre 3 horários e vários limiares olhando a frequência. Com isso o dataset WDO_N_M5 deve ficar perto de ~33 tentativas efetivas depois desta, ainda abaixo do limite de ~50.

## Notas de implementação
- Módulo `defasagem_dolar_bolsa`. `signals(df, s, k, m, win=None)`: sem `win`, carrega `store.load("WIN$N", "M5")` (sem holdout); `win` existe só para o teste de causalidade. O WIN é cortado em `timestamp <= última barra do WDO` antes de qualquer cálculo.
- `stop = s * adr_WDO` e `alvo = 1,5 * stop`, em pontos, calculados na barra 11:25 e repetidos (ffill por dia) até o fim do pregão; sem entrada se alguma distância for <= 0 ou NaN.
- O `adr` de cada ativo usa os 20 pregões anteriores do próprio ativo (no WIN, inclui pregões que não estão no df do WDO, sempre anteriores). Só dias do df do WDO são sinalizados; dias sem a barra 11:25 do WIN (após 04/02/2026) não operam.
- Teste próprio de causalidade: 51 barras (25 espaçadas + barras com posição aberta), recalculando com WDO e WIN cortados na barra k; 0 divergências.

Relatório: reports/20261023-231511_defasagem_dolar_bolsa_WDO_N_M5
