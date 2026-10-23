import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './style.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: () => import('./views/ReportsView.vue') },
    { path: '/reports/:id', component: () => import('./views/ReportDetailView.vue'), props: true },
    { path: '/hypotheses/:id?', component: () => import('./views/HypothesesView.vue'), props: true },
    { path: '/cycles/:id?', component: () => import('./views/CyclesView.vue'), props: true },
    { path: '/datasets', component: () => import('./views/DatasetsView.vue') },
    { path: '/glossario', component: () => import('./views/GlossaryView.vue') },
  ],
  scrollBehavior: (to, from) => (to.hash || to.path === from.path ? undefined : { top: 0 }),
})

createApp(App).use(router).mount('#app')
