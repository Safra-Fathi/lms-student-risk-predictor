from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
import logging
from typing import List, Optional
from datetime import datetime

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model
try:
    model = joblib.load('lms_risk_model.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

app = FastAPI(
    title="LMS Student Risk Prediction API",
    description="Machine Learning API for predicting student risk of failure",
    version="1.0.0"
)

# CORS Configuration for Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Pydantic Models ====================

class StudentPredictionRequest(BaseModel):
    """Single student prediction request"""
    student_id: str = Field(..., description="Unique student identifier")
    course_id: str = Field(..., description="Course identifier")
    attendance_rate: float = Field(..., ge=0, le=1, description="Attendance rate (0-1)")
    avg_session_duration_pct: float = Field(..., ge=0, le=1, description="Average session duration percentage (0-1)")
    consecutive_absences: int = Field(..., ge=0, description="Number of consecutive absences")
    assignment_submission_rate: float = Field(..., ge=0, le=1, description="Assignment submission rate (0-1)")
    avg_assignment_score: float = Field(..., ge=0, le=100, description="Average assignment score (0-100)")
    late_submission_count: int = Field(..., ge=0, description="Number of late submissions")
    exam_score_avg: float = Field(..., ge=0, le=100, description="Average exam score (0-100)")
    exam_improvement_trend: float = Field(..., description="Exam score improvement trend")

    class Config:
        json_schema_extra = {
            "example": {
                "student_id": "s_1000",
                "course_id": "c_1",
                "attendance_rate": 0.738,
                "avg_session_duration_pct": 0.54,
                "consecutive_absences": 2,
                "assignment_submission_rate": 0.832,
                "avg_assignment_score": 71.19,
                "late_submission_count": 2,
                "exam_score_avg": 71.17,
                "exam_improvement_trend": 0.0376
            }
        }

class PredictionResponse(BaseModel):
    """Single prediction response"""
    student_id: str
    course_id: str
    at_risk: bool
    risk_probability: float
    confidence: float
    recommendation: str
    timestamp: str

class BatchPredictionRequest(BaseModel):
    """Batch prediction request"""
    students: List[StudentPredictionRequest] = Field(..., description="List of student prediction requests")

class BatchPredictionResponse(BaseModel):
    """Batch prediction response"""
    total_students: int
    at_risk_count: int
    on_track_count: int
    predictions: List[PredictionResponse]
    processing_time: float

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_status: str
    timestamp: str

class StatisticsResponse(BaseModel):
    """Statistics about predictions"""
    total_predictions: int
    at_risk_students: int
    on_track_students: int
    average_risk_probability: float

# ==================== Helper Functions ====================

def prepare_features(request: StudentPredictionRequest) -> np.ndarray:
    """Convert request to model features"""
    features = np.array([
        request.attendance_rate,
        request.avg_session_duration_pct,
        request.consecutive_absences,
        request.assignment_submission_rate,
        request.avg_assignment_score,
        request.late_submission_count,
        request.exam_score_avg,
        request.exam_improvement_trend
    ]).reshape(1, -1)
    return features

def get_recommendation(at_risk: bool, probability: float) -> str:
    """Generate recommendation based on prediction"""
    if not at_risk:
        return "Student is on track. Continue current study plan."
    elif probability > 0.8:
        return "High risk. Immediate intervention required - contact academic advisor."
    elif probability > 0.6:
        return "Moderate-high risk. Schedule tutoring and increase engagement."
    else:
        return "Moderate risk. Monitor progress and offer support resources."

# ==================== API Endpoints ====================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        model_status="loaded",
        timestamp=datetime.now().isoformat()
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_single(request: StudentPredictionRequest):
    """
    Predict if a single student is at risk of failing.
    
    Returns:
    - at_risk: Boolean indicating if student is at risk
    - risk_probability: Probability of being at risk (0-1)
    - confidence: Model confidence in prediction
    - recommendation: Actionable recommendation
    """
    try:
        features = prepare_features(request)
        
        # Get prediction
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0]
        
        at_risk = bool(prediction == 1)
        risk_prob = float(probability[1])  # Probability of at-risk class
        confidence = float(np.max(probability))
        
        recommendation = get_recommendation(at_risk, risk_prob)
        
        logger.info(f"Prediction made for student {request.student_id}: at_risk={at_risk}")
        
        return PredictionResponse(
            student_id=request.student_id,
            course_id=request.course_id,
            at_risk=at_risk,
            risk_probability=round(risk_prob, 4),
            confidence=round(confidence, 4),
            recommendation=recommendation,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.post("/predict-batch", response_model=BatchPredictionResponse, tags=["Predictions"])
async def predict_batch(request: BatchPredictionRequest):
    """
    Predict for multiple students in a single request.
    
    This endpoint is optimized for batch processing.
    """
    import time
    start_time = time.time()
    
    try:
        predictions = []
        at_risk_count = 0
        
        for student_request in request.students:
            features = prepare_features(student_request)
            
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0]
            
            at_risk = bool(prediction == 1)
            risk_prob = float(probability[1])
            confidence = float(np.max(probability))
            
            if at_risk:
                at_risk_count += 1
            
            recommendation = get_recommendation(at_risk, risk_prob)
            
            predictions.append(PredictionResponse(
                student_id=student_request.student_id,
                course_id=student_request.course_id,
                at_risk=at_risk,
                risk_probability=round(risk_prob, 4),
                confidence=round(confidence, 4),
                recommendation=recommendation,
                timestamp=datetime.now().isoformat()
            ))
        
        processing_time = time.time() - start_time
        on_track_count = len(request.students) - at_risk_count
        
        logger.info(f"Batch prediction completed: {len(request.students)} students, {at_risk_count} at-risk")
        
        return BatchPredictionResponse(
            total_students=len(request.students),
            at_risk_count=at_risk_count,
            on_track_count=on_track_count,
            predictions=predictions,
            processing_time=round(processing_time, 4)
        )
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

@app.get("/model-info", tags=["Model"])
async def model_info():
    """Get information about the model"""
    return {
        "model_type": str(type(model).__name__),
        "features": [
            "attendance_rate",
            "avg_session_duration_pct",
            "consecutive_absences",
            "assignment_submission_rate",
            "avg_assignment_score",
            "late_submission_count",
            "exam_score_avg",
            "exam_improvement_trend"
        ],
        "target": "at_risk",
        "target_classes": ["On Track", "At Risk"],
        "version": "1.0.0"
    }

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API documentation"""
    return {
        "message": "LMS Student Risk Prediction API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "predict": "POST /predict - Single prediction",
            "batch_predict": "POST /predict-batch - Batch predictions",
            "model_info": "GET /model-info - Model information"
        }
    }