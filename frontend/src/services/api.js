import axios from 'axios'

const BASE_URL = '/api'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

// Response interceptor: normalise errors
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const message =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      err.message ||
      'An unexpected error occurred.'
    return Promise.reject(new Error(message))
  }
)

export const healthCheck = () => api.get('/health').then((r) => r.data)

export const getDiseases = () => api.get('/diseases').then((r) => r.data.diseases)

export const getModelPerformance = () => api.get('/model-performance').then((r) => r.data.performance)

export const getPredictionHistory = (limit = 20) =>
  api.get(`/prediction-history?limit=${limit}`).then((r) => r.data)

export const predictHeart = (data) =>
  api.post('/predict/heart', data).then((r) => r.data)

export const predictDiabetes = (data) =>
  api.post('/predict/diabetes', data).then((r) => r.data)

export const predictBreastCancer = (data) =>
  api.post('/predict/breast-cancer', data).then((r) => r.data)

export const predictDisease = (diseaseId, data) => {
  switch (diseaseId) {
    case 'heart':        return predictHeart(data)
    case 'diabetes':     return predictDiabetes(data)
    case 'breast_cancer':return predictBreastCancer(data)
    default: return Promise.reject(new Error(`Unknown disease: ${diseaseId}`))
  }
}

export default api
