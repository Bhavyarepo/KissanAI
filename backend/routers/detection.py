from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import Farmer, PestDetection, DiseaseDetection
from auth import get_current_farmer
from services.ml_service import MLService
from services.gemini_service import GeminiService
import os
import uuid
from typing import List

router = APIRouter()
ml_service = MLService()
gemini_service = GeminiService()

@router.post("/pest")
async def detect_pest(
    file: UploadFile = File(...),
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    os.makedirs("uploads", exist_ok=True)
    filename = f"pest_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    path = os.path.join("uploads", filename)
    with open(path, 'wb') as f:
        f.write(await file.read())
    
    # Validation: Is it a crop?
    is_crop, message = await gemini_service.is_image_a_crop(path)
    if not is_crop:
        os.remove(path)
        raise HTTPException(status_code=400, detail=message)
    
    # Detection
    result = ml_service.detect_pest_disease(path, 'pest')
    
    # Save to history
    db_detection = PestDetection(
        farmer_id=int(current_farmer.id),
        pest_type=str(result['name']),
        confidence_score=float(result['confidence_score']),
        image_path=str(path),
        recommended_treatment=str(result['recommended_treatment']),
        severity=str(result['severity'])
    )
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    
    return result

@router.post("/disease")
async def detect_disease(
    file: UploadFile = File(...),
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    os.makedirs("uploads", exist_ok=True)
    filename = f"disease_{uuid.uuid4()}.{file.filename.split('.')[-1]}"
    path = os.path.join("uploads", filename)
    with open(path, 'wb') as f:
        f.write(await file.read())
    
    # Validation: Is it a crop?
    is_crop, message = await gemini_service.is_image_a_crop(path)
    if not is_crop:
        os.remove(path)
        raise HTTPException(status_code=400, detail=message)
    
    # Detection
    result = ml_service.detect_pest_disease(path, 'disease')
    
    # Save to history
    db_detection = DiseaseDetection(
        farmer_id=int(current_farmer.id),
        disease_type=str(result['name']),
        confidence_score=float(result['confidence_score']),
        image_path=str(path),
        recommended_treatment=str(result['recommended_treatment']),
        severity=str(result['severity'])
    )
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    
    return result

@router.get("/pest/history")
async def get_pest_history(
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    return db.query(PestDetection).filter(PestDetection.farmer_id == current_farmer.id).order_by(PestDetection.created_at.desc()).all()

@router.get("/disease/history")
async def get_disease_history(
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    return db.query(DiseaseDetection).filter(DiseaseDetection.farmer_id == current_farmer.id).order_by(DiseaseDetection.created_at.desc()).all()
