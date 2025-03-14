import requests
import pickle
import pandas as pd
import numpy as np
from typing import Dict, Any
import os

# Load configuration
API_BASE_URL = "http://127.0.0.1:8000"  # Default to test server URL

def load_model_and_features():
    """Load the trained model and feature names"""
    try:
        with open('models/liver_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        with open('models/feature_names.pkl', 'rb') as f:
            feature_names = pickle.load(f)
            
        return model, feature_names
    except FileNotFoundError:
        print("Error: Model files not found. Please run train_model.py first.")
        return None, None

def preprocess_patient_data(patient_data: Dict[str, Any], medical_data: Dict[str, Any]) -> pd.DataFrame:
    """Preprocess patient and medical test data for prediction"""
    # Convert gender to binary format (1: Male, 0: Female)
    gender_binary = 1 if patient_data.get('gender', '').lower() == 'male' else 0
    
    # Create a dataframe with the right features in the right order
    data = pd.DataFrame({
        'Age': [patient_data.get('age', 0)],
        'Gender': [gender_binary],
        'Total_Bilirubin': [medical_data.get('total_bilirubin', 0.0)],
        'Direct_Bilirubin': [medical_data.get('direct_bilirubin', 0.0)],
        'Alkaline_Phosphotase': [medical_data.get('alkaline_phosphotase', 0.0)],
        'Alamine_Aminotransferase': [medical_data.get('alamine_aminotransferase', 0.0)],
        'Aspartate_Aminotransferase': [medical_data.get('aspartate_aminotransferase', 0.0)],
        'Total_Proteins': [medical_data.get('total_proteins', 0.0)],
        'Albumin': [medical_data.get('albumin', 0.0)],
        'Albumin_and_Globulin_Ratio': [medical_data.get('albumin_globulin_ratio', 0.0)]
    })
    
    return data

def fetch_patient_data():
    """Fetch the latest patient data from the API"""
    try:
        # Get latest patient
        patient_response = requests.get(f"{API_BASE_URL}/patients/latest/")
        if patient_response.status_code != 200:
            print(f"Error fetching patient data: {patient_response.status_code}")
            return None, None
        
        patient = patient_response.json()
        patient_id = patient.get('patient_id')
        
        # Get medical test data for this patient
        med_test_response = requests.get(f"{API_BASE_URL}/medical_tests/patient/{patient_id}")
        if med_test_response.status_code != 200:
            print(f"Error fetching medical test data: {med_test_response.status_code}")
            return patient, None
            
        medical_test = med_test_response.json()
        return patient, medical_test
    
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        print("Is the API server running? If using test server, run test_server.py first.")
        return None, None

def predict_liver_disease():
    """Main function to predict liver disease using the API data"""
    print("Liver Disease Prediction System - API Mode")
    print("-----------------------------------------")
    
    # Load model and features
    model, feature_names = load_model_and_features()
    if model is None or feature_names is None:
        return
    
    # Fetch patient data from API
    print("Fetching patient data from API...")
    patient, medical_test = fetch_patient_data()
    
    if patient is None:
        print("Failed to retrieve patient data. Exiting.")
        return
        
    if medical_test is None:
        print("Failed to retrieve medical test data. Exiting.")
        return
    
    # Show the data we're using for prediction
    print("\nPatient Information:")
    print(f"ID: {patient.get('patient_id')}")
    print(f"Age: {patient.get('age')}")
    print(f"Gender: {patient.get('gender')}")
    
    print("\nMedical Test Results:")
    print(f"Total Bilirubin: {medical_test.get('total_bilirubin', 'N/A')}")
    print(f"Direct Bilirubin: {medical_test.get('direct_bilirubin', 'N/A')}")
    print(f"Alkaline Phosphotase: {medical_test.get('alkaline_phosphotase', 'N/A')}")
    print(f"Alamine Aminotransferase: {medical_test.get('alamine_aminotransferase', 'N/A')}")
    print(f"Aspartate Aminotransferase: {medical_test.get('aspartate_aminotransferase', 'N/A')}")
    print(f"Total Proteins: {medical_test.get('total_proteins', 'N/A')}")
    print(f"Albumin: {medical_test.get('albumin', 'N/A')}")
    print(f"Albumin/Globulin Ratio: {medical_test.get('albumin_globulin_ratio', 'N/A')}")
    
    # Preprocess the data
    preprocessed_data = preprocess_patient_data(patient, medical_test)
    
    # Ensure the columns match the expected feature names
    preprocessed_data = preprocessed_data.reindex(columns=feature_names)
    
    # Make prediction
    prediction = model.predict(preprocessed_data)[0]
    prediction_proba = model.predict_proba(preprocessed_data)[0]
    
    # Interpret results
    print("\nPrediction Results:")
    print("-" * 40)
    
    if prediction == 1:
        confidence = prediction_proba[1] * 100
        print(f"⚠️  Liver Disease Likely - Confidence: {confidence:.1f}%")
        print("\nRecommendation: The patient should consult with a hepatologist for further evaluation.")
    else:
        confidence = prediction_proba[0] * 100
        print(f"✅ No Liver Disease Detected - Confidence: {confidence:.1f}%")
        print("\nRecommendation: The patient appears to have normal liver function values.")
    
    print("\nNote: This prediction is based on machine learning and should not replace professional medical advice.")

if __name__ == "__main__":
    predict_liver_disease()