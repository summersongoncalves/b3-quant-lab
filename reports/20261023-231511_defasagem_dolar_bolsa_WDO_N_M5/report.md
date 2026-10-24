# defasagem_dolar_bolsa em WDO_N_M5

**Veredito automático: PROMISING**  
WDO: at 11:30, trade against the WIN morning move when the dollar has not followed; stop s*adr, target 1.5x stop · day trade · gerado em 2026-10-23T23:15:11

## Critérios (definidos antes do teste)

- ✅ Sem look-ahead (sinal não usa dados futuros)
- ✅ Sharpe fora da amostra >= mínimo
- ✅ Trades suficientes fora da amostra
- ❌ Deflated Sharpe (descontando nº de tentativas)
- ❌ Maioria dos anos positiva
- ✅ Maioria dos parâmetros vizinhos positiva
- ✅ Continua positiva com custos 2x

## Resultado fora da amostra (walk-forward)

| Métrica | Valor |
|---|---|
| Período | 2023-08-01 → 2026-02-05 (629 dias) |
| P&L total / custos | R$ 2,052.34 / R$ 1,500.40 |
| Retorno anual acima do CDI | 0.8% |
| Sharpe / Sortino | 0.61 / 0.76 |
| Deflated Sharpe (20 tentativas no dataset) | 8.7% |
| Max drawdown | -1.6% |
| Trades / acerto / payoff | 121 / 48% / 1.32 |
| Profit factor | 1.21 |
| Exposição | 6% das barras |
| Custos / lucro bruto | 42% |
| Sharpe com custos 2x | 0.16 |

Sharpe por ano: 2023: -2.49, 2024: -0.23, 2025: 1.76, 2026: 3.99

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-08-01 → 2023-08-28 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 0.61 |
| 2023-08-29 → 2023-09-26 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | -0.2 |
| 2023-09-27 → 2023-10-25 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 0.35 |
| 2023-10-26 → 2023-11-24 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | 0.78 |
| 2023-11-27 → 2023-12-22 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | -0.66 |
| 2023-12-26 → 2024-01-24 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | -1.82 |
| 2024-01-25 → 2024-02-23 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | -0.99 |
| 2024-02-26 → 2024-03-22 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 0.56 |
| 2024-03-25 → 2024-04-22 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.97 |
| 2024-04-23 → 2024-05-21 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.32 |
| 2024-05-22 → 2024-06-19 | `{'s': 0.25, 'k': 0.3, 'm': 0.2}` | 1.6 |
| 2024-06-20 → 2024-07-17 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 0.92 |
| 2024-07-18 → 2024-08-14 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | -0.37 |
| 2024-08-15 → 2024-09-11 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.28 |
| 2024-09-12 → 2024-10-09 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 0.33 |
| 2024-10-10 → 2024-11-06 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | -0.7 |
| 2024-11-07 → 2024-12-06 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | -3.57 |
| 2024-12-09 → 2025-01-09 | `{'s': 0.25, 'k': 0.3, 'm': 0.2}` | -2.37 |
| 2025-01-10 → 2025-02-06 | `{'s': 0.25, 'k': 0.3, 'm': 0.2}` | 0.33 |
| 2025-02-07 → 2025-03-10 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.25 |
| 2025-03-11 → 2025-04-07 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.98 |
| 2025-04-08 → 2025-05-08 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 2.15 |
| 2025-05-09 → 2025-06-05 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 2.86 |
| 2025-06-06 → 2025-07-04 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | 1.75 |
| 2025-07-07 → 2025-08-01 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | -0.55 |
| 2025-08-04 → 2025-08-29 | `{'s': 0.25, 'k': 0.3, 'm': 0.2}` | 1.0 |
| 2025-09-01 → 2025-09-26 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | 1.86 |
| 2025-09-29 → 2025-10-24 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | 2.98 |
| 2025-10-27 → 2025-11-24 | `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | 1.48 |
| 2025-11-25 → 2025-12-22 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | -1.06 |
| 2025-12-23 → 2026-01-23 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.37 |
| 2026-01-26 → 2026-02-05 | `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 1.93 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'s': 0.2, 'k': 0.3, 'm': 0.2}` | 0.32 | 136 | -1.8% |
| `{'s': 0.25, 'k': 0.3, 'm': 0.2}` | 0.29 | 136 | -1.8% |
| `{'s': 0.3, 'k': 0.3, 'm': 0.2}` | 0.64 | 136 | -1.6% |

## Análise do validador
**Veredito final:** REJEITADA
**Concorda com o veredito automático?** Não. O automático deu PROMISING, mas a estratégia falha um critério que a própria hipótese pré-registrou: "o resultado deve continuar positivo sem os 10 maiores trades". No OOS, o total cai de R$ 2.052 para **−R$ 1.221** sem os 10 maiores (R$ +254 sem os 5 maiores, −R$ 3.849 sem os 20 maiores). Também falham DSR (8,7%) e anos estáveis: 2023 dá −R$ 943 e 2024 dá −R$ 289, e só 2025 (+R$ 2.640, mais que o total) e o começo de 2026 (+R$ 645, 8 trades) são positivos. Posso ser mais rígido que os `GATES`, e aqui o critério pré-registrado manda.

**Código e causalidade.** O código implementa a regra da hipótese: barra 11:25 nos dois ativos, `adr` de 20 pregões com `shift(1)` em cada ativo, filtro de 09:05, rolagem pelo calendário, `stop = s·adr_WDO` e alvo 1,5x, ffill por dia. O WIN é cortado em `timestamp <= última barra do df`. Por isso o `lookahead_check` padrão, que chama `signals` sem `win`, também trunca o WIN e cobre esse vazamento. No walk-forward, o WIN vem inteiro do período de pesquisa, mas cada dia só usa a barra 11:25 do próprio dia e os ranges dos pregões anteriores. Não há vazamento de treino para teste. Refiz um teste independente, truncando WDO e WIN juntos em 35 pontos (25 aleatórios e 10 barras 11:25): 0 divergências. O WIN termina em 04/02/2026, então 05/02 não opera, o que está correto. Não achei bug no motor.

### Pontos fortes
- **Acerto entre resolvidos acima do pré-registro.** Com s = 0,25 na amostra inteira, foram 45,5% (50 alvos e 60 stops, 0 `stop_both`), contra p* de 43,4% e 37,6% de neutro. No OOS foram 46,4% (45/97). Passa o limite de ≥ 42%.
- **Controle 1 a favor da defasagem.** Com o mesmo lado em todos os dias com |z_win| ≥ 0,30, sem a condição `m`, são 322 trades com média de R$ 0,4 por trade. Nos 186 dias que o filtro de defasagem descarta, a média é de −R$ 4,7 e o acerto de 41,9%. Os dias de sinal dão R$ +7,4 por trade. No período OOS: sinal R$ +7,6, C1 R$ +1,4, dias descartados −R$ 3,0.
- **Controle 2 não é a 008 disfarçada.** Com o lado do próprio WDO, a média é de −R$ 38,8 por trade e o acerto de 29,4%. A correlação diária é de −0,29 com a 008 (64 dias em comum) e de 0,01 com a 015 (51 dias).
- **Risco por trade limpo.** A maior perda é de R$ 292 (0,29% de R$ 100 mil), com razão perda/(stop + C) de no máximo 1,00, sem gap além do stop e 0 `stop_both`. O pior dia foi −R$ 292 (23/04/2025). A maior sequência de perdas tem 6 trades (−R$ 891).
- Bate o baseline: `opening_range_breakout` no WDO tem Sharpe −0,35 na amostra inteira, contra 0,29 da 016 com s = 0,25.

### Pontos fracos e riscos
- **O erro-padrão engole a conclusão.** Com 110 trades resolvidos, o EP do acerto é de ~4,7 p.p. Os 45,5% ficam só 0,4 EP acima de p*. Ficam 1,7 EP acima do neutro (p ≈ 0,05 unilateral, sem descontar as ~33 tentativas no dataset). O IC de 95% vai de 36% a 55% e inclui o neutro. A diferença sinal − C1 é de ~R$ 7 por trade, com desvio de R$ 176 por trade: EP ≈ R$ 20, longe de ser significativa.
- **Concentração.** O resultado sem os 10 maiores é negativo, nos três valores de `s` (OOS −R$ 1.221; amostra inteira com s = 0,25: −R$ 1.868). O lucro são uns poucos alvos a mais por sorte de amostra, não um fluxo regular.
- **Regime.** Todo o lucro vem de 2025–26, e 2023–24 são negativos nos três `s`. A hipótese previa risco em 2024 (dólar fiscal): esse ano é exatamente negativo.
- **Lado.** No OOS, vender dólar (bolsa subindo) dá R$ 1.602 em 56 trades. Comprar dá R$ 450 em 65. Com s = 0,25 na amostra inteira, comprar dá −R$ 38: o lado "compra dólar quando a bolsa cai" não funciona sozinho.
- **De onde vem o lucro não bate com o mecanismo.** Nos 49 sinais em que o WDO já tinha andado 0 a 0,2 adr a favor, a média é de −R$ 34. Nos 87 em que o WDO tinha andado contra (dólar e bolsa no mesmo sentido), a média é de +R$ 30,7. Uma defasagem pura deveria dar lucro nos dois grupos. O lucro está nos dias de correlação "quebrada". Isso é um achado pós-hoc e não pode virar filtro sem novo pré-registro. Como controle, desfazer o movimento do WDO em todos os dias dá −R$ 16,7 por trade (618 trades), então o efeito não é reversão simples do WDO.
- **Parâmetro na borda.** O walk-forward escolhe s = 0,30 (extremo da grade) em 22 de 32 janelas. Na grade completa, s = 0,30 tem Sharpe 0,64 contra 0,29 do pré-registrado 0,25. O Sharpe OOS de 0,61 depende de ter caído no extremo.
- **Custos.** Comem 42% do bruto, e com custos 2x o Sharpe cai para 0,16. A execução seria realista (11:30, longe do leilão, 1 contrato de WDO com liquidez farta), mas a margem é fina.
- **Capital limitado.** Max DD de R$ 1.562 (1,6%), do pico em 13/08/2024 ao vale em 05/11/2024. A recuperação só veio em 09/04/2025: cerca de 8 meses no total, quase 5 depois do vale. Isso para um retorno de 0,8% a.a. acima do CDI.

### O que testar a seguir (sugestões concretas para o estrategista)
1. Não refinar a 016 no WDO M5. O dataset já tem ~33 tentativas efetivas, e um filtro sobre "WDO contra vs. a favor" seria ajuste pós-hoc sobre 136 trades.
2. Se a ideia de lead-lag WIN→WDO for retomada, pré-registrar como nova hipótese a versão "correlação quebrada" (WDO andou no mesmo sentido do WIN até 11:30, apostar na volta do WDO). Ela precisa de critério de existência próprio e de uma amostra que não contamine: outro horário de sinal já descartado (10:55) não serve, porque também foi olhado. O ideal é esperar mais dados de pesquisa ou usar outro par (WIN × DI ou WDO × DOL).
3. Qualquer versão nova deve declarar de antemão o desempenho por lado e por ano. Também deve exigir que o resultado sem os 10 maiores seja positivo nos dois lados separadamente.
