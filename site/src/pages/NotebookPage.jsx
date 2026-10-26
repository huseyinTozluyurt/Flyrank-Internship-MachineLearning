import { Link, useParams } from 'react-router-dom'
import { allModules, bySlug, colabUrl, githubUrl } from '../content/index.js'
import Figure from '../components/Figure.jsx'
import Inline from '../components/Inline.jsx'
import NotFound from './NotFound.jsx'

export default function NotebookPage() {
  const { slug } = useParams()
  const m = bySlug[slug]
  if (!m) return <NotFound />
  const idx = allModules.findIndex((x) => x.slug === slug)
  const prev = allModules[idx - 1]
  const next = allModules[idx + 1]
  const related = (m.related || []).map((s) => bySlug[s]).filter(Boolean)

  return (
    <article className="page module">
      <header className="page-head">
        <p className="eyebrow">
          <Link to={`/category/${m.category}`}>{m.categoryTitle}</Link>
          {m.group && <> · {m.group}</>}
        </p>
        <h1>{m.title}</h1>
        <p className="lede"><Inline text={m.summary} /></p>
        <div className="tags">
          {m.methods.map((t) => <span key={t} className="tag">{t}</span>)}
        </div>
      </header>

      <section className="meta-box">
        <div>
          <h4>Notebook{m.notebooks.length > 1 ? 's' : ''}</h4>
          <ul className="nb-list">
            {m.notebooks.map((p) => (
              <li key={p}>
                <code>{p}</code>
                <span className="nb-links">
                  <a href={githubUrl(p)} target="_blank" rel="noreferrer">GitHub</a>
                  <a href={colabUrl(p)} target="_blank" rel="noreferrer">Colab</a>
                </span>
              </li>
            ))}
          </ul>
        </div>
        <div>
          <h4>Data</h4>
          <p>{m.data}</p>
          <h4>Question</h4>
          <p><Inline text={m.question} /></p>
        </div>
      </section>

      {m.stats?.length > 0 && (
        <div className="stats">
          {m.stats.map((s) => (
            <div key={s.label} className="stat"><b>{s.value}</b><span>{s.label}</span></div>
          ))}
        </div>
      )}

      <section>
        <h2>Pipeline</h2>
        <ol className="pipeline">
          {m.pipeline.map((step, i) => (
            <li key={i}>
              <span className="step-num">{i + 1}</span>
              <div>
                <h3>{step.title}</h3>
                <p><Inline text={step.text} /></p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      {m.figures?.length > 0 && (
        <section>
          <h2>Graphs and images</h2>
          <div className="figures">
            {m.figures.map((f, i) => (
              <Figure
                key={f.file || f.path}
                number={i + 1}
                src={f.path || `figures/${m.slug}/${f.file}`}
                caption={f.caption}
              />
            ))}
          </div>
        </section>
      )}

      {m.table && (
        <section>
          <h2>Results table</h2>
          <div className="table-wrap">
            <table>
              <caption>{m.table.caption}</caption>
              <thead><tr>{m.table.head.map((h) => <th key={h}>{h}</th>)}</tr></thead>
              <tbody>
                {m.table.rows.map((r, i) => (
                  <tr key={i}>{r.map((c, j) => <td key={j}>{c}</td>)}</tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}

      <section>
        <h2>Findings</h2>
        <ul className="findings">
          {m.findings.map((f, i) => <li key={i}><Inline text={f} /></li>)}
        </ul>
      </section>

      {m.trust && (
        <aside className="trust">
          <h4>How far to trust this</h4>
          <p><Inline text={m.trust} /></p>
        </aside>
      )}

      {related.length > 0 && (
        <section>
          <h2>Related pages</h2>
          <div className="related">
            {related.map((r) => <Link key={r.slug} to={`/modules/${r.slug}`}>{r.title}</Link>)}
          </div>
        </section>
      )}

      <nav className="prev-next">
        {prev ? <Link to={`/modules/${prev.slug}`}>← {prev.title}</Link> : <span />}
        {next ? <Link to={`/modules/${next.slug}`}>{next.title} →</Link> : <span />}
      </nav>
    </article>
  )
}
