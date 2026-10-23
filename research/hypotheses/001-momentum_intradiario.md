# 001 · Momentum intradiário: o movimento da manhã continua até o fechamento
- Dataset: WIN$N M5
- Modo: daytrade
- Estado: PROMISSORA

## Padrão
Quando o WIN anda bastante entre a abertura do pregão e um horário fixo do dia (12h, 14h ou 16h), o trecho que falta até o fechamento tende a seguir a mesma direção. O efeito parece mais forte quando o movimento acumulado é grande em relação ao normal recente.

## Regras
Definições (barras de 5 min rotuladas pelo horário de abertura; tudo calculado no fechamento da barra de sinal):
- `abertura_dia` = `open` da primeira barra do dia. Só operar dias cuja primeira barra começa até 09:30 (descarta os poucos dias com pregão começando à tarde).
- Barra de sinal = a barra cujo **fechamento** acontece em `signal_time` (ex.: para `signal_time = "12:00"`, é a barra rotulada 11:55).
- `mov` = `close` da barra de sinal − `abertura_dia` (em pontos).
- `escala` = mediana de `|mov|` nos **20 dias anteriores** (mesma `signal_time`, só dias passados; sem o dia atual). Dias sem 20 dias de histórico não operam.

Entrada:
- Se `|mov| > k × escala`: posição alvo = `sinal(mov)` (+1 comprado se `mov > 0`, −1 vendido se `mov < 0`), definida no fechamento da barra de sinal. Pela convenção do motor, a execução acontece na abertura da barra seguinte.
- Caso contrário, não opera no dia.
- No máximo 1 entrada por dia, só na barra de sinal (nenhuma entrada em outro horário).

Saída:
- Mantém a posição até o fim do pregão; o motor zera no fechamento (day trade). Sem stop e sem alvo.

1 contrato, ambos os lados.

## Parâmetros
| nome | padrão | grade |
|---|---|---|
| signal_time | "14:00" | ["12:00", "14:00", "16:00"] |
| k | 0.5 | [0.0, 0.5, 1.0] |

Janela da `escala` fixa em 20 dias (não é parâmetro). Grade total: 9 combinações.

## Por que pode falhar
1. **Custos contra uma vantagem pequena**: na exploração, o ganho bruto médio por trade ficou entre ~14 e ~88 pontos, conforme a combinação. A ida e volta custa ~12–13 pontos (2 ticks de slippage + emolumentos). Com `k = 0` e sinal às 14h, a média bruta (~14 pts) não paga os custos. O padrão só deve se sustentar com o filtro `k > 0`.
2. **Depende de poucos dias de tendência forte e de um ano**: 2026 tem poucos dias na amostra, e as médias desse ano foram muito altas (ex.: 478 pts com 12h/k=1). Em 2025 o efeito foi fraco em algumas combinações (16h/k=0: −2 pts). Os ganhos podem estar concentrados em poucos dias de notícia (comportamento de cauda), não num padrão estável. O checador de concentração (tirar os 5 melhores trades) é decisivo aqui.
3. **Sobreposição com o baseline de opening range breakout**: com `signal_time = "12:00"`, a regra é quase a mesma coisa que o rompimento da faixa de abertura segurado até o fechamento (que já falhou no Deflated Sharpe). Se só a combinação das 12h funcionar, não é ideia nova. O teste interessante são as entradas das 14h e 16h, que ficam bem menos tempo posicionadas.

Explicação econômica plausível (não obrigatória): literatura de "market intraday momentum" (Gao, Han, Li e Zhou, *Journal of Financial Economics*, 2018) atribui o efeito a fluxo de rebalanceamento/hedge de gama no fim do dia e a investidores que reagem tarde à informação da manhã. No WIN, hedge de opções e ajuste de posições institucionais perto do fechamento seriam o canal análogo. Não há nota em `knowledge/` sobre isso; a referência vem da literatura geral.

## Origem
Primeira ideia (não há hipóteses anteriores). Nasceu de exploração em `store.load("WIN$N", "M5")` (amostra de pesquisa 2023-03-24 → 2026-02-04, 714 dias), scripts `research/scratch/explore_001.py` e `research/scratch/explore_001b.py`.

O que foi olhado até chegar aqui (contar como tentativas escondidas, cerca de 5 análises e ~15 variações):
1. Retorno médio e amplitude média por hora do dia: sem viés de direção relevante (médias de −1 a +2 pts por barra).
2. Correlação do movimento da manhã com a última hora: 1ª meia hora → última hora = 0,09; abertura → 12h vs. última hora = 0,15 (seguir o sinal das 12h: +30 pts brutos, 54% de acerto). Foi o primeiro indício.
3. Gap de abertura vs. primeira hora e vs. o dia: correlações −0,02 e −0,09. Fraco, descartado (e contaminado por saltos de rolagem da série contínua).
4. Tamanho da 1ª meia hora vs. continuação até o fechamento: só os quartis de movimento grande continuam (+130 e +160 pts). Daí veio o filtro `k`.
5. Grade 3×3 (horário de sinal × `k`) com resultados por ano, que é exatamente a grade proposta. Médias brutas por trade de 14 a 88 pts; Sharpe anualizado bruto aproximado de 0,4 a 2,5. Melhor combinação: 16h com k=1 (65 pts, 56% de acerto, todos os anos positivos). Atenção: essa grade foi vista na amostra inteira antes do walk-forward, então o resultado do validador vai ser otimista.

Relatório: reports/20261023-185603_momentum_intradiario_WIN_N_M5
