#!/usr/bin/env python3

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Loading environment variables from the .env file
load_dotenv()

# Retrieving MongoDB URI from the environment variable
uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(uri)
db = client.liver_disease_db

# Retrieving collections
patients_collection = db.patients
medical_tests_collection = db.medical_tests
diagnosis_collection = db.diagnosis

# Checking data in the 'patients' collection
patients_count = patients_collection.count_documents({})
print(f"Patients Count: {patients_count}")

# Checking data in the 'medical_tests' collection
medical_tests_count = medical_tests_collection.count_documents({})
print(f"Medical Tests Count: {medical_tests_count}")

# Checking data in the 'diagnosis' collection
diagnosis_count = diagnosis_collection.count_documents({})
print(f"Diagnosis Count: {diagnosis_count}")

#  printing the first few records in each collection to ensure data format
print("\nSample Patients Data:")
for patient in patients_collection.find().limit(5):
    print(patient)

print("\nSample Medical Tests Data:")
for test in medical_tests_collection.find().limit(5):
    print(test)

print("\nSample Diagnosis Data:")
for diag in diagnosis_collection.find().limit(5):
    print(diag)
