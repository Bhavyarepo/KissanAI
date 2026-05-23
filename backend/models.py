from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Farmer(Base):
    __tablename__ = "farmers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    location = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    village = Column(String(50), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    crop_history = relationship("CropHistory", back_populates="farmer")
    soil_data = relationship("SoilData", back_populates="farmer")
    notifications = relationship("Notification", back_populates="farmer")

class SoilData(Base):
    __tablename__ = "soil_data"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    location = Column(String(100), nullable=False)
    ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)
    phosphorus = Column(Float, nullable=True)
    potassium = Column(Float, nullable=True)
    organic_matter = Column(Float, nullable=True)
    moisture = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    soil_type = Column(String(50), nullable=True)
    source = Column(String(50), default="api")  # api, dataset, manual
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="soil_data")

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100), nullable=False)
    temperature = Column(Float, nullable=False)
    humidity = Column(Float, nullable=False)
    rainfall = Column(Float, nullable=False)
    wind_speed = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    weather_condition = Column(String(50), nullable=False)
    forecast_days = Column(Integer, default=7)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CropHistory(Base):
    __tablename__ = "crop_history"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    crop_name = Column(String(100), nullable=False)
    season = Column(String(20), nullable=False)  # kharif, rabi, summer
    year = Column(Integer, nullable=False)
    area_planted = Column(Float, nullable=False)  # in acres
    yield_obtained = Column(Float, nullable=True)  # in kg
    fertilizer_used = Column(Text, nullable=True)  # JSON string
    profit_loss = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="crop_history")

class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    crop_name = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    expected_yield = Column(Float, nullable=False)
    expected_profit = Column(Float, nullable=False)
    sustainability_score = Column(Float, nullable=False)
    fertilizer_recommendation = Column(Text, nullable=True)  # JSON string
    planting_date = Column(DateTime, nullable=True)
    harvesting_date = Column(DateTime, nullable=True)
    expert_advice = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PestDetection(Base):
    __tablename__ = "pest_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    pest_type = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    image_path = Column(String(255), nullable=False)
    recommended_treatment = Column(Text, nullable=True)
    severity = Column(String(20), nullable=True)  # low, medium, high
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DiseaseDetection(Base):
    __tablename__ = "disease_detections"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    disease_type = Column(String(100), nullable=False)
    confidence_score = Column(Float, nullable=False)
    image_path = Column(String(255), nullable=False)
    recommended_treatment = Column(Text, nullable=True)
    severity = Column(String(20), nullable=True)  # low, medium, high
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MarketData(Base):
    __tablename__ = "market_data"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_name = Column(String(100), nullable=False)
    market_name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    price_per_kg = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    quality_grade = Column(String(20), nullable=True)  # A, B, C
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    farmer_id = Column(Integer, ForeignKey("farmers.id"))
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # weather, market, reminder
    priority = Column(String(20), default="medium")  # low, medium, high
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    farmer = relationship("Farmer", back_populates="notifications")

