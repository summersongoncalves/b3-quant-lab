<script setup lang="ts">
import { api } from '../api'
import { useAsync } from '../useAsync'
import DocBrowser from '../components/DocBrowser.vue'
import VerdictBadge from '../components/VerdictBadge.vue'

defineProps<{ id?: string }>()
const { data: items, error, loading } = useAsync(api.hypotheses)
</script>

<template>
  <main class="page">
    <div class="page-header">
      <div>
        <h1>Hipóteses</h1>
        <p class="subtitle">Propostas do agente estrategista, em <code class="mono">research/hypotheses/</code>.</p>
      </div>
    </div>
    <div v-if="loading" class="state">Carregando…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <DocBrowser v-else :items="items ?? []" :selected="id" base-path="/hypotheses" :load="api.hypothesis"
      :doc-path="(id) => `research/hypotheses/${id}.md`"
      empty="Nenhuma hipótese ainda. Rode /ciclo no Claude Code para o estrategista propor a primeira.">
      <template #item="{ item }">
        <div class="title">{{ item.title }}</div>
        <div class="meta">
          <span class="mono muted">{{ item.dataset }}</span>
          <VerdictBadge v-if="item.state" :verdict="item.state" />
        </div>
      </template>
    </DocBrowser>
  </main>
</template>

<style scoped>
.title { font-weight: 500; }
.meta { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin-top: 2px; font-size: 12px; }
</style>
