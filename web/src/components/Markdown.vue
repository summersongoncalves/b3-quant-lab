<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import { repoPath, routeFor } from '../links'

// `path` is the document's repo-relative path, used to resolve its relative links.
const props = defineProps<{ source: string; path?: string }>()
const router = useRouter()

// Files come from local agents, but sanitize anyway: markdown can carry raw HTML.
const html = computed(() => {
  const clean = DOMPurify.sanitize(marked.parse(props.source, { async: false }))
  if (!props.path) return clean
  const tpl = document.createElement('template')
  tpl.innerHTML = clean
  for (const a of tpl.content.querySelectorAll('a[href]')) {
    const target = repoPath(a.getAttribute('href')!, props.path)
    if (target) a.setAttribute('href', routeFor(target))
  }
  return tpl.innerHTML
})

// Internal links go through the router instead of reloading the page.
function onClick(e: MouseEvent) {
  const a = (e.target as HTMLElement).closest('a')
  const href = a?.getAttribute('href')
  if (!href?.startsWith('/') || e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return
  e.preventDefault()
  router.push(href)
}
</script>

<template>
  <div class="markdown" v-html="html" @click="onClick" />
</template>
