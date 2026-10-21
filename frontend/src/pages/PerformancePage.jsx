import { useState, useEffect } from 'react'
import { getModelPerformance } from '../services/api'
import MetricsTable from '../components/MetricsTable'
import ConfusionMatrix from '../components/ConfusionMatrix'
import ROCCurve from '../components/ROCCurve'

const TABS = [
  { id: 'heart', label: 'Heart Disease', icon: '❤️' },
  { id: 'diabetes', label: 'Diabetes', icon: '🩸' },
  { id: 'breast_cancer', label: 'Breast Cancer', icon: '🎗️' },
]

export default function PerformancePage() {
  const [performance, setPerformance] = useState({})
  const [activeTab, setActiveTab] = useState('heart')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getModelPerformance()
      .then(setPerformance)
      .finally(() => setLoading(false))
  }, [])

  if (loading) {
    return (
      <div className="loading-overlay" style={{ marginTop: 'var(--space-3xl)' }}>
        <div className="loading-spinner" /> Loading performance metrics...
      </div>
    )
  }

  const data = performance[activeTab]
  const hasError = data?.error
  const noData = !data || Object.keys(data).length === 0

  return (
    <div className="performance-page">
      <div className="container">
        <h1 className="section-title">Model Performance</h1>
        <p className="section-subtitle" style={{ marginBottom: 'var(--space-xl)' }}>
          Detailed evaluation metrics for the machine learning models.
        </p>

        <div className="disease-tab-list" role="tablist" aria-label="Disease Model Tabs">
          {TABS.map((tab) => (
            <button
              key={tab.id}
              role="tab"
              aria-selected={activeTab === tab.id}
              className={`disease-tab${activeTab === tab.id ? ' active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span aria-hidden="true">{tab.icon}</span> {tab.label}
            </button>
          ))}
        </div>

        {hasError || noData ? (
          <div className="card">
            <div className="empty-state">
              <div className="empty-state-icon">⚠️</div>
              <p>{hasError ? data.error : 'No performance data available.'}</p>
              <p style={{ fontSize: '0.875rem', marginTop: 'var(--space-sm)' }}>
                Please run <code>python backend/ml/train.py</code> to train the models and generate metrics.
              </p>
            </div>
          </div>
        ) : (
          <div>
            <div className="dataset-info-grid">
              <div className="dataset-info-item">
                <div className="dataset-info-value">{data.dataset.total_samples}</div>
                <div className="dataset-info-label">Total Samples</div>
              </div>
              <div className="dataset-info-item">
                <div className="dataset-info-value">{data.dataset.n_features}</div>
                <div className="dataset-info-label">Features</div>
              </div>
              <div className="dataset-info-item">
                <div className="dataset-info-value">{data.dataset.train_samples}</div>
                <div className="dataset-info-label">Train Set Size</div>
              </div>
              <div className="dataset-info-item">
                <div className="dataset-info-value">{data.dataset.test_samples}</div>
                <div className="dataset-info-label">Test Set Size</div>
              </div>
            </div>

            <div className="card" style={{ marginBottom: 'var(--space-xl)' }}>
              <h2 className="chart-card-title">Model Comparison</h2>
              <MetricsTable models={data.models} bestModel={data.best_model} />
            </div>

            <div className="charts-grid">
              {data.models
                .filter((m) => m.model === data.best_model)
                .map((bestModel) => (
                  <div key="confusion-matrix" className="chart-card">
                    <h2 className="chart-card-title">Confusion Matrix (Best Model)</h2>
                    <ConfusionMatrix cm={bestModel.confusion_matrix} />
                  </div>
                ))}

              {data.models
                .filter((m) => m.model === data.best_model)
                .map((bestModel) => (
                  <div key="roc-curve" className="chart-card">
                    <h2 className="chart-card-title">ROC Curve (Best Model)</h2>
                    <ROCCurve
                      rocData={bestModel.roc_curve}
                      auc={bestModel.roc_auc}
                      modelName={bestModel.model}
                    />
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
