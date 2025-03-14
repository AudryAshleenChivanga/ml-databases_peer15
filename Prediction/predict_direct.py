import pandas as pd
import pickle
import os

def load_model(model_path='models/liver_model_from_csv.pkl'):
    """Load the trained model"""
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        print(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def load_feature_names(path='models/feature_names_from_csv.pkl'):
    """Load feature names used during training"""
    try:
        with open(path, 'rb') as f:
            features = pickle.load(f)
        return features
    except Exception as e:
        print(f"Error loading feature names: {e}")
        return None

def get_user_input():
    """Get patient data from user input"""
    print("\n=== Enter Patient Data ===")
    
    patient_data = {
        'Age': int(input("Age: ")),
        'gender_numeric': int(input("Gender (1 for Male, 0 for Female): ")),
        'total_bilirubin': float(input("Total Bilirubin: ")),
        'direct_bilirubin': float(input("Direct Bilirubin: ")),
        'alkaline_phosphotase': int(input("Alkaline Phosphotase: ")),
        'alamine_aminotransferase': int(input("Alamine Aminotransferase: ")),
        'aspartate_aminotransferase': int(input("Aspartate Aminotransferase: ")),
        'total_proteins': float(input("Total Proteins: ")),
        'albumin': float(input("Albumin: ")),
        'albumin_and_globulin_ratio': float(input("Albumin and Globulin Ratio: "))
    }
    
    return pd.DataFrame([patient_data])

def main():
    # Load the model
    model = load_model()
    if not model:
        print("Could not load the model. Please make sure you've trained it first.")
        return
    
    # Get feature names
    features = load_feature_names()
    
    # Get user input
    user_data = get_user_input()
    
    # Ensure we have all required features in the right order
    if features:
        # Select only columns that the model was trained on and in correct order
        user_data = user_data[features]
    
    # Make prediction
    prediction = model.predict(user_data)[0]
    
    # Get probability if available
    probability = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(user_data)[0]
        probability = probabilities[1] if prediction == 1 else probabilities[0]
    
    # Display results
    print("\n===== PREDICTION RESULTS =====")
    if prediction == 1:
        result = "POSITIVE - Patient likely has liver disease"
    else:
        result = "NEGATIVE - Patient likely does not have liver disease"
    
    print(f"\nPrediction: {result}")
    if probability is not None:
        print(f"Confidence: {probability:.2%}")
    
    print("\nPATIENT DATA USED FOR PREDICTION:")
    for feature, value in user_data.iloc[0].items():
        print(f"  {feature}: {value}")
        
    print("\nDISCLAIMER: This is a demonstration prediction only and should not")
    print("be used for actual medical diagnosis.")

if __name__ == "__main__":
    main()