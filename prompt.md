You are an expert Full-Stack AI/ML Developer and UI/UX Engineer.

Build a complete, working, production-quality educational project named:

# Disease Prediction from Medical Data

## 1. PROJECT OBJECTIVE

Develop a web-based Machine Learning application that predicts the possibility of selected diseases from structured patient medical data.

The system must support:

1. Heart Disease Prediction
2. Diabetes Prediction
3. Breast Cancer Prediction

The project is strictly an educational/research demonstration. It must NOT claim to provide medical diagnosis or replace a doctor.

Display this disclaimer prominently:

"Educational purpose only. This prediction is not a medical diagnosis. Please consult a qualified healthcare professional for medical advice."

---

# 2. TECHNOLOGY STACK

Use:

Frontend:

* React.js
* HTML5
* CSS3
* JavaScript
* Responsive design
* Modern dashboard UI

Backend:

* Python
* FastAPI

Machine Learning:

* Scikit-learn
* Pandas
* NumPy
* XGBoost

Visualization:

* Plotly or Chart.js

Database:

* SQLite for storing non-sensitive demo prediction history
* Do NOT store personally identifiable patient information unnecessarily.

Development:

* Create a clean modular project structure.
* Include requirements.txt
* Include README.md
* Include .env.example if required.
* Make the application easy to run locally.

---

# 3. DATASETS

Use publicly available structured datasets from the UCI Machine Learning Repository or equivalent well-known public ML datasets.

Datasets:

A. Heart Disease
Typical features may include:

* age
* sex
* chest pain type
* resting blood pressure
* cholesterol
* fasting blood sugar
* resting ECG
* maximum heart rate
* exercise-induced angina
* ST depression
* slope
* number of major vessels
* thalassemia
* target

B. Diabetes
Typical features may include:

* pregnancies
* glucose
* blood pressure
* skin thickness
* insulin
* BMI
* diabetes pedigree function
* age
* target

C. Breast Cancer
Use the Wisconsin Breast Cancer dataset.

Use appropriate preprocessing for each dataset.

Do not hard-code fake ML predictions.

---

# 4. MACHINE LEARNING PIPELINE

Implement a complete ML pipeline:

1. Load dataset
2. Validate dataset
3. Handle missing values
4. Remove/handle invalid values where appropriate
5. Separate features and target
6. Perform train-test split
7. Apply feature scaling where required
8. Train multiple classification models
9. Evaluate models
10. Select the best model based on suitable evaluation metrics
11. Save trained model and preprocessing pipeline
12. Load saved model during prediction
13. Return prediction and probability/confidence carefully labelled as model-estimated probability

Algorithms to implement:

* Logistic Regression
* Support Vector Machine (SVM)
* Random Forest
* XGBoost

Use Pipeline/ColumnTransformer where appropriate to avoid data leakage.

Use stratified train-test split for classification.

Use random_state for reproducibility.

---

# 5. MODEL EVALUATION

For every disease dataset calculate:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

Generate:

* Confusion matrix
* ROC curve
* Model comparison chart

Create a model comparison table like:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
| ----- | -------- | --------- | ------ | -------- | ------- |

Do NOT automatically choose a model using accuracy alone.

For medical screening-style educational evaluation, explain why recall/sensitivity can be important.

---

# 6. DATA PREPROCESSING

Create reusable preprocessing modules.

For numerical features:

* Missing value handling
* StandardScaler where appropriate

For categorical features:

* Encoding where required

Make sure the exact same preprocessing is applied during training and prediction.

Prevent data leakage.

Store preprocessing objects together with the model using joblib.

---

# 7. PROJECT ARCHITECTURE

Create this structure:

disease-prediction/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   │
│   ├── api/
│   │   ├── prediction.py
│   │   ├── models.py
│   │   └── health.py
│   │
│   ├── ml/
│   │   ├── preprocessing.py
│   │   ├── train.py
│   │   ├── evaluate.py
│   │   ├── predict.py
│   │   └── model_utils.py
│   │
│   ├── models/
│   │   ├── heart/
│   │   ├── diabetes/
│   │   └── breast_cancer/
│   │
│   ├── datasets/
│   │   ├── heart/
│   │   ├── diabetes/
│   │   └── breast_cancer/
│   │
│   └── database/
│       └── database.py
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── charts/
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── public/
│
├── README.md
├── .gitignore
└── requirements.txt

You may modify the structure if necessary, but maintain clear separation between frontend, backend, ML, datasets, models, and database.

---

# 8. FRONTEND UI

Create a modern professional AI healthcare dashboard.

Main pages:

## Dashboard

Show:

* Project title
* Short description
* Three disease cards
* Heart Disease
* Diabetes
* Breast Cancer
* Model performance summary
* Recent predictions
* Educational disclaimer

Use a clean medical/AI visual style.

---

# 9. PREDICTION PAGE

When the user selects a disease, dynamically display the appropriate input form.

Example:

Heart Disease:

* Age
* Sex
* Chest pain
* Blood pressure
* Cholesterol
* Blood sugar
* ECG
* Maximum heart rate
* Exercise angina
* ST depression
* Other required dataset features

Diabetes:

* Pregnancies
* Glucose
* Blood pressure
* Skin thickness
* Insulin
* BMI
* Diabetes pedigree
* Age

Breast Cancer:

* Required Wisconsin dataset features

Do not ask for unnecessary personal information.

Use:

* Proper labels
* Input validation
* Helpful units
* Min/max validation where appropriate
* Dropdowns for categorical values
* Numeric fields for numerical values

---

# 10. PREDICTION RESULT

After submitting the form, show:

Disease:
[Selected Disease]

Result:

* Lower model-estimated likelihood
  OR
* Higher model-estimated likelihood

Also display:

* Model used
* Model-estimated probability
* Prediction timestamp
* Short explanation

IMPORTANT:

Do NOT display:
"You definitely have this disease."

Instead use language such as:

"The model estimates a higher likelihood based on the entered data. This is not a diagnosis."

Add:

"Consult a qualified healthcare professional for proper evaluation."

Use an easy-to-understand result card.

---

# 11. EXPLAINABLE AI

Add a simple explainability section.

For tree-based models:

* Feature importance

If feasible, implement SHAP.

Show:

"Factors that influenced this model prediction"

Display top contributing features using a horizontal bar chart.

Clearly explain that feature importance is a model explanation and does not establish medical causation.

---

# 12. MODEL PERFORMANCE PAGE

Create a dedicated page:

"Model Performance"

For each disease display:

* Dataset size
* Number of features
* Train/test split
* Accuracy
* Precision
* Recall
* F1
* ROC-AUC

Charts:

1. Model comparison
2. Confusion matrix
3. ROC curve

Allow user to switch between:

* Heart Disease
* Diabetes
* Breast Cancer

---

# 13. API ENDPOINTS

Create FastAPI endpoints:

GET /api/health

GET /api/diseases

POST /api/predict/heart

POST /api/predict/diabetes

POST /api/predict/breast-cancer

GET /api/model-performance

GET /api/prediction-history

Use Pydantic schemas for request validation.

Return clean JSON responses.

Handle invalid input gracefully.

---

# 14. DATABASE

Use SQLite only for demo prediction history.

Store:

* prediction ID
* disease type
* model name
* prediction result
* estimated probability
* timestamp

Avoid storing unnecessary personal/identifying patient information.

---

# 15. SECURITY

Implement basic security practices:

* Validate all API inputs
* Handle exceptions
* Do not expose stack traces to frontend
* Do not hard-code secrets
* Configure CORS properly
* Do not log sensitive medical information
* Do not store unnecessary patient identifiers

---

# 16. ERROR HANDLING

Frontend:

* Display user-friendly validation messages
* Loading state
* API error state
* Empty state

Backend:

* Proper HTTP status codes
* Pydantic validation
* Exception handling
* Logging without sensitive data

---

# 17. MODEL TRAINING

Create a training script:

python backend/ml/train.py

It should:

1. Load all datasets
2. Preprocess them
3. Train:

   * Logistic Regression
   * SVM
   * Random Forest
   * XGBoost
4. Evaluate all models
5. Select the best model according to a documented metric strategy
6. Save the model
7. Save preprocessing pipeline
8. Save evaluation metrics
9. Generate evaluation plots if appropriate

The training process should be reproducible.

---

# 18. SAMPLE DATA

If the actual datasets are not available in the project directory:

* Clearly document where to download the public datasets.
* Do NOT create fake medical records and present them as real data.
* Provide a clear dataset setup instruction in README.md.

If a small synthetic dataset is required only for testing the UI/API, clearly label it as:

"SYNTHETIC TEST DATA – NOT REAL PATIENT DATA"

---

# 19. README

Create a complete README.md containing:

1. Project title
2. Project objective
3. Features
4. Technologies
5. ML algorithms
6. Dataset sources
7. Project architecture
8. Installation
9. Backend setup
10. Frontend setup
11. Dataset setup
12. Model training commands
13. How to run the application
14. API documentation
15. Screenshots section placeholder
16. Model evaluation
17. Limitations
18. Medical disclaimer
19. Future enhancements

---

# 20. USER EXPERIENCE

The application must be:

* Responsive
* Clean
* Beginner-friendly
* Professional
* Fast
* Accessible
* Easy to demonstrate during a college project presentation

Add:

* Navigation bar
* Dashboard
* Prediction pages
* Model performance
* About project
* Disclaimer

---

# 21. CODE QUALITY

Follow these rules:

* Write clean modular code
* Use meaningful variable names
* Add comments for important ML logic
* Avoid duplicate code
* Use functions/classes where appropriate
* Keep frontend and backend separated
* Never hard-code predictions
* Never use fake accuracy values
* Never claim clinical accuracy
* Make all ML metrics come from actual model evaluation

---

# 22. TESTING

Implement basic tests for:

Backend:

* Health endpoint
* Prediction endpoint
* Invalid input
* Missing input
* Model loading

ML:

* Dataset loading
* Preprocessing
* Prediction shape
* Model prediction

Frontend:

* Form rendering
* Validation
* API response handling

---

# 23. FINAL EXECUTION

After creating the project:

1. Install dependencies.
2. Verify dataset paths.
3. Train all models.
4. Verify saved models.
5. Start FastAPI backend.
6. Start React frontend.
7. Test every prediction endpoint.
8. Fix all errors.
9. Verify frontend-backend integration.
10. Verify charts and model metrics.
11. Verify responsive UI.
12. Provide exact terminal commands to run the project.

Do not stop at generating a basic skeleton.

Actually implement the complete working project with all necessary source files.

If any dependency, dataset path, API issue, or code error occurs, diagnose and fix it.

At the end, provide:

A. Final project structure
B. Installation commands
C. Model training command
D. Backend run command
E. Frontend run command
F. Test commands
G. Short explanation of how the complete system works
H. Important limitations and medical disclaimer

Build this as a complete college-level AI/ML project that can be demonstrated locally.
