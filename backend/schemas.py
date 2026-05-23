from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Authentication schemas
class FarmerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str
    state: str
    district: str
    village: Optional[str] = None
    password: str

class FarmerLogin(BaseModel):
    email: EmailStr
    password: str

class FarmerResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    location: str
    state: str
    district: str
    village: Optional[str]
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Soil data schemas
class SoilDataCreate(BaseModel):
    location: str
    ph: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    organic_matter: Optional[float] = None
    moisture: Optional[float] = None
    temperature: Optional[float] = None
    soil_type: Optional[str] = None

class SoilDataResponse(BaseModel):
    id: int
    farmer_id: int
    location: str
    ph: Optional[float]
    nitrogen: Optional[float]
    phosphorus: Optional[float]
    potassium: Optional[float]
    organic_matter: Optional[float]
    moisture: Optional[float]
    temperature: Optional[float]
    soil_type: Optional[str]
    source: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Weather data schemas
class WeatherDataResponse(BaseModel):
    id: int
    location: str
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: Optional[float]
    pressure: Optional[float]
    weather_condition: str
    forecast_days: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Crop recommendation schemas
class CropRecommendationRequest(BaseModel):
    location: str
    state: str
    district: str
    season: str  # kharif, rabi, summer

class CropRecommendationResponse(BaseModel):
    crop_name: str
    confidence_score: float
    expected_yield: float
    expected_profit: float
    sustainability_score: float
    fertilizer_recommendation: Optional[dict]
    planting_date: Optional[datetime]
    harvesting_date: Optional[datetime]
    expert_advice: Optional[str] = None

# Detection schemas
class DetectionResponse(BaseModel):
    type: str  # pest or disease
    name: str
    confidence_score: float
    recommended_treatment: Optional[str]
    severity: Optional[str]

# Market data schemas
class MarketDataResponse(BaseModel):
    crop_name: str
    market_name: str
    location: str
    price_per_kg: float
    date: datetime
    quality_grade: Optional[str]
    
    class Config:
        from_attributes = True

class MarketRecommendationResponse(BaseModel):
    crop_name: str
    best_markets: List[MarketDataResponse]
    average_price: float
    price_trend: str  # increasing, decreasing, stable

# Notification schemas
class NotificationCreate(BaseModel):
    message: str
    notification_type: str
    priority: str = "medium"

class NotificationResponse(BaseModel):
    id: int
    farmer_id: int
    message: str
    notification_type: str
    priority: str
    is_sent: bool
    sent_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

