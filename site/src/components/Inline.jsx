import { Link } from 'react-router-dom'

// Renders a small subset of inline markdown: `code`, **bold** and [text](url).
const TOKEN = /(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))/g

export default function Inline({ text }) {
  if (!text) return null
  return text.split(TOKEN).map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`')) return <code key={i}>{part.slice(1, -1)}</code>
    if (part.startsWith('**') && part.endsWith('**')) return <strong key={i}>{part.slice(2, -2)}</strong>
    const link = part.match(/^\[([^\]]+)\]\(([^)]+)\)$/)
    if (link) {
      const [, label, href] = link
      if (href.startsWith('#/')) return <Link key={i} to={href.slice(1)}>{label}</Link>
      return <a key={i} href={href} target="_blank" rel="noreferrer">{label}</a>
    }
    return part
  })
}
