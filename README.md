# LMS Student Risk Predictor
A machine learning system that predicts whether a student 
is at risk of failing based on attendance, assignments, and exam data.

## Models Used
- Logistic Regression
- Random Forest
- XGBoost

## Features
- attendance_rate
- avg_session_duration_pct
- consecutive_absences
- assignment_submission_rate
- avg_assignment_score
- late_submission_count
- exam_score_avg
- exam_improvement_trend

## How to Run

### Train the model
Open the Jupyter notebook and run all cells.

### Run the API
pip install fastapi uvicorn
uvicorn main:app --reload

### Test the API
Open browser and go to:
http://127.0.0.1:8000/docs

## Tech Stack
Python · pandas · scikit-learn · XGBoost · FastAPI
