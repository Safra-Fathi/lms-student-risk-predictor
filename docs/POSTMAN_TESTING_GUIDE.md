# Postman Testing Guide - LMS Student Risk Predictor API

## Table of Contents
1. [Setup](#setup)
2. [Environment Configuration](#environment-configuration)
3. [Testing Endpoints](#testing-endpoints)
4. [Sample Requests](#sample-requests)
5. [Troubleshooting](#troubleshooting)
6. [Postman Collection](#postman-collection)

---

## Setup

### Prerequisites
- **Postman** installed ([Download here](https://www.postman.com/downloads/))
- **API running** on `http://localhost:8000`
- Verify API is running: `docker-compose up`

### Starting Postman
1. Open Postman
2. Create a new workspace or use existing
3. Create a new collection called "LMS Risk Predictor API"

---

## Environment Configuration

### Create Environment Variables

1. **Click** the gear icon ⚙️ in top-right → **Environments**
2. **Click** "+ Create New Environment"
3. **Name**: `LMS-API-Dev`
4. **Add Variables**:

| Variable | Initial Value | Current Value |
|----------|---------------|---------------|
| `base_url` | `http://localhost:8000` | `http://localhost:8000` |
| `content_type` | `application/json` | `application/json` |

5. **Save** and **Select** this environment from the dropdown

### Using Variables in Requests
Reference variables using double curly braces: `{{base_url}}`

Example: `{{base_url}}/predict`

---

## Testing Endpoints

### 1. Health Check

#### Request Details
- **Method**: `GET`
- **URL**: `{{base_url}}/health`
- **Headers**: None required

#### Steps
1. Create new request: **+ Tab** → **Get**
2. Enter URL: `{{base_url}}/health`
3. Click **Send**

#### Expected Response (200 OK)
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "timestamp": "2024-04-22T10:30:00.123456"
}
```

#### 🎯 Purpose
Verify API is running and model is loaded.

---

### 2. Single Student Prediction

#### Request Details
- **Method**: `POST`
- **URL**: `{{base_url}}/predict`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: JSON (raw)

#### Steps
1. Create new request: **+ Tab** → **Post**
2. Enter URL: `{{base_url}}/predict`
3. Go to **Headers** tab
   - Verify `Content-Type: application/json` exists
4. Go to **Body** tab
   - Select **raw**
   - Select **JSON** from dropdown
   - Paste sample request body (see below)
5. Click **Send**

#### Sample Request Body (On-Track Student)
```json
{
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
```

#### Expected Response (200 OK)
```json
{
  "student_id": "s_1000",
  "course_id": "c_1",
  "at_risk": false,
  "risk_probability": 0.1234,
  "confidence": 0.8765,
  "recommendation": "Student is on track. Continue current study plan.",
  "timestamp": "2024-04-22T10:30:00.123456"
}
```

#### 🎯 Purpose
Test single student risk prediction.

---

#### Sample Request Body (At-Risk Student)
```json
{
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
```

#### Expected Response (200 OK)
```json
{
  "student_id": "s_1001",
  "course_id": "c_1",
  "at_risk": true,
  "risk_probability": 0.8765,
  "confidence": 0.9234,
  "recommendation": "High risk. Immediate intervention required - contact academic advisor.",
  "timestamp": "2024-04-22T10:30:00.123456"
}
```

---

### 3. Batch Prediction

#### Request Details
- **Method**: `POST`
- **URL**: `{{base_url}}/predict-batch`
- **Headers**: 
  - `Content-Type: application/json`
- **Body**: JSON (raw)

#### Steps
1. Create new request: **+ Tab** → **Post**
2. Enter URL: `{{base_url}}/predict-batch`
3. Go to **Headers** tab
   - Verify `Content-Type: application/json`
4. Go to **Body** tab
   - Select **raw** → **JSON**
   - Paste sample batch request (see below)
5. Click **Send**

#### Sample Request Body
```json
{
  "students": [
    {
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
    },
    {
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
    },
    {
      "student_id": "s_1002",
      "course_id": "c_3",
      "attendance_rate": 0.701,
      "avg_session_duration_pct": 0.682,
      "consecutive_absences": 1,
      "assignment_submission_rate": 0.816,
      "avg_assignment_score": 72.92,
      "late_submission_count": 0,
      "exam_score_avg": 76.92,
      "exam_improvement_trend": -0.15
    }
  ]
}
```

#### Expected Response (200 OK)
```json
{
  "total_students": 3,
  "at_risk_count": 1,
  "on_track_count": 2,
  "predictions": [
    {
      "student_id": "s_1000",
      "course_id": "c_1",
      "at_risk": false,
      "risk_probability": 0.1234,
      "confidence": 0.8765,
      "recommendation": "Student is on track. Continue current study plan.",
      "timestamp": "2024-04-22T10:30:00.123456"
    },
    {
      "student_id": "s_1001",
      "course_id": "c_1",
      "at_risk": true,
      "risk_probability": 0.8765,
      "confidence": 0.9234,
      "recommendation": "High risk. Immediate intervention required - contact academic advisor.",
      "timestamp": "2024-04-22T10:30:00.123456"
    },
    {
      "student_id": "s_1002",
      "course_id": "c_3",
      "at_risk": false,
      "risk_probability": 0.2345,
      "confidence": 0.8234,
      "recommendation": "Student is on track. Continue current study plan.",
      "timestamp": "2024-04-22T10:30:00.123456"
    }
  ],
  "processing_time": 0.0234
}
```

#### 🎯 Purpose
Test batch predictions for multiple students efficiently.

---

### 4. Model Information

#### Request Details
- **Method**: `GET`
- **URL**: `{{base_url}}/model-info`
- **Headers**: None required

#### Steps
1. Create new request: **+ Tab** → **Get**
2. Enter URL: `{{base_url}}/model-info`
3. Click **Send**

#### Expected Response (200 OK)
```json
{
  "model_type": "RandomForestClassifier",
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
  "target_classes": [
    "On Track",
    "At Risk"
  ],
  "version": "1.0.0"
}
```

#### 🎯 Purpose
Get model details, features, and version information.

---

## Sample Requests

### Quick Copy-Paste Reference

#### On-Track Student (Low Risk)
```json
{
  "student_id": "s_1000",
  "course_id": "c_1",
  "attendance_rate": 0.95,
  "avg_session_duration_pct": 0.90,
  "consecutive_absences": 0,
  "assignment_submission_rate": 0.95,
  "avg_assignment_score": 85,
  "late_submission_count": 0,
  "exam_score_avg": 88,
  "exam_improvement_trend": 0.15
}
```

#### Moderate Risk Student
```json
{
  "student_id": "s_2000",
  "course_id": "c_2",
  "attendance_rate": 0.70,
  "avg_session_duration_pct": 0.65,
  "consecutive_absences": 3,
  "assignment_submission_rate": 0.60,
  "avg_assignment_score": 62,
  "late_submission_count": 3,
  "exam_score_avg": 60,
  "exam_improvement_trend": -0.05
}
```

#### High-Risk Student
```json
{
  "student_id": "s_3000",
  "course_id": "c_1",
  "attendance_rate": 0.40,
  "avg_session_duration_pct": 0.35,
  "consecutive_absences": 8,
  "assignment_submission_rate": 0.25,
  "avg_assignment_score": 35,
  "late_submission_count": 10,
  "exam_score_avg": 25,
  "exam_improvement_trend": -0.25
}
```

---

## Advanced Testing

### Using Pre-request Script

Add validation before sending request:

1. Go to **Pre-request Script** tab
2. Add this script:

```javascript
// Validate base_url is set
if (!pm.environment.get("base_url")) {
    console.error("base_url not set in environment");
}

// Log request details
console.log("Sending request to: " + pm.environment.get("base_url"));
console.log("Timestamp: " + new Date().toISOString());
```

3. Click **Send** to execute

### Using Tests (Assertions)

Add validation after response:

1. Go to **Tests** tab
2. Add these tests:

```javascript
// Test 1: Status code is 200
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

// Test 2: Response has required fields
pm.test("Response has required fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property("student_id");
    pm.expect(jsonData).to.have.property("at_risk");
    pm.expect(jsonData).to.have.property("risk_probability");
});

// Test 3: Risk probability is between 0 and 1
pm.test("Risk probability is valid (0-1)", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.risk_probability).to.be.above(0);
    pm.expect(jsonData.risk_probability).to.be.below(1);
});

// Test 4: Recommendation exists
pm.test("Recommendation is not empty", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.recommendation).to.not.be.empty;
});
```

3. Click **Send** to run tests with assertions

---

## Error Testing

### Test Validation Errors

#### Missing Required Field
**URL**: `{{base_url}}/predict`
**Body** (missing `student_id`):
```json
{
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
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "loc": ["body", "student_id"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### Invalid Data Type
**Body** (attendance_rate as string):
```json
{
  "student_id": "s_1000",
  "course_id": "c_1",
  "attendance_rate": "not_a_number",
  "avg_session_duration_pct": 0.54,
  "consecutive_absences": 2,
  "assignment_submission_rate": 0.832,
  "avg_assignment_score": 71.19,
  "late_submission_count": 2,
  "exam_score_avg": 71.17,
  "exam_improvement_trend": 0.0376
}
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "loc": ["body", "attendance_rate"],
      "msg": "value is not a valid float",
      "type": "type_error.float"
    }
  ]
}
```

#### Out of Range Value
**Body** (attendance_rate > 1):
```json
{
  "student_id": "s_1000",
  "course_id": "c_1",
  "attendance_rate": 1.5,
  "avg_session_duration_pct": 0.54,
  "consecutive_absences": 2,
  "assignment_submission_rate": 0.832,
  "avg_assignment_score": 71.19,
  "late_submission_count": 2,
  "exam_score_avg": 71.17,
  "exam_improvement_trend": 0.0376
}
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "loc": ["body", "attendance_rate"],
      "msg": "ensure this value is less than or equal to 1",
      "type": "value_error.number.not_le",
      "ctx": {"limit_value": 1}
    }
  ]
}
```

---

## Postman Collection

### Export Collection

1. Click collection menu → **Export**
2. Select **Postman v2.1** format
3. Save as `LMS-Risk-Predictor-API.json`

### Import Collection

1. Click **Import** (top-left)
2. Select the `.json` file
3. Collection appears in sidebar

---

## Testing Workflow

### Step-by-Step Guide

```
1. Start API
   └─ docker-compose up

2. Open Postman
   └─ Select environment: LMS-API-Dev

3. Test Health
   └─ GET /health → Verify "healthy" status

4. Test Single Prediction (On-Track)
   └─ POST /predict → Verify at_risk: false

5. Test Single Prediction (At-Risk)
   └─ POST /predict → Verify at_risk: true

6. Test Batch Prediction
   └─ POST /predict-batch → Verify multiple predictions

7. Test Model Info
   └─ GET /model-info → Verify features list

8. Test Error Cases
   └─ Send invalid data → Verify 422 response

9. Run Test Suite
   └─ Execute Tests tab → Verify all assertions pass
```

---

## Monitoring Response

### View Response Metrics

In Postman response panel:

| Metric | Location | Example |
|--------|----------|---------|
| **Status** | Top-right | `200 OK` |
| **Time** | Top-right | `145ms` |
| **Size** | Top-right | `450B` |
| **Body** | Main panel | JSON response |
| **Headers** | Headers tab | Content-Type, etc |
| **Cookies** | Cookies tab | Session info |

### Response Pretty-Print

1. Click **Pretty** button in response
2. Select **JSON** format
3. View formatted response

---

## Common Issues & Fixes

### ❌ "Could not get any response"
**Cause**: API not running
**Fix**: Run `docker-compose up` and verify port 8000 is accessible

### ❌ 422 Unprocessable Entity
**Cause**: Invalid request data
**Fix**: Check request body matches expected schema

### ❌ CORS Error
**Cause**: Frontend trying to access API from different origin
**Fix**: Verify CORS_ORIGINS in config includes your domain

### ❌ "Cannot GET /predict"
**Cause**: Wrong HTTP method (using GET instead of POST)
**Fix**: Ensure method is POST for /predict endpoint

### ❌ Empty Response
**Cause**: Model file not found
**Fix**: Verify `lms_risk_model.pkl` exists in project directory

---

## Tips & Tricks

### 💡 Save Request
After configuring request:
1. Click **Save** button
2. Name: `Predict - On Track Student`
3. Collection: `LMS Risk Predictor API`
4. Click **Save**

### 💡 Duplicate Request
1. Right-click request → **Duplicate**
2. Modify body for different test case
3. Save with new name

### 💡 Use Postman Variables
In body or URL, use: `{{variable_name}}`

Example body:
```json
{
  "student_id": "{{student_id}}",
  "course_id": "{{course_id}}",
  ...
}
```

Then set in environment or collection variables.

### 💡 Keyboard Shortcuts
- **Send**: `Ctrl+Enter` (Windows) / `Cmd+Enter` (Mac)
- **Save**: `Ctrl+S` (Windows) / `Cmd+S` (Mac)
- **Format**: `Ctrl+I` (Windows) / `Cmd+I` (Mac)

### 💡 View Documentation
In Postman, hover over **?** icon for help on any feature.

---

## Summary

✅ Health check working  
✅ Single predictions working  
✅ Batch predictions working  
✅ Model info accessible  
✅ Error handling tested  
✅ All assertions passing  

**Your API is ready for production!** 🚀
