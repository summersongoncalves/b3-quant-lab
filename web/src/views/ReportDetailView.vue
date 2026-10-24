<script setup lang="ts">
import { computed } from 'vue'
import { api } from '../api'
import { useAsync } from '../useAsync'
import { brl, date, dateTime, num, params as fmtParams, pct } from '../format'
import VerdictBadge from '../components/VerdictBadge.vue'
import EquityChart from '../components/EquityChart.vue'
import BarChart from '../components/BarChart.vue'
import GridHeatmap from '../components/GridHeatmap.vue'
import Markdown from '../components/Markdown.vue'
import Term from '../components/Term.vue'

const props = defineProps<{ id: string }>()
const { data: r, error, loading } = useAsync(() => api.report(props.id))

// What each automatic check means, shown next to it (same order as pipeline.GATES).
const CHECKS: Record<string, { label: string; term: string; why: (g: Record<string, number>) => string }> = {
  no_lookahead: { label: 'Sem look-ahead', term: 'lookahead', why: () => 'O sinal não muda quando os dados futuros são removidos.' },
  oos_sharpe: { label: 'Sharpe fora da amostra', term: 'oos', why: (g) => `Mínimo ${num(g.min_oos_sharpe)} no walk-forward.` },
  oos_trades: { label: 'Trades suficientes', term: 'trade', why: (g) => `Mínimo ${g.min_oos_trades} trades; com poucos, o resultado é sorte.` },
  deflated_sharpe: { label: 'Deflated Sharpe', term: 'dsr', why: (g) => `≥ ${pct(g.min_dsr, 0)}: melhor que o melhor de N estratégias aleatórias.` },
  stable_years: { label: 'Estável no tempo', term: 'sharpe', why: (g) => `≥ ${pct(g.min_share_positive_years, 0)} dos anos com Sharpe positivo.` },
  robust_grid: { label: 'Parâmetros robustos', term: 'robust_grid', why: (g) => `≥ ${pct(g.min_share_positive_grid, 0)} da grade com Sharpe positivo.` },
  survives_2x_costs: { label: 'Sobrevive a custos 2x', term: 'stress_costs', why: () => 'Continua positiva com custos e slippage dobrados.' },
}

const years = computed(() => Object.entries(r.value?.oos.sharpe_by_year ?? {}))

// Histogram of trade P&L: shows whether profit comes from many trades or a few outliers.
const histogram = computed(() => {
  const pnls = r.value?.trade_pnls ?? []
  if (!pnls.length) return null
  const bins = 24
  const lo = Math.min(...pnls)
  const hi = Math.max(...pnls)
  const width = (hi - lo) / bins || 1
  const counts = new Array(bins).fill(0)
  for (const p of pnls) counts[Math.min(bins - 1, Math.floor((p - lo) / width))]++
  const centers = counts.map((_, i) => lo + width * (i + 0.5))
  return { labels: centers.map((c) => brl(c)), values: counts, signs: centers }
})

const topTradesShare = computed(() => {
  const pnls = [...(r.value?.trade_pnls ?? [])].sort((a, b) => b - a)
  const total = pnls.reduce((a, b) => a + b, 0)
  if (!pnls.length || total <= 0) return null
  const top5 = pnls.slice(0, 5).reduce((a, b) => a + b, 0)
  return top5 / total
})
</script>

<template>
  <main class="page">
    <RouterLink to="/" class="back">← Relatórios</RouterLink>
    <div v-if="loading" class="state">Carregando…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <template v-else-if="r">
      <div class="page-header">
        <div>
          <h1>{{ r.title }} <span class="muted dataset"><Term id="dataset">{{ r.dataset }}</Term></span></h1>
          <p class="subtitle">{{ r.summary || r.description }}</p>
          <p class="subtitle small">
            <Term :id="r.daytrade ? 'daytrade' : 'swing'">{{ r.daytrade ? 'Day trade' : 'Swing trade' }}</Term>
            · código <span class="mono">{{ r.strategy }}</span> · gerado em {{ dateTime(r.created) }}
          </p>
        </div>
        <VerdictBadge :verdict="r.verdict" big />
      </div>

      <div class="kpis">
        <div class="card kpi"><div class="muted"><Term id="sharpe">Sharpe</Term> <Term id="oos">OOS</Term></div><div class="v" :class="r.oos.sharpe >= 0 ? 'pos' : 'neg'">{{ num(r.oos.sharpe) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="dsr">Deflated Sharpe</Term></div><div class="v">{{ pct(r.deflated_sharpe) }}</div><div class="muted small">{{ r.trials_on_dataset }} <Term id="trials">tentativas</Term> no dataset</div></div>
        <div class="card kpi"><div class="muted"><Term id="pnl">P&amp;L</Term> (1 unidade)</div><div class="v" :class="r.oos.total_pnl >= 0 ? 'pos' : 'neg'">{{ brl(r.oos.total_pnl) }}</div><div class="muted small"><Term id="costs">custos</Term> {{ brl(r.oos.total_cost) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="drawdown">Max drawdown</Term></div><div class="v neg">{{ pct(r.oos.max_drawdown) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="trade">Trades</Term></div><div class="v">{{ r.oos.trades }}</div><div class="muted small"><Term id="win_rate">acerto</Term> {{ pct(r.oos.win_rate, 0) }} · <Term id="payoff">payoff</Term> {{ num(r.oos.payoff) }}</div></div>
      </div>

      <div class="layout">
        <section class="card">
          <h2><Term id="equity">Patrimônio</Term> <Term id="oos">fora da amostra</Term></h2>
          <p class="muted small chart-note">{{ date(r.oos.start) }} → {{ date(r.oos.end) }} · janelas <Term id="walk_forward">walk-forward</Term> costuradas</p>
          <EquityChart v-if="r.equity" v-bind="r.equity" />
          <img v-else-if="r.has_png" :src="`/api/reports/${r.id}/equity.png`" alt="Curva de patrimônio" class="png" />
        </section>

        <section class="card">
          <h2><Term id="gates">Critérios</Term></h2>
          <ul class="checks">
            <li v-for="(ok, key) in r.checks" :key="key">
              <span class="icon" :class="ok ? 'pos' : 'neg'">{{ ok ? '✓' : '✗' }}</span>
              <div>
                <div><Term v-if="CHECKS[key]" :id="CHECKS[key].term">{{ CHECKS[key].label }}</Term><template v-else>{{ key }}</template></div>
                <div class="muted small">{{ CHECKS[key]?.why(r.gates) }}</div>
              </div>
            </li>
          </ul>
          <div v-if="r.lookahead_problems.length" class="alert">
            <strong><Term id="lookahead">Look-ahead</Term> detectado</strong>
            <div v-for="p in r.lookahead_problems" :key="p" class="mono small">{{ p }}</div>
          </div>
        </section>
      </div>

      <section v-if="r.validator_analysis" class="card section">
        <Markdown :source="r.validator_analysis" :path="`reports/${id}/report.md`" />
      </section>

      <div class="two">
        <section class="card">
          <h2><Term id="sharpe">Sharpe</Term> por ano</h2>
          <BarChart :labels="years.map(([y]) => y)" :values="years.map(([, s]) => s)" :format="(v) => num(v)" />
        </section>
        <section class="card">
          <h2>Distribuição do <Term id="pnl">P&amp;L</Term> por <Term id="trade">trade</Term></h2>
          <BarChart v-if="histogram" v-bind="histogram" :format="(v) => `${v} trades`" />
          <p v-if="topTradesShare !== null" class="muted small">
            Os <Term id="concentration">5 melhores trades</Term> somam <strong>{{ pct(topTradesShare, 0) }}</strong> do lucro total.
            {{ topTradesShare > 0.5 ? 'Resultado concentrado: cuidado.' : 'Lucro bem distribuído.' }}
          </p>
        </section>
      </div>

      <div class="kpis secondary">
        <div class="card kpi"><div class="muted"><Term id="excess_return">Retorno anual acima do CDI</Term></div><div class="v sm">{{ pct(r.oos.annual_excess_return) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="sortino">Sortino</Term></div><div class="v sm">{{ num(r.oos.sortino) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="profit_factor">Profit factor</Term></div><div class="v sm">{{ num(r.oos.profit_factor) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="cost_to_gross">Custos / bruto</Term></div><div class="v sm">{{ pct(r.oos.cost_to_gross, 0) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="stress_costs">Sharpe c/ custos 2x</Term></div><div class="v sm">{{ num(r.oos_2x_costs.sharpe) }}</div></div>
        <div class="card kpi"><div class="muted"><Term id="exposure">Exposição</Term></div><div class="v sm">{{ pct(r.oos.exposure, 0) }}</div></div>
      </div>

      <div class="two">
        <section class="card">
          <h2><Term id="robust_grid">Robustez da grade</Term></h2>
          <p class="muted small">Sharpe de cada combinação na amostra de pesquisa inteira (<Term id="in_sample">in-sample</Term>). Procure uma região estável, não um pico isolado.</p>
          <GridHeatmap :grid="r.grid" :param-help="r.param_help" />
        </section>
        <section class="card">
          <h2><Term id="walk_forward">Walk-forward</Term></h2>
          <p class="muted small"><Term id="train_test">Treino</Term> {{ r.walk_forward.train_days }} dias → teste {{ r.walk_forward.test_days }} dias. Mais escolhido: <span class="mono">{{ fmtParams(r.most_chosen_params) }}</span></p>
          <div class="table-wrap folds">
            <table>
              <thead><tr>
                <th><Term id="fold">Teste</Term></th><th><Term id="params">Parâmetros</Term></th>
                <th class="num"><Term text="Sharpe que os parâmetros escolhidos tiveram no período de treino. Costuma ser bem maior que o resultado fora da amostra.">Sharpe treino</Term></th>
              </tr></thead>
              <tbody>
                <tr v-for="f in r.walk_forward.folds" :key="f.test_start">
                  <td class="small nowrap">{{ date(f.test_start) }} → {{ date(f.test_end) }}</td>
                  <td class="mono">{{ fmtParams(f.params) }}</td>
                  <td class="num" :class="f.train_sharpe >= 0 ? 'pos' : 'neg'">{{ num(f.train_sharpe) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </template>
  </main>
</template>

<style scoped>
.back { display: inline-block; margin-bottom: 12px; font-size: 13px; }
.dataset { font-weight: 500; font-size: 16px; font-family: var(--mono); }
.kpis { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 16px; }
.kpis.secondary { margin-top: 16px; grid-template-columns: repeat(auto-fit, minmax(115px, 1fr)); }
.kpi .v { font-size: 24px; font-weight: 700; font-variant-numeric: tabular-nums; margin-top: 2px; }
.kpi .v.sm { font-size: 18px; }
.small { font-size: 12px; }
.nowrap { white-space: nowrap; }
.layout { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 16px; }
.two { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; margin-top: 16px; }
.section { margin-top: 16px; }
.chart-note { margin: -8px 0 12px; }
.png { width: 100%; border-radius: 6px; }
.checks { list-style: none; margin: 0; padding: 0; display: grid; gap: 12px; }
.checks li { display: flex; gap: 10px; align-items: flex-start; }
.icon { font-weight: 700; width: 18px; flex-shrink: 0; }
.alert { margin-top: 16px; padding: 10px 12px; border-radius: 8px; background: var(--negative-bg); color: var(--negative); }
.folds { max-height: 360px; overflow-y: auto; }
@media (max-width: 860px) {
  .layout, .two { grid-template-columns: 1fr; }
}
</style>
