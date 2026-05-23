from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
from database import get_db
from models import Farmer
from auth import get_current_farmer
from services.ml_service import MLService
from services import ModelNotReadyError
import os
import uuid

router = APIRouter()

ml_service = MLService()

def _ensure_models_ready():
    if not (ml_service.crop_model and ml_service.yield_model and ml_service.fertilizer_model):
        raise ModelNotReadyError("Models not trained. Run backend/ml/train_all.py to prepare models.")

@router.get("/recommend/{farmer_id}")
async def recommend_for_farmer(farmer_id: int, db: Session = Depends(get_db)):
    try:
        _ensure_models_ready()
    except ModelNotReadyError as e:
        raise HTTPException(status_code=503, detail=str(e))

    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    # Placeholder soil/weather; integrate real retrieval or cached values
    soil_data = { 'ph': 6.7, 'nitrogen': 48, 'phosphorus': 30, 'potassium': 40, 'organic_matter': 2.7 }
    weather_data = { 'temperature': 27.0, 'rainfall': 12.0, 'humidity': 70 }

    season = 'kharif'
    recommendations = ml_service.get_crop_recommendations(soil_data, weather_data, season, farmer.state)

    from services.gemini_service import GeminiService
    gemini = GeminiService()

    # Attach simple price forecast placeholder + Gemini advice
    for r in recommendations:
        r['price_forecast'] = {
            'next_month_avg': round(r['expected_profit'] / max(r['expected_yield'], 1.0), 2),
            'confidence': 0.7
        }
        # Add Gemini expert advice
        r['expert_advice'] = await gemini.get_enhanced_recommendations(
            r['crop_name'], soil_data, weather_data
        )
    return recommendations

@router.get("/fertilizer/{farmer_id}")
async def fertilizer_for_farmer(farmer_id: int, db: Session = Depends(get_db)):
    try:
        _ensure_models_ready()
    except ModelNotReadyError as e:
        raise HTTPException(status_code=503, detail=str(e))

    farmer = db.query(Farmer).filter(Farmer.id == farmer_id).first()
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer not found")

    # Minimal fertilizer suggestion using MLService crop rec fertilizer field
    soil_data = { 'ph': 6.7, 'nitrogen': 48, 'phosphorus': 30, 'potassium': 40, 'organic_matter': 2.7 }
    weather_data = { 'temperature': 27.0, 'rainfall': 12.0, 'humidity': 70 }
    season = 'kharif'
    rec = ml_service.get_crop_recommendations(soil_data, weather_data, season, farmer.state)[0]
    return rec.get('fertilizer_recommendation', {})

@router.post("/disease-detect")
async def disease_detect(file: UploadFile = File(...)):
    try:
        _ensure_models_ready()  # For now, reuse simple placeholder model
    except ModelNotReadyError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    os.makedirs("uploads", exist_ok=True)
    filename = f"disease_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    path = os.path.join("uploads", filename)
    with open(path, 'wb') as f:
        f.write(await file.read())
    return ml_service.detect_pest_disease(path, 'disease')

@router.post("/pest-detect")
async def pest_detect(file: UploadFile = File(...)):
    try:
        _ensure_models_ready()
    except ModelNotReadyError as e:
        raise HTTPException(status_code=503, detail=str(e))

    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    os.makedirs("uploads", exist_ok=True)
    filename = f"pest_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    path = os.path.join("uploads", filename)
    with open(path, 'wb') as f:
        f.write(await file.read())
    return ml_service.detect_pest_disease(path, 'pest')

@router.get("/market/{commodity}")
async def market_prices(commodity: str):
    # Placeholder: trained price model would provide historical + forecast
    return {
        'commodity': commodity,
        'historical_points': 60,
        'forecast': [{ 'date_offset_days': i*7, 'price': 100 + i*2 } for i in range(1, 5)]
    }

@router.post("/faq")
async def faq_chatbot(query: Dict[str, Any]):
    from services.gemini_service import GeminiService
    gemini = GeminiService()
    
    question = query.get('question', '')
    if not question:
        raise HTTPException(status_code=400, detail='question is required')
    
    answer = await gemini.get_farming_advice(question)
    return { 'answer': answer }






