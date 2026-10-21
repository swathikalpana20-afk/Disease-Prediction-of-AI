import { useEffect, useRef } from 'react'

/**
 * ROCCurve — renders an ROC curve chart using Plotly.
 * rocData = { fpr: [...], tpr: [...] }
 * auc = float
 */
export default function ROCCurve({ rocData, auc, modelName, color = '#3b82f6' }) {
  const ref = useRef(null)

  useEffect(() => {
    if (!rocData || !rocData.fpr || !ref.current) return

    let Plotly
    import('plotly.js-dist-min').then((mod) => {
      Plotly = mod.default

      const trace = {
        x: rocData.fpr,
        y: rocData.tpr,
        type: 'scatter',
        mode: 'lines',
        name: modelName || 'Model',
        line: { color, width: 2.5 },
      }

      const diagonal = {
        x: [0, 1], y: [0, 1],
        type: 'scatter', mode: 'lines',
        name: 'Random (AUC=0.5)',
        line: { color: 'rgba(255,255,255,0.15)', dash: 'dash', width: 1 },
      }

      const layout = {
        xaxis: {
          title: 'False Positive Rate',
          tickfont: { color: '#94a3b8', size: 11 },
          titlefont: { color: '#94a3b8', size: 12 },
          gridcolor: 'rgba(255,255,255,0.05)',
          linecolor: 'rgba(255,255,255,0.1)',
          range: [0, 1],
        },
        yaxis: {
          title: 'True Positive Rate',
          tickfont: { color: '#94a3b8', size: 11 },
          titlefont: { color: '#94a3b8', size: 12 },
          gridcolor: 'rgba(255,255,255,0.05)',
          linecolor: 'rgba(255,255,255,0.1)',
          range: [0, 1],
        },
        paper_bgcolor: 'rgba(0,0,0,0)',
        plot_bgcolor: 'rgba(0,0,0,0)',
        font: { family: 'Inter, sans-serif', color: '#94a3b8' },
        margin: { t: 10, r: 10, b: 50, l: 55 },
        legend: {
          x: 0.6, y: 0.05,
          bgcolor: 'rgba(15,31,54,0.8)',
          bordercolor: 'rgba(255,255,255,0.1)',
          borderwidth: 1,
          font: { size: 10 },
        },
        annotations: auc ? [{
          x: 0.65, y: 0.15, xref: 'paper', yref: 'paper',
          text: `AUC = ${auc.toFixed(3)}`,
          showarrow: false,
          font: { color: color, size: 13, family: 'Space Grotesk, sans-serif' },
          bgcolor: 'rgba(15,31,54,0.8)',
          borderpad: 6,
        }] : [],
      }

      Plotly.react(ref.current, [trace, diagonal], layout, {
        responsive: true,
        displayModeBar: false,
      })
    })

    return () => {
      if (Plotly && ref.current) Plotly.purge(ref.current)
    }
  }, [rocData, auc, modelName, color])

  if (!rocData) {
    return <p style={{ color: 'var(--clr-text-muted)', fontSize: '0.875rem' }}>No ROC curve data available.</p>
  }

  return <div ref={ref} style={{ width: '100%', height: 280 }} aria-label="ROC Curve chart" />
}
