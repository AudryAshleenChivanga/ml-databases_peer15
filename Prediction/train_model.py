import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os

# Create directories if they don't exist
os.makedirs('models', exist_ok=True)

# Function to generate synthetic data mimicking liver disease patterns
def generate_synthetic_data(n_samples=1000):
    np.random.seed(42)  # For reproducibility
    
    # Generate age between 20 and 80
    age = np.random.randint(20, 80, n_samples)
    
    # Generate gender (1 for Male, 0 for Female)
    gender = np.random.binomial(1, 0.5, n_samples)
    
    # Healthy ranges for liver function tests
    total_bilirubin = np.random.normal(0.7, 0.3, n_samples)
    direct_bilirubin = np.random.normal(0.2, 0.1, n_samples)
    alkaline_phosphotase = np.random.normal(150, 50, n_samples)
    alamine_aminotransferase = np.random.normal(30, 10, n_samples)
    aspartate_aminotransferase = np.random.normal(30, 10, n_samples)
    total_proteins = np.random.normal(7, 0.5, n_samples)
    albumin = np.random.normal(4, 0.3, n_samples)
    albumin_and_globulin_ratio = np.random.normal(1.1, 0.2, n_samples)
    
    # Initialize target variable (0: healthy, 1: liver disease)
    y = np.zeros(n_samples)
    
    # Create patterns for patients with liver disease (about 30% of patients)
    disease_indices = np.random.choice(n_samples, size=int(n_samples * 0.3), replace=False)
    
    # Modify values for patients with liver disease
    total_bilirubin[disease_indices] = np.random.normal(2, 0.8, len(disease_indices))
    direct_bilirubin[disease_indices] = np.random.normal(0.8, 0.3, len(disease_indices))
    alkaline_phosphotase[disease_indices] = np.random.normal(300, 100, len(disease_indices))
    alamine_aminotransferase[disease_indices] = np.random.normal(80, 30, len(disease_indices))
    aspartate_aminotransferase[disease_indices] = np.random.normal(90, 40, len(disease_indices))
    total_proteins[disease_indices] = np.random.normal(6, 0.7, len(disease_indices))
    albumin[disease_indices] = np.random.normal(3, 0.5, len(disease_indices))
    albumin_and_globulin_ratio[disease_indices] = np.random.normal(0.8, 0.3, len(disease_indices))
    
    # Set target values for disease cases
    y[disease_indices] = 1
    
    # Ensure values are within realistic ranges
    total_bilirubin = np.clip(total_bilirubin, 0.1, 10.0)
    direct_bilirubin = np.clip(direct_bilirubin, 0.0, 5.0)
    alkaline_phosphotase = np.clip(alkaline_phosphotase, 20, 800)
    alamine_aminotransferase = np.clip(alamine_aminotransferase, 5, 300)
    aspartate_aminotransferase = np.clip(aspartate_aminotransferase, 5, 300)
    total_proteins = np.clip(total_proteins, 2.0, 10.0)
    albumin = np.clip(albumin, 1.0, 6.0)
    albumin_and_globulin_ratio = np.clip(albumin_and_globulin_ratio, 0.1, 3.0)
    
    # Create dataframe
    data = pd.DataFrame({
        'Age': age,
        'Gender': gender,
        'Total_Bilirubin': total_bilirubin,
        'Direct_Bilirubin': direct_bilirubin,
        'Alkaline_Phosphotase': alkaline_phosphotase,
        'Alamine_Aminotransferase': alamine_aminotransferase,
        'Aspartate_Aminotransferase': aspartate_aminotransferase,
        'Total_Proteins': total_proteins,
        'Albumin': albumin,
        'Albumin_and_Globulin_Ratio': albumin_and_globulin_ratio,
        'Dataset': y
    })
    
    return data

def train_model():
    print("Generating synthetic liver disease data...")
    data = generate_synthetic_data(2000)  # Generate 2000 synthetic samples
    
    # Separate features and target
    X = data.drop('Dataset', axis=1)
    y = data['Dataset']
    
    # Save feature names for later use
    feature_names = list(X.columns)
    with open('models/feature_names.pkl', 'wb') as f:
        pickle.dump(feature_names, f)
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier...")
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy on test data: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save the model
    print("Saving model to models/liver_model.pkl")
    with open('models/liver_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print("Model training and saving complete.")
    return model

if __name__ == "__main__":
    train_model()