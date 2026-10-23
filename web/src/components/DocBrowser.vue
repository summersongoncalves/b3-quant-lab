<script setup lang="ts" generic="T extends { id: string }">
// Two-pane list + markdown viewer shared by the hypotheses and cycles pages.
import Markdown from './Markdown.vue'
import { useAsync } from '../useAsync'

const props = defineProps<{
  items: T[]
  selected?: string
  basePath: string
  load: (id: string) => Promise<{ markdown: string }>
  empty: string
}>()

const doc = useAsync(async () => (props.selected ? props.load(props.selected) : null))
</script>

<template>
  <div v-if="!items.length" class="card state">{{ empty }}</div>
  <div v-else class="browser">
    <aside class="card list">
      <RouterLink v-for="item in items" :key="item.id" :to="`${basePath}/${item.id}`"
        class="item" :class="{ active: item.id === selected }">
        <slot name="item" :item="item">{{ item.id }}</slot>
      </RouterLink>
    </aside>
    <article class="card doc">
      <div v-if="!selected" class="state">Selecione um item.</div>
      <div v-else-if="doc.loading.value" class="state">Carregando…</div>
      <div v-else-if="doc.error.value" class="state error">{{ doc.error.value }}</div>
      <Markdown v-else-if="doc.data.value" :source="doc.data.value.markdown" />
    </article>
  </div>
</template>

<style scoped>
.browser { display: grid; grid-template-columns: minmax(0, 300px) minmax(0, 1fr); gap: 16px; align-items: start; }
.list { padding: 6px; display: grid; gap: 2px; max-height: calc(100vh - 160px); overflow-y: auto; }
.item { display: block; padding: 8px 10px; border-radius: 6px; color: var(--text); }
.item:hover { background: var(--surface-2); text-decoration: none; }
.item.active { background: var(--surface-2); box-shadow: inset 3px 0 0 var(--accent); }
.doc { min-height: 300px; }
@media (max-width: 760px) { .browser { grid-template-columns: 1fr; } }
</style>
