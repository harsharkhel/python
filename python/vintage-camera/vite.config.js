import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  // Optimize MediaPipe WASM loading
  optimizeDeps: {
    exclude: ['@mediapipe/tasks-vision'],
  },
})
