# reteste_abertura em WIN_N_M5

**Veredito automático: PROMISING**  
Retest of the day open after a 0.3 ADR morning excursion, stop behind the open, target at the day extreme · day trade · gerado em 2026-10-23T21:01:54

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ✅ Sharpe fora da amostra >= mínimo
- ✅ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ✅ Maioria dos anos positiva
- ✅ Maioria dos parâmetros vizinhos positiva
- ✅ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-07-20 → 2026-02-04 (636 dias) |
| P&L total / custos | R$ 2,744.36 / R$ 487.50 |
| Retorno anual acima do CDI | 1.1% |
| Sharpe / Sortino | 1.20 / 1.76 |
| Deflated Sharpe (21 tentativas no dataset) | 81.5% |
| Max drawdown | -1.0% |
| Trades / acerto / payoff | 195 / 54% / 1.14 |
| Profit factor | 1.36 |
| Exposição | 10% das barras |
| Custos / lucro bruto | 15% |
| Sharpe com custos 2x | 0.99 |

Sharpe por ano: 2023: -2.21, 2024: 2.65, 2025: 1.11, 2026: 2.87

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-07-20 → 2023-08-16 | `{'stop_mult': 0.25}` | 0.67 |
| 2023-08-17 → 2023-09-14 | `{'stop_mult': 0.25}` | -0.26 |
| 2023-09-15 → 2023-10-13 | `{'stop_mult': 0.25}` | -0.59 |
| 2023-10-16 → 2023-11-13 | `{'stop_mult': 0.25}` | -2.59 |
| 2023-11-14 → 2023-12-12 | `{'stop_mult': 0.2}` | -2.21 |
| 2023-12-13 → 2024-01-12 | `{'stop_mult': 0.25}` | -0.58 |
| 2024-01-15 → 2024-02-09 | `{'stop_mult': 0.25}` | 1.52 |
| 2024-02-14 → 2024-03-12 | `{'stop_mult': 0.25}` | 1.91 |
| 2024-03-13 → 2024-04-10 | `{'stop_mult': 0.2}` | 2.18 |
| 2024-04-11 → 2024-05-09 | `{'stop_mult': 0.3}` | 2.61 |
| 2024-05-10 → 2024-06-07 | `{'stop_mult': 0.3}` | 4.92 |
| 2024-06-10 → 2024-07-05 | `{'stop_mult': 0.3}` | 5.28 |
| 2024-07-08 → 2024-08-02 | `{'stop_mult': 0.3}` | 5.73 |
| 2024-08-05 → 2024-08-30 | `{'stop_mult': 0.2}` | 2.15 |
| 2024-09-02 → 2024-09-27 | `{'stop_mult': 0.2}` | -0.42 |
| 2024-09-30 → 2024-10-25 | `{'stop_mult': 0.25}` | -1.57 |
| 2024-10-28 → 2024-11-26 | `{'stop_mult': 0.25}` | 0.37 |
| 2024-11-27 → 2024-12-26 | `{'stop_mult': 0.25}` | 2.63 |
| 2024-12-27 → 2025-01-27 | `{'stop_mult': 0.25}` | 2.22 |
| 2025-01-28 → 2025-02-24 | `{'stop_mult': 0.2}` | 0.89 |
| 2025-02-25 → 2025-03-26 | `{'stop_mult': 0.2}` | -1.52 |
| 2025-03-27 → 2025-04-25 | `{'stop_mult': 0.2}` | 0.07 |
| 2025-04-28 → 2025-05-26 | `{'stop_mult': 0.2}` | 2.54 |
| 2025-05-27 → 2025-06-24 | `{'stop_mult': 0.2}` | 3.68 |
| 2025-06-25 → 2025-07-22 | `{'stop_mult': 0.2}` | 1.31 |
| 2025-07-23 → 2025-08-19 | `{'stop_mult': 0.2}` | 0.25 |
| 2025-08-20 → 2025-09-16 | `{'stop_mult': 0.3}` | -0.95 |
| 2025-09-17 → 2025-10-14 | `{'stop_mult': 0.3}` | 0.6 |
| 2025-10-15 → 2025-11-11 | `{'stop_mult': 0.3}` | -0.73 |
| 2025-11-12 → 2025-12-10 | `{'stop_mult': 0.3}` | 2.64 |
| 2025-12-11 → 2026-01-13 | `{'stop_mult': 0.2}` | 3.12 |
| 2026-01-14 → 2026-02-04 | `{'stop_mult': 0.2}` | 2.72 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'stop_mult': 0.2}` | 0.97 | 218 | -1.2% |
| `{'stop_mult': 0.25}` | 1.13 | 218 | -0.8% |
| `{'stop_mult': 0.3}` | 0.9 | 218 | -1.1% |

## Análise do validador
**Veredito final:** PROMISSORA (não é candidata ao holdout)

**Concorda com o veredito automático?** Sim, com ressalvas mais duras. O único gate que falha é o DSR: 81,5% com as 21 tentativas registradas e ~76% com as ~49 tentativas efetivas declaradas na hipótese (ver a hipótese 006, Origem). Os critérios prévios da própria hipótese passam: 2024 (+R$ 2.256) e 2025 (+R$ 1.085) positivos, e o resultado sem os 10 maiores trades fica positivo (+R$ 734). A análise abaixo, porém, mostra que o sinal é em grande parte "direção do dia", e não uma ideia de price action nova. Por isso a estratégia não deve ir para o holdout nessa forma.

Código: confere com a hipótese. O `adr` usa `shift(1)` sobre os pregões, `max_ant`/`min_ant` usam `shift(1)` dentro do dia, o alvo usa o extremo até a barra de sinal (incluindo ela), e os sinais com stop ≤ 0 ou alvo ≤ 0 são descartados antes da escolha da primeira entrada. Não achei look-ahead. Stop e alvo são medidos a partir do close da barra de sinal e aplicados pelo motor a partir da abertura seguinte. Então o nível real do stop fica a (open[t+1] − close[t]) do nível "abertura ∓ s·adr" da hipótese. É uma diferença pequena e simétrica. **Não achei bug no motor.**

### Pontos fortes
- **Bracket limpo.** No OOS (195 trades), as saídas se dividem em 34,9% `target`, 34,9% `stop` e 30,3% `close`, com **0% de `stop_both`**. Stop e alvo ficam a ~1.200 pontos um do outro, contra ~220 pontos de range de barra, então o resultado não depende da suposição do motor para a barra ambígua.
- **Acerto acima do equilíbrio.** O acerto real é de 54,4%, contra p* ≈ 45% da hipótese e 46,6% de equilíbrio pelo payoff realizado (ganho médio R$ 97,1, perda média R$ 84,8). A margem é de ~8 p.p., ~2 erros-padrão com n = 195. As saídas no fechamento ganham em média R$ 33,9 (59 trades, +R$ 2.003).
- **Perdas do tamanho projetado.** O stop mediano é de 512 pontos (~R$ 102), o p90 de 700 e o máximo de 930 (~R$ 186). A perda nos stops é de 1,03x a 1,04x a distância projetada, com o custo incluído. Não houve nenhum gap além do stop no OOS. A maior perda foi de R$ 167,9, e o pior dia também foi de −R$ 167,9 (2024-11-29), 0,17% do capital.
- **Risco por trade pequeno.** A maior sequência foi de 5 perdas seguidas, ou −R$ 1.039 (1,0% de R$ 100 mil). Esse valor é também o max drawdown.
- **Custos absorvíveis.** Os custos comem 15% do bruto, e o Sharpe com custos 2x fica em 0,99. A execução é realista: 1 contrato de WIN entre 10h e 12h (150 de 218 entradas), longe dos leilões.
- **Grade estável.** Os três valores de stop_mult ficam positivos no in-sample (Sharpe de 0,97 / 1,13 / 0,90), todos com o mesmo sinal e o mesmo alvo.
- **Pouco sobreposta aos baselines no P&L.** A correlação diária com o ORB é de 0,14 em todos os dias e de 0,38 nos dias em que a 006 opera. Com a 001, é de 0,06 em todos os dias e de 0,17 nos dias da 006. O ORB opera em 209 dos 218 dias da 006, do mesmo lado em 82% deles, mas **perde R$ 11.452 nesses dias**, contra +R$ 8.273 no total. Nos dias da 006, a reação na abertura vai contra a entrada do ORB. Com a 001 são 98 dias em comum (72% do mesmo lado), e a 001 perde R$ 898 neles.
- **Bate o baseline em Sharpe e risco, não em P&L.** O ORB no walk-forward, no mesmo dataset, tem Sharpe 1,07, max DD −4,0%, 577 trades e +R$ 8.803. A 006 tem Sharpe 1,20, DD −1,0% e +R$ 2.744. A diferença de Sharpe não é significativa.

### Pontos fracos e riscos
- **(1) 2023 negativo.** No OOS, 2023 tem 38 trades, −R$ 813 e Sharpe −2,21. O drawdown começa em 2023-08-01, atinge o fundo em 2023-12-05 e só se recupera em 2024-04-18: **176 pregões (~8 meses) debaixo d'água**. O DD de R$ 1.039 equivale a ~1 ano de lucro médio (~R$ 1.075/ano). Para quem opera o próprio dinheiro, isso é muito pior do que o Sharpe 1,2 sugere.
- **(2) O sinal é basicamente direção do dia.** Fiz duas comparações.
  - **Segurar o mesmo sinal até o fechamento.** No OOS, com os mesmos parâmetros do walk-forward, dá +R$ 3.191 (contra R$ 2.744 do bracket), Sharpe 0,94 e **todos os anos positivos** (2023: +R$ 358). O bracket sobe o Sharpe de 0,94 para 1,20, mas corta o P&L e é ele que torna 2023 negativo (−R$ 813). Nos dias de sinal, o pregão fecha do lado da excursão em 61,5% das vezes.
  - **Regra ingênua, sem reteste.** Entrar do lado da excursão de 0,3 `adr` (de um lado só) às 10:30 e segurar até o fechamento dá, no mesmo período OOS, **Sharpe 1,81, +R$ 11.390, 431 trades** e todos os anos positivos. Às 11:00 dá Sharpe 1,78. É um diagnóstico sem grade e sem walk-forward: conta como tentativa escondida para quem o retomar. Nos dias da 006, essa regra ingênua perde em média R$ 40 por dia, e a 006 ganha R$ 15,8 por dia. A correlação entre as duas nesses dias é de 0,55. Leitura: o reteste da abertura não cria vantagem própria. Ele seleciona os dias em que o momentum da manhã falhou e reentra com um preço melhor, recuperando um resíduo de "direção do dia". A explicação econômica da hipótese ("a abertura segurou") não é necessária para explicar o resultado.
- **(4) Concentração.** Os 5 maiores trades são 40% do P&L, e os **10 maiores, 73%**. Sem os 10 maiores sobram R$ 734. **Sem os 20 maiores, o resultado vira −R$ 841.** Os maiores trades são alvos de R$ 177 a R$ 257, então não é um outlier isolado: a vantagem média é de R$ 14 por trade, para um ganho médio de R$ 97.
- **Parâmetros instáveis no walk-forward.** O walk-forward pula entre 0,2, 0,25 e 0,3 o tempo todo (0,3 em todo o meio de 2024; 0,2 em quase todo 2025). Como os três dividem o mesmo sinal, isso mostra mais que o stop_mult é ruído do que que a estratégia é frágil. Mesmo assim, nenhum tamanho de stop é melhor de forma consistente.
- **Multiplicidade.** O DSR fica em ~76% com N ≈ 49. A própria hipótese admite que a família foi escolhida depois de ver o retorno, e foi a terceira de price action olhada nesta iteração.
- **Retorno absoluto baixo.** O retorno fica 1,1%/ano acima do CDI com R$ 100 mil e 1 contrato, com 10% de exposição.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Pré-registrar a família "direção do dia por excursão da manhã" como hipótese própria**, parente da 001. A regra: lado da excursão de 0,3 `adr` (de um lado só) num horário fixo (grade pequena: 10:30 / 11:00 / 11:30), segurar até o fechamento, sem stop. Declarar no registro, como tentativa escondida, o diagnóstico deste validador (Sharpe 1,8 no período OOS, sem walk-forward). Medir a correlação com a 001 (signal_time 12:00, k = 0,0) antes de validar, porque pode ser a mesma coisa.
2. **Se quiser manter a 006, testá-la como reentrada condicional** sobre a regra do item 1, e não como estratégia isolada. Isso é o que os números sugerem: ela ganha nos dias em que a regra ingênua perde. Com um portfólio de 1 contrato, a pergunta certa é se a 006 reduz o drawdown da regra ingênua nos dias de reteste.
3. **Não refinar stop_mult nem o alvo.** O bracket só piorou 2023 e não muda o sinal. Se testar o bracket de novo, compare sempre com a mesma entrada segurada até o fechamento.
4. **Investigar o regime de 2023** (segundo semestre: range diário, tendência, rolagens) antes de qualquer holdout, porque é ali que estão o drawdown e os 8 meses de recuperação.
