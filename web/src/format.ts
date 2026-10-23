const brlFormatter = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL', maximumFractionDigits: 0 })

export const brl = (v: number) => brlFormatter.format(v)
export const pct = (v: number, digits = 1) => `${(v * 100).toFixed(digits).replace('.', ',')}%`
export const num = (v: number, digits = 2) =>
  Number.isFinite(v) ? v.toFixed(digits).replace('.', ',') : '∞'
// A bare 'YYYY-MM-DD' parses as UTC midnight, which is the previous day in Brazil.
export const date = (iso: string) =>
  new Date(iso.length === 10 ? `${iso}T00:00` : iso).toLocaleDateString('pt-BR')
export const dateTime = (iso: string) =>
  new Date(iso).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' })
export const params = (p: Record<string, unknown>) =>
  Object.entries(p).map(([k, v]) => `${k}=${v}`).join(' · ')

/** Reads a CSS custom property so charts follow the light/dark theme. */
export const cssVar = (name: string) => getComputedStyle(document.documentElement).getPropertyValue(name).trim()
