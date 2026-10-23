<script setup lang="ts">
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'
import { baseOptions } from '../charts'
import { brl, cssVar } from '../format'

const props = defineProps<{ dates: string[]; pnl: number[]; drawdown: number[] }>()

const labels = computed(() =>
  props.dates.map((d) => new Date(d + 'T00:00').toLocaleDateString('pt-BR', { month: 'short', year: '2-digit' })))

function opts(title: string): ChartOptions<'line'> {
  const o = baseOptions<'line'>()
  o.plugins!.tooltip = {
    callbacks: {
      title: (items) => new Date(props.dates[items[0].dataIndex] + 'T00:00').toLocaleDateString('pt-BR'),
      label: (item) => `${title}: ${brl(item.parsed.y ?? 0)}`,
    },
  }
  o.scales!.y!.ticks = { callback: (v) => brl(Number(v)), maxTicksLimit: 5 }
  return o
}

const equity = computed(() => ({
  labels: labels.value,
  datasets: [{ data: props.pnl, borderColor: cssVar('--chart-line'), borderWidth: 1.6, pointRadius: 0, tension: 0 }],
}))
const drawdown = computed(() => ({
  labels: labels.value,
  datasets: [{
    data: props.drawdown, borderColor: cssVar('--chart-dd'), backgroundColor: cssVar('--chart-dd') + '33',
    fill: 'origin', borderWidth: 1, pointRadius: 0, tension: 0,
  }],
}))
const equityOpts = opts('P&L acumulado')
const ddOpts = opts('Drawdown')
ddOpts.scales!.x!.display = false
</script>

<template>
  <div class="equity">
    <div class="main"><Line :data="equity" :options="equityOpts" /></div>
    <div class="dd-label muted">Drawdown</div>
    <div class="dd"><Line :data="drawdown" :options="ddOpts" /></div>
  </div>
</template>

<style scoped>
.main { height: 280px; }
.dd { height: 100px; }
.dd-label { font-size: 12px; margin: 8px 0 2px; }
</style>
