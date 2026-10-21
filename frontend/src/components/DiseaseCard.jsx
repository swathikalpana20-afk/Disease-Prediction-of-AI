import { Link } from 'react-router-dom'

export default function DiseaseCard({ disease }) {
  const cls = `disease-card disease-card--${disease.id}`

  return (
    <Link to={`/predict/${disease.id}`} className={cls} id={`disease-card-${disease.id}`}>
      <span className="disease-card-icon" aria-hidden="true">{disease.icon}</span>
      <h3 className="disease-card-title">{disease.name}</h3>
      <p className="disease-card-desc">{disease.description}</p>
      <span className="disease-card-cta">
        Run Prediction <span aria-hidden="true">→</span>
      </span>
    </Link>
  )
}
