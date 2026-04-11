from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

model = joblib.load('lms_risk_model.pkl')

app = FastAPI(title="LMS Student Risk Prediction API")