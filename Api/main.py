from fastapi import FastAPI, HTTPException
import mysql.connector
import os
from pydantic import BaseModel
from mysql.connector import Error

# Initialize FastAPI app
app = FastAPI()

# Database connection configuration
db_config = {
    "host": os.getenv("DATABASE_HOST", "localhost"),  # Default to localhost if not set
    "user": os.getenv("DATABASE_USER", "root"),   # Default to app_user if not set
    "password": os.getenv("DATABASE_PASSWORD", "StrongPassword123!"),  # Default password
    "database": os.getenv("DATABASE_NAME", "liver_disease_db"),  # Default database name
}

# Helper function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
        else:
            raise HTTPException(status_code=500, detail="Unable to connect to the database.")
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Function to execute SQL from a file
def execute_sql_file(sql_file: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        with open(sql_file, 'r') as file:
            sql_script = file.read()
        # Execute the SQL script
        for result in cursor.execute(sql_script, multi=True):
            pass
        connection.commit()
        print(f"Executed SQL file: {sql_file}")
    except Exception as e:
        print(f"Error executing SQL file {sql_file}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error executing SQL file: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Execute schema.sql and data.sql on startup
@app.on_event("startup")
def initialize_database():
    try:
        print("Initializing database...")
        # Execute schema.sql to create tables
        execute_sql_file("sqlSchema.sql")
        # Execute data.sql to insert data
        execute_sql_file("data.sql")
        print("Database initialization complete!")
    except Exception as e:
        print(f"Database initialization failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database initialization failed: {str(e)}")

# Pydantic models for request validation
class PatientCreate(BaseModel):
    age: int
    gender: str

class MedicalTestCreate(BaseModel):
    patient_id: int
    total_bilirubin: float
    direct_bilirubin: float
    alkaline_phosphotase: int
    alamine_aminotransferase: int  # Fixed typo here
    aspartate_aminotransferase: int
    total_proteins: float
    albumin: float
    albumin_and_globulin_ratio: float

class DiagnosisCreate(BaseModel):
    patient_id: int
    diagnosis: int

# Create (POST) - Add a new patient
@app.post("/patients/")
def create_patient(patient: PatientCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO patients (age, gender) VALUES (%s, %s)"
        cursor.execute(query, (patient.age, patient.gender))
        connection.commit()
        return {"message": "Patient created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Read (GET) - Get all patients
@app.get("/patients/")
def get_patients():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM patients"
        cursor.execute(query)
        patients = cursor.fetchall()
        return {"patients": patients}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Update (PUT) - Update a patient
@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, patient: PatientCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "UPDATE patients SET age = %s, gender = %s WHERE patient_id = %s"
        cursor.execute(query, (patient.age, patient.gender, patient_id))
        connection.commit()
        return {"message": "Patient updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Delete (DELETE) - Delete a patient
@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM patients WHERE patient_id = %s"
        cursor.execute(query, (patient_id,))
        connection.commit()
        return {"message": "Patient deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Create (POST) - Add a new medical test
@app.post("/medical_tests/")
def create_medical_test(test: MedicalTestCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO medical_tests (
            patient_id, total_bilirubin, direct_bilirubin, alkaline_phosphotase,
            alamine_aminotransferase, aspartate_aminotransferase, total_proteins,
            albumin, albumin_and_globulin_ratio
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            test.patient_id, test.total_bilirubin, test.direct_bilirubin,
            test.alkaline_phosphotase, test.alamine_aminotransferase,
            test.aspartate_aminotransferase, test.total_proteins,
            test.albumin, test.albumin_and_globulin_ratio
        ))
        connection.commit()
        return {"message": "Medical test created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Read (GET) - Get all medical tests
@app.get("/medical_tests/")
def get_medical_tests():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM medical_tests"
        cursor.execute(query)
        tests = cursor.fetchall()
        return {"medical_tests": tests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Create (POST) - Add a new diagnosis
@app.post("/diagnosis/")
def create_diagnosis(diagnosis: DiagnosisCreate):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO diagnosis (patient_id, diagnosis) VALUES (%s, %s)"
        cursor.execute(query, (diagnosis.patient_id, diagnosis.diagnosis))
        connection.commit()
        return {"message": "Diagnosis created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# Read (GET) - Get all diagnoses
@app.get("/diagnosis/")
def get_diagnoses():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM diagnosis"
        cursor.execute(query)
        diagnoses = cursor.fetchall()
        return {"diagnoses": diagnoses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        cursor.close()
        connection.close()
