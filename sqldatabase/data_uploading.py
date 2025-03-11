#!/usr/bin/env python3
import pandas as pd
from sqlalchemy import create_engine

# Step 1: Read the CSV file
csv_file = "indian_liver_patient.csv"  # Path to your CSV file
data = pd.read_csv(csv_file)

# Step 2: Clean and preprocess the data
# Rename columns for consistency
data.rename(columns={
    'Total_Protiens': 'Total_Proteins',  # Fix column name
    'Dataset': 'Diagnosis'  # Rename 'Dataset' to 'Diagnosis'
}, inplace=True)

# Fill missing values in 'Albumin_and_Globulin_Ratio' with the mean
data['Albumin_and_Globulin_Ratio'] = data['Albumin_and_Globulin_Ratio'].fillna(data['Albumin_and_Globulin_Ratio'].mean())

# Convert 'Gender' to binary (1 for Male, 0 for Female)
data['Gender'] = data['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

# Convert 'Diagnosis' to binary (1 for Liver disease, 0 for No disease)
data['Diagnosis'] = data['Diagnosis'].apply(lambda x: 1 if x == 1 else 0)

# Step 3: Connect to the MySQL database
# Replace with your database credentials
db_username = 'Ashleen'
db_password = 'password'
db_host = 'localhost'
db_name = 'liver_disease_db'

# Create a connection string
connection_string = f"mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}"

# Create a SQLAlchemy engine
engine = create_engine(connection_string)

# Step 4: Insert data into the database
# Insert into 'patients' table
patients_data = data[['Age', 'Gender']].copy()
patients_data.to_sql('patients', con=engine, if_exists='append', index=False)

# Retrieve the auto-generated patient_ids
query = "SELECT patient_id FROM patients"
patient_ids = pd.read_sql(query, con=engine)

# Add patient_ids to the original data
data['patient_id'] = patient_ids['patient_id']

# Insert into 'medical_tests' table
medical_tests_data = data[[
    'patient_id', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase',
    'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins',
    'Albumin', 'Albumin_and_Globulin_Ratio'
]].copy()
medical_tests_data.to_sql('medical_tests', con=engine, if_exists='append', index=False)

# Retrieve the auto-generated test_ids
query = "SELECT test_id FROM medical_tests"
test_ids = pd.read_sql(query, con=engine)

# Add test_ids to the original data
data['test_id'] = test_ids['test_id']

# Insert into 'diagnosis' table
diagnosis_data = data[['patient_id', 'Diagnosis']].copy()
diagnosis_data.to_sql('diagnosis', con=engine, if_exists='append', index=False)

print("Data inserted successfully!")
