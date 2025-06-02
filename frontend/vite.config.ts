import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  css: {
    postcss: './postcss.config.js'
  },
  server: {
    watch: {
      usePolling: true
    },
    host: '0.0.0.0', // Allow connections from all IPs
    port: 5173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://api:8000',  // Use the service name from docker-compose
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        secure: false
      }
    }
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
