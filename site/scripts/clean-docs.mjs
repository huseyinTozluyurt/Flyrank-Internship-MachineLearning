// Remove only the files a previous `vite build` wrote into docs/, so the
// guides, PDF and paper images that also live there are left untouched.
import { rmSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const docs = fileURLToPath(new URL('../../docs/', import.meta.url))
for (const path of ['assets', 'figures', 'index.html']) {
  rmSync(docs + path, { recursive: true, force: true })
}
