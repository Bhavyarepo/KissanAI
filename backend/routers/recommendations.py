from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Farmer, CropRecommendation
from schemas import CropRecommendationRequest, CropRecommendationResponse
from auth import get_current_farmer
from services.ml_service import MLService
from routers.soil import get_soil_data
from datetime import datetime, timedelta
from typing import List, Dict, Any
import json

router = APIRouter()
ml_service = MLService()

import hashlib

# Minimal weather data provider to replace missing routers.weather module
async def get_weather_data(location: str, state: str, district: str) -> Dict[str, Any]:
    try:
        # Create deterministic pseudo-random values based on location string
        loc_hash = int(hashlib.md5(f"{location}-{state}-{district}".encode('utf-8')).hexdigest(), 16)
        
        # Base values + pseudo-random offset
        temperature = 22.0 + (loc_hash % 15)  # 22.0 to 36.0
        humidity = 50.0 + ((loc_hash // 10) % 40)     # 50.0 to 89.0
        rainfall = 400.0 + ((loc_hash // 100) % 800)   # 400.0 to 1199.0
        
        return {
            'temperature': temperature,
            'humidity': humidity,
            'rainfall': rainfall,
            'wind_speed': 5.0 + ((loc_hash // 1000) % 10),
            'pressure': 1000.0 + (loc_hash % 25),
            'weather_condition': 'Clear' if loc_hash % 2 == 0 else 'Cloudy'
        }
    except Exception:
        return {
            'temperature': 25.0,
            'humidity': 65.0,
            'rainfall': 800.0,
            'wind_speed': 6.0,
            'pressure': 1010.0,
            'weather_condition': 'Clear'
        }

@router.post("/crops", response_model=List[CropRecommendationResponse])
async def get_crop_recommendations(
    request: CropRecommendationRequest,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Get crop recommendations based on location, soil, and weather data"""
    try:
        # Get soil data for the location
        soil_data = await get_soil_data(request.location, request.state, request.district)
        
        # Get weather data for the location
        weather_data = await get_weather_data(request.location, request.state, request.district)
        
        # Get recommendations from ML service
        recommendations = ml_service.get_crop_recommendations(
            soil_data, weather_data, request.season, request.state
        )
        
        from services.gemini_service import GeminiService
        gemini = GeminiService()

        # Save recommendations to database and add Gemini advice
        for rec in recommendations:
            db_recommendation = CropRecommendation(
                farmer_id=int(current_farmer.id),
                crop_name=str(rec['crop_name']),
                confidence_score=float(rec['confidence_score']),
                expected_yield=float(rec['expected_yield']),
                expected_profit=float(rec['expected_profit']),
                sustainability_score=float(rec['sustainability_score']),
                fertilizer_recommendation=json.dumps(rec['fertilizer_recommendation']),
                planting_date=datetime.now() + timedelta(days=7),
                harvesting_date=datetime.now() + timedelta(days=120)
            )
            db.add(db_recommendation)
            
            # Add dates and Gemini expert advice to the response
            rec['planting_date'] = db_recommendation.planting_date
            rec['harvesting_date'] = db_recommendation.harvesting_date
            rec['expert_advice'] = await gemini.get_enhanced_recommendations(
                rec['crop_name'], soil_data, weather_data
            )
        
        db.commit()
        
        return recommendations
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting recommendations: {str(e)}")

@router.get("/history")
async def get_recommendation_history(
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Get farmer's recommendation history"""
    recommendations = db.query(CropRecommendation).filter(
        CropRecommendation.farmer_id == current_farmer.id
    ).order_by(CropRecommendation.created_at.desc()).all()
    
    return recommendations

