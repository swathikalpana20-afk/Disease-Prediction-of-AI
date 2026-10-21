import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import PredictionForm from '../components/PredictionForm'
import ResultCard from '../components/ResultCard'
import FeatureImportanceChart from '../components/FeatureImportanceChart'
import { getDiseases, predictDisease } from '../services/api'

export default function PredictPage() {
  const { disease: diseaseId } = useParams()
  const navigate = useNavigate()
  const [disease, setDisease] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [pageLoading, setPageLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getDiseases()
      .then((diseases) => {
        const found = diseases.find((d) => d.id === diseaseId)
        if (!found) navigate('/', { replace: true })
        else setDisease(found)
      })
      .catch((err) => setError(err.message))
      .finally(() => setPageLoading(false))
  }, [diseaseId, navigate])

  const handleSubmit = async (formData) => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const res = await predictDisease(diseaseId, formData)
      setResult(res)
      // Scroll to result
      setTimeout(() => {
        document.getElementById('prediction-result')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 100)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (pageLoading) {
    return (
      <div className="loading-overlay" style={{ marginTop: 'var(--space-3xl)' }}>
        <div className="loading-spinner" /> Loading…
      </div>
    )
  }

  if (!disease) return null

  return (
    <div className="predict-page">
      <div className="container">
        {/* Breadcrumb */}
        <nav className="breadcrumb" aria-label="Breadcrumb">
          <Link to="/">Dashboard</Link>
          <span className="breadcrumb-sep">›</span>
          <span className="breadcrumb-current">{disease.name} Prediction</span>
        </nav>

        {/* Form Card */}
        <div className="predict-form-card">
          <div className="predict-form-header">
            <div className="predict-form-icon" aria-hidden="true">{disease.icon}</div>
            <div>
              <h1 style={{ fontSize: '1.5rem', marginBottom: 4 }}>{disease.name} Prediction</h1>
              <p style={{ fontSize: '0.875rem', color: 'var(--clr-text-secondary)' }}>
                {disease.description}
              </p>
            </div>
          </div>

          {error && (
            <div className="error-alert" style={{ marginBottom: 'var(--space-lg)' }} role="alert">
              <span>⚠️</span>
              <div>
                <strong>Error:</strong> {error}
                {error.includes('Run train.py') || error.includes('trained') ? (
                  <><br /><small>Please run <code>python backend/ml/train.py</code> to train the models first.</small></>
                ) : null}
              </div>
            </div>
          )}

          <PredictionForm disease={disease} onSubmit={handleSubmit} loading={loading} />
        </div>

        {/* Result */}
        {result && (
          <>
            <ResultCard result={result} />
            {Object.keys(result.feature_importance || {}).length > 0 && (
              <div className="predict-form-card" style={{ maxWidth: 900, margin: 'var(--space-lg) auto 0' }}>
                <FeatureImportanceChart importance={result.feature_importance} />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
