import { useEffect, useState } from 'react'

export default function Figure({ src, caption, number }) {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    if (!open) return
    const onKey = (e) => e.key === 'Escape' && setOpen(false)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [open])

  return (
    <figure className="figure">
      <button className="figure-img" onClick={() => setOpen(true)} aria-label={`Enlarge figure ${number}`}>
        <img src={src} alt={caption} loading="lazy" />
      </button>
      <figcaption>
        <span className="fig-num">Figure {number}.</span> {caption}
      </figcaption>
      {open && (
        <div className="lightbox" role="dialog" aria-modal="true" onClick={() => setOpen(false)}>
          <img src={src} alt={caption} />
          <p>{caption}</p>
          <button className="lightbox-close" aria-label="Close">×</button>
        </div>
      )}
    </figure>
  )
}
