/**
 * Verified sample data for "Try Demo" functionality.
 * Values precisely match backend schemas (backend/api/prediction.py)
 * and model preprocessing pipelines (backend/ml/preprocessing.py).
 */

export const DEMO_DATA = {
  // Heart Disease (Cleveland UCI dataset format)
  // Matches HeartPredictionRequest schema
  heart: {
    age: 52,
    sex: 1, // Male (1: Male, 0: Female)
    cp: 0, // Typical Angina (0-3)
    trestbps: 125, // mm Hg (50-250)
    chol: 212, // mg/dl (50-600)
    fbs: 0, // Fasting Blood Sugar <= 120 (0: False, 1: True)
    restecg: 1, // ST-T Wave Abnormality (0-2)
    thalach: 168, // bpm (50-250)
    exang: 0, // Exercise Induced Angina No (0: No, 1: Yes)
    oldpeak: 1.0, // ST Depression (0-10)
    slope: 2, // Slope of Peak Exercise ST (0: Upsloping, 1: Flat, 2: Downsloping)
    ca: 2, // Number of Major Vessels (0-3)
    thal: 3, // Thalassemia (1: Normal, 2: Fixed Defect, 3: Reversible Defect)
  },

  // Diabetes (Pima Indians Diabetes dataset format)
  // Matches DiabetesPredictionRequest schema
  diabetes: {
    Pregnancies: 2,
    Glucose: 138,
    BloodPressure: 62,
    SkinThickness: 35,
    Insulin: 0,
    BMI: 33.6,
    DiabetesPedigreeFunction: 0.627,
    Age: 47,
  },

  // Breast Cancer (Wisconsin Diagnostic dataset format)
  // Matches BreastCancerPredictionRequest schema & feature names in ML pipeline
  breast_cancer: {
    'mean radius': 17.99,
    'mean texture': 10.38,
    'mean perimeter': 122.8,
    'mean area': 1001.0,
    'mean smoothness': 0.1184,
    'mean compactness': 0.2776,
    'mean concavity': 0.3001,
    'mean concave points': 0.1471,
    'mean symmetry': 0.2419,
    'mean fractal dimension': 0.0787,
    'radius error': 1.095,
    'texture error': 0.9053,
    'perimeter error': 8.589,
    'area error': 153.4,
    'smoothness error': 0.0064,
    'compactness error': 0.049,
    'concavity error': 0.0537,
    'concave points error': 0.0159,
    'symmetry error': 0.03,
    'fractal dimension error': 0.0062,
    'worst radius': 25.38,
    'worst texture': 17.33,
    'worst perimeter': 184.6,
    'worst area': 2019.0,
    'worst smoothness': 0.1622,
    'worst compactness': 0.6656,
    'worst concavity': 0.7119,
    'worst concave points': 0.2654,
    'worst symmetry': 0.4601,
    'worst fractal dimension': 0.1189,
  },
}
