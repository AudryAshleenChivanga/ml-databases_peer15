# Liver Disease Database Setup and Data Cleaning
---
## ERD Diagram

You can view the **Entity Relationship Diagram (ERD)** for the database schema [here](https://dbdocs.io/a.chivanga/liverdb?view=table_structure).
---
## Step 1: Running the SQL Schema

To set up the database, first run the `sqlSchema.sql` file. This will create the required tables and the database.

```bash
mysql < sqlSchema.sql
```
---
- **Step 2: Data Cleaning**

 - Before inserting data into the database, certain data cleaning steps are applied:
- Column Names: Renamed for consistency.
- Missing Values: In the Albumin_and_Globulin_Ratio column, missing values are filled with the column mean.
- Gender Conversion: The Gender column is converted to binary values (1 for Male, 0 for Female).
- Diagnosis Conversion: The Diagnosis column is converted to binary values (1 for Liver disease, 0 for No disease).
---
- **Step 3: MySQL Setup**
- Log in to MySQL as the root user:

````
mysql -u root -p
````
Check if the user 'Ashleen'@'localhost' exists:
````
SELECT user, host FROM mysql.user;
````
Exporting the Database Data 
````
mysqldump -u Ashleen -p --no-create-info liver_disease_db > data.sql
````
- Those are some of the steps you follow for accessing our sqlschema . 
---

## **MongoDB Database and Collections**
- Database:
The MongoDB database used is liver_disease_db, which contains the following collections:

- patients: Stores patient details, including Age and Gender.
- medical_tests: Stores the results of medical tests for each patient.
- diagnosis: Stores the binary diagnosis (1 for liver disease, 0 for no disease).

- You can inspect the collections using MongoDB Compass or via the MongoDB shell however you need our private key for that!:
````
show dbs
use liver_disease_db
show collections
````
Data Insertion :
We inserted into MongoDB using the insert_many()
````
patients_collection.insert_many(patients_data_dict)
````
- That's it for our DataBases !

## **The API - Task 2**

- This is a FastAPI-based application for managing patient data and medical test results. It provides endpoints for creating, reading, updating, and deleting patient records, as well as managing medical test data.

---

- **API Repository**

-  https://github.com/1772hojaz/ml-databases_peer15_API.git

---
- **REMOTE API LINK**

- https://ml-databases-peer15-api-w1yu-q265fdkji.vercel.app/docs#/
  
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
---



## **Liver Disease Prediction System - Task 3**

## Overview
- This system trains a machine learning model to predict liver disease and offers multiple ways to use it:

1. **Direct prediction**: Use the model directly with CSV data
2. **API-based prediction**: Fetch data from an API and make predictions
3. **Test server**: For demonstrations without a database

## **CONTRIBUTIONS**
- Task 1: **Audry Ashleen Chivanga**
- Task 2: **Humphrey Nyahoja**
- Task 3: **Dieudonne Ngum**
