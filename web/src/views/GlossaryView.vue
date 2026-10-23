<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { CATEGORIES, GLOSSARY } from '../glossary'

const route = useRoute()
const query = ref('')

// Accent-insensitive search over the term, its translation and the explanation.
const fold = (s: string) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()

const groups = computed(() => {
  const q = fold(query.value.trim())
  const match = GLOSSARY.filter((e) => !q || fold(`${e.term} ${e.pt ?? ''} ${e.short} ${e.long ?? ''}`).includes(q))
  return CATEGORIES.map((c) => ({
    category: c,
    entries: match.filter((e) => e.category === c).sort((a, b) => a.term.localeCompare(b.term, 'pt-BR')),
  })).filter((g) => g.entries.length)
})

const selected = computed(() => route.hash.slice(1))

async function scrollToHash() {
  await nextTick()
  if (selected.value) document.getElementById(selected.value)?.scrollIntoView({ block: 'center' })
}
onMounted(scrollToHash)
watch(selected, () => {
  query.value = ''
  scrollToHash()
})
</script>

<template>
  <main class="page">
    <div class="page-header">
      <div>
        <h1>Glossário</h1>
        <p class="subtitle">Os termos (a maioria em inglês) que aparecem nos relatórios, explicados de forma simples. Passe o mouse sobre um termo sublinhado em qualquer tela para ver o resumo.</p>
      </div>
    </div>

    <input v-model="query" type="search" class="search" placeholder="Buscar termo… (ex.: sharpe, custos, vwap)" aria-label="Buscar termo" />

    <section v-for="g in groups" :key="g.category" class="group">
      <h2>{{ g.category }}</h2>
      <dl class="card entries">
        <div v-for="e in g.entries" :id="e.id" :key="e.id" class="entry" :class="{ selected: e.id === selected }">
          <dt>
            <RouterLink :to="`/glossario#${e.id}`" class="term">{{ e.term }}</RouterLink>
            <span v-if="e.pt" class="muted pt">{{ e.pt }}</span>
          </dt>
          <dd>
            <p>{{ e.short }}</p>
            <p v-if="e.long" class="muted">{{ e.long }}</p>
          </dd>
        </div>
      </dl>
    </section>
    <p v-if="!groups.length" class="state">Nenhum termo encontrado.</p>
  </main>
</template>

<style scoped>
.search { width: 100%; max-width: 420px; margin-bottom: 20px; }
.group { margin-bottom: 24px; }
.entries { margin: 0; padding: 0; }
.entry { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 4px 20px; padding: 12px 16px; border-bottom: 1px solid var(--border); scroll-margin-top: 70px; }
.entry:last-child { border-bottom: none; }
.entry.selected { background: var(--warning-bg); }
dt { display: flex; flex-direction: column; }
.term { font-weight: 600; color: var(--text); }
.pt { font-size: 12px; }
dd { margin: 0; }
dd p { margin: 0 0 4px; }
@media (max-width: 640px) {
  .entry { grid-template-columns: 1fr; }
}
</style>
