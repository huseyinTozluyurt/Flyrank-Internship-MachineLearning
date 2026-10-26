import { analysis } from './analysis.js'
import { ml } from './ml.js'
import { track } from './track.js'

export const REPO = 'https://github.com/huseyinTozluyurt/Flyrank-Internship-MachineLearning'
export const githubUrl = (path) => `${REPO}/blob/main/${path}`
export const colabUrl = (path) =>
  `https://colab.research.google.com/github/huseyinTozluyurt/Flyrank-Internship-MachineLearning/blob/main/${path}`

export const categories = [
  {
    id: 'analysis',
    title: 'Data Analysis',
    blurb: 'Exploring the data before modeling: distributions, missing values, segments, structure and anomalies.',
    modules: analysis,
  },
  {
    id: 'ml',
    title: 'ML Modules',
    blurb: 'Supervised models and the staged Content Refresh Recommendation Engine, each evaluated on held-out clients.',
    modules: ml,
  },
  {
    id: 'track',
    title: 'Internship track',
    blurb: 'The weekly ML assignments and capstone milestones, from research question to the final capstone notebook.',
    modules: track,
  },
]

export const allModules = categories.flatMap((c) =>
  c.modules.map((m) => ({ ...m, category: c.id, categoryTitle: c.title })),
)

export const bySlug = Object.fromEntries(allModules.map((m) => [m.slug, m]))

// Groups modules within a category, keeping the order of first appearance.
export function groupModules(modules) {
  const groups = []
  for (const m of modules) {
    const name = m.group || null
    let g = groups.find((x) => x.name === name)
    if (!g) groups.push((g = { name, modules: [] }))
    g.modules.push(m)
  }
  return groups
}
