import { useState } from 'react'
import { NavLink, Link } from 'react-router-dom'

const navItems = [
  { to: '/', label: 'Dashboard', icon: '🏠', exact: true },
  { to: '/performance', label: 'Model Performance', icon: '📊' },
  { to: '/about', label: 'About', icon: 'ℹ️' },
]

export default function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <nav className="navbar" role="navigation" aria-label="Main navigation">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand" aria-label="Disease Prediction AI Home">
          <div className="navbar-brand-icon" aria-hidden="true">🧬</div>
          <span>Disease Prediction <span style={{ color: 'var(--clr-accent)', fontWeight: 400 }}>AI</span></span>
        </Link>

        <ul className={`navbar-nav${menuOpen ? ' open' : ''}`} role="list">
          {navItems.map(({ to, label, icon, exact }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={exact}
                className={({ isActive }) => `nav-link${isActive ? ' active' : ''}`}
                onClick={() => setMenuOpen(false)}
              >
                <span aria-hidden="true">{icon}</span>
                {label}
              </NavLink>
            </li>
          ))}
        </ul>

        <button
          className="navbar-mobile-toggle"
          aria-label="Toggle navigation menu"
          aria-expanded={menuOpen}
          onClick={() => setMenuOpen((o) => !o)}
        >
          {menuOpen ? '✕' : '☰'}
        </button>
      </div>
    </nav>
  )
}
