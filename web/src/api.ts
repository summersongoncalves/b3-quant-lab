// Types mirror the JSON written by src/quantlab/research/pipeline.py and report.py.

export type Verdict = 'REJECTED' | 'PROMISING' | 'HOLDOUT_CANDIDATE'

export interface ReportSummary {
  id: string
  strategy: string
  title: string
  dataset: string
  daytrade: boolean
  created: string
  verdict: Verdict
  validator_verdict: string | null
  sharpe: number
  deflated_sharpe: number
  trades: number
  max_drawdown: number
  total_pnl: number
}

export interface Metrics {
  start: string
  end: string
  days: number
  total_pnl: number
  total_cost: number
  annual_excess_return: number
  annual_vol: number
  sharpe: number
  sortino: number
  max_drawdown: number
  calmar: number
  trades: number
  win_rate: number
  profit_factor: number
  avg_trade: number
  payoff: number
  exposure: number
  cost_to_gross: number
  sharpe_by_year: Record<string, number>
}

export type Params = Record<string, string | number | boolean>

// Portuguese display fields, filled by the API from the strategy module.
export interface StrategyLabels {
  title: string
  summary: string
  param_help: Record<string, string>
}

export interface Report extends StrategyLabels {
  id: string
  strategy: string
  description: string
  dataset: string
  daytrade: boolean
  created: string
  verdict: Verdict
  checks: Record<string, boolean>
  gates: Record<string, number>
  lookahead_problems: string[]
  oos: Metrics
  oos_2x_costs: { sharpe: number; total_pnl: number; max_drawdown: number }
  deflated_sharpe: number
  trials_on_dataset: number
  walk_forward: {
    train_days: number
    test_days: number
    folds: { test_start: string; test_end: string; params: Params; train_sharpe: number }[]
  }
  most_chosen_params: Params
  grid: { params: Params; sharpe: number; trades: number; max_drawdown: number }[]
  equity?: { dates: string[]; pnl: number[]; drawdown: number[] }
  trade_pnls?: number[]
  validator_analysis: string | null
  has_png: boolean
}

export interface Hypothesis {
  id: string
  title: string
  dataset: string | null
  mode: string | null
  state: string | null
}

export interface Dataset {
  id: string
  bars: number
  start: string
  end: string
  holdout_start: string | null
  trials: number
}

export interface StrategyInfo extends StrategyLabels {
  name: string
  description: string
  timeframe: string
  daytrade: boolean
  params: Params
  grid: Record<string, (string | number)[]>
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`/api${path}`)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText} em /api${path}`)
  return res.json() as Promise<T>
}

export const api = {
  reports: () => get<ReportSummary[]>('/reports'),
  report: (id: string) => get<Report>(`/reports/${encodeURIComponent(id)}`),
  hypotheses: () => get<Hypothesis[]>('/hypotheses'),
  hypothesis: (id: string) => get<{ id: string; markdown: string }>(`/hypotheses/${encodeURIComponent(id)}`),
  cycles: () => get<{ id: string }[]>('/cycles'),
  cycle: (id: string) => get<{ id: string; markdown: string }>(`/cycles/${encodeURIComponent(id)}`),
  datasets: () => get<Dataset[]>('/datasets'),
  strategies: () => get<StrategyInfo[]>('/strategies'),
}
