import {
  BarElement, CategoryScale, Chart, Filler, LinearScale, LineElement, PointElement, Tooltip,
  type ChartOptions,
} from 'chart.js'
import { cssVar } from './format'

Chart.register(BarElement, CategoryScale, Filler, LinearScale, LineElement, PointElement, Tooltip)

/** Shared look for every chart: theme-aware colors, no legend, thin grid. */
export function baseOptions<T extends 'line' | 'bar'>(): ChartOptions<T> {
  const grid = cssVar('--chart-grid')
  const muted = cssVar('--text-muted')
  Chart.defaults.font.family = 'Inter, system-ui, sans-serif'
  Chart.defaults.color = muted
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { display: false } },
    scales: {
      x: { grid: { display: false }, ticks: { maxTicksLimit: 8, maxRotation: 0 } },
      y: { grid: { color: grid }, border: { display: false } },
    },
  } as unknown as ChartOptions<T>
}
