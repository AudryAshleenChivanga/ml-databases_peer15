#!/usr/bin/env python3

import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve MongoDB URI from the environment variable
uri = os.getenv("MONGO_URI")

# Path to the CSV file
csv_file = "indian_liver_patient.csv"  # Path to your CSV file
data = pd.read_csv(csv_file)

# Connecting to MongoDB
client = MongoClient(uri)
db = client.liver_disease_db

# Inserting data into patients collection
patients_data = data[['Age', 'Gender']].copy()
patients_data_dict = patients_data.to_dict(orient='records')
patients_collection = db.patients
patients_collection.insert_many(patients_data_dict)

# Inserting data into medical_tests collection
medical_tests_data = data[[
    'Age', 'Gender', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase',
    'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Protiens', 'Albumin', 
    'Albumin_and_Globulin_Ratio'
]].copy()

medical_tests_data_dict = medical_tests_data.to_dict(orient='records')
medical_tests_collection = db.medical_tests
medical_tests_collection.insert_many(medical_tests_data_dict)

print("Medical tests data inserted successfully!")
