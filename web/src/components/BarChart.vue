<script setup lang="ts">
import { computed } from 'vue'
import { Bar } from 'vue-chartjs'
import { baseOptions } from '../charts'
import { cssVar } from '../format'

// Bars are colored by sign of `signs` (defaults to the values themselves).
const props = defineProps<{
  labels: string[]; values: number[]; format: (v: number) => string; signs?: number[]; height?: number
}>()

const data = computed(() => ({
  labels: props.labels,
  datasets: [{
    data: props.values,
    backgroundColor: (props.signs ?? props.values).map((v) => cssVar(v >= 0 ? '--positive' : '--negative')),
    borderRadius: 3,
    maxBarThickness: 40,
  }],
}))

const options = computed(() => {
  const o = baseOptions<'bar'>()
  o.plugins!.tooltip = { callbacks: { label: (item) => props.format(item.parsed.y ?? 0) } }
  o.scales!.y!.ticks = { callback: (v) => props.format(Number(v)), maxTicksLimit: 5 }
  return o
})
</script>

<template>
  <div :style="{ height: `${height ?? 180}px` }"><Bar :data="data" :options="options" /></div>
</template>
