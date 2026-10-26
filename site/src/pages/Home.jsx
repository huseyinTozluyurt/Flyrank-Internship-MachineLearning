import { Link } from 'react-router-dom'
import { allModules, categories, groupModules } from '../content/index.js'
import ModuleCard from '../components/ModuleCard.jsx'

export default function Home() {
  const figures = allModules.reduce((n, m) => n + (m.figures?.length || 0), 0)
  const notebooks = new Set(allModules.flatMap((m) => m.notebooks)).size
  return (
    <article className="page">
      <header className="hero">
        <p className="eyebrow">FlyRank Machine Learning Internship · Hüseyin Tozluyurt</p>
        <h1>Data analysis and ML modules, one page per notebook</h1>
        <p className="lede">
          Every notebook in the repository is explained here as a pipeline: the question it asks, the steps it runs,
          the charts it produced and what the outputs actually show. The thread running through all of them is an
          exploratory ranking of pages carrying a supplied decline label, to help an editor decide which pages to
          review first.
        </p>
        <div className="stats">
          <div className="stat"><b>{allModules.length}</b><span>module pages</span></div>
          <div className="stat"><b>{notebooks}</b><span>notebooks covered</span></div>
          <div className="stat"><b>{figures}</b><span>figures from saved outputs</span></div>
          <div className="stat"><b>30,000</b><span>pages in the starter CSV</span></div>
        </div>
        <div className="hero-actions">
          <Link className="btn primary" to="/paper">Read the capstone paper</Link>
          <Link className="btn" to="/category/analysis">Start with the data analysis</Link>
        </div>
      </header>

      <section className="callout">
        <h2>How to read these pages</h2>
        <ul>
          <li>Each page lists its notebook(s) with links to GitHub and Colab, the data it used, a numbered pipeline, figures and findings.</li>
          <li>Numbers come from the notebooks' saved outputs. Where two notebooks report different figures for the same idea, the page says so.</li>
          <li>Review queues are review candidates and reason codes are prompts for an editor, not causes. Nothing here is evidence that editing a page improves its traffic.</li>
          <li>Charts that identify individual clients are left out.</li>
        </ul>
      </section>

      {categories.map((c) => (
        <section key={c.id} className="home-cat">
          <div className="section-head">
            <h2><Link to={`/category/${c.id}`}>{c.title}</Link></h2>
            <p>{c.blurb}</p>
          </div>
          {groupModules(c.modules).map((g) => (
            <div key={g.name || 'main'}>
              {g.name && <h3 className="group-title">{g.name}</h3>}
              <div className="grid">
                {g.modules.map((m) => <ModuleCard key={m.slug} m={m} />)}
              </div>
            </div>
          ))}
        </section>
      ))}
    </article>
  )
}
