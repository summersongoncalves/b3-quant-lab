// Glossary of the (mostly English) terms shown in the UI. `short` is the tooltip
// text; `long` is extra detail shown only on the glossary page.

export interface Entry {
  id: string
  term: string
  pt?: string // literal translation, when the term is in English
  category: Category
  short: string
  long?: string
}

export const CATEGORIES = [
  'Resultado',
  'Risco',
  'Validação',
  'Veredito',
  'Custos',
  'Mercado e dados',
  'Estratégias e indicadores',
] as const
export type Category = (typeof CATEGORIES)[number]

export const GLOSSARY: Entry[] = [
  // Resultado
  { id: 'trade', term: 'Trade', pt: 'operação', category: 'Resultado',
    short: 'Uma operação completa: entrar numa posição e sair dela.',
    long: 'Num day trade, cada trade abre e fecha no mesmo dia. Quanto mais trades, mais confiável é a estatística: com poucos, o resultado pode ser só sorte.' },
  { id: 'pnl', term: 'P&L', pt: 'Profit and Loss, lucro e prejuízo', category: 'Resultado',
    short: 'O resultado em reais. "1 unidade" quer dizer operando 1 contrato (ou 1 lote) por vez.',
    long: 'O P&L mostrado já desconta custos e slippage.' },
  { id: 'win_rate', term: 'Win rate', pt: 'taxa de acerto', category: 'Resultado',
    short: 'Porcentagem de trades que deram lucro.',
    long: 'Sozinha, não diz nada: uma estratégia pode acertar 30% e ganhar dinheiro (se ganha muito quando acerta) ou acertar 80% e perder (se perde muito quando erra). Veja junto com o payoff.' },
  { id: 'payoff', term: 'Payoff', pt: 'relação ganho/perda', category: 'Resultado',
    short: 'Ganho médio dos trades vencedores dividido pela perda média dos perdedores. Payoff 2 = quando ganha, ganha o dobro do que perde quando perde.' },
  { id: 'profit_factor', term: 'Profit factor', pt: 'fator de lucro', category: 'Resultado',
    short: 'Soma de todos os ganhos dividida pela soma de todas as perdas. Acima de 1 dá lucro; 1,5 já é bom.' },
  { id: 'equity', term: 'Equity', pt: 'patrimônio, curva de capital', category: 'Resultado',
    short: 'Gráfico do lucro acumulado ao longo do tempo. Uma curva boa sobe de forma constante, sem depender de saltos isolados.' },
  { id: 'excess_return', term: 'Retorno acima do CDI', pt: 'excess return', category: 'Resultado',
    short: 'Quanto a estratégia rendeu por ano além do que a renda fixa (CDI) renderia com o mesmo capital.' },
  { id: 'exposure', term: 'Exposição', pt: 'exposure', category: 'Resultado',
    short: 'Porcentagem do tempo em que a estratégia ficou posicionada (comprada ou vendida).' },

  // Risco
  { id: 'sharpe', term: 'Sharpe', pt: 'índice de Sharpe', category: 'Risco',
    short: 'Retorno acima do CDI dividido pela oscilação (volatilidade), por ano. Mede quanto você ganha por unidade de "susto".',
    long: 'Regra de bolso: abaixo de 0,5 é fraco, perto de 1 é bom, acima de 2 é excelente, e acima de 3 em backtest é motivo para desconfiar de erro.' },
  { id: 'sortino', term: 'Sortino', category: 'Risco',
    short: 'Igual ao Sharpe, mas só conta a oscilação para baixo (as quedas). Subidas fortes não são penalizadas.' },
  { id: 'volatility', term: 'Volatilidade', pt: 'volatility', category: 'Risco',
    short: 'Quanto o resultado oscila de um dia para o outro. Mais volatilidade = mais incerteza.' },
  { id: 'drawdown', term: 'Drawdown', pt: 'rebaixamento', category: 'Risco',
    short: 'Queda do patrimônio a partir do último pico. O Max drawdown (Max DD) é a maior queda da história da estratégia.',
    long: 'É a medida de dor: quanto você teria perdido, no pior momento, se tivesse começado no topo. Em %, sobre o capital de referência.' },

  // Validação
  { id: 'backtest', term: 'Backtest', pt: 'teste no passado', category: 'Validação',
    short: 'Simulação da estratégia em dados históricos, como se ela tivesse operado naquela época.' },
  { id: 'in_sample', term: 'In-sample', pt: 'dentro da amostra', category: 'Validação',
    short: 'Dados usados para escolher os parâmetros. Resultados aqui são sempre otimistas, porque a estratégia "já viu" esses dados.' },
  { id: 'oos', term: 'OOS', pt: 'out-of-sample, fora da amostra', category: 'Validação',
    short: 'Dados que a estratégia não viu ao escolher os parâmetros. É o resultado que conta de verdade.' },
  { id: 'walk_forward', term: 'Walk-forward', pt: 'andar para frente', category: 'Validação',
    short: 'Divide o histórico em blocos: escolhe os parâmetros com o passado (treino) e testa no bloco seguinte (teste). Repete andando no tempo.',
    long: 'Simula o que aconteceria na vida real: você só pode decidir com o que já aconteceu. Os pedaços de teste, costurados, formam o resultado OOS.' },
  { id: 'train_test', term: 'Treino e teste', pt: 'train / test', category: 'Validação',
    short: 'Treino é o período usado para escolher os parâmetros; teste é o período seguinte, onde eles são avaliados sem ajuste.' },
  { id: 'fold', term: 'Janela', pt: 'fold', category: 'Validação',
    short: 'Cada rodada do walk-forward: um período de treino seguido de um período de teste.' },
  { id: 'holdout', term: 'Holdout', pt: 'reserva', category: 'Validação',
    short: 'O final do histórico, trancado. Nenhum agente pode usar. Serve como prova final, uma única vez, só a seu pedido.',
    long: 'Se a estratégia for ajustada depois de ver o holdout, ele deixa de ser prova: vira mais um dado de treino.' },
  { id: 'lookahead', term: 'Look-ahead', pt: 'olhar para frente', category: 'Validação',
    short: 'Erro em que a estratégia usa, sem querer, uma informação do futuro. Faz qualquer coisa parecer genial no backtest e perder dinheiro na vida real.' },
  { id: 'overfitting', term: 'Overfitting', pt: 'sobreajuste', category: 'Validação',
    short: 'Quando os parâmetros se encaixam no ruído do passado em vez de num padrão real. Brilha no treino e falha fora da amostra.' },
  { id: 'dsr', term: 'Deflated Sharpe', pt: 'Sharpe "desinflado" (DSR)', category: 'Validação',
    short: 'Probabilidade de o Sharpe não ser sorte, já descontando quantas estratégias foram testadas no mesmo dataset. O mínimo exigido é 95%.',
    long: 'Quem testa 100 ideias aleatórias acaba achando uma com Sharpe alto por acaso. O DSR corrige isso usando o número de tentativas do registro.' },
  { id: 'trials', term: 'Tentativas', pt: 'trials', category: 'Validação',
    short: 'Quantas configurações já foram avaliadas no dataset. Quanto mais tentativas, mais alto o Deflated Sharpe exigido.' },
  { id: 'grid', term: 'Grade', pt: 'grid de parâmetros', category: 'Validação',
    short: 'A lista de valores testados para cada parâmetro. Cada combinação conta como uma tentativa.' },
  { id: 'heatmap', term: 'Heatmap', pt: 'mapa de calor', category: 'Validação',
    short: 'Tabela colorida com o Sharpe de cada combinação da grade. Verde = positivo, vermelho = negativo. Procure uma região verde, não um ponto isolado.' },
  { id: 'robust_grid', term: 'Robustez da grade', category: 'Validação',
    short: 'Se a estratégia funciona em vários parâmetros vizinhos, o padrão é mais provável de ser real. Se só um funciona, é provavelmente sorte.' },
  { id: 'stress_costs', term: 'Custos 2x', pt: 'teste de estresse', category: 'Validação',
    short: 'Refaz a conta com custos e slippage dobrados. Se o lucro some, a vantagem era frágil demais.' },
  { id: 'concentration', term: 'Concentração', category: 'Validação',
    short: 'Quanto do lucro vem de poucos trades. Se tirar os 5 melhores e o lucro sumir, a estratégia dependia de sorte em poucos dias.' },
  { id: 'gates', term: 'Critérios', pt: 'gates', category: 'Validação',
    short: 'Requisitos automáticos que a estratégia precisa cumprir. Não mudam para fazer uma estratégia passar.' },
  { id: 'baseline', term: 'Baseline', pt: 'referência', category: 'Validação',
    short: 'Estratégia simples que serve de régua: toda ideia nova precisa ser melhor que ela.' },

  // Veredito
  { id: 'verdict_rejected', term: 'Rejeitada', pt: 'REJECTED', category: 'Veredito',
    short: 'Falhou em algum critério. Não vale insistir sem uma ideia nova.' },
  { id: 'verdict_promising', term: 'Promissora', pt: 'PROMISING', category: 'Veredito',
    short: 'Passou em parte dos critérios. Tem algo, mas ainda não é confiável o bastante para o holdout.' },
  { id: 'verdict_holdout', term: 'Candidata ao holdout', pt: 'HOLDOUT_CANDIDATE', category: 'Veredito',
    short: 'Passou em todos os critérios. Pode ir para a prova final no holdout, se você decidir.' },

  // Custos
  { id: 'costs', term: 'Custos', category: 'Custos',
    short: 'Corretagem, emolumentos da B3 e slippage, descontados de cada trade.' },
  { id: 'slippage', term: 'Slippage', pt: 'escorregamento', category: 'Custos',
    short: 'Diferença entre o preço que você queria e o preço que conseguiu. A simulação assume alguns ticks contra você em cada ordem.' },
  { id: 'cost_to_gross', term: 'Custos / bruto', category: 'Custos',
    short: 'Quanto do lucro bruto foi consumido pelos custos. Acima de 50% é sinal de que a vantagem é pequena demais.' },
  { id: 'tick', term: 'Tick', category: 'Custos',
    short: 'A menor variação de preço possível. No WIN, 1 tick = 5 pontos = R$ 1,00 por contrato.' },

  // Mercado e dados
  { id: 'dataset', term: 'Dataset', pt: 'conjunto de dados', category: 'Mercado e dados',
    short: 'O histórico de um ativo num timeframe, ex.: WIN_N_M5 = mini-índice, barras de 5 minutos.' },
  { id: 'timeframe', term: 'Timeframe', pt: 'tempo gráfico', category: 'Mercado e dados',
    short: 'A duração de cada barra: M5 = 5 minutos, H1 = 1 hora, D1 = 1 dia.' },
  { id: 'bar', term: 'Barra', pt: 'candle', category: 'Mercado e dados',
    short: 'Resumo do preço num intervalo: abertura (open), máxima (high), mínima (low) e fechamento (close), o chamado OHLC.' },
  { id: 'volume', term: 'Volume', category: 'Mercado e dados',
    short: 'Quantos contratos foram negociados no intervalo. Volume alto mostra participação forte no movimento.' },
  { id: 'win', term: 'WIN$N', category: 'Mercado e dados',
    short: 'Mini-contrato futuro do Ibovespa. O "$N" indica a série contínua, que emenda os contratos que vencem.' },
  { id: 'roll', term: 'Rolagem', pt: 'roll', category: 'Mercado e dados',
    short: 'Troca do contrato que vence pelo próximo. Na série contínua pode aparecer como um salto de preço artificial.' },
  { id: 'cdi', term: 'CDI', category: 'Mercado e dados',
    short: 'Taxa da renda fixa no Brasil. É o "rendimento sem risco" contra o qual a estratégia é comparada.' },
  { id: 'daytrade', term: 'Day trade', category: 'Mercado e dados',
    short: 'Abre e fecha a posição no mesmo dia. Nunca dorme posicionado.' },
  { id: 'swing', term: 'Swing trade', category: 'Mercado e dados',
    short: 'Mantém a posição por alguns dias ou semanas.' },

  // Estratégias e indicadores
  { id: 'signal', term: 'Sinal', pt: 'signal', category: 'Estratégias e indicadores',
    short: 'A decisão da estratégia: comprar, vender ou ficar de fora. Calculado no fechamento de uma barra e executado na abertura da seguinte.' },
  { id: 'long_short', term: 'Comprado / vendido', pt: 'long / short', category: 'Estratégias e indicadores',
    short: 'Comprado (long) ganha se o preço sobe. Vendido (short) ganha se o preço cai.' },
  { id: 'params', term: 'Parâmetros', pt: 'params', category: 'Estratégias e indicadores',
    short: 'Os "botões de ajuste" da estratégia, como horários e limites. Quanto mais parâmetros, maior o risco de overfitting.' },
  { id: 'momentum', term: 'Momentum', pt: 'impulso', category: 'Estratégias e indicadores',
    short: 'Ideia de que o que está subindo tende a continuar subindo (e o que cai, a continuar caindo).' },
  { id: 'breakout', term: 'Breakout', pt: 'rompimento', category: 'Estratégias e indicadores',
    short: 'Entrada quando o preço sai de uma faixa (máxima ou mínima) que vinha respeitando.' },
  { id: 'opening_range', term: 'Opening range', pt: 'faixa de abertura', category: 'Estratégias e indicadores',
    short: 'A máxima e a mínima dos primeiros minutos do pregão.' },
  { id: 'moving_average', term: 'Média móvel', pt: 'moving average', category: 'Estratégias e indicadores',
    short: 'Média dos últimos N preços, recalculada a cada barra. Suaviza o ruído e mostra a tendência.' },
  { id: 'vwap', term: 'VWAP', pt: 'Volume-Weighted Average Price, preço médio ponderado por volume', category: 'Estratégias e indicadores',
    short: 'Preço médio do dia (ou da semana) pesando cada preço pelo volume negociado. Muito usado por institucionais como "preço justo" do período.',
    long: 'A VWAP diária recomeça a cada pregão; a semanal recomeça na segunda-feira. Preço acima da VWAP sugere compradores no controle; abaixo, vendedores.' },
  { id: 'relative_volume', term: 'Volume relativo', pt: 'relative volume', category: 'Estratégias e indicadores',
    short: 'Volume do dia até agora dividido pelo volume típico até o mesmo horário. 2,0 = o dobro do normal.' },
]

export const BY_ID: Record<string, Entry> = Object.fromEntries(GLOSSARY.map((e) => [e.id, e]))
