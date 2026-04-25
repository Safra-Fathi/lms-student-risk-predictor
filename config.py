"""
Configuration module for the LMS Risk Predictor API
"""
import os
from typing import List

class Settings:
    """Application settings"""
    
    # API Configuration
    API_TITLE: str = os.getenv("API_TITLE", "LMS Student Risk Prediction API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    
    # Log Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Model Configuration
    MODEL_PATH: str = os.getenv("MODEL_PATH", "lms_risk_model.pkl")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8000").split(",")
    
    # Feature names (must match training features)
    FEATURE_NAMES: List[str] = [
        "attendance_rate",
        "avg_session_duration_pct",
        "consecutive_absences",
        "assignment_submission_rate",
        "avg_assignment_score",
        "late_submission_count",
        "exam_score_avg",
        "exam_improvement_trend"
    ]
    
    # Risk thresholds for recommendations
    HIGH_RISK_THRESHOLD: float = 0.8
    MODERATE_HIGH_RISK_THRESHOLD: float = 0.6
    MODERATE_RISK_THRESHOLD: float = 0.5

settings = Settings()
