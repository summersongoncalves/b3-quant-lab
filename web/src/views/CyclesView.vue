<script setup lang="ts">
import { api } from '../api'
import { useAsync } from '../useAsync'
import DocBrowser from '../components/DocBrowser.vue'

defineProps<{ id?: string }>()
const { data: items, error, loading } = useAsync(api.cycles)
</script>

<template>
  <main class="page">
    <div class="page-header">
      <div>
        <h1>Ciclos de pesquisa</h1>
        <p class="subtitle">Resumo de cada execução do <code class="mono">/ciclo</code>, em <code class="mono">reports/ciclos/</code>.</p>
      </div>
    </div>
    <div v-if="loading" class="state">Carregando…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <DocBrowser v-else :items="items ?? []" :selected="id" base-path="/cycles" :load="api.cycle"
      :doc-path="(id) => `reports/ciclos/${id}.md`"
      empty="Nenhum ciclo rodado ainda. No Claude Code, dentro do projeto: /ciclo WIN$N M5 3 daytrade" />
  </main>
</template>
