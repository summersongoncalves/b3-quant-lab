<script setup lang="ts">
const links = [
  { to: '/', label: 'Relatórios' },
  { to: '/hypotheses', label: 'Hipóteses' },
  { to: '/cycles', label: 'Ciclos' },
  { to: '/datasets', label: 'Dados' },
  { to: '/glossario', label: 'Glossário' },
]
</script>

<template>
  <header class="topbar">
    <div class="topbar-inner">
      <RouterLink to="/" class="brand">Quant Lab <span>B3</span></RouterLink>
      <nav>
        <RouterLink v-for="l in links" :key="l.to" :to="l.to"
          :class="{ active: l.to === '/' ? $route.path === '/' || $route.path.startsWith('/reports') : $route.path.startsWith(l.to) }">
          {{ l.label }}
        </RouterLink>
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped>
.topbar { background: var(--surface); border-bottom: 1px solid var(--border); position: sticky; top: 0; z-index: 10; }
.topbar-inner { max-width: 1200px; margin: 0 auto; padding: 0 16px; display: flex; align-items: center; gap: 24px; height: 52px; }
.brand { font-weight: 700; color: var(--text); white-space: nowrap; }
.brand span { color: var(--accent); }
.brand:hover { text-decoration: none; }
nav { display: flex; gap: 4px; overflow-x: auto; }
nav a { color: var(--text-muted); padding: 6px 10px; border-radius: 6px; white-space: nowrap; }
nav a:hover { color: var(--text); background: var(--surface-2); text-decoration: none; }
nav a.active { color: var(--text); background: var(--surface-2); font-weight: 500; }
</style>
