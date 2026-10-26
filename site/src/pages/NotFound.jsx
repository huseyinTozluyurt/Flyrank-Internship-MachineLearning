import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <article className="page">
      <h1>Page not found</h1>
      <p>That page does not exist. <Link to="/">Back to the overview</Link>.</p>
    </article>
  )
}
