import { useEffect, useState } from 'react'
import { Link, Route, Routes, useLocation } from 'react-router-dom'
import Sidebar from './components/Sidebar.jsx'
import Footer from './components/Footer.jsx'
import Home from './pages/Home.jsx'
import Paper from './pages/Paper.jsx'
import CategoryPage from './pages/CategoryPage.jsx'
import NotebookPage from './pages/NotebookPage.jsx'
import NotFound from './pages/NotFound.jsx'

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false)
  const { pathname } = useLocation()

  useEffect(() => {
    window.scrollTo(0, 0)
    setMenuOpen(false)
  }, [pathname])

  return (
    <div className="layout">
      <header className="topbar">
        <button className="menu-btn" onClick={() => setMenuOpen((o) => !o)} aria-label="Toggle navigation" aria-expanded={menuOpen}>
          ☰
        </button>
        <Link to="/" className="brand">FlyRank ML Internship</Link>
      </header>
      <Sidebar open={menuOpen} onNavigate={() => setMenuOpen(false)} />
      <main className="content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/paper" element={<Paper />} />
          <Route path="/category/:id" element={<CategoryPage />} />
          <Route path="/modules/:slug" element={<NotebookPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
        <Footer />
      </main>
    </div>
  )
}
