#!/usr/bin/env python3
import pandas as pd
from pymongo import MongoClient

# MongoDB URI
uri = "mongodb+srv://achivanga:WipaaGQctjY4qiFl@cluster0.z131u.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


client = MongoClient(uri)


db = client['liver_disease_db']


csv_file = 'indian_liver_patient.csv'
data = pd.read_csv(csv_file)


data.rename(columns={
    'Total_Protiens': 'Total_Proteins',  
    'Dataset': 'Diagnosis'  
}, inplace=True)

# Filling missing values
data['Albumin_and_Globulin_Ratio'] = data['Albumin_and_Globulin_Ratio'].fillna(data['Albumin_and_Globulin_Ratio'].mean())

# Converting 'Gender' and 'Diagnosis' to binary
data['Gender'] = data['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
data['Diagnosis'] = data['Diagnosis'].apply(lambda x: 1 if x == 1 else 0)

# Creating the 'patients' collection and insert data
patients_data = data[['Age', 'Gender']].copy()
patients_collection = db['patients']
patients_data_dict = patients_data.to_dict(orient='records')
patients_collection.insert_many(patients_data_dict)

# getting patient_ids after inserting into 'patients'
patient_ids = [patient['_id'] for patient in patients_collection.find()]

# Adding patient_ids to the original data
data['patient_id'] = patient_ids

# Creating the 'medical_tests' collection and insert data
medical_tests_data = data[['patient_id', 'Total_Bilirubin', 'Direct_Bilirubin', 'Alkaline_Phosphotase', 
                           'Alamine_Aminotransferase', 'Aspartate_Aminotransferase', 'Total_Proteins', 
                           'Albumin', 'Albumin_and_Globulin_Ratio']].copy()

medical_tests_collection = db['medical_tests']
medical_tests_data_dict = medical_tests_data.to_dict(orient='records')
medical_tests_collection.insert_many(medical_tests_data_dict)

# Create the 'diagnosis' collection and insert data
diagnosis_data = data[['patient_id', 'Diagnosis']].copy()
diagnosis_collection = db['diagnosis']
diagnosis_data_dict = diagnosis_data.to_dict(orient='records')
diagnosis_collection.insert_many(diagnosis_data_dict)

print("Data inserted successfully into MongoDB!")
