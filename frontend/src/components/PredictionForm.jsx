import { useState } from 'react'
import { DEMO_DATA } from '../services/demoData'

function FormField({ feature, value, onChange, error }) {
  const id = `field-${feature.name.replace(/\s+/g, '-')}`

  return (
    <div className="form-field">
      <label className="form-label" htmlFor={id}>{feature.label}</label>
      {feature.type === 'select' ? (
        <select
          id={id}
          className={`form-select${error ? ' error' : ''}`}
          value={value ?? ''}
          onChange={(e) => onChange(feature.name, e.target.value)}
          aria-required="true"
          aria-invalid={!!error}
          aria-describedby={error ? `${id}-error` : undefined}
        >
          <option value="">— Select —</option>
          {feature.options?.map((opt) => (
            <option key={opt.value} value={opt.value}>{opt.label}</option>
          ))}
        </select>
      ) : (
        <input
          id={id}
          type="number"
          className={`form-input${error ? ' error' : ''}`}
          value={value ?? ''}
          onChange={(e) => onChange(feature.name, e.target.value)}
          min={feature.min}
          max={feature.max}
          step={feature.step ?? 1}
          placeholder={feature.min !== undefined ? `${feature.min} – ${feature.max}` : ''}
          aria-required="true"
          aria-invalid={!!error}
          aria-describedby={error ? `${id}-error` : undefined}
        />
      )}
      {feature.unit && <span className="form-unit">{feature.unit}</span>}
      {error && <span id={`${id}-error`} className="form-error" role="alert">{error}</span>}
    </div>
  )
}

function validate(features, formData) {
  const errors = {}
  for (const f of features) {
    const val = formData[f.name]
    if (val === '' || val === undefined || val === null) {
      errors[f.name] = 'This field is required.'
      continue
    }
    const num = parseFloat(val)
    if (isNaN(num)) {
      errors[f.name] = 'Please enter a valid number.'
      continue
    }
    if (f.min !== undefined && num < f.min) errors[f.name] = `Minimum value is ${f.min}.`
    if (f.max !== undefined && num > f.max) errors[f.name] = `Maximum value is ${f.max}.`
  }
  return errors
}

export default function PredictionForm({ disease, onSubmit, loading }) {
  const [formData, setFormData] = useState({})
  const [errors, setErrors] = useState({})
  const [isDemoLoaded, setIsDemoLoaded] = useState(false)

  const handleChange = (name, value) => {
    setFormData((prev) => ({ ...prev, [name]: value }))
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: undefined }))
  }

  const handleLoadDemo = () => {
    const sample = DEMO_DATA[disease.id]
    if (!sample) return
    const populated = {}
    disease.features.forEach((f) => {
      if (sample[f.name] !== undefined) {
        populated[f.name] = sample[f.name]
      }
    })
    setFormData(populated)
    setErrors({})
    setIsDemoLoaded(true)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    const errs = validate(disease.features, formData)
    if (Object.keys(errs).length > 0) {
      setErrors(errs)
      return
    }
    // Convert string values to numbers
    const numericData = {}
    for (const f of disease.features) {
      numericData[f.name] = parseFloat(formData[f.name])
    }
    onSubmit(numericData)
  }

  const handleReset = () => {
    setFormData({})
    setErrors({})
    setIsDemoLoaded(false)
  }

  const diseaseColorMap = { heart: 'btn-heart', diabetes: 'btn-diabetes', breast_cancer: 'btn-cancer' }
  const submitBtnCls = `btn btn-lg ${diseaseColorMap[disease.id] || 'btn-primary'}`

  return (
    <form onSubmit={handleSubmit} noValidate aria-label={`${disease.name} prediction form`}>
      <div className="form-grid">
        {disease.features.map((feature) => (
          <FormField
            key={feature.name}
            feature={feature}
            value={formData[feature.name] ?? ''}
            onChange={handleChange}
            error={errors[feature.name]}
          />
        ))}
      </div>

      <div style={{ display: 'flex', gap: 'var(--space-md)', flexWrap: 'wrap', alignItems: 'center' }}>
        <button
          id={`submit-predict-${disease.id}`}
          type="submit"
          className={submitBtnCls}
          disabled={loading}
        >
          {loading ? (
            <>
              <span className="loading-spinner" aria-hidden="true" /> Predicting…
            </>
          ) : (
            <>🔬 Run Prediction</>
          )}
        </button>

        <button
          id={`demo-btn-${disease.id}`}
          type="button"
          className="btn btn-demo"
          onClick={handleLoadDemo}
          disabled={loading}
          title="Fill form with sample clinical values"
        >
          ✨ Try Demo
        </button>

        <button
          id={`reset-btn-${disease.id}`}
          type="button"
          className="btn btn-secondary"
          onClick={handleReset}
          disabled={loading}
        >
          Reset Form
        </button>

        {isDemoLoaded && (
          <span
            id={`demo-notice-${disease.id}`}
            className="demo-notice"
            role="status"
            aria-live="polite"
          >
            ℹ️ Demo data — for educational purposes only
          </span>
        )}
      </div>
    </form>
  )
}
