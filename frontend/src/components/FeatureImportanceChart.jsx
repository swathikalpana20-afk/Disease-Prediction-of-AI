/**
 * FeatureImportanceChart
 * Renders a horizontal bar chart of SHAP / feature importance values.
 * Positive values → the feature pushes toward positive class (disease detected).
 * Negative values → the feature pushes toward negative class.
 *
 * Clearly labelled as MODEL EXPLANATION, not causal medical evidence.
 */
export default function FeatureImportanceChart({ importance }) {
  if (!importance || Object.keys(importance).length === 0) return null

  const entries = Object.entries(importance).slice(0, 12) // Top 12
  const maxAbs = Math.max(...entries.map(([, v]) => Math.abs(v)), 1e-6)

  return (
    <section className="importance-section" aria-label="Feature importance explanation">
      <h3 className="importance-title">🔍 Factors That Influenced This Prediction</h3>
      <p className="importance-note">
        These are model-level feature importances / SHAP values. They explain what the model
        used to make its estimate — they do <strong>not</strong> establish medical causation.
      </p>

      <div role="list">
        {entries.map(([feature, value]) => {
          const isPos = value >= 0
          const width = (Math.abs(value) / maxAbs) * 100
          return (
            <div key={feature} className="importance-bar-item" role="listitem">
              <span className="importance-bar-label" title={feature}>{feature}</span>
              <div className="importance-bar-track" aria-hidden="true">
                <div
                  className={`importance-bar-fill importance-bar-fill--${isPos ? 'pos' : 'neg'}`}
                  style={{ width: `${width}%` }}
                />
              </div>
              <span className="importance-bar-value" aria-label={`${value.toFixed(3)}`}>
                {value > 0 ? '+' : ''}{value.toFixed(3)}
              </span>
            </div>
          )
        })}
      </div>
    </section>
  )
}
