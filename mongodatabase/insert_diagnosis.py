#!/usr/bin/env python3

import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieving MongoDB URI from the environment variable
uri = os.getenv("MONGO_URI")

# Reading the CSV file into a pandas DataFrame
csv_file = "indian_liver_patient.csv"  # Path to your CSV file
data = pd.read_csv(csv_file)

# Connecting to MongoDB
client = MongoClient(uri)
db = client.liver_disease_db

# Preparing diagnosis data
diagnosis_data = data[['Dataset']].copy()
diagnosis_data['Diagnosis'] = diagnosis_data['Dataset'].apply(lambda x: 1 if x == 1 else 0)  # Converting to binary
diagnosis_data_dict = diagnosis_data.to_dict(orient='records')

# Inserting data into the diagnosis collection
diagnosis_collection = db.diagnosis
diagnosis_collection.insert_many(diagnosis_data_dict)

print("Diagnosis data inserted successfully!")
