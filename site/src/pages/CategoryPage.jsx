import { useParams } from 'react-router-dom'
import { categories, groupModules } from '../content/index.js'
import ModuleCard from '../components/ModuleCard.jsx'
import NotFound from './NotFound.jsx'

export default function CategoryPage() {
  const { id } = useParams()
  const c = categories.find((x) => x.id === id)
  if (!c) return <NotFound />
  return (
    <article className="page">
      <header className="page-head">
        <p className="eyebrow">Category</p>
        <h1>{c.title}</h1>
        <p className="lede">{c.blurb}</p>
      </header>
      {groupModules(c.modules).map((g) => (
        <section key={g.name || 'main'}>
          {g.name && <h2 className="group-title">{g.name}</h2>}
          <div className="grid">
            {g.modules.map((m) => <ModuleCard key={m.slug} m={m} />)}
          </div>
        </section>
      ))}
    </article>
  )
}
