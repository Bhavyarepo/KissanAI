import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def train_mock_models():
    models_root = 'models'
    ensure_dir(models_root)
    
    print("Generating mock data...")
    n_samples = 100
    # Features: ph, nitrogen, phosphorus, potassium, organic_matter, temperature, rainfall, humidity, season_encoded, state_encoded
    X = np.random.rand(n_samples, 10)
    
    # Target: crops
    crops = ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Cotton', 'Millets']
    y_crop = np.random.choice(crops, n_samples)
    
    # Target: yield
    y_yield = np.random.rand(n_samples) * 5000
    
    # Target: fertilizer
    fertilizers = ['NPK 20-20-20', 'NPK 18-18-18', 'Urea', 'DAP']
    y_fert = np.random.choice(fertilizers, n_samples)
    
    print("Training mock models...")
    
    # Scaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Crop model
    crop_model = RandomForestClassifier(n_estimators=10)
    crop_model.fit(X_scaled, y_crop)
    
    # Yield model
    yield_model = RandomForestRegressor(n_estimators=10)
    yield_model.fit(X_scaled, y_yield)
    
    # Fertilizer model
    # For fertilizer, we use only first 5 features (soil)
    X_soil = X[:, :5]
    fert_scaler = StandardScaler()
    X_soil_scaled = fert_scaler.fit_transform(X_soil)
    fert_model = RandomForestClassifier(n_estimators=10)
    fert_model.fit(X_soil_scaled, y_fert)
    
    # Price model (dummy regressor)
    price_model = RandomForestRegressor(n_estimators=10)
    price_model.fit(X_scaled, y_yield)
    
    print("Saving mock models...")
    joblib.dump(crop_model, os.path.join(models_root, 'crop_model.pkl'))
    joblib.dump(yield_model, os.path.join(models_root, 'yield_model.pkl'))
    joblib.dump(fert_model, os.path.join(models_root, 'fertilizer_model.pkl'))
    joblib.dump(fert_scaler, os.path.join(models_root, 'fertilizer_scaler.pkl'))
    joblib.dump(scaler, os.path.join(models_root, 'scaler.pkl'))
    joblib.dump(price_model, os.path.join(models_root, 'price_model.pkl'))
    
    print("Mock models created successfully in 'models/' directory.")

if __name__ == '__main__':
    train_mock_models()
