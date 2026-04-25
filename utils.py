"""
Utility functions for the LMS Risk Predictor API
"""
import numpy as np
from typing import Dict, Any
from config import settings

def validate_student_data(data: Dict[str, Any]) -> bool:
    """
    Validate student data against expected ranges
    
    Returns:
        bool: True if data is valid
    """
    # Check required fields
    required_fields = settings.FEATURE_NAMES
    if not all(field in data for field in required_fields):
        return False
    
    # Validate ranges
    if not (0 <= data['attendance_rate'] <= 1):
        return False
    if not (0 <= data['avg_session_duration_pct'] <= 1):
        return False
    if not (0 <= data['assignment_submission_rate'] <= 1):
        return False
    if not (0 <= data['avg_assignment_score'] <= 100):
        return False
    if not (0 <= data['exam_score_avg'] <= 100):
        return False
    
    return True

def format_probability(probability: float, decimal_places: int = 4) -> float:
    """Format probability to specified decimal places"""
    return round(probability, decimal_places)

def calculate_risk_level(probability: float) -> str:
    """
    Categorize risk level based on probability
    
    Args:
        probability: Risk probability (0-1)
    
    Returns:
        str: Risk level category
    """
    if probability >= settings.HIGH_RISK_THRESHOLD:
        return "High"
    elif probability >= settings.MODERATE_HIGH_RISK_THRESHOLD:
        return "Moderate-High"
    elif probability >= settings.MODERATE_RISK_THRESHOLD:
        return "Moderate"
    else:
        return "Low"

def get_intervention_priority(probability: float) -> int:
    """
    Get intervention priority level (1-5, where 1 is highest priority)
    
    Args:
        probability: Risk probability (0-1)
    
    Returns:
        int: Priority level (1-5)
    """
    if probability >= settings.HIGH_RISK_THRESHOLD:
        return 1
    elif probability >= 0.8:
        return 2
    elif probability >= settings.MODERATE_HIGH_RISK_THRESHOLD:
        return 3
    elif probability >= settings.MODERATE_RISK_THRESHOLD:
        return 4
    else:
        return 5

def aggregate_batch_statistics(predictions: list) -> Dict[str, Any]:
    """
    Calculate aggregate statistics for batch predictions
    
    Args:
        predictions: List of prediction responses
    
    Returns:
        dict: Aggregated statistics
    """
    at_risk_predictions = [p for p in predictions if p['at_risk']]
    risk_probabilities = [p['risk_probability'] for p in predictions]
    
    return {
        "total_predictions": len(predictions),
        "at_risk_count": len(at_risk_predictions),
        "on_track_count": len(predictions) - len(at_risk_predictions),
        "average_risk_probability": round(np.mean(risk_probabilities), 4),
        "max_risk_probability": round(np.max(risk_probabilities), 4),
        "min_risk_probability": round(np.min(risk_probabilities), 4),
        "std_risk_probability": round(np.std(risk_probabilities), 4)
    }
