import { useEffect, useRef } from 'react'
import paperHtml from '../content/paper.html?raw'

export default function Paper() {
  const ref = useRef(null)

  // The router owns the URL hash, so in-page "#section" links scroll instead of navigating.
  useEffect(() => {
    const el = ref.current
    const onClick = (e) => {
      const a = e.target.closest('a')
      if (!a) return
      const href = a.getAttribute('href') || ''
      if (href.startsWith('#') && !href.startsWith('#/')) {
        e.preventDefault()
        document.getElementById(decodeURIComponent(href.slice(1)))?.scrollIntoView({ behavior: 'smooth' })
      }
    }
    el.addEventListener('click', onClick)
    return () => el.removeEventListener('click', onClick)
  }, [])

  return (
    <article className="page paper">
      <header className="page-head">
        <p className="eyebrow">Capstone paper</p>
        <h1>Which content pages should an editor review first?</h1>
      </header>
      <div ref={ref} className="paper-body" dangerouslySetInnerHTML={{ __html: paperHtml }} />
    </article>
  )
}
