# momentum_intradiario em WIN_N_M5

**Veredito automático: PROMISING**  
Intraday momentum: open-to-signal_time move continues to the close · day trade · gerado em 2026-10-23T18:56:03

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
| P&L total / custos | R$ 5,958.50 / R$ 1,027.50 |
| Retorno anual acima do CDI | 2.4% |
| Sharpe / Sortino | 1.61 / 2.28 |
| Deflated Sharpe (18 tentativas no dataset) | 94.3% |
| Max drawdown | -1.4% |
| Trades / acerto / payoff | 411 / 54% / 1.22 |
| Profit factor | 1.42 |
| Exposição | 29% das barras |
| Custos / lucro bruto | 15% |
| Sharpe com custos 2x | 1.33 |

Sharpe por ano: 2023: 2.11, 2024: 2.04, 2025: 1.2, 2026: 1.88

![equity](equity.png)

## Parâmetros escolhidos em cada janela

| Teste | Parâmetros | Sharpe no treino |
|---|---|---|
| 2023-07-20 → 2023-08-16 | `{'signal_time': '16:00', 'k': 0.5}` | 1.04 |
| 2023-08-17 → 2023-09-14 | `{'signal_time': '16:00', 'k': 0.0}` | 2.43 |
| 2023-09-15 → 2023-10-13 | `{'signal_time': '16:00', 'k': 0.0}` | 2.61 |
| 2023-10-16 → 2023-11-13 | `{'signal_time': '16:00', 'k': 1.0}` | 3.7 |
| 2023-11-14 → 2023-12-12 | `{'signal_time': '16:00', 'k': 1.0}` | 2.56 |
| 2023-12-13 → 2024-01-12 | `{'signal_time': '16:00', 'k': 1.0}` | 1.94 |
| 2024-01-15 → 2024-02-09 | `{'signal_time': '12:00', 'k': 0.5}` | 3.71 |
| 2024-02-14 → 2024-03-12 | `{'signal_time': '12:00', 'k': 0.5}` | 3.64 |
| 2024-03-13 → 2024-04-10 | `{'signal_time': '12:00', 'k': 0.5}` | 3.62 |
| 2024-04-11 → 2024-05-09 | `{'signal_time': '12:00', 'k': 1.0}` | 1.91 |
| 2024-05-10 → 2024-06-07 | `{'signal_time': '14:00', 'k': 0.5}` | 1.15 |
| 2024-06-10 → 2024-07-05 | `{'signal_time': '14:00', 'k': 0.5}` | 2.32 |
| 2024-07-08 → 2024-08-02 | `{'signal_time': '14:00', 'k': 0.5}` | 3.63 |
| 2024-08-05 → 2024-08-30 | `{'signal_time': '14:00', 'k': 0.5}` | 3.77 |
| 2024-09-02 → 2024-09-27 | `{'signal_time': '14:00', 'k': 1.0}` | 1.6 |
| 2024-09-30 → 2024-10-25 | `{'signal_time': '14:00', 'k': 1.0}` | 1.5 |
| 2024-10-28 → 2024-11-26 | `{'signal_time': '16:00', 'k': 1.0}` | 2.21 |
| 2024-11-27 → 2024-12-26 | `{'signal_time': '16:00', 'k': 0.0}` | 1.93 |
| 2024-12-27 → 2025-01-27 | `{'signal_time': '16:00', 'k': 1.0}` | 3.12 |
| 2025-01-28 → 2025-02-24 | `{'signal_time': '12:00', 'k': 0.0}` | 3.98 |
| 2025-02-25 → 2025-03-26 | `{'signal_time': '12:00', 'k': 1.0}` | 5.08 |
| 2025-03-27 → 2025-04-25 | `{'signal_time': '12:00', 'k': 0.5}` | 4.25 |
| 2025-04-28 → 2025-05-26 | `{'signal_time': '12:00', 'k': 0.5}` | 4.2 |
| 2025-05-27 → 2025-06-24 | `{'signal_time': '14:00', 'k': 1.0}` | 2.19 |
| 2025-06-25 → 2025-07-22 | `{'signal_time': '14:00', 'k': 1.0}` | 0.77 |
| 2025-07-23 → 2025-08-19 | `{'signal_time': '16:00', 'k': 1.0}` | 1.43 |
| 2025-08-20 → 2025-09-16 | `{'signal_time': '12:00', 'k': 1.0}` | 0.09 |
| 2025-09-17 → 2025-10-14 | `{'signal_time': '12:00', 'k': 1.0}` | 0.19 |
| 2025-10-15 → 2025-11-11 | `{'signal_time': '12:00', 'k': 1.0}` | -0.63 |
| 2025-11-12 → 2025-12-10 | `{'signal_time': '16:00', 'k': 1.0}` | 1.08 |
| 2025-12-11 → 2026-01-13 | `{'signal_time': '16:00', 'k': 0.0}` | 2.04 |
| 2026-01-14 → 2026-02-04 | `{'signal_time': '16:00', 'k': 1.0}` | 2.13 |

## Grade completa (amostra de pesquisa inteira, só para ver robustez)

| Parâmetros | Sharpe | Trades | Max DD |
|---|---|---|---|
| `{'signal_time': '12:00', 'k': 0.0}` | 0.69 | 693 | -3.0% |
| `{'signal_time': '12:00', 'k': 0.5}` | 1.32 | 516 | -1.5% |
| `{'signal_time': '12:00', 'k': 1.0}` | 1.17 | 353 | -1.3% |
| `{'signal_time': '14:00', 'k': 0.0}` | 0.04 | 691 | -3.6% |
| `{'signal_time': '14:00', 'k': 0.5}` | 0.72 | 499 | -2.5% |
| `{'signal_time': '14:00', 'k': 1.0}` | 1.01 | 351 | -1.5% |
| `{'signal_time': '16:00', 'k': 0.0}` | 0.65 | 691 | -2.5% |
| `{'signal_time': '16:00', 'k': 0.5}` | 0.77 | 507 | -2.0% |
| `{'signal_time': '16:00', 'k': 1.0}` | 1.4 | 358 | -0.8% |

## Análise do validador
**Veredito final:** PROMISSORA
**Concorda com o veredito automático?** Sim, e com ressalvas mais duras do que o automático registra. O DSR já reprova com as 18 tentativas registradas (94,3% < 95%). Somando as ~15 variações exploratórias escondidas da seção "Origem" (33 tentativas), o DSR cai para 92,3%; com 50 tentativas fica em 90,9%. Além disso, o lucro OOS depende muito da cauda: tirando os 20 melhores trades (5% de 411), o P&L fica em -R$ 10. Não é candidata ao holdout. Não rejeito porque a estratégia passa em tudo o mais com folga razoável, bate o baseline e sobrevive ao corte dos 5 melhores trades, que a própria hipótese definiu como teste decisivo.

Conferência do código: implementa a hipótese. A barra de sinal é a rotulada `signal_time - 5min`. A `escala` usa a mediana móvel de 20 dias com `shift(1)`, então exclui o dia atual. Com `k=0`, os 20 primeiros dias têm escala NaN e não operam. A posição é decidida no fechamento da barra de sinal e executada na abertura seguinte, e o day trade zera no fechamento. Não achei look-ahead escondido: não usa `high`/`low` nem estatística da série inteira. Dados: 714 de 716 dias têm a barra 11:55 e 2 dias abrem às 13:00 (filtrados). O fechamento varia entre 18:20 (556 dias) e 17:50 (153 dias), então a janela de 16h é 30 min mais curta em parte da amostra. Os 5 maiores dias não mostram salto de rolagem dentro do dia (gap máximo intra-dia de 195 pts em 09/04/2025, coerente com o dia do tarifaço).

### Pontos fortes
- Sharpe OOS de 1,61 (Sortino 2,28), contra 1,07 do baseline `opening_range_breakout` no mesmo dataset e período. O DSR também é maior (94,3% contra 83,5%) e o max DD é menor (-1,4% contra -4,0% sobre R$ 100 mil, ou R$ 1.500 contra cerca de R$ 4.000).
- Todos os anos OOS são positivos (2023: 2,11; 2024: 2,04; 2025: 1,20; 2026: 1,88), assim como 78% dos 32 meses e 10 de 11 trimestres (o único negativo é 2025T3, com -R$ 668).
- Custos baixos frente ao bruto: 15%. A média líquida é de 72 pts por trade (mediana de 57). Com custos 2x, o Sharpe fica em 1,33. Na amostra inteira com custos 3x, 12h/k=0,5 fica em 0,87 e 16h/k=1 em 0,74.
- Sem os 5 maiores trades sobra R$ 3.670 (62% do total). Sem os 5 melhores dias, o Sharpe ainda é 1,12.
- A correlação do P&L diário OOS com o ORB é de 0,26, então há alguma informação nova. A sobreposição se concentra na combinação das 12h (0,37 a 0,44). Nas de 14h e 16h fica entre 0,20 e 0,25.
- Execução realista: 1 contrato de WIN, entrada a mercado às 12h, 14h ou 16h (fora do leilão de abertura) e saída no fechamento. A liquidez não é problema nesse tamanho.

### Pontos fracos e riscos
- **DSR reprova e as tentativas estão subcontadas.** 94,3% com 18 tentativas e cerca de 92% com as tentativas escondidas. Como a grade foi escolhida olhando a amostra inteira, o walk-forward também está otimista (a hipótese admite isso).
- **Lucro na cauda.** Os 5 melhores trades respondem por 38% do lucro, os 10 melhores por 62% e os 20 melhores por 100%. Os maiores caem em dias de notícia de 2025: 09/04 (+3.588 pts, tarifaço), 16/12, 09/07, 08/04 e 14/02. A assimetria dos retornos diários é 1,1 e a curtose 11,6. É o perfil esperado de momentum, mas significa que o resultado depende de ainda haver dias de choque no futuro. Sem os 10 melhores dias, o Sharpe cai para 0,72.
- **Parâmetros instáveis.** O walk-forward escolhe 16h em 13 janelas, 12h em 11 e 14h em 8, e k=1 em 17, k=0,5 em 10 e k=0 em 5. Ele pula entre extremos da grade em janelas seguidas (ex.: 16h/k=0 seguido de 16h/k=1). E o k escolhido mais vezes, k=1, foi o que menos rendeu fora da amostra: 171 trades a 26 pts de média, contra 113 pts com k=0,5 e 95 com k=0. Ou seja, a seleção em 80 dias não acerta o melhor k.
- **Boa parte do resultado vem das 12h.** As janelas com 12h dão R$ 2.615 (44% do P&L OOS, 93 pts/trade), e é aí que a sobreposição com o ORB é maior. Nas combinações de 14h e 16h com k ≤ 0,5, o Sharpe na amostra inteira sem os 5 melhores dias fica entre -0,51 e 0,16. Só 16h/k=1 continua firme sem a cauda (0,90), e foi justamente a melhor combinação na exploração, com viés de seleção. 14h/k=0 não paga custos (1,4 pts/trade, custos = 90% do bruto).
- **Regime.** Em 2025 o acerto ficou abaixo de 50% (48%), e o ano só fecha positivo graças a poucos trades: sem os 3 maiores, o P&L de 2025 cai de R$ 2.082 para R$ 494. Em 2026 só há 18 trades OOS, e sem os 3 melhores o ano fica negativo (-R$ 276). Em 2023, as combinações de 12h e 14h foram negativas ou nulas com parâmetros fixos.
- **Drawdown longo.** Foram 197 dias abaixo do pico. Em termos de nocional (1 contrato ≈ R$ 26 mil), o DD de R$ 1.500 equivale a cerca de 5,8%, não 1,4%. O percentual do relatório usa R$ 100 mil de capital.

### O que testar a seguir (sugestões concretas para o estrategista)
1. **Testar a ideia nova sem as 12h.** Uma hipótese com `signal_time` em {14:00, 15:00, 16:00} e k em {0,75, 1,0, 1,25}, ou k fixo em 1,0, mostra se o momentum de fim de dia existe sem o componente que já é ORB. Também vale registrar a correlação com o ORB como critério.
2. **Reduzir os graus de liberdade.** Fixar k em vez de deixar o walk-forward escolher (ele escolhe mal) ou trocar k por um filtro contínuo, como posição proporcional a `mov/escala` com teto em 1. Uma grade menor também melhora o DSR.
3. **Medir a dependência de dias de choque.** Reportar o resultado excluindo os dias com range acima do percentil 95 da `escala`. Se o Sharpe cair para perto de zero, a estratégia é "comprar cauda" e deve ser avaliada como tal (ex.: risco de dias de reversão forte).
4. **Normalizar a hora de saída.** Comparar a saída fixa às 17:45 com a saída no fechamento, para não misturar dias de 17:50 com dias de 18:20. E checar se o lucro vem dos últimos 30 minutos (leilão de fechamento ou ajuste), o que mudaria a executabilidade.
5. **Validar em outro ativo** (WDO$N M5 ou ações líquidas) sem nova exploração. Momentum intradiário real tende a aparecer em vários mercados, e um ativo novo dá um teste independente sem gastar o holdout do WIN.
