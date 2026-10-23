<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api, type Verdict } from '../api'
import { useAsync } from '../useAsync'
import { brl, dateTime, num, pct } from '../format'
import VerdictBadge from '../components/VerdictBadge.vue'
import Term from '../components/Term.vue'

const router = useRouter()
const { data: reports, error, loading } = useAsync(api.reports)

const dataset = ref('')
const verdict = ref<'' | Verdict>('')
const mode = ref<'' | 'daytrade' | 'swing'>('')

const datasets = computed(() => [...new Set((reports.value ?? []).map((r) => r.dataset))].sort())
const filtered = computed(() =>
  (reports.value ?? []).filter((r) =>
    (!dataset.value || r.dataset === dataset.value) &&
    (!verdict.value || r.verdict === verdict.value) &&
    (!mode.value || (mode.value === 'daytrade') === r.daytrade)))

const counts = computed(() => {
  const all = reports.value ?? []
  return {
    total: all.length,
    candidates: all.filter((r) => r.verdict === 'HOLDOUT_CANDIDATE').length,
    promising: all.filter((r) => r.verdict === 'PROMISING').length,
    rejected: all.filter((r) => r.verdict === 'REJECTED').length,
  }
})
</script>

<template>
  <main class="page">
    <div class="page-header">
      <div>
        <h1>Relatórios de validação</h1>
        <p class="subtitle">Cada linha é uma execução de <code class="mono">quantlab validate</code>, com métricas <Term id="oos">fora da amostra</Term> (<Term id="walk_forward">walk-forward</Term>).</p>
      </div>
    </div>

    <div v-if="loading" class="state">Carregando…</div>
    <div v-else-if="error" class="state error">
      {{ error }}<br /><span class="muted">A API está rodando? <code class="mono">uv run quantlab serve</code></span>
    </div>
    <template v-else>
      <div class="tiles">
        <div class="card tile"><div class="muted">Estratégias testadas</div><div class="big">{{ counts.total }}</div></div>
        <div class="card tile"><div class="muted"><Term id="verdict_holdout">Candidatas ao holdout</Term></div><div class="big pos">{{ counts.candidates }}</div></div>
        <div class="card tile"><div class="muted"><Term id="verdict_promising">Promissoras</Term></div><div class="big" style="color: var(--warning)">{{ counts.promising }}</div></div>
        <div class="card tile"><div class="muted"><Term id="verdict_rejected">Rejeitadas</Term></div><div class="big neg">{{ counts.rejected }}</div></div>
      </div>

      <div class="filters">
        <select v-model="dataset" aria-label="Dataset">
          <option value="">Todos os datasets</option>
          <option v-for="d in datasets" :key="d" :value="d">{{ d }}</option>
        </select>
        <select v-model="verdict" aria-label="Veredito">
          <option value="">Todos os vereditos</option>
          <option value="HOLDOUT_CANDIDATE">Candidata ao holdout</option>
          <option value="PROMISING">Promissora</option>
          <option value="REJECTED">Rejeitada</option>
        </select>
        <select v-model="mode" aria-label="Modo">
          <option value="">Day trade e swing</option>
          <option value="daytrade">Day trade</option>
          <option value="swing">Swing</option>
        </select>
      </div>

      <div class="card table-wrap" style="padding: 0">
        <table>
          <thead>
            <tr>
              <th>Estratégia</th><th><Term id="dataset">Dataset</Term></th><th>Veredito</th>
              <th class="num"><Term id="sharpe">Sharpe</Term> <Term id="oos">OOS</Term></th>
              <th class="num"><Term id="dsr">Deflated Sharpe</Term></th>
              <th class="num"><Term id="trade">Trades</Term></th><th class="num"><Term id="drawdown">Max DD</Term></th>
              <th class="num"><Term id="pnl">P&amp;L</Term></th><th>Data</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in filtered" :key="r.id" class="clickable" @click="router.push(`/reports/${r.id}`)">
              <td>
                <RouterLink :to="`/reports/${r.id}`" @click.stop>{{ r.title }}</RouterLink>
                <div class="muted small">{{ r.daytrade ? 'Day trade' : 'Swing trade' }} · <span class="mono">{{ r.strategy }}</span></div>
              </td>
              <td class="mono">{{ r.dataset }}</td>
              <td>
                <VerdictBadge :verdict="r.verdict" />
                <div v-if="r.validator_verdict" class="muted small">validador: {{ r.validator_verdict }}</div>
              </td>
              <td class="num" :class="r.sharpe >= 0 ? 'pos' : 'neg'">{{ num(r.sharpe) }}</td>
              <td class="num" :class="{ pos: r.deflated_sharpe >= 0.95 }">{{ pct(r.deflated_sharpe) }}</td>
              <td class="num">{{ r.trades }}</td>
              <td class="num neg">{{ pct(r.max_drawdown) }}</td>
              <td class="num" :class="r.total_pnl >= 0 ? 'pos' : 'neg'">{{ brl(r.total_pnl) }}</td>
              <td class="muted small nowrap">{{ dateTime(r.created) }}</td>
            </tr>
            <tr v-if="!filtered.length"><td colspan="9" class="state">Nenhum relatório com esses filtros.</td></tr>
          </tbody>
        </table>
      </div>
    </template>
  </main>
</template>

<style scoped>
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; margin-bottom: 20px; }
.tile .big { font-size: 26px; font-weight: 700; margin-top: 2px; font-variant-numeric: tabular-nums; }
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.small { font-size: 12px; }
.nowrap { white-space: nowrap; }
</style>
