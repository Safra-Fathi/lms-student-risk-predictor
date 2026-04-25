# LMS Student Risk Predictor

A machine learning system that predicts whether a student is at risk of failing based on attendance, assignments, and exam data. Includes a comprehensive FastAPI REST API designed for Next.js integration.

## Features

- **Machine Learning Models**: Logistic Regression, Random Forest, XGBoost
- **REST API**: FastAPI with CORS support for frontend integration
- **Single & Batch Predictions**: Predict one or multiple students efficiently
- **CORS-Enabled**: Ready for Next.js and other frontend frameworks
- **Docker Support**: Containerized for easy deployment
- **Interactive API Docs**: Swagger UI for testing endpoints

## Input Features

- `attendance_rate` - Attendance rate (0-1)
- `avg_session_duration_pct` - Average session duration percentage (0-1)
- `consecutive_absences` - Number of consecutive absences
- `assignment_submission_rate` - Assignment submission rate (0-1)
- `avg_assignment_score` - Average assignment score (0-100)
- `late_submission_count` - Number of late submissions
- `exam_score_avg` - Average exam score (0-100)
- `exam_improvement_trend` - Exam score improvement trend

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Build and run
docker-compose up --build

# API will be available at http://localhost:8000
```

### Option 2: Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn main:app --reload

# Access at http://localhost:8000
```

## API Endpoints

### Health Check
```
GET /health
```

### Single Student Prediction
```
POST /predict
Content-Type: application/json

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

### Batch Predictions
```
POST /predict-batch
Content-Type: application/json

{
  "students": [
    { /* student 1 data */ },
    { /* student 2 data */ }
  ]
}
```

### Model Information
```
GET /model-info
```

## Interactive Documentation

Access the Swagger UI at:
```
http://localhost:8000/docs
```

## Next.js Integration

See [NEXTJS_INTEGRATION.md](./NEXTJS_INTEGRATION.md) for detailed integration guide with code examples.

### Quick Setup

Create `lib/api-client.ts`:
```typescript
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function predictStudent(student: StudentData) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(student),
  });
  return response.json();
}
```

Set environment variable in `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn
- **ML**: pandas, scikit-learn, XGBoost
- **Deployment**: Docker, Docker Compose
- **Frontend Compatible**: CORS-enabled for any frontend framework

## Project Structure

```
.
├── main.py                    # FastAPI application
├── config.py                  # Configuration settings
├── utils.py                   # Utility functions
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker image definition
├── docker-compose.yml         # Docker Compose configuration
├── lms_risk_model.pkl         # Trained ML model
├── lms_student_dataset.csv    # Training dataset
├── studentmarksprediction.ipynb # Model training notebook
├── NEXTJS_INTEGRATION.md      # Next.js integration guide
└── README.md                  # This file
```

## Development

### Training the Model
Open the Jupyter notebook and run all cells:
```bash
jupyter notebook studentmarksprediction.ipynb
```

### Environment Variables
Copy `.env.example` to `.env` and modify as needed:
```bash
cp .env.example .env
```

### Testing

Using curl:
```bash
# Single prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# Health check
curl http://localhost:8000/health
```

## API Response Format

**Success Response:**
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

**Error Response:**
```json
{
  "detail": "Prediction failed: Invalid input data"
}
```

## Deployment

### Production Deployment

For production deployment, update:
1. **CORS Origins** in `main.py` with your domain
2. **Model Path** if using cloud storage
3. **Environment Variables** in `docker-compose.yml`

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Performance Notes

- **Batch Processing**: Use `/predict-batch` for multiple predictions (~0.001s per student)
- **Single Prediction**: ~0.01-0.05s per request
- **Model Size**: ~5-10MB (depends on model type)

## License

[Add your license here]

## Support

For issues or questions, please open an issue on the repository.
