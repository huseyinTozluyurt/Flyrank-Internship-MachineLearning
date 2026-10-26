import { NavLink } from 'react-router-dom'
import { categories, groupModules } from '../content/index.js'

export default function Sidebar({ open, onNavigate }) {
  return (
    <nav className={`sidebar${open ? ' open' : ''}`} aria-label="Modules">
      <NavLink to="/" end onClick={onNavigate} className="side-top">Overview</NavLink>
      <NavLink to="/paper" onClick={onNavigate} className="side-top">Capstone paper</NavLink>
      {categories.map((c) => (
        <div key={c.id} className="side-cat">
          <NavLink to={`/category/${c.id}`} onClick={onNavigate} className="side-cat-title">{c.title}</NavLink>
          {groupModules(c.modules).map((g) => (
            <div key={g.name || 'main'} className="side-group">
              {g.name && <div className="side-group-title">{g.name}</div>}
              <ul>
                {g.modules.map((m) => (
                  <li key={m.slug}>
                    <NavLink to={`/modules/${m.slug}`} onClick={onNavigate}>{m.title}</NavLink>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </nav>
  )
}
