const DISEASE_LABELS = {
  heart: 'Heart Disease',
  diabetes: 'Diabetes',
  breast_cancer: 'Breast Cancer',
}

function ProbabilityGauge({ probability, isHigh }) {
  const r = 54
  const circumference = 2 * Math.PI * r
  const pct = Math.min(Math.max(probability, 0), 1)
  const dashoffset = circumference * (1 - pct)

  return (
    <div className="probability-gauge" role="img" aria-label={`Model-estimated probability: ${(pct * 100).toFixed(1)}%`}>
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle className="gauge-track" cx="70" cy="70" r={r} />
        <circle
          className={`gauge-fill gauge-fill--${isHigh ? 'high' : 'low'}`}
          cx="70" cy="70" r={r}
          strokeDasharray={circumference}
          strokeDashoffset={dashoffset}
        />
      </svg>
      <div className="gauge-label">
        <span className={`gauge-pct gauge-pct--${isHigh ? 'high' : 'low'}`}>
          {(pct * 100).toFixed(1)}%
        </span>
        <span className="gauge-sub">probability</span>
      </div>
    </div>
  )
}

function formatTimestamp(ts) {
  if (!ts) return '—'
  try {
    return new Date(ts).toLocaleString()
  } catch {
    return ts
  }
}

export default function ResultCard({ result }) {
  const isHigh = result.prediction === 1
  const diseaseName = DISEASE_LABELS[result.disease] || result.disease

  return (
    <div className="result-card" id="prediction-result" role="region" aria-label="Prediction result">
      <h2 style={{ fontSize: '1.2rem', fontWeight: 700, marginBottom: 'var(--space-lg)' }}>
        Prediction Result — {diseaseName}
      </h2>

      <div className="result-header">
        <ProbabilityGauge probability={result.probability} isHigh={isHigh} />

        <div style={{ flex: 1 }}>
          <span className={`result-badge result-badge--${isHigh ? 'high' : 'low'}`}>
            {isHigh ? '⚠️' : '✅'} {result.result_label}
          </span>

          <div className="result-meta">
            <div className="meta-item">
              <span className="meta-label">Disease</span>
              <span className="meta-value">{diseaseName}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Model Used</span>
              <span className="meta-value">{result.model_name}</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Est. Probability</span>
              <span className="meta-value">{(result.probability * 100).toFixed(2)}%</span>
            </div>
            <div className="meta-item">
              <span className="meta-label">Timestamp</span>
              <span className="meta-value" style={{ fontSize: '0.8rem' }}>
                {formatTimestamp(result.timestamp)}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="result-explanation">
        <strong>Model Explanation:</strong> {result.explanation}
      </div>

      <div className="result-disclaimer" role="note">
        <span aria-hidden="true">⚠️</span>
        <p>{result.disclaimer}</p>
      </div>
    </div>
  )
}
