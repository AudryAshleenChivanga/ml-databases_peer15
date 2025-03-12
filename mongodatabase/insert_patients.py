#!/usr/bin/env python3
import os
from pymongo import MongoClient
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve MongoDB URI from the environment variable
uri = os.getenv("MONGO_URI")

# Reading the CSV file
csv_file = "indian_liver_patient.csv"  
data = pd.read_csv(csv_file)

# Connecting to MongoDB
client = MongoClient(uri)
db = client.liver_disease_db

# Preparing data for patients collection
patients_data = data[['Age', 'Gender']].copy()
patients_data['Gender'] = patients_data['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

# Inserting data into patients collection
patients_collection = db.patients
patients_data_dict = patients_data.to_dict(orient='records')
patients_collection.insert_many(patients_data_dict)

print("Patients data inserted successfully!")
