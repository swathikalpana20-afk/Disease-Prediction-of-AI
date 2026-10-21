/**
 * ConfusionMatrix — renders a 2×2 confusion matrix heatmap.
 * cm = [[TN, FP], [FN, TP]]
 */
export default function ConfusionMatrix({ cm }) {
  if (!cm || cm.length < 2) return <p style={{ color: 'var(--clr-text-muted)' }}>No confusion matrix data.</p>

  const [[tn, fp], [fn, tp]] = cm

  const cells = [
    { label: 'True Negative', abbr: 'TN', value: tn, cls: 'cm-tn' },
    { label: 'False Positive', abbr: 'FP', value: fp, cls: 'cm-fp' },
    { label: 'False Negative', abbr: 'FN', value: fn, cls: 'cm-fn' },
    { label: 'True Positive', abbr: 'TP', value: tp, cls: 'cm-tp' },
  ]

  return (
    <div>
      {/* Axis labels */}
      <div style={{ display: 'flex', marginBottom: 4, fontSize: '0.72rem', color: 'var(--clr-text-muted)' }}>
        <div style={{ width: 36 }} />
        <div style={{ flex: 1, textAlign: 'center' }}>Predicted Negative</div>
        <div style={{ flex: 1, textAlign: 'center' }}>Predicted Positive</div>
      </div>

      <div style={{ display: 'flex', alignItems: 'stretch' }}>
        <div style={{
          writingMode: 'vertical-rl', transform: 'rotate(180deg)',
          fontSize: '0.72rem', color: 'var(--clr-text-muted)',
          display: 'flex', alignItems: 'center', marginRight: 8, userSelect: 'none'
        }}>
          Actual
        </div>
        <div className="confusion-matrix-grid" role="table" aria-label="Confusion matrix">
          {cells.map((c) => (
            <div key={c.abbr} className={`cm-cell ${c.cls}`} role="cell" aria-label={`${c.label}: ${c.value}`}>
              <span className="cm-cell-value">{c.value ?? '—'}</span>
              <span className="cm-cell-label">{c.abbr}</span>
            </div>
          ))}
        </div>
      </div>

      <p style={{ fontSize: '0.7rem', color: 'var(--clr-text-muted)', marginTop: 8 }}>
        TP=True Positive · TN=True Negative · FP=False Positive · FN=False Negative
      </p>
    </div>
  )
}
