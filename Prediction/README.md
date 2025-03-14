# Liver Disease Prediction System - Task 3

## Overview
This system predicts liver disease likelihood using machine learning. The implementation offers three flexible approaches to accommodate different usage scenarios:

1. **Direct prediction**: Use the model directly with the Indian Liver Patient dataset
2. **API-based prediction**: Fetch data from an API and make predictions
3. **Test server**: Run demonstrations without requiring a database

## Project Structure

### Setup Instructions

#### Prerequisites
- Python 3.8+
- Required packages (install using requirements below)

#### Installation
1. Clone the repository (if not already done)
2. Create and activate a virtual environment (recommended)
3. Install required packages

### Usage Options

#### Option 1: Direct Prediction with CSV Data
This approach works without any database or API connection, using the Indian Liver Patient dataset directly.

1. Train the model using the CSV data
2. Make predictions using direct input
   - The script will prompt you to enter patient details or use sample data

#### Option 2: Using the Test Server (Recommended for Demonstration)
This approach demonstrates the API-based prediction without requiring a real database.

1. Start the test server in one terminal
2. In another terminal, run the prediction script

#### Option 3: Using the Real API with Database
For full integration with the database from Task 1 and API from Task 2.

1. Ensure the MySQL server is running with the correct configuration
2. Start the FastAPI application
3. Run the prediction script

## Detailed File Descriptions

### Model Training
- **train_model.py**: Creates a sample RandomForest model with synthetic data
  - Generates data with patterns that simulate liver disease indicators
  - Trains with 97.5% test accuracy
  - Saves model to models/liver_model.pkl
- **train_from_csv.py**: Trains a model using the actual Indian Liver Patient dataset
  - Preprocesses real patient data from the CSV file
  - Includes feature engineering and data cleaning
  - Saves model to models/liver_model_from_csv.pkl

### Prediction Scripts
- **simple_predict.py**: Prediction via API endpoints
  - Fetches latest patient from /patients/latest/ endpoint
  - Gets medical test results from /medical_tests/patient/{id} endpoint
  - Preprocesses data and makes prediction
  - Displays detailed results with confidence score
- **predict_direct.py**: Standalone prediction without API
  - Takes user input or uses sample data
  - Makes predictions using the trained model directly
  - No database or API connection required

### Support Files
- **preprocessing.py**: Data preprocessing utilities
  - Converts categorical features to numeric
  - Handles missing values
  - Formats data for model compatibility
- **test_server.py**: Mock API server
  - Simulates API endpoints that return patient data
  - Provides consistent test data for demonstrations
  - Runs on http://127.0.0.1:8000
- **config.py**: Configuration settings
  - API base URL and endpoints
  - Model and feature name file paths
- **sample_inputs.py**: Sample patient data
  - Contains example data for healthy patients and those with liver disease
  - Useful for quick testing and demonstrations

## Model Details
The liver disease prediction model uses a Random Forest Classifier with the following features:
- Age
- Gender (encoded as numeric)
- Total Bilirubin
- Direct Bilirubin
- Alkaline Phosphotase
- Alamine Aminotransferase
- Aspartate Aminotransferase
- Total Proteins
- Albumin
- Albumin and Globulin Ratio

Performance metrics for the model trained on the Indian Liver Patient dataset:
- Accuracy: ~75-80% (varies by train/test split)
- Precision: ~80% for liver disease detection
- Recall: ~75% for liver disease detection

## Integration with Other Tasks
This module integrates with:
- **Task 1**: Uses the database schema structure (patients, medical_tests tables)
- **Task 2**: Connects to the API endpoints to retrieve patient data

## Contributors
- Ngum
- [Other team members]

## Acknowledgments
- Indian Liver Patient Dataset from the UCI Machine Learning Repository
- [Other acknowledgments]

## Disclaimer
The predictions made by this system are for educational purposes only and should not be used for actual medical diagnosis.
