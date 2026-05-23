try:
    import numpy as np  # type: ignore
except Exception:
    np = None  # type: ignore

try:
    import pandas as pd  # type: ignore
except Exception:
    pd = None  # type: ignore
import os
from typing import List, Dict, Any
import json

# Optional heavy dependencies
try:
    from sklearn.preprocessing import StandardScaler  # type: ignore
except Exception:  # sklearn not available
    StandardScaler = None  # type: ignore

try:
    import joblib  # type: ignore
except Exception:
    joblib = None  # type: ignore

try:
    import tensorflow as tf  # type: ignore
except Exception:
    tf = None  # type: ignore

class MLService:
    def __init__(self):
        self.crop_model = None
        self.yield_model = None
        self.fertilizer_model = None
        self.fertilizer_scaler = None
        # Initialize scaler if available
        self.scaler = StandardScaler() if StandardScaler is not None else None
        self.price_model = None
        self.disease_model = None
        self.pest_model = None
        self.faq_model_dir = None
        self.models_path = "models/"
        os.makedirs(self.models_path, exist_ok=True)
        self._load_or_train_models()
    
    def _load_or_train_models(self):
        """Load existing models or train new ones"""
        # Load pre-trained models if present; do not auto-train here anymore.
        # Load classical ML models if joblib is available
        if joblib is not None:
            try:
                self.crop_model = joblib.load(os.path.join(self.models_path, "crop_model.pkl"))
            except Exception:
                self.crop_model = None
            try:
                self.yield_model = joblib.load(os.path.join(self.models_path, "yield_model.pkl"))
            except Exception:
                self.yield_model = None
            try:
                self.fertilizer_model = joblib.load(os.path.join(self.models_path, "fertilizer_model.pkl"))
                self.fertilizer_scaler = joblib.load(os.path.join(self.models_path, "fertilizer_scaler.pkl"))
            except Exception:
                self.fertilizer_model = None
                self.fertilizer_scaler = None
            try:
                loaded_scaler = joblib.load(os.path.join(self.models_path, "scaler.pkl"))
                self.scaler = loaded_scaler
            except Exception:
                # keep existing scaler (may be None)
                pass
            try:
                self.price_model = joblib.load(os.path.join(self.models_path, "price_model.pkl"))
            except Exception:
                self.price_model = None
        else:
            # joblib not available; keep models as None
            self.crop_model = None
            self.yield_model = None
            self.fertilizer_model = None
            self.fertilizer_scaler = None
            self.price_model = None

        # CNNs via TensorFlow (optional)
        if tf is not None:
            try:
                self.disease_model = tf.keras.models.load_model(os.path.join(self.models_path, 'disease_model.h5'))
            except Exception:
                self.disease_model = None
            try:
                self.pest_model = tf.keras.models.load_model(os.path.join(self.models_path, 'pest_model.h5'))
            except Exception:
                self.pest_model = None
        else:
            self.disease_model = None
            self.pest_model = None
        # FAQ
        faq_dir = os.path.join(self.models_path, 'faq_model')
        if os.path.isdir(faq_dir):
            self.faq_model_dir = faq_dir
        else:
            self.faq_model_dir = None
    
    def _create_sample_data(self):
        """Create sample training data for demonstration"""
        if np is None or pd is None:
            raise RuntimeError("NumPy/Pandas not available for sample data generation in this setup")
        np.random.seed(42)
        n_samples = 1000
        
        # Generate sample data
        data = {
            'ph': np.random.normal(6.5, 1.0, n_samples),
            'nitrogen': np.random.normal(50, 20, n_samples),
            'phosphorus': np.random.normal(30, 15, n_samples),
            'potassium': np.random.normal(40, 18, n_samples),
            'organic_matter': np.random.normal(2.5, 1.0, n_samples),
            'temperature': np.random.normal(25, 5, n_samples),
            'rainfall': np.random.normal(1000, 300, n_samples),
            'humidity': np.random.normal(70, 15, n_samples),
            'season_encoded': np.random.choice([0, 1, 2], n_samples),  # 0: kharif, 1: rabi, 2: summer
            'state_encoded': np.random.choice([0, 1, 2, 3, 4], n_samples),  # 5 states
        }
        
        # Define crop recommendations based on conditions
        crops = []
        yields = []
        fertilizers = []
        
        for i in range(n_samples):
            ph = data['ph'][i]
            temp = data['temperature'][i]
            rainfall = data['rainfall'][i]
            season = data['season_encoded'][i]
            
            # Simple rule-based crop selection
            if ph > 6.0 and ph < 7.5 and temp > 20 and temp < 35:
                if rainfall > 800 and season == 0:  # kharif
                    crop = 'Rice'
                    yield_val = np.random.normal(4000, 500)
                    fertilizer = 'NPK 20-20-20'
                elif rainfall > 600 and season == 1:  # rabi
                    crop = 'Wheat'
                    yield_val = np.random.normal(3500, 400)
                    fertilizer = 'NPK 18-18-18'
                elif rainfall > 400 and season == 2:  # summer
                    crop = 'Maize'
                    yield_val = np.random.normal(3000, 300)
                    fertilizer = 'NPK 15-15-15'
                else:
                    crop = 'Sugarcane'
                    yield_val = np.random.normal(80000, 10000)
                    fertilizer = 'NPK 12-12-12'
            elif ph > 5.5 and ph < 6.5:
                crop = 'Cotton'
                yield_val = np.random.normal(2000, 200)
                fertilizer = 'NPK 19-19-19'
            else:
                crop = 'Millets'
                yield_val = np.random.normal(1500, 150)
                fertilizer = 'NPK 10-10-10'
            
            crops.append(crop)
            yields.append(max(0, yield_val))
            fertilizers.append(fertilizer)
        
        data['crop'] = crops
        data['yield'] = yields
        data['fertilizer'] = fertilizers
        
        return pd.DataFrame(data)
    
    def _train_models(self):
        """Deprecated: training moved to backend/ml scripts using Kaggle datasets."""
        raise RuntimeError("Training is handled by dedicated scripts in backend/ml. Run train_all.py instead.")
    
    def get_crop_recommendations(self, soil_data: Dict[str, Any], weather_data: Dict[str, Any], 
                                season: str, state: str) -> List[Dict[str, Any]]:
        """Get crop recommendations based on soil and weather data"""
        if self.crop_model is None or self.yield_model is None or self.scaler is None or np is None:
            raise RuntimeError("Crop/yield models or scaler not available on this setup")
        # Encode season and state
        season_encoding = {'kharif': 0, 'rabi': 1, 'summer': 2}.get(season.lower(), 0)
        state_encoding = {'andhra_pradesh': 0, 'telangana': 1, 'karnataka': 2, 
                         'tamil_nadu': 3, 'kerala': 4}.get(state.lower().replace(' ', '_'), 0)
        
        # Prepare input features
        features = np.array([[
            soil_data.get('ph', 6.5),
            soil_data.get('nitrogen', 50),
            soil_data.get('phosphorus', 30),
            soil_data.get('potassium', 40),
            soil_data.get('organic_matter', 2.5),
            weather_data.get('temperature', 25),
            weather_data.get('rainfall', 1000),
            weather_data.get('humidity', 70),
            season_encoding,
            state_encoding
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get predictions
        crop_prediction = self.crop_model.predict(features_scaled)[0]
        yield_prediction = self.yield_model.predict(features_scaled)[0]
        
        # Calculate confidence score (simplified)
        confidence_score = min(0.95, max(0.6, np.random.random()))
        
        # Calculate expected profit (simplified)
        crop_prices = {
            'Rice': 25, 'Wheat': 20, 'Maize': 18, 'Sugarcane': 3, 
            'Cotton': 60, 'Millets': 15
        }
        price_per_kg = crop_prices.get(crop_prediction, 20)
        expected_profit = yield_prediction * price_per_kg * 0.3  # 30% profit margin
        
        # Calculate sustainability score
        sustainability_score = min(0.95, max(0.5, 
            (soil_data.get('organic_matter', 2.5) / 5.0) * 0.4 + 
            (1 - abs(soil_data.get('ph', 6.5) - 6.8) / 6.8) * 0.3 +
            (weather_data.get('rainfall', 1000) / 1500) * 0.3
        ))
        
        result = [{
            'crop_name': crop_prediction,
            'confidence_score': round(confidence_score, 2),
            'expected_yield': round(max(0, yield_prediction), 2),
            'expected_profit': round(expected_profit, 2),
            'sustainability_score': round(sustainability_score, 2),
        }]
        # Optional fertilizer suggestion via separate model
        try:
            if self.fertilizer_model is not None and self.fertilizer_scaler is not None:
                fert_features = self.fertilizer_scaler.transform(features[:, :5])
                fert_pred = self.fertilizer_model.predict(fert_features)[0]
                result[0]['fertilizer_recommendation'] = {
                    'type': str(fert_pred),
                    'quantity_per_acre': '50-75 kg',
                    'application_method': 'Broadcast and mix with soil'
                }
        except Exception:
            pass
        return result
    
    def detect_pest_disease(self, image_path: str, detection_type: str) -> Dict[str, Any]:
        """Detect pest or disease from image (simplified implementation)"""
        # If CNN models are available, use them; otherwise fallback to heuristic
        if tf is not None and np is not None:
            try:
                img = tf.keras.preprocessing.image.load_img(image_path, target_size=(224,224))
                arr = tf.keras.preprocessing.image.img_to_array(img)
                arr = np.expand_dims(arr, axis=0)
                arr = arr / 255.0
                if detection_type == 'disease' and self.disease_model is not None:
                    preds = self.disease_model.predict(arr, verbose=0)[0]
                    idx = int(np.argmax(preds))
                    conf = float(np.max(preds))
                    name = f"class_{idx}"
                    return {
                        'type': 'disease',
                        'name': name,
                        'confidence_score': round(conf, 2),
                        'recommended_treatment': None,
                        'severity': 'medium'
                    }
                if detection_type == 'pest' and self.pest_model is not None:
                    preds = self.pest_model.predict(arr, verbose=0)[0]
                    idx = int(np.argmax(preds))
                    conf = float(np.max(preds))
                    name = f"class_{idx}"
                    return {
                        'type': 'pest',
                        'name': name,
                        'confidence_score': round(conf, 2),
                        'recommended_treatment': None,
                        'severity': 'medium'
                    }
            except Exception:
                pass
        # Fallback random as before
        if detection_type == 'pest':
            pests = ['Aphids', 'Whiteflies', 'Thrips', 'Caterpillars', 'Beetles']
            pest = np.random.choice(pests)
            confidence = np.random.uniform(0.7, 0.95)
            treatments = {
                'Aphids': 'Apply neem oil or insecticidal soap',
                'Whiteflies': 'Use yellow sticky traps and neem oil',
                'Thrips': 'Apply spinosad or pyrethrin',
                'Caterpillars': 'Use Bt (Bacillus thuringiensis)',
                'Beetles': 'Apply diatomaceous earth or neem oil'
            }
            severity = np.random.choice(['low', 'medium', 'high'])
            return {
                'type': 'pest',
                'name': pest,
                'confidence_score': round(confidence, 2),
                'recommended_treatment': treatments[pest],
                'severity': severity
            }
        else:
            diseases = ['Leaf Blight', 'Powdery Mildew', 'Root Rot', 'Bacterial Spot', 'Virus']
            disease = np.random.choice(diseases)
            confidence = np.random.uniform(0.7, 0.95)
            treatments = {
                'Leaf Blight': 'Apply copper fungicide',
                'Powdery Mildew': 'Use sulfur fungicide or baking soda solution',
                'Root Rot': 'Improve drainage and apply fungicide',
                'Bacterial Spot': 'Apply copper-based bactericide',
                'Virus': 'Remove infected plants and control vectors'
            }
            severity = np.random.choice(['low', 'medium', 'high'])
            return {
                'type': 'disease',
                'name': disease,
                'confidence_score': round(confidence, 2),
                'recommended_treatment': treatments[disease],
                'severity': severity
            }

