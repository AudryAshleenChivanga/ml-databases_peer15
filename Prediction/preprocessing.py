import pandas as pd

def preprocess_patient_data(patient_data, medical_tests_data):
    """
    Preprocess patient and medical test data for model prediction.
    
    Args:
        patient_data (dict): Patient demographics
        medical_tests_data (dict): Medical test results
    
    Returns:
        pd.DataFrame: Preprocessed data ready for model prediction
    """
    # Combine patient and medical tests data
    combined_data = {}
    
    # Extract patient information
    combined_data['age'] = patient_data.get('age')
    
    # Convert gender to numeric (Male = 1, Female = 0)
    gender = patient_data.get('gender')
    if gender:
        combined_data['gender_numeric'] = 1 if gender.lower() == 'male' else 0
    else:
        combined_data['gender_numeric'] = None
    
    # Extract medical test information
    if medical_tests_data:
        combined_data['total_bilirubin'] = medical_tests_data.get('total_bilirubin')
        combined_data['direct_bilirubin'] = medical_tests_data.get('direct_bilirubin')
        combined_data['alkaline_phosphotase'] = medical_tests_data.get('alkaline_phosphotase')
        combined_data['alamine_aminotransferase'] = medical_tests_data.get('alamine_aminotransferase')
        combined_data['aspartate_aminotransferase'] = medical_tests_data.get('aspartate_aminotransferase')
        combined_data['total_proteins'] = medical_tests_data.get('total_proteins')
        combined_data['albumin'] = medical_tests_data.get('albumin')
        combined_data['albumin_and_globulin_ratio'] = medical_tests_data.get('albumin_and_globulin_ratio')
    
    # Convert to DataFrame and check for missing values
    df = pd.DataFrame([combined_data])
    
    # Check for missing values
    missing_columns = df.columns[df.isnull().any()].tolist()
    if missing_columns:
        print(f"Warning: Missing values in columns: {missing_columns}")
        # Replace missing values with mean/median or reasonable defaults
        # For demo purposes, replacing with zeros (in practice, use better imputation)
        df.fillna(0, inplace=True)
    
    return df