from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv

from database import get_db, engine
from models import Base
from routers import auth, recommendations, soil, market, notifications, detection
# Updated endpoints will be exposed via new unified router `api_v2`
from routers import api_v2
from services.ml_service import MLService

# Load environment variables
load_dotenv()

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="AI Crop Recommendation and Farmer Advisory System",
    description="An AI-powered system for crop recommendations, pest/disease detection, and farmer advisory",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations (legacy)"])
app.include_router(soil.router, prefix="/api/soil", tags=["Soil Data (legacy)"])
app.include_router(market.router, prefix="/api/market", tags=["Market Advisory (legacy)"])
app.include_router(notifications.router, prefix="/api/notifications", tags=["Notifications"])
app.include_router(detection.router, prefix="/api/detection", tags=["Detection"])
app.include_router(api_v2.router, prefix="/api", tags=["v2"])

# Initialize ML service
ml_service = MLService()

@app.get("/")
async def root():
    return {"message": "AI Crop Recommendation and Farmer Advisory System API"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Simple query to check DB
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

