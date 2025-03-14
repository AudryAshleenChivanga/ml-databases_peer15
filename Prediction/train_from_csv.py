import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# Path to the dataset
CSV_PATH = os.path.join('..', 'sqldatabase', 'indian_liver_patient.csv')

def train_model_from_csv():
    print("Training liver disease prediction model from CSV data...")
    
    # Load the dataset
    print(f"Loading data from {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)
    
    # Display basic information about the dataset
    print("\nDataset Information:")
    print(f"Shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    
    # Data preprocessing
    print("\nPreprocessing data...")
    
    # Rename columns to match our database schema
    df.rename(columns={
        'Total_Bilirubin': 'total_bilirubin',
        'Direct_Bilirubin': 'direct_bilirubin',
        'Alkaline_Phosphotase': 'alkaline_phosphotase',
        'Alamine_Aminotransferase': 'alamine_aminotransferase',
        'Aspartate_Aminotransferase': 'aspartate_aminotransferase',
        'Total_Protiens': 'total_proteins',
        'Albumin': 'albumin',
        'Albumin_and_Globulin_Ratio': 'albumin_and_globulin_ratio',
        'Dataset': 'diagnosis'
    }, inplace=True)
    
    # Convert gender to numeric (Male=1, Female=0)
    df['gender_numeric'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)
    
    # Handle missing values
    if df['albumin_and_globulin_ratio'].isna().sum() > 0:
        mean_value = df['albumin_and_globulin_ratio'].mean()
        print(f"Replacing {df['albumin_and_globulin_ratio'].isna().sum()} missing values in albumin_and_globulin_ratio with mean: {mean_value:.2f}")
        df['albumin_and_globulin_ratio'].fillna(mean_value, inplace=True)
    
    # Adjust the diagnosis values if needed
    # In the dataset: 1=liver disease, 2=no liver disease
    # We want: 1=liver disease, 0=no liver disease
    if 2 in df['diagnosis'].unique():
        print("Converting diagnosis values: 2 -> 0 (no liver disease)")
        df['diagnosis'] = df['diagnosis'].replace(2, 0)
    
    # Select features
    features = [
        'Age', 'gender_numeric', 
        'total_bilirubin', 'direct_bilirubin', 'alkaline_phosphotase', 
        'alamine_aminotransferase', 'aspartate_aminotransferase', 
        'total_proteins', 'albumin', 'albumin_and_globulin_ratio'
    ]
    
    X = df[features]
    y = df['diagnosis']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"\nTraining set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Train a Random Forest model
    print("\nTraining Random Forest classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy:.4f}")
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    model_dir = os.path.join(os.path.dirname(__file__), 'models')
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'liver_model_from_csv.pkl')
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"\nModel saved to {model_path}")
    
    # Save feature names
    feature_path = os.path.join(model_dir, 'feature_names_from_csv.pkl')
    with open(feature_path, 'wb') as f:
        pickle.dump(features, f)
    
    print(f"Feature names saved to {feature_path}")
    
    return model_path

if __name__ == "__main__":
    train_model_from_csv()
