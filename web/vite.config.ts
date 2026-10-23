import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    // The Python API (`uv run quantlab serve`) owns /api.
    proxy: { '/api': 'http://127.0.0.1:8000' },
  },
})
