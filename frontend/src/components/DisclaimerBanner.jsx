export default function DisclaimerBanner() {
  return (
    <div className="disclaimer-banner" role="alert" aria-live="polite">
      <span aria-hidden="true">⚠️</span>
      <p>
        <strong>Educational purpose only.</strong>{' '}
        This prediction tool is NOT a medical diagnosis. Always consult a qualified
        healthcare professional for medical advice.
      </p>
    </div>
  )
}
