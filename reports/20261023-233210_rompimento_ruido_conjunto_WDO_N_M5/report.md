# rompimento_ruido_conjunto em WDO_N_M5

**Veredito automático: REJECTED**  
WDO: follow the noise-band breakout when WIN breaks out on the opposite side; stop s*adr, target 1.5x stop, 24-bar time exit · day trade · gerado em 2026-10-23T23:32:10

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ❌ Sharpe fora da amostra >= mínimo
- ✅ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ❌ Maioria dos anos positiva
- ✅ Maioria dos parâmetros vizinhos positiva
- ❌ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-08-01 → 2026-02-05 (629 dias) |
| P&L total / custos | R$ -413.26 / R$ 3,509.20 |
| Retorno anual acima do CDI | -0.2% |
| Sharpe / Sortino | -0.11 / -0.20 |
| Deflated Sharpe (25 tentativas no dataset) | 0.6% |
| Max drawdown | -2.1% |
| Trades / acerto / payoff | 283 / 48% / 1.06 |
| Profit factor | 0.98 |
| Exposição | 6% das barras |
| Custos / lucro bruto | 113% |
| Sharpe com custos 2x | -1.05 |

Sharpe por ano: 2023: -0.18, 2024: 0.7, 2025: -0.87, 2026: -1.41

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 1.51 |
| 2023-08-29 → 2023-09-26 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 2.49 |
| 2023-09-27 → 2023-10-25 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 1.67 |
| 2023-10-26 → 2023-11-24 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 0.3 |
| 2023-11-27 → 2023-12-22 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -1.6 |
| 2023-12-26 → 2024-01-24 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -0.82 |
| 2024-01-25 → 2024-02-23 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -2.6 |
| 2024-02-26 → 2024-03-22 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -1.94 |
| 2024-03-25 → 2024-04-22 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -1.77 |
| 2024-04-23 → 2024-05-21 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 2.34 |
| 2024-05-22 → 2024-06-19 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -0.2 |
| 2024-06-20 → 2024-07-17 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -0.56 |
| 2024-07-18 → 2024-08-14 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -1.07 |
| 2024-08-15 → 2024-09-11 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 1.06 |
| 2024-09-12 → 2024-10-09 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 1.09 |
| 2024-10-10 → 2024-11-06 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 0.96 |
| 2024-11-07 → 2024-12-06 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 2.05 |
| 2024-12-09 → 2025-01-09 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 3.31 |
| 2025-01-10 → 2025-02-06 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 2.43 |
| 2025-02-07 → 2025-03-10 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 0.71 |
| 2025-03-11 → 2025-04-07 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | -0.45 |
| 2025-04-08 → 2025-05-08 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | -2.34 |
| 2025-05-09 → 2025-06-05 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | -0.36 |
| 2025-06-06 → 2025-07-04 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | -1.1 |
| 2025-07-07 → 2025-08-01 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | -0.52 |
| 2025-08-04 → 2025-08-29 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 0.38 |
| 2025-09-01 → 2025-09-26 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 0.57 |
| 2025-09-29 → 2025-10-24 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 1.16 |
| 2025-10-27 → 2025-11-24 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 0.79 |
| 2025-11-25 → 2025-12-22 | `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | 0.63 |
| 2025-12-23 → 2026-01-23 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 1.58 |
| 2026-01-26 → 2026-02-05 | `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 2.6 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'s': 0.2, 'faixa': 14, 'horizonte': 24}` | -0.13 | 306 | -2.4% |
| `{'s': 0.25, 'faixa': 14, 'horizonte': 24}` | 0.16 | 306 | -2.1% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Sim. Além dos 4 critérios automáticos que falharam (Sharpe OOS -0,11, DSR 0,6%, anos instáveis, custos 2x com Sharpe -1,05), a hipótese cai pelos próprios critérios pré-registrados: o acerto entre os resolvidos (41,2%) fica abaixo do mínimo de 42% e do p* de 44,5%, e o Controle 1 (só o WDO rompe, WIN dentro da faixa) acerta **mais** (43,0%). A confirmação do WIN não acrescenta lado, que era o modo de falha nº 1 previsto na própria hipótese.

### Revisão do código
- Implementa o que a hipótese diz: faixa por tabela dia × horário com `rolling(14).shift(1)`, gatilho por transição no mesmo pregão, janela 10:00 a 15:30, 1 entrada por dia, rolagem por calendário, `adr` com `shift(1)`, posição nas barras t..t+23 e stop/alvo NaN depois. Uma reimplementação independente (controles) reproduz a posição barra a barra.
- WIN: carregado sem `include_holdout`, cortado em `<=` última barra do WDO e alinhado por timestamp exato (98,9% das barras do WDO têm par; as duas séries abrem às 09:00 e são rotuladas pela abertura). A faixa do WIN só usa pregões anteriores, e `mv_WIN(t)` usa só `close_WIN(t)`. Não achei vazamento.
- Observação (não é bug do motor): o WIN de pesquisa termina em 04/02/2026. No holdout do WDO, `store.load("WIN$N")` sem `include_holdout` não traz WIN, e a estratégia **não geraria nenhum sinal**. Qualquer estratégia futura com WIN auxiliar precisa resolver isso antes de pensar em holdout.

### Números (backtest na amostra de pesquisa inteira, 1 contrato)
| Variante | Trades | P&L R$ | R$/trade | Sharpe | Acerto resolvidos | Sem top 10 |
|---|---|---|---|---|---|---|
| Regra s=0,20 | 306 | -494 | -1,6 | -0,13 | 41,2% | -2.891 |
| Regra s=0,25 | 306 | +695 | +2,3 | 0,16 | 40,8% | -2.271 |
| Sem bracket (só tempo, 24 barras) | 306 | +1.321 | +4,3 | 0,22 | n/a | -3.985 |
| Controle 1: só WDO (WIN = 0) | 356 | -689 | -1,9 | -0,17 | 43,0% | -3.025 |
| Controle 1b: WDO com qualquer WIN | 409 | -20 | 0,0 | 0,00 | 43,6% | -2.390 |
| Controle 2: mesma direção | 77 | -241 | -3,1 | -0,14 | 40,4% | -1.986 |
| Baseline ORB (padrão) | 671 | -5.215 | -7,8 | -0,35 | | |

- **Saídas (s=0,20)**: stop 132 (43%), alvo 93 (30%), tempo 80 (26%), `stop_both` 1 (0,3%). O stop não está no ruído de barra, e a suposição do motor não pesa. A geometria bate quase exatamente com a neutra (26% alvo, 48% stop, 26% tempo), com um leve desvio para o alvo que não compensa os custos.
- **Gaps**: nenhum stop saiu mais de R$ 20 além da distância projetada. A pior perda (-R$ 226, em 02/01/2025) é o stop num dia de `adr` alto. O risco de cauda está controlado.
- **Custos**: R$ 3.794 contra R$ 3.300 de bruto (115%). O bruto é positivo, mas fica no nível de 1 tick por trade.
- **Regime e lado**: 2024 +938, 2025 -1.609 (s=0,20). Com s=0,25, as compras somam +1.604 e as vendas -909, o que confirma o modo de falha nº 3 (fiscal de 2024). Sem bracket o sinal se **inverte**: as vendas ganham +1.419 e as compras perdem -98. O lado vencedor troca conforme a regra de saída, e isso é ruído, não efeito.
- **Concentração**: todas as variantes ficam negativas sem os 10 maiores trades (-2.300 a -4.000). O top 5 está todo entre dez/2024 e abr/2025.
- **Comparação com o Controle 2**: na mesma direção o resultado é um pouco pior por trade (-3,1 contra -1,6), como previsto, mas a diferença está dentro do ruído com 77 trades.
- **Risco**: max DD de R$ 2.424 (2,4% de R$ 100 mil), do pico em 23/12/2024 ao fundo em 05/08/2025, **sem recuperação** até o fim da amostra (mais de 13 meses abaixo do pico). Pior dia -R$ 226, maior sequência de 9 perdas (-R$ 993).
- **Estabilidade**: o walk-forward alterna entre 0,20 e 0,25 em blocos, seguindo o regime, com Sharpe de treino oscilando entre -2,6 e +3,3. Nenhum parâmetro é estável.
- **Correlação com a 016**: 0,003 na série diária completa. As duas operam juntas em só 31 dias (0,38 nesses dias). Não há diversificação a aproveitar, porque nenhuma das duas tem edge.

### Pontos fortes
- Implementação limpa e causal, risco por trade pequeno e conhecido (stop ≈ projetado, sem gaps, `stop_both` desprezível).
- O pré-registro com controles funcionou: derrubou a hipótese de forma inequívoca.

### Pontos fracos e riscos
- A confirmação do WIN não dá lado: o Controle 1 é igual ou melhor, e o acerto fica 3 p.p. abaixo do p*.
- O resultado depende do regime (fiscal 2024) e o lado vencedor muda com a regra de saída.
- Os custos consomem mais que o bruto.
- Drawdown sem recuperação há mais de 13 meses.

### O que testar a seguir (sugestões concretas para o estrategista)
- **Não refinar** (nem s, nem horizonte, nem janela). A grade foi de 2 pontos, e mexer no horizonte para aproveitar o +4,3/trade sem bracket seria ajuste ao ruído (sem os 10 maiores dá -3.985).
- O WDO M5 já tem ~40 tentativas efetivas: 008, 010, 012 a 015 e 018 caíram no neutro com o mesmo padrão de geometria. A recomendação é **mudar de dataset ou de horizonte** (por exemplo, swing diário do WDO ou outro ativo), em vez de propor mais uma variação intradiária de rompimento/reversão no WDO M5.
- Se o WIN voltar como dado auxiliar, primeiro resolva o carregamento no holdout (o WIN de pesquisa termina antes do holdout do WDO).
