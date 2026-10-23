<script setup lang="ts">
import { computed, onBeforeUnmount, ref, useId } from 'vue'
import { BY_ID } from '../glossary'

// A label with a dotted underline that explains itself on hover, focus or tap.
// Pass `id` for a glossary entry, or `text` for a one-off explanation.
// `bare` drops the underline, for labels that already look clickable (badges).
const props = defineProps<{ id?: string; text?: string; bare?: boolean }>()
// Two root nodes (label + teleported tooltip): send class/style to the label.
defineOptions({ inheritAttrs: false })

const entry = computed(() => (props.id ? BY_ID[props.id] : undefined))
const body = computed(() => props.text ?? entry.value?.short ?? '')
const tipId = useId()

const anchor = ref<HTMLElement>()
const open = ref(false)
const pos = ref({ top: 0, left: 0, below: true })
let hideTimer: number | undefined

function show() {
  clearTimeout(hideTimer)
  if (!body.value || !anchor.value) return
  const r = anchor.value.getBoundingClientRect()
  const width = Math.min(300, window.innerWidth - 32)
  const below = r.bottom + 160 < window.innerHeight
  pos.value = {
    top: below ? r.bottom + 6 : r.top - 6,
    left: Math.max(16, Math.min(r.left + r.width / 2 - width / 2, window.innerWidth - width - 16)),
    below,
  }
  open.value = true
  window.addEventListener('scroll', close, { once: true, capture: true })
}

function close() {
  open.value = false
}

// A short delay lets the pointer move from the label onto the tooltip (to click its link).
function hide() {
  clearTimeout(hideTimer)
  hideTimer = window.setTimeout(() => (open.value = false), 120)
}

function toggle() {
  if (open.value) close()
  else show()
}

onBeforeUnmount(() => {
  clearTimeout(hideTimer)
  window.removeEventListener('scroll', close, { capture: true })
})
</script>

<template>
  <span ref="anchor" v-bind="$attrs" class="term" :class="{ bare: bare || !body, inert: !body }"
    :tabindex="body ? 0 : undefined" :role="body ? 'button' : undefined" :aria-describedby="open ? tipId : undefined"
    @mouseenter="show" @mouseleave="hide" @focus="show" @blur="hide"
    @click.stop.prevent="toggle" @keydown.esc="close">
    <slot>{{ entry?.term ?? id }}</slot>
  </span>
  <Teleport to="body">
    <div v-if="open" :id="tipId" role="tooltip" class="tip" :class="{ above: !pos.below }"
      :style="{ top: `${pos.top}px`, left: `${pos.left}px` }"
      @mouseenter="show" @mouseleave="hide">
      <div v-if="entry" class="tip-title">
        {{ entry.term }}<span v-if="entry.pt" class="tip-pt"> · {{ entry.pt }}</span>
      </div>
      <div>{{ body }}</div>
      <RouterLink v-if="entry" :to="`/glossario#${entry.id}`" class="tip-link" @click="close">
        Ver no glossário →
      </RouterLink>
    </div>
  </Teleport>
</template>

<style scoped>
.term {
  text-decoration: underline dotted var(--text-muted);
  text-underline-offset: 3px;
  cursor: help;
  border-radius: 3px;
}
.term.bare { text-decoration: none; }
.term.inert { cursor: inherit; }
.term:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.tip {
  position: fixed;
  z-index: 100;
  width: min(300px, calc(100vw - 32px));
  padding: 10px 12px;
  border-radius: 8px;
  background: var(--text);
  color: var(--bg);
  font-size: 13px;
  font-weight: 400;
  line-height: 1.45;
  text-transform: none;
  letter-spacing: normal;
  text-align: left;
  white-space: normal;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
}
.tip.above { transform: translateY(-100%); }
.tip-title { font-weight: 600; margin-bottom: 4px; }
.tip-pt { font-weight: 400; opacity: 0.75; }
.tip-link { display: inline-block; margin-top: 6px; color: inherit; opacity: 0.85; text-decoration: underline; font-size: 12px; }
</style>
