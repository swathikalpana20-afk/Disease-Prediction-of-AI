# Disease Prediction from Medical Data

An educational machine learning web application that predicts the likelihood of Heart Disease, Diabetes, and Breast Cancer using real clinical data.

## 🚀 Features
- **3 Disease Models:** Heart Disease, Diabetes, Breast Cancer.
- **Multiple ML Algorithms:** Logistic Regression, SVM, Random Forest, XGBoost.
- **Explainable AI (XAI):** SHAP values to explain feature importance for predictions.
- **Performance Metrics:** Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Confusion Matrix.
- **Modern UI:** Built with React, Vite, and Plotly for an interactive dark-mode dashboard.

## 🛠️ Technology Stack
- **Frontend:** React 18, Vite, Plotly.js, standard CSS3.
- **Backend:** Python 3.11+, FastAPI, Uvicorn, SQLite (via SQLAlchemy).
- **Machine Learning:** Scikit-learn, XGBoost, SHAP, Pandas.

## ⚠️ Disclaimer
**Educational purpose only. This prediction is not a medical diagnosis. Please consult a qualified healthcare professional for medical advice.**

## 📥 Installation

### Prerequisites
- Node.js (v18+)
- Python (3.11+)

### 1. Backend Setup
1. Open a terminal in the `disease-prediction/backend` folder.
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` (optional, default values are provided).

### 2. Frontend Setup
1. Open a new terminal in the `disease-prediction/frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```

### 3. Model Training (Required First Step!)
You must download the datasets and train the models before starting the server. The script handles data downloading automatically.
```bash
# In the root or backend directory
python backend/ml/train.py
```
This will create `best_model.json`, `metrics.json`, and `.joblib` files inside `backend/models/`.

## 🏃 Running the Application

### Start the Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```
API Docs: `http://localhost:8000/docs`

### Start the Frontend Dev Server
```bash
cd frontend
npm run dev
```
Open `http://localhost:5173` in your browser.

## 🧪 Running Tests
```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests (if configured)
cd frontend
npm test
```
