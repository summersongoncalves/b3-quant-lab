import { ref, watchEffect, type Ref } from 'vue'

/** Runs `loader` (again whenever its reactive inputs change) and tracks loading/error state. */
export function useAsync<T>(loader: () => Promise<T>) {
  const data = ref<T | null>(null) as Ref<T | null>
  const error = ref<string | null>(null)
  const loading = ref(true)

  watchEffect(async (onCleanup) => {
    let cancelled = false
    onCleanup(() => (cancelled = true))
    loading.value = true
    error.value = null
    try {
      const result = await loader()
      if (!cancelled) data.value = result
    } catch (e) {
      if (!cancelled) error.value = e instanceof Error ? e.message : String(e)
    } finally {
      if (!cancelled) loading.value = false
    }
  })

  return { data, error, loading }
}
