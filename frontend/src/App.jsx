import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import DisclaimerBanner from './components/DisclaimerBanner'
import Dashboard from './pages/Dashboard'
import PredictPage from './pages/PredictPage'
import PerformancePage from './pages/PerformancePage'
import AboutPage from './pages/AboutPage'

export default function App() {
  return (
    <Router>
      <div className="app-shell">
        <Navbar />
        <DisclaimerBanner />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/predict/:disease" element={<PredictPage />} />
            <Route path="/performance" element={<PerformancePage />} />
            <Route path="/about" element={<AboutPage />} />
          </Routes>
        </main>
        <footer className="app-footer">
          <p>
            ⚠️ <strong>Educational purpose only.</strong> This application is NOT a medical diagnosis tool.
            Always consult a qualified healthcare professional.
          </p>
        </footer>
      </div>
    </Router>
  )
}
