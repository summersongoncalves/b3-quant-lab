# recuo_vwap_tendencia_semanal em WDO_N_M5

**Veredito automático: REJECTED**  
WDO: first pullback to the daily VWAP (10:00-12:55) in the direction of the 5-session trend; stop s*adr, target 1.5x stop · day trade · gerado em 2026-10-23T23:06:46

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ❌ Sharpe fora da amostra >= mínimo
- ✅ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ❌ Maioria dos anos positiva
- ❌ Maioria dos parâmetros vizinhos positiva
- ❌ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-08-01 → 2026-02-05 (629 dias) |
| P&L total / custos | R$ -5,120.59 / R$ 1,897.20 |
| Retorno anual acima do CDI | -2.1% |
| Sharpe / Sortino | -1.47 / -2.43 |
| Deflated Sharpe (17 tentativas no dataset) | 0.0% |
| Max drawdown | -6.1% |
| Trades / acerto / payoff | 153 / 36% / 1.19 |
| Profit factor | 0.67 |
| Exposição | 6% das barras |
| Custos / lucro bruto | 59% |
| Sharpe com custos 2x | -1.99 |

Sharpe por ano: 2023: -2.77, 2024: -2.44, 2025: -0.41, 2026: 3.35

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -1.0 |
| 2023-08-29 → 2023-09-26 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -0.54 |
| 2023-09-27 → 2023-10-25 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | 0.46 |
| 2023-10-26 → 2023-11-24 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -0.65 |
| 2023-11-27 → 2023-12-22 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -1.6 |
| 2023-12-26 → 2024-01-24 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -2.13 |
| 2024-01-25 → 2024-02-23 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -1.89 |
| 2024-02-26 → 2024-03-22 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -0.27 |
| 2024-03-25 → 2024-04-22 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -0.75 |
| 2024-04-23 → 2024-05-21 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | 0.49 |
| 2024-05-22 → 2024-06-19 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -0.11 |
| 2024-06-20 → 2024-07-17 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -0.69 |
| 2024-07-18 → 2024-08-14 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -1.83 |
| 2024-08-15 → 2024-09-11 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -0.7 |
| 2024-09-12 → 2024-10-09 | `{'s': 0.2, 'k': 1.5, 'z0': 0.5}` | -0.79 |
| 2024-10-10 → 2024-11-06 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -1.06 |
| 2024-11-07 → 2024-12-06 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -3.35 |
| 2024-12-09 → 2025-01-09 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -1.25 |
| 2025-01-10 → 2025-02-06 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -2.3 |
| 2025-02-07 → 2025-03-10 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -0.79 |
| 2025-03-11 → 2025-04-07 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -0.13 |
| 2025-04-08 → 2025-05-08 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | 1.66 |
| 2025-05-09 → 2025-06-05 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | 1.38 |
| 2025-06-06 → 2025-07-04 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -0.25 |
| 2025-07-07 → 2025-08-01 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -1.6 |
| 2025-08-04 → 2025-08-29 | `{'s': 0.2, 'k': 1.5, 'z0': 0.5}` | 0.24 |
| 2025-09-01 → 2025-09-26 | `{'s': 0.2, 'k': 1.5, 'z0': 0.5}` | 0.76 |
| 2025-09-29 → 2025-10-24 | `{'s': 0.2, 'k': 1.5, 'z0': 0.5}` | 0.65 |
| 2025-10-27 → 2025-11-24 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -2.05 |
| 2025-11-25 → 2025-12-22 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -1.94 |
| 2025-12-23 → 2026-01-23 | `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -1.2 |
| 2026-01-26 → 2026-02-05 | `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | 2.68 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'s': 0.2, 'k': 1.5, 'z0': 0.5}` | -1.69 | 170 | -5.4% |
| `{'s': 0.25, 'k': 1.5, 'z0': 0.5}` | -1.09 | 170 | -5.1% |
| `{'s': 0.3, 'k': 1.5, 'z0': 0.5}` | -1.32 | 170 | -6.5% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Falha em 5 dos 7 `GATES` (Sharpe OOS -1,47; DSR 0,0%; anos; grade; custos 2x) e em todos os critérios prévios da hipótese que dependem de resultado. O ponto central, o viés da semana, não só não acrescentou os ~5 p.p. esperados como ficou **abaixo** da geometria neutra.

Código confere com a hipótese: `adr` e `T5` com `shift(1)`, ajuste e exclusão da rolagem só pelo calendário, VWAP diária causal, `t−1` do mesmo pregão, 1 entrada por dia com ffill até o fim do pregão, `stop = s × adr` e `alvo = 1,5 × stop` em pontos. Não achei look-ahead além do que o teste automático cobre, nem bug no motor: a perda em stop excede o stop projetado em exatamente R$ 12,40 (o custo) em todos os 96 stops, ou seja, nenhum gap além do stop e o motor aplicou o bracket como esperado.

Números (backtest direto, amostra de pesquisa inteira, `s` = 0,25, 1 contrato):

| Teste | Trades | Líquido R$ | Médio R$ | Sharpe | Acerto resolvidos |
|---|---|---|---|---|---|
| Estratégia (viés semanal) | 170 | -4.077 | -24,0 | -1,09 | **36,0%** |
| `s` = 0,20 / 0,30 | 170 / 170 | -5.181 / -5.590 | -30,5 / -32,9 | -1,69 / -1,32 | 33,1% / 33,1% |
| Controle sem filtro (todos os toques, lado de onde veio) | 501 | -8.464 | -16,9 | -1,30 | 38,7% |
| Controle, só nos dias SEM viés forte | 331 | -2.695 | -8,1 | | 41,7% |
| Lado oposto ao viés (contra a semana) | 170 | -265 | -1,6 | -0,07 | 41,2% |
| Mesma entrada sem bracket (até o fechamento) | 170 | -4.168 | -24,5 | -0,55 | n/a |
| Baseline `opening_range_breakout` | 671 | -5.215 | -7,8 | -0,35 | |

- **Critério 4 (acerto)**: 36,0% entre resolvidos contra p* = 43,6% e geometria neutra ~39%. Ficou 3 p.p. **abaixo** do neutro, não 5 acima. A favor da semana o toque na VWAP rende menos que contra ela (41,2%).
- **Critério 5 (controle)**: o controle sem filtro também perde, mas a estratégia é pior por trade (-24,0 contra -16,9). Nos dias com viés forte, o mesmo toque com o lado do controle perde -33,9 por trade; nos demais dias, -8,1. O filtro de tendência seleciona dias **piores** para esse setup. A hipótese cai pelo próprio critério.
- **Critério 1 (anos)**: 2023 -27,2 por trade (48), 2024 -46,4 (55), 2025 -14,2 (61), 2026 +107 (só 6 trades). Negativo em 2024 e 2025.
- **Critério 2 (concentração)**: -6.741 sem os 10 maiores, -9.086 sem os 20. Já é negativo com eles.
- **Critério 3 (grade)**: as 3 combinações negativas (-1,69, -1,09, -1,32). Walk-forward alterna entre 0,20, 0,25 e 0,30 sem padrão, com Sharpe de treino quase sempre negativo; 0,30 é o mais escolhido.
- **Critério 6 (lados)**: comprados 79 trades, -2.876 (-36,4/trade, acerto 35,1%); vendidos 91, -1.201 (-13,2/trade, 37,0%). A pior fase é a de compras em 2024 (42 trades, -2.355), justamente a alta do dólar no fim de 2024: as perdas de 04/12, 19/12 e 20/12/2024 (-220, -265, -283) estão entre as 4 maiores. Comprar o recuo na tendência de alta perdeu no regime em que deveria ganhar. Vendidos de 2025 (queda do dólar) ficaram no zero (-1,2/trade).
- **Critério 7 (correlação diária, dias em comum)**: 008 `direcao_do_dia` 0,06 (84 dias); 012 `falha_balanco_inicial` -0,16 (99); 013 `fechamento_gap` 0,12 (69); 014 `rompimento_extremo_anterior` 0,31 (39). Baixa, mas irrelevante: são todas negativas, e diversificar estratégias sem vantagem não cria vantagem.
- **Sem bracket**: -24,5 por trade, igual ao com bracket. A falta de vantagem está no lado/entrada, não na geometria de saída.

### Pontos fortes
- Implementação limpa e fiel à hipótese; risco por trade realmente controlado: stop mediano R$ 141,5, perda máxima R$ 283 (0,28% de R$ 100 mil), pior dia -R$ 283, nenhum gap além do stop, 0 `stop_both` (stop bem fora do ruído de uma barra).
- O alvo se resolve dentro do pregão: só 20 de 170 saídas (12%) no fechamento.
- A hipótese trazia o controle certo e um critério de queda explícito, que permitiu derrubá-la sem ambiguidade.

### Pontos fracos e riscos
- Bruto já negativo (-R$ 1.969) antes de custos (R$ 2.108). Custos comem 59% do bruto absoluto no OOS, mas o problema é anterior a eles.
- Max drawdown de R$ 5.105 (5,1%) com pico no primeiro dia (05/04/2023) e vale em 24/11/2025: a curva **nunca** saiu do drawdown em ~2,6 anos. Maior sequência: 7 perdas seguidas, pior sequência -R$ 1.012.
- Lucro de 2026 (+R$ 644) vem de 6 trades vendidos: ruído.
- `trials_on_dataset` no relatório é 17, abaixo das ~29 tentativas (efetivas + escondidas) que a hipótese declara. Com 29 o DSR seria ainda menor; não muda o veredito, mas o contador do registro não captura as tentativas escondidas.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Não refinar esta regra** (z0, N, janela, s ou k): grade, lados, anos, controle e versão sem bracket concordam que não há vantagem. Ajustar z0/N agora seria mineração.
- O único sinal fora do sorteio nesta rodada é o inverso: toque na VWAP **contra** a tendência de 5 pregões teve 41,2% de acerto, e o controle em dias sem tendência 41,7%, ambos ainda abaixo de p* (43,6%). Isso sugere, no máximo, reversão de curto prazo no dólar intradiário depois de semanas fortes. Se for testado, deve ser hipótese nova, com seu próprio custo de tentativa e sem reaproveitar estes números como evidência (o lado oposto deu -1,6/trade, ou seja, nada).
- Após 5 hipóteses reprovadas no WDO M5 (008, 012, 013, 014, 015), todas com acerto no nível do sorteio ou abaixo, considerar mudar de dataset/timeframe (WDO H1/D1 para swing de vários dias, onde o momentum de câmbio citado de fato é documentado) em vez de mais um gatilho intradiário em M5.
