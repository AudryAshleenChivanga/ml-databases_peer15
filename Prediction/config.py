import os

# API configuration
API_BASE_URL = "http://127.0.0.1:8000"  # Use this consistently

# Model paths
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'liver_model.pkl')
FEATURE_NAMES_PATH = os.path.join(MODEL_DIR, 'feature_names.pkl')