<script setup lang="ts">
import { computed } from 'vue'
import Term from './Term.vue'

// Accepts the automatic verdict (English enum) or the validator's (Portuguese text).
const props = defineProps<{ verdict: string; big?: boolean }>()

const view = computed(() => {
  const v = props.verdict.toUpperCase()
  if (v.includes('REJEIT') || v.includes('REJECT')) return { label: 'Rejeitada', tone: 'neg', term: 'verdict_rejected' }
  if (v.includes('HOLDOUT')) return { label: 'Candidata ao holdout', tone: 'pos', term: 'verdict_holdout' }
  if (v.includes('PROMIS')) return { label: 'Promissora', tone: 'warn', term: 'verdict_promising' }
  return { label: props.verdict, tone: 'neutral', term: undefined }
})
</script>

<template>
  <Term v-if="view.term" :id="view.term" bare><span class="badge" :class="[view.tone, { big }]">{{ view.label }}</span></Term>
  <span v-else class="badge" :class="[view.tone, { big }]">{{ view.label }}</span>
</template>

<style scoped>
.badge { display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 12px; font-weight: 600; white-space: nowrap; }
.badge.big { font-size: 13px; padding: 4px 12px; }
.pos { color: var(--positive); background: var(--positive-bg); }
.neg { color: var(--negative); background: var(--negative-bg); }
.warn { color: var(--warning); background: var(--warning-bg); }
.neutral { color: var(--text-muted); background: var(--surface-2); }
</style>
