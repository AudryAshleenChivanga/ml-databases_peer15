# Liver Disease Prediction API

This is a FastAPI-based application for managing patient data and medical test results. It provides endpoints for creating, reading, updating, and deleting patient records, as well as managing medical test data.

---

- **This is a Locally run API**
- For The remote api see https://github.com/1772hojaz/ml-databases_peer15_API.git

## **REMOTE API LINK**
- The link https://ml-databases-peer15-api-w1yu-q265fdkji.vercel.app/docs#/
  
---

## **Features**
- **Patient Management**:
  - Create, read, update, and delete patient records.
  - Store patient age and gender (binary: 1 for male, 0 for female).

- **Medical Test Management**:
  - Create, read, update, and delete medical test records.
  - Store test results such as bilirubin levels, enzyme levels, and protein levels.

- **Diagnosis Management**:
  - Create and retrieve diagnosis records (1 for liver disease, 0 for no disease).

---

## **Endpoints**

### **Patient Endpoints**
- **POST `/patients/`**: Create a new patient.
- **GET `/patients/`**: Retrieve all patients.
- **GET `/patients/{patient_id}`**: Retrieve a specific patient by ID.
- **PUT `/patients/{patient_id}`**: Update a patient by ID.
- **DELETE `/patients/{patient_id}`**: Delete a patient by ID.

### **Medical Test Endpoints**
- **POST `/medical_tests/`**: Create a new medical test.
- **GET `/medical_tests/`**: Retrieve all medical tests.
- **GET `/medical_tests/{test_id}`**: Retrieve a specific medical test by ID.
- **PUT `/medical_tests/{test_id}`**: Update a medical test by ID.
- **DELETE `/medical_tests/{test_id}`**: Delete a medical test by ID.

### **Diagnosis Endpoints**
- **POST `/diagnosis/`**: Create a new diagnosis.
- **GET `/diagnosis/`**: Retrieve all diagnoses.
