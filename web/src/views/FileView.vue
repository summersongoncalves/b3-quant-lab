<script setup lang="ts">
import { computed } from 'vue'
import { api } from '../api'
import { useAsync } from '../useAsync'
import Markdown from '../components/Markdown.vue'

const props = defineProps<{ path: string | string[] }>()
const filePath = computed(() => (Array.isArray(props.path) ? props.path.join('/') : props.path))
const { data: file, error, loading } = useAsync(() => api.file(filePath.value))
</script>

<template>
  <main class="page">
    <div class="page-header">
      <div>
        <h1 class="mono path">{{ filePath }}</h1>
        <p class="subtitle">Arquivo do repositório, somente leitura.</p>
      </div>
    </div>
    <div v-if="loading" class="state">Carregando…</div>
    <div v-else-if="error" class="state error">{{ error }}</div>
    <article v-else-if="file" class="card">
      <Markdown v-if="file.kind === 'markdown'" :source="file.content" :path="file.path" />
      <pre v-else class="code"><code>{{ file.content }}</code></pre>
    </article>
  </main>
</template>

<style scoped>
.path { font-size: 16px; word-break: break-all; }
.code { margin: 0; font-family: var(--mono); font-size: 12.5px; line-height: 1.55; overflow-x: auto; white-space: pre; }
</style>
