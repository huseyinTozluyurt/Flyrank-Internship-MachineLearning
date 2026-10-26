import { Link } from 'react-router-dom'
import Inline from './Inline.jsx'

export default function ModuleCard({ m }) {
  return (
    <Link to={`/modules/${m.slug}`} className="card">
      <h3>{m.title}</h3>
      <p><Inline text={m.short} /></p>
      <div className="card-meta">
        {m.figures?.length ? `${m.figures.length} figure${m.figures.length > 1 ? 's' : ''} · ` : ''}
        {m.pipeline.length} steps
      </div>
    </Link>
  )
}
