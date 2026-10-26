import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages serves main:/docs at /Flyrank-Internship-MachineLearning/.
// A relative base plus HashRouter keeps every route working without a 404 fallback.
export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: '../docs',
    // docs/ also holds the repo's markdown guides and the research PDF; keep them.
    emptyOutDir: false,
    assetsDir: 'assets',
  },
})
