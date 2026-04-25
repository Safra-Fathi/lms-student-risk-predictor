# Next.js Integration Guide

## Overview
This API is designed to work seamlessly with Next.js frontend applications. It provides prediction endpoints for student risk assessment.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required. For production, consider adding JWT or API key authentication.

## API Endpoints

### 1. Health Check
**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_status": "loaded",
  "timestamp": "2024-04-22T10:30:00"
}
```

### 2. Single Student Prediction
**Endpoint:** `POST /predict`

**Request Body:**
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

**Response:**
```json
{
  "student_id": "s_1000",
  "course_id": "c_1",
  "at_risk": false,
  "risk_probability": 0.1234,
  "confidence": 0.8765,
  "recommendation": "Student is on track. Continue current study plan.",
  "timestamp": "2024-04-22T10:30:00"
}
```

### 3. Batch Prediction
**Endpoint:** `POST /predict-batch`

**Request Body:**
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
    }
  ]
}
```

**Response:**
```json
{
  "total_students": 2,
  "at_risk_count": 1,
  "on_track_count": 1,
  "predictions": [
    {
      "student_id": "s_1000",
      "course_id": "c_1",
      "at_risk": false,
      "risk_probability": 0.1234,
      "confidence": 0.8765,
      "recommendation": "Student is on track. Continue current study plan.",
      "timestamp": "2024-04-22T10:30:00"
    },
    {
      "student_id": "s_1001",
      "course_id": "c_1",
      "at_risk": true,
      "risk_probability": 0.8765,
      "confidence": 0.9234,
      "recommendation": "High risk. Immediate intervention required - contact academic advisor.",
      "timestamp": "2024-04-22T10:30:00"
    }
  ],
  "processing_time": 0.1234
}
```

### 4. Model Information
**Endpoint:** `GET /model-info`

**Response:**
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
  "target_classes": ["On Track", "At Risk"],
  "version": "1.0.0"
}
```

## Next.js Integration Examples

### Setup API Client

Create `lib/api-client.ts`:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface StudentData {
  student_id: string;
  course_id: string;
  attendance_rate: number;
  avg_session_duration_pct: number;
  consecutive_absences: number;
  assignment_submission_rate: number;
  avg_assignment_score: number;
  late_submission_count: number;
  exam_score_avg: number;
  exam_improvement_trend: number;
}

export interface PredictionResult {
  student_id: string;
  course_id: string;
  at_risk: boolean;
  risk_probability: number;
  confidence: number;
  recommendation: string;
  timestamp: string;
}

export async function predictStudent(student: StudentData): Promise<PredictionResult> {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(student),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function predictBatch(students: StudentData[]) {
  const response = await fetch(`${API_BASE_URL}/predict-batch`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ students }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  return response.json();
}

export async function getHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);
  return response.json();
}
```

### Usage in Next.js Component

```typescript
'use client';

import { useState } from 'react';
import { predictStudent, StudentData, PredictionResult } from '@/lib/api-client';

export default function PredictionForm() {
  const [result, setResult] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const formData = new FormData(e.currentTarget);
      const student: StudentData = {
        student_id: formData.get('student_id') as string,
        course_id: formData.get('course_id') as string,
        attendance_rate: parseFloat(formData.get('attendance_rate') as string),
        avg_session_duration_pct: parseFloat(formData.get('avg_session_duration_pct') as string),
        consecutive_absences: parseInt(formData.get('consecutive_absences') as string),
        assignment_submission_rate: parseFloat(formData.get('assignment_submission_rate') as string),
        avg_assignment_score: parseFloat(formData.get('avg_assignment_score') as string),
        late_submission_count: parseInt(formData.get('late_submission_count') as string),
        exam_score_avg: parseFloat(formData.get('exam_score_avg') as string),
        exam_improvement_trend: parseFloat(formData.get('exam_improvement_trend') as string),
      };

      const prediction = await predictStudent(student);
      setResult(prediction);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {/* Form fields for student data */}
      </form>
      {result && (
        <div>
          <h2>Prediction Result</h2>
          <p>At Risk: {result.at_risk ? 'Yes' : 'No'}</p>
          <p>Risk Probability: {(result.risk_probability * 100).toFixed(2)}%</p>
          <p>Recommendation: {result.recommendation}</p>
        </div>
      )}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
}
```

## Environment Variables

Create `.env.local` in your Next.js project:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## CORS Configuration

The API has CORS enabled for all origins in development. For production, update the `allow_origins` in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `422`: Validation error (invalid input)
- `500`: Server error

Example error response:
```json
{
  "detail": "Prediction failed: Invalid model state"
}
```

## Performance Tips

1. **Batch Predictions**: Use `/predict-batch` for multiple students - it's more efficient
2. **Caching**: Consider caching model predictions on the frontend for identical requests
3. **Error Handling**: Always implement proper error handling in your frontend

## Testing the API

Access the interactive API documentation:
```
http://localhost:8000/docs
```

This provides a Swagger UI where you can test all endpoints directly.
