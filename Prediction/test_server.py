from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional
import uvicorn
import random

app = FastAPI(title="Liver Disease Prediction Test Server")

# Sample data models
class Patient(BaseModel):
    patient_id: int
    age: int
    gender: str  # "Male" or "Female"

class MedicalTest(BaseModel):
    test_id: int
    patient_id: int
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: float
    alamine_aminotransferase: float
    aspartate_aminotransferase: float
    total_proteins: float
    albumin: float
    albumin_globulin_ratio: float

# Sample data
patients = [
    Patient(patient_id=1, age=45, gender="Male"),
    Patient(patient_id=2, age=32, gender="Female"),
    Patient(patient_id=3, age=60, gender="Male"),
    Patient(patient_id=4, age=38, gender="Female")
]

# Sample medical tests - values chosen to represent both healthy and potentially diseased states
medical_tests = [
    MedicalTest(
        test_id=1, 
        patient_id=1,
        total_bilirubin=1.2,
        direct_bilirubin=0.4,
        alkaline_phosphotase=290,
        alamine_aminotransferase=80,
        aspartate_aminotransferase=70,
        total_proteins=6.8,
        albumin=3.4,
        albumin_globulin_ratio=1.0
    ),
    MedicalTest(
        test_id=2, 
        patient_id=2,
        total_bilirubin=0.7,
        direct_bilirubin=0.2,
        alkaline_phosphotase=190,
        alamine_aminotransferase=30,
        aspartate_aminotransferase=35,
        total_proteins=7.2,
        albumin=4.1,
        albumin_globulin_ratio=1.3
    ),
    MedicalTest(
        test_id=3, 
        patient_id=3,
        total_bilirubin=2.1,
        direct_bilirubin=1.1,
        alkaline_phosphotase=420,
        alamine_aminotransferase=120,
        aspartate_aminotransferase=155,
        total_proteins=6.1,
        albumin=2.9,
        albumin_globulin_ratio=0.8
    ),
    MedicalTest(
        test_id=4, 
        patient_id=4,
        total_bilirubin=0.9,
        direct_bilirubin=0.3,
        alkaline_phosphotase=210,
        alamine_aminotransferase=25,
        aspartate_aminotransferase=30,
        total_proteins=7.4,
        albumin=4.2,
        albumin_globulin_ratio=1.3
    )
]

# API Endpoints
@app.get("/")
def read_root():
    return {"message": "Liver Disease Prediction Test Server"}

@app.get("/patients/")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for patient in patients:
        if patient.patient_id == patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/patients/latest/")
def get_latest_patient():
    if not patients:
        raise HTTPException(status_code=404, detail="No patients found")
    return patients[-1]  # Return the last patient in the list

@app.get("/medical_tests/")
def get_medical_tests():
    return medical_tests

@app.get("/medical_tests/patient/{patient_id}")
def get_medical_test_by_patient(patient_id: int):
    for test in medical_tests:
        if test.patient_id == patient_id:
            return test
    raise HTTPException(status_code=404, detail="Medical test not found for this patient")

if __name__ == "__main__":
    print("Starting test server on http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")
    uvicorn.run(app, host="127.0.0.1", port=8000)