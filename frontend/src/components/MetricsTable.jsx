function getMetricClass(value) {
  if (value >= 0.85) return 'metric-badge--good'
  if (value >= 0.70) return 'metric-badge--medium'
  return 'metric-badge--low'
}

export default function MetricsTable({ models = [], bestModel }) {
  if (!models.length) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📊</div>
        <p>No metrics available. Run <code>python backend/ml/train.py</code> first.</p>
      </div>
    )
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="metrics-table" aria-label="Model comparison metrics">
        <thead>
          <tr>
            <th scope="col">Model</th>
            <th scope="col">Accuracy</th>
            <th scope="col">Precision</th>
            <th scope="col">Recall *</th>
            <th scope="col">F1 Score</th>
            <th scope="col">ROC-AUC</th>
          </tr>
        </thead>
        <tbody>
          {models.map((m) => {
            const isBest = m.model === bestModel
            return (
              <tr key={m.model} className={isBest ? 'best-row' : ''}>
                <td>
                  {m.model}
                  {isBest && (
                    <span className="metric-badge metric-badge--good" style={{ marginLeft: 8 }}>
                      ★ Best
                    </span>
                  )}
                </td>
                {['accuracy','precision','recall','f1_score','roc_auc'].map((key) => (
                  <td key={key}>
                    <span className={`metric-badge ${getMetricClass(m[key] ?? 0)}`}>
                      {((m[key] ?? 0) * 100).toFixed(1)}%
                    </span>
                  </td>
                ))}
              </tr>
            )
          })}
        </tbody>
      </table>
      <p style={{ fontSize: '0.72rem', color: 'var(--clr-text-muted)', marginTop: 8 }}>
        * Recall (Sensitivity) is especially important in medical screening — a false negative
        (missing a real case) is typically more harmful than a false positive. Best model is
        selected by F1 Score, not accuracy alone.
      </p>
    </div>
  )
}
