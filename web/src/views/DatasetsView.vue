<script setup lang="ts">
import { api } from '../api'
import { useAsync } from '../useAsync'
import { date } from '../format'
import Term from '../components/Term.vue'

const datasets = useAsync(api.datasets)
const strategies = useAsync(api.strategies)

// Share of the dataset's time span that is in the frozen holdout.
function holdoutShare(d: { start: string; end: string; holdout_start: string | null }) {
  if (!d.holdout_start) return 0
  const s = +new Date(d.start), e = +new Date(d.end), h = +new Date(d.holdout_start)
  return Math.max(0, Math.min(1, (e - h) / (e - s)))
}
</script>

<template>
  <main class="page">
    <div class="page-header">
      <div>
        <h1>Dados e estratégias</h1>
        <p class="subtitle">Datasets baixados do MT5. A parte final (<Term id="holdout">holdout</Term>) fica trancada para o teste final.</p>
      </div>
    </div>

    <section class="card table-wrap" style="padding: 0">
      <div v-if="datasets.loading.value" class="state">Carregando…</div>
      <div v-else-if="datasets.error.value" class="state error">{{ datasets.error.value }}</div>
      <table v-else>
        <thead>
          <tr>
            <th><Term id="dataset">Dataset</Term></th><th class="num"><Term id="bar">Barras</Term></th><th>Período</th>
            <th>Pesquisa | <Term id="holdout">holdout</Term></th><th class="num"><Term id="trials">Tentativas</Term></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="d in datasets.data.value ?? []" :key="d.id">
            <td class="mono">{{ d.id }}</td>
            <td class="num">{{ d.bars.toLocaleString('pt-BR') }}</td>
            <td class="nowrap">{{ date(d.start) }} → {{ date(d.end) }}</td>
            <td>
              <div class="bar" :title="`Holdout desde ${d.holdout_start ? date(d.holdout_start) : '—'}`">
                <div class="holdout" :style="{ width: `${holdoutShare(d) * 100}%` }" />
              </div>
              <div class="muted small">holdout desde {{ d.holdout_start ? date(d.holdout_start) : '—' }}</div>
            </td>
            <td class="num">{{ d.trials }}</td>
          </tr>
        </tbody>
      </table>
    </section>
    <p class="muted small">Tentativas = configurações já avaliadas no dataset. Quanto mais, mais alto o <Term id="dsr">Deflated Sharpe</Term> exigido.</p>

    <h2 style="margin-top: 28px">Estratégias implementadas</h2>
    <section class="card table-wrap" style="padding: 0">
      <table>
        <thead><tr><th>Nome</th><th>Modo</th><th><Term id="timeframe">Timeframe</Term></th><th><Term id="grid">Grade</Term></th></tr></thead>
        <tbody>
          <tr v-for="s in strategies.data.value ?? []" :key="s.name">
            <td>
              <div><strong>{{ s.title }}</strong> <span class="mono muted">{{ s.name }}</span></div>
              <div class="muted small">{{ s.summary || s.description }}</div>
            </td>
            <td class="nowrap"><Term :id="s.daytrade ? 'daytrade' : 'swing'">{{ s.daytrade ? 'Day trade' : 'Swing trade' }}</Term></td>
            <td class="mono">{{ s.timeframe }}</td>
            <td class="mono small">
              <div v-for="(values, key) in s.grid" :key="key"><Term :text="s.param_help[key]">{{ key }}</Term>: {{ values.join(', ') }}</div>
            </td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<style scoped>
.bar { height: 8px; min-width: 160px; border-radius: 4px; background: var(--accent); opacity: 0.85; overflow: hidden; display: flex; justify-content: flex-end; }
.holdout { background: repeating-linear-gradient(45deg, var(--text-muted), var(--text-muted) 3px, var(--surface-2) 3px, var(--surface-2) 6px); }
.small { font-size: 12px; }
.nowrap { white-space: nowrap; }
</style>
