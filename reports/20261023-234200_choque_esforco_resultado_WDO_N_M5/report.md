# choque_esforco_resultado em WDO_N_M5

**Veredito automático: REJECTED**  
WDO: follow a wide, high-volume bar closing at its extreme; stop s*adr, target 1.5x stop, 12-bar time exit · day trade · gerado em 2026-10-23T23:42:00

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
| P&L total / custos | R$ -2,814.26 / R$ 2,728.00 |
| Retorno anual acima do CDI | -1.1% |
| Sharpe / Sortino | -1.13 / -1.69 |
| Deflated Sharpe (27 tentativas no dataset) | 0.0% |
| Max drawdown | -3.2% |
| Trades / acerto / payoff | 220 / 37% / 1.30 |
| Profit factor | 0.76 |
| Exposição | 2% das barras |
| Custos / lucro bruto | 3163% |
| Sharpe com custos 2x | -2.19 |

Sharpe por ano: 2023: -3.78, 2024: -1.74, 2025: 0.23, 2026: -0.28

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -2.98 |
| 2023-08-29 → 2023-09-26 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -3.12 |
| 2023-09-27 → 2023-10-25 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -3.62 |
| 2023-10-26 → 2023-11-24 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -3.24 |
| 2023-11-27 → 2023-12-22 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -1.88 |
| 2023-12-26 → 2024-01-24 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -1.47 |
| 2024-01-25 → 2024-02-23 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -3.31 |
| 2024-02-26 → 2024-03-22 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -4.38 |
| 2024-03-25 → 2024-04-22 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -4.6 |
| 2024-04-23 → 2024-05-21 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -2.07 |
| 2024-05-22 → 2024-06-19 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -0.49 |
| 2024-06-20 → 2024-07-17 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -0.88 |
| 2024-07-18 → 2024-08-14 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -0.72 |
| 2024-08-15 → 2024-09-11 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -1.08 |
| 2024-09-12 → 2024-10-09 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 0.02 |
| 2024-10-10 → 2024-11-06 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 0.25 |
| 2024-11-07 → 2024-12-06 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | 1.56 |
| 2024-12-09 → 2025-01-09 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | 0.27 |
| 2025-01-10 → 2025-02-06 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -1.66 |
| 2025-02-07 → 2025-03-10 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -0.82 |
| 2025-03-11 → 2025-04-07 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 0.16 |
| 2025-04-08 → 2025-05-08 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 1.03 |
| 2025-05-09 → 2025-06-05 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -0.88 |
| 2025-06-06 → 2025-07-04 | `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | 1.1 |
| 2025-07-07 → 2025-08-01 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 2.26 |
| 2025-08-04 → 2025-08-29 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 1.55 |
| 2025-09-01 → 2025-09-26 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -0.35 |
| 2025-09-29 → 2025-10-24 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | 0.2 |
| 2025-10-27 → 2025-11-24 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -1.1 |
| 2025-11-25 → 2025-12-22 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -0.76 |
| 2025-12-23 → 2026-01-23 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -1.88 |
| 2026-01-26 → 2026-02-05 | `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -0.61 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'s': 0.15, 'k': 2.5, 'horizonte': 12}` | -1.56 | 243 | -4.0% |
| `{'s': 0.2, 'k': 2.5, 'horizonte': 12}` | -1.37 | 243 | -4.7% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Falham 5 de 7 critérios (Sharpe OOS -1,13, DSR 0,0%, anos, grade, custos 2x) e, mais importante, caem os critérios pré-registrados da própria hipótese: o acerto entre os resolvidos (s = 0,20) foi **35,5%** (49 alvos / 138 resolvidos), abaixo do corte de 41%, abaixo do p* de 44,5% e igual à geometria neutra (~36%). O efeito não existe.

Código: implementa a hipótese (rng/vol de referência por horário com `shift(1)`, clv, janela 09:30–16:00, 1ª barra do dia, rolagem por calendário, saída no fechamento da 12ª barra após a entrada). Sem look-ahead escondido; uma reimplementação independente reproduziu os 243 trades e o P&L ao centavo. Nenhum bug no motor encontrado.

Backtest na amostra de pesquisa inteira (s = 0,20, 1 contrato, R$ 100 mil):

| Versão | Trades | P&L | Bruto | Acerto resolvidos | Sem 10 maiores | 2024 / 2025 |
|---|---|---|---|---|---|---|
| 019 (s = 0,20) | 243 | R$ -3.996 | R$ -983 | 35,5% | R$ -6.106 | -1.778 / +348 |
| 019 (s = 0,15) | 243 | R$ -3.838 | R$ -825 | 37,3% | R$ -5.417 | -1.614 / -324 |
| Controle 1 (clv no meio, lado close−open) | 204 | R$ -1.469 | R$ +1.060 | 39,6% | R$ -3.737 | -882 / +45 |
| Controle 2 (rv < 1,5, só leitura) | 23 | R$ +1.127 | R$ +1.413 | 66,7% (n = 12) | R$ -667 | +401 / +821 |
| Sem filtro de volume | 312 | R$ -4.310 | R$ -442 | 34,9% | R$ -6.618 | -2.346 / +876 |
| Mesma entrada sem bracket (só tempo) | 243 | R$ -5.718 | R$ -2.705 | n/a (36,2% geral) | R$ -9.654 | -3.190 / -1.247 |

### Pontos fortes
- Risco bem controlado e como projetado: 0 `stop_both`; 89 stops com perda mediana de R$ 117 e pior de R$ 216, nenhum stop além da distância projetada mais custos (0 de 89). Pior dia R$ -216 (0,22%).
- Correlação diária praticamente nula com a 014 (0,02; 0,09 nos 74 dias em comum) e com a 018 (-0,02).
- Implementação limpa e fiel à hipótese; o pré-registro foi claro e permitiu matar a ideia sem ambiguidade.

### Pontos fracos e riscos
- **Sem lado**: o bruto já é negativo (R$ -983 com bracket; R$ -2.705 sem bracket, -1,1 ponto por trade em 1 hora). O bracket só reduz o prejuízo; não há borda a proteger. Custos (R$ 3.013) são 3x o resultado bruto em módulo.
- **Controle 1 é melhor que a estratégia** (bruto R$ +1.060 contra -983; acerto resolvido 39,6% contra 35,5%): o fechamento no extremo não acrescenta nada, até piora. A leitura de Wyckoff "esforço com resultado continua" falha.
- **Controle 2 (sem volume) é melhor que com volume** em 23 trades: o volume alto, peça central da hipótese, não ajuda; se algo, um choque com volume alto tende a reverter levemente (absorção/exaustão), o contrário do previsto. Com 23 trades, é ruído e não deve virar hipótese sem pré-registro.
- **Concentração e regime**: negativa sem os 10 maiores (R$ -6.106); 2023 e 2024 negativos, 2025 levemente positivo (+R$ 348) — o critério "2024 e 2025 positivos" falha.
- **Capital limitado**: max DD de R$ 4.707 (4,7%) desde 2023-05-08, sem recuperação até o fim da amostra; maior sequência de 10 perdas seguidas (R$ -825).
- Walk-forward alterna entre s = 0,15 e 0,20 com Sharpe de treino negativo em quase todas as janelas: escolhe o "menos ruim".
- Baseline `opening_range_breakout` no WDO também é negativo (Sharpe -0,35, DD -10%); a 019 tem DD menor só porque opera 2% das barras, não por ter borda.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Parar a família "evento dá o lado" no WDO intradiário.** É a sétima tentativa (008, 012, 013, 014, 018, 019) com acerto no neutro; o dataset WDO_N_M5 já está perto de ~45 tentativas efetivas, o que torna o DSR inatingível para qualquer variante.
- Não transformar os controles em estratégia (reversão após choque com volume, ou choque sem volume): seriam escolhidos depois de ver o resultado. Se o estrategista quiser testar "reversão de exaustão após choque de volume", precisa de nova hipótese pré-registrada, idealmente em outro ativo (WIN ou DOL cheio) para não gastar mais tentativas no WDO_N_M5.
- O único achado aproveitável é descritivo: a barra de choque prevê **volatilidade** (+40% de excursão), não direção. Isso serve como filtro de regime/tamanho de stop para outras estratégias, ou para estruturas sem lado, e não como gatilho direcional.
