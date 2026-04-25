"""
Test examples for the LMS Risk Predictor API
Can be run with: pytest test_api.py
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Test data
SAMPLE_STUDENT = {
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

AT_RISK_STUDENT = {
    "student_id": "s_1001",
    "course_id": "c_1",
    "attendance_rate": 0.653,
    "avg_session_duration_pct": 0.604,
    "consecutive_absences": 2,
    "assignment_submission_rate": 0.403,
    "avg_assignment_score": 46.39,
    "late_submission_count": 4,
    "exam_score_avg": 16.62,
    "exam_improvement_trend": -0.0996
}

def test_health():
    """Test health check endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")

def test_single_prediction():
    """Test single prediction endpoint"""
    response = requests.post(
        f"{BASE_URL}/predict",
        json=SAMPLE_STUDENT,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "student_id" in data
    assert "at_risk" in data
    assert "risk_probability" in data
    assert "recommendation" in data
    print("✓ Single prediction test passed")
    print(f"  Result: {json.dumps(data, indent=2)}")

def test_batch_prediction():
    """Test batch prediction endpoint"""
    response = requests.post(
        f"{BASE_URL}/predict-batch",
        json={"students": [SAMPLE_STUDENT, AT_RISK_STUDENT]},
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_students"] == 2
    assert len(data["predictions"]) == 2
    print("✓ Batch prediction test passed")
    print(f"  At Risk: {data['at_risk_count']}, On Track: {data['on_track_count']}")

def test_model_info():
    """Test model info endpoint"""
    response = requests.get(f"{BASE_URL}/model-info")
    assert response.status_code == 200
    data = response.json()
    assert "model_type" in data
    assert "features" in data
    assert len(data["features"]) == 8
    print("✓ Model info test passed")

def run_all_tests():
    """Run all tests"""
    print("\n🧪 Running API Tests...\n")
    try:
        test_health()
        test_single_prediction()
        test_batch_prediction()
        test_model_info()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")

if __name__ == "__main__":
    run_all_tests()
