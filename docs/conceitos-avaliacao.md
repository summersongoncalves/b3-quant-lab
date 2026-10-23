# Como avaliar uma estratégia (e não se enganar)

Guia de estudo do laboratório. Cada conceito explica **o que é**, **por que importa** e **onde está no código**. Também serve de roteiro para entrevistas: quem sabe explicar estes pontos mostra maturidade em pesquisa quantitativa.

---

## 1. O maior inimigo: você acha padrões em ruído

Preço de mercado é, em grande parte, ruído. Se você testar 100 regras aleatórias, umas 5 vão parecer "significativas" a 95% de confiança **por puro acaso**. Quase todo o resto deste documento existe para lidar com isso.

> **Pergunta de entrevista clássica:** "Seu backtest tem Sharpe 2. Por que eu não deveria acreditar?"
> Boa resposta: quantas variações você testou até chegar nele? Tem look-ahead? Custos realistas? Funciona fora da amostra? Depende de poucos trades?

---

## 2. Vieses que invalidam um backtest

### Look-ahead bias (viés de olhar o futuro)
Usar uma informação que você não teria no momento da decisão. Exemplos sutis:
- decidir comprar "no fechamento" usando o próprio fechamento (só sabe o fechamento quando ele já aconteceu);
- normalizar um indicador com a média ou o desvio **da série inteira**;
- usar a máxima do dia para decidir uma entrada às 11h.

**No código:** o motor executa na abertura da barra seguinte (`engine.py`), e `validation.lookahead_check` recalcula o sinal com os dados cortados em vários pontos. Se o sinal muda quando o futuro some, há vazamento. O teste `test_lookahead_check_catches_peeking` mostra o detector pegando uma estratégia que trapaceia.

### Survivorship bias (viés de sobrevivência)
Testar só ações que existem hoje ignora as que quebraram ou saíram da bolsa (ex.: OGX). A carteira "sobrevivente" parece melhor do que era. Afeta estratégias de seleção de ações. Mini-índice e mini-dólar não têm esse problema.

### Data snooping / overfitting (sobreajuste)
Ajustar regras e parâmetros até o passado ficar bonito. A estratégia "decora" o ruído do passado e falha no futuro. Sinais de alerta: muitos parâmetros, valores muito específicos (média de 37 períodos, mas não 35 nem 40), lucro concentrado em poucos trades.

---

## 3. Separação dos dados

```
|------------- pesquisa (80%) --------------|---- holdout (20%) ----|
  walk-forward: [treino][teste]                 trancado. Usado UMA vez,
                     [treino][teste]            no fim, por decisão humana.
                          [treino][teste]
```

- **In-sample (dentro da amostra):** dados onde você escolhe parâmetros. Resultado aqui é otimista por definição.
- **Out-of-sample, OOS (fora da amostra):** dados que não influenciaram nenhuma escolha. É o que vale.
- **Walk-forward:** escolhe os melhores parâmetros numa janela de treino e opera a janela seguinte com eles, avançando no tempo. Simula o que você faria na vida real: recalibrar periodicamente sem ver o futuro. As janelas de teste costuradas formam o resultado OOS. *Código:* `validation.walk_forward`.
- **Holdout:** os 20% finais de cada dataset são congelados no primeiro download (`data/holdouts.json`). Se você testar no holdout, não gostar, ajustar e testar de novo, o holdout virou treino. Por isso `quantlab holdout` recusa uma segunda tentativa.

---

## 4. Métricas: o que cada uma diz

| Métrica | O que é | Leitura |
|---|---|---|
| **Retorno acima do CDI** | Retorno anualizado menos o que o dinheiro renderia parado | No Brasil, com CDI a ~14%, ganhar 10% ao ano é **perder** |
| **Volatilidade anual** | Desvio padrão dos retornos diários × √252 | Quanto o resultado oscila |
| **Sharpe** | Retorno acima do CDI ÷ volatilidade, anualizado | > 1 é bom; > 2 em backtest costuma ser bug ou overfitting |
| **Sortino** | Igual ao Sharpe, mas só penaliza a volatilidade das quedas | Útil quando os ganhos são assimétricos |
| **Max drawdown** | Maior queda do pico ao vale do patrimônio | O que você teria de aguentar psicologicamente |
| **Calmar** | Retorno anual ÷ max drawdown | Retorno por unidade de "dor" |
| **Win rate (taxa de acerto)** | % de trades positivos | Sozinha não diz nada: 90% de acerto com payoff 0,05 perde dinheiro |
| **Payoff** | Ganho médio ÷ perda média | Combine com a taxa de acerto |
| **Profit factor** | Soma dos ganhos ÷ soma das perdas | > 1,3 depois dos custos começa a ser interessante |
| **Custos / bruto** | Quanto da vantagem bruta vai para custos | > 50% = vantagem frágil |
| **Exposição** | % do tempo posicionado | Baixa exposição com bom retorno é eficiente |

**Por que métricas diárias, mesmo no intraday?** Para comparar estratégias de timeframes diferentes na mesma régua, e porque Sharpe calculado em barras de 5 min com √(n° de barras) distorce o resultado.

**Detalhe do CDI no código** (`metrics.daily_excess_returns`): no futuro, você deposita só margem, que pode ficar em título rendendo CDI, então o P&L já é retorno excedente. Na ação, o dinheiro sai do CDI enquanto está posicionado, então desconta o CDI proporcional à exposição.

---

## 5. Significância estatística

### PSR: Probabilistic Sharpe Ratio
Um Sharpe medido em 60 dias é muito menos confiável que um medido em 1.000. O PSR dá a **probabilidade de o Sharpe verdadeiro ser maior que zero**, considerando o tamanho da amostra e o formato da distribuição dos retornos. Retornos com assimetria negativa (muitos ganhos pequenos e perdas grandes raras, típico de "vender volatilidade") e caudas gordas (curtose alta) reduzem a confiança.

### DSR: Deflated Sharpe Ratio
O PSR compara com zero. Mas, se você testou 200 variações, a melhor delas teria um Sharpe alto **mesmo sem nenhuma habilidade**. O DSR calcula esse "Sharpe esperado do melhor entre N chutes" e pergunta: **qual a probabilidade de o resultado ser melhor que o melhor acaso?**

Por isso existe o `research/registry.jsonl`: ele conta todas as tentativas por dataset. Quanto mais o ciclo de agentes roda, **mais difícil fica passar**. Isso é intencional e é a defesa contra o próprio ciclo virar uma máquina de overfitting.

Critério do laboratório: DSR ≥ 95%.

Referências: Bailey & López de Prado, *The Deflated Sharpe Ratio* (2014); López de Prado, *Advances in Financial Machine Learning* (2018), caps. 11 a 14.

---

## 6. Robustez

- **Grade vizinha:** se só `média=37` funciona e 35 e 40 não, é ruído. O critério exige que a maioria das combinações da grade tenha Sharpe positivo.
- **Estabilidade no tempo:** a maioria dos anos deve ser positiva. Uma estratégia que ganhou tudo em março de 2020 é uma aposta num evento, não um padrão.
- **Custos 2x:** se dobrar custos e slippage mata a estratégia, ela vive no limite.
- **Concentração:** quanto sobra se tirar os 5 melhores trades? (O validador checa.)
- **Parâmetros do walk-forward:** se cada janela escolhe um extremo diferente da grade, não existe um parâmetro "certo". É ruído.

---

## 7. Especificidades da B3

| Item | Detalhe |
|---|---|
| **WIN (mini-índice)** | 1 ponto = R$ 0,20; tick = 5 pontos (R$ 1,00 por contrato) |
| **WDO (mini-dólar)** | 1 ponto = R$ 10,00; tick = 0,5 ponto (R$ 5,00 por contrato) |
| **Vencimentos** | WIN vence em meses pares (quarta-feira mais próxima do dia 15); WDO todo mês (1º dia útil). Séries contínuas (`WIN$N`) emendam contratos, e o salto na rolagem **não é movimento real** de preço |
| **Horários** | Leilão de abertura (~9h) e de fechamento; a primeira barra é distorcida. Horário de verão americano muda o horário de abertura de alguns ativos ao longo do ano |
| **Custos** | Clear não cobra corretagem. Sobram emolumentos e taxas da B3 (`instruments.py`, **valores aproximados: calibre com uma nota de corretagem**) e slippage (1 tick por lado, por padrão) |
| **IR (imposto de renda)** | Day trade: 20% sobre o lucro líquido mensal. Swing: 15% (ações têm isenção para vendas até R$ 20 mil/mês; futuros não). Prejuízo compensa lucro do mesmo tipo. O motor ainda **não** desconta IR |
| **Dados do MT5** | Histórico intraday é limitado (meses a poucos anos, conforme a corretora). Timeframe diário vai bem mais longe |

---

## 8. Checklist mental para qualquer resultado

1. Tem look-ahead? (automático + leitura do código)
2. Quantas tentativas até chegar aqui? (DSR)
3. Fora da amostra se sustenta? (walk-forward)
4. Sobrevive a custos realistas e a custos dobrados?
5. Depende de poucos trades, poucos dias ou um único ano?
6. Os parâmetros são estáveis?
7. Bate o baseline e o CDI?
8. Dá para executar de verdade (liquidez, horário, leilão)?

Só depois de tudo isso: holdout, uma vez.
