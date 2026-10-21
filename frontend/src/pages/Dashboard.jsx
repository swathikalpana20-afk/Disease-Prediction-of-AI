import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import DiseaseCard from '../components/DiseaseCard'
import { getDiseases, getPredictionHistory, getModelPerformance } from '../services/api'

const DISEASE_COLORS = {
  heart: 'var(--clr-heart)',
  diabetes: 'var(--clr-diabetes)',
  breast_cancer: 'var(--clr-cancer)',
}

function StatStrip({ diseases }) {
  return (
    <div className="stats-strip">
      <div className="stat-item">
        <span className="stat-value">3</span>
        <span className="stat-label">Diseases</span>
      </div>
      <div className="stat-item">
        <span className="stat-value">4</span>
        <span className="stat-label">ML Algorithms</span>
      </div>
      <div className="stat-item">
        <span className="stat-value">~1.5K</span>
        <span className="stat-label">Training Records</span>
      </div>
      <div className="stat-item">
        <span className="stat-value">F1</span>
        <span className="stat-label">Selection Metric</span>
      </div>
    </div>
  )
}

function HistoryItem({ item }) {
  const color = DISEASE_COLORS[item.disease_type] || 'var(--clr-primary)'
  const isHigh = item.prediction_result === 1
  return (
    <div className="history-item">
      <div>
        <div className="history-disease" style={{ color }}>
          {item.disease_type === 'breast_cancer' ? 'Breast Cancer'
           : item.disease_type === 'heart' ? 'Heart Disease'
           : 'Diabetes'}
        </div>
        <div className="history-model">{item.model_name}</div>
      </div>
      <span
        className="history-prob"
        style={{ color: isHigh ? 'var(--clr-danger)' : 'var(--clr-success)' }}
      >
        {(item.estimated_probability * 100).toFixed(1)}%
      </span>
      <span className="history-time">
        {new Date(item.timestamp).toLocaleTimeString()}
      </span>
    </div>
  )
}

export default function Dashboard() {
  const [diseases, setDiseases] = useState([])
  const [history, setHistory] = useState([])
  const [performance, setPerformance] = useState({})
  const [loading, setLoading] = useState(true)
  const [apiError, setApiError] = useState(null)

  useEffect(() => {
    const load = async () => {
      try {
        const [d, h, p] = await Promise.all([
          getDiseases(),
          getPredictionHistory(10),
          getModelPerformance(),
        ])
        setDiseases(d)
        setHistory(h.history || [])
        setPerformance(p)
      } catch (err) {
        setApiError(err.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div>
      {/* Hero */}
      <section className="hero">
        <div className="container">
          <div className="hero-badge">
            <span>🧬</span> Educational AI/ML Project
          </div>
          <h1 className="hero-title">
            Disease Prediction{' '}
            <span className="highlight">from Medical Data</span>
          </h1>
          <p className="hero-subtitle">
            An educational machine learning application that estimates the likelihood of
            heart disease, diabetes, and breast cancer using real clinical datasets and
            four classification algorithms.
          </p>
          <StatStrip diseases={diseases} />
        </div>
      </section>

      {/* API error */}
      {apiError && (
        <div className="container" style={{ marginBottom: 'var(--space-xl)' }}>
          <div className="error-alert">
            <span>⚠️</span>
            <div>
              <strong>Backend Unavailable:</strong> {apiError}
              <br />
              <small>Make sure the FastAPI server is running on port 8000 and models are trained.</small>
            </div>
          </div>
        </div>
      )}

      {/* Disease Cards */}
      <section className="page-section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="section-header">
            <h2 className="section-title">Select a Disease to Predict</h2>
            <p className="section-subtitle">
              Choose a disease model below to enter clinical parameters and receive a
              model-estimated likelihood. All predictions are for educational purposes only.
            </p>
          </div>

          {loading ? (
            <div className="loading-overlay">
              <div className="loading-spinner" />
              Loading disease models…
            </div>
          ) : (
            <div className="disease-cards-grid">
              {diseases.map((d) => <DiseaseCard key={d.id} disease={d} />)}
            </div>
          )}
        </div>
      </section>

      {/* Two-col: Performance Summary + History */}
      <section className="page-section" style={{ paddingTop: 0 }}>
        <div className="container">
          <div className="two-col">
            {/* Performance Summary */}
            <div>
              <h2 className="section-title" style={{ marginBottom: 'var(--space-lg)' }}>
                📊 Model Performance Summary
              </h2>
              {Object.keys(performance).length === 0 ? (
                <div className="card">
                  <p style={{ color: 'var(--clr-text-muted)', fontSize: '0.875rem' }}>
                    No metrics yet. Run <code>python backend/ml/train.py</code> first.
                  </p>
                </div>
              ) : (
                Object.entries(performance).map(([disease, data]) => {
                  if (data.error) return null
                  const best = data.models?.find((m) => m.model === data.best_model)
                  return (
                    <div key={disease} className="card" style={{ marginBottom: 'var(--space-md)', padding: 'var(--space-lg)' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 8 }}>
                        <div>
                          <div style={{ fontWeight: 600, color: DISEASE_COLORS[disease] }}>
                            {disease === 'breast_cancer' ? 'Breast Cancer'
                             : disease === 'heart' ? 'Heart Disease' : 'Diabetes'}
                          </div>
                          <div style={{ fontSize: '0.8rem', color: 'var(--clr-text-muted)' }}>
                            Best: {data.best_model}
                          </div>
                        </div>
                        {best && (
                          <div style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--clr-success)' }}>
                              {(best.f1_score * 100).toFixed(1)}%
                            </div>
                            <div style={{ fontSize: '0.7rem', color: 'var(--clr-text-muted)' }}>F1 Score</div>
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })
              )}
              <Link to="/performance" className="btn btn-secondary btn-sm" style={{ marginTop: 'var(--space-md)' }}>
                View Full Metrics →
              </Link>
            </div>

            {/* Recent Predictions */}
            <div>
              <h2 className="section-title" style={{ marginBottom: 'var(--space-lg)' }}>
                🕐 Recent Predictions
              </h2>
              {history.length === 0 ? (
                <div className="card">
                  <p style={{ color: 'var(--clr-text-muted)', fontSize: '0.875rem' }}>
                    No predictions yet. Run a disease prediction above to see history here.
                  </p>
                </div>
              ) : (
                <div className="prediction-history-list">
                  {history.map((item) => <HistoryItem key={item.id} item={item} />)}
                </div>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
