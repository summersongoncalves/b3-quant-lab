<script setup lang="ts">
import { computed } from 'vue'
import type { Report } from '../api'
import { num, params as fmtParams } from '../format'
import Term from './Term.vue'

// Sharpe of every grid combination. With two varying params it is drawn as a
// matrix: a robust strategy shows a smooth area of positive cells, an overfit
// one shows a single bright cell among bad neighbors.
const props = defineProps<{ grid: Report['grid']; paramHelp?: Record<string, string> }>()

const varying = computed(() => {
  const keys = Object.keys(props.grid[0]?.params ?? {})
  return keys.filter((k) => new Set(props.grid.map((g) => String(g.params[k]))).size > 1)
})

const matrix = computed(() => {
  if (varying.value.length !== 2) return null
  const [rowKey, colKey] = varying.value
  const uniq = (k: string) => [...new Set(props.grid.map((g) => String(g.params[k])))]
  const rows = uniq(rowKey)
  const cols = uniq(colKey)
  const cell = (r: string, c: string) =>
    props.grid.find((g) => String(g.params[rowKey]) === r && String(g.params[colKey]) === c)
  return { rowKey, colKey, rows, cols, cell }
})

const maxAbs = computed(() => Math.max(0.5, ...props.grid.map((g) => Math.abs(g.sharpe))))

function cellStyle(sharpe: number) {
  const alpha = Math.min(1, Math.abs(sharpe) / maxAbs.value) * 0.55 + 0.08
  const color = sharpe >= 0 ? 'var(--positive)' : 'var(--negative)'
  return { background: `color-mix(in srgb, ${color} ${Math.round(alpha * 100)}%, transparent)` }
}
</script>

<template>
  <div class="table-wrap">
    <table v-if="matrix" class="heat">
      <thead>
        <tr>
          <th>
            <Term :text="paramHelp?.[matrix.rowKey]">{{ matrix.rowKey }}</Term> ↓ ·
            <Term :text="paramHelp?.[matrix.colKey]">{{ matrix.colKey }}</Term> →
          </th>
          <th v-for="c in matrix.cols" :key="c" class="num">{{ c }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in matrix.rows" :key="r">
          <th class="mono">{{ r }}</th>
          <td v-for="c in matrix.cols" :key="c" class="num">
            <template v-if="matrix.cell(r, c)">
              <span class="cell" :style="cellStyle(matrix.cell(r, c)!.sharpe)">{{ num(matrix.cell(r, c)!.sharpe) }}</span>
              <div class="muted small">{{ matrix.cell(r, c)!.trades }} trades</div>
            </template>
          </td>
        </tr>
      </tbody>
    </table>
    <table v-else>
      <thead><tr><th><Term id="params">Parâmetros</Term></th><th class="num"><Term id="sharpe">Sharpe</Term></th><th class="num"><Term id="trade">Trades</Term></th></tr></thead>
      <tbody>
        <tr v-for="(g, i) in grid" :key="i">
          <td class="mono">{{ fmtParams(g.params) }}</td>
          <td class="num"><span class="cell" :style="cellStyle(g.sharpe)">{{ num(g.sharpe) }}</span></td>
          <td class="num">{{ g.trades }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.heat th:first-child { white-space: nowrap; }
.cell { display: inline-block; min-width: 52px; padding: 4px 8px; border-radius: 6px; font-weight: 600; text-align: center; }
.small { font-size: 11px; }
</style>
