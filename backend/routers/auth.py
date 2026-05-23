from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Farmer
from schemas import FarmerCreate, FarmerLogin, Token, FarmerResponse
from auth import verify_password, get_password_hash, create_access_token, get_current_farmer
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=FarmerResponse)
async def register_farmer(farmer: FarmerCreate, db: Session = Depends(get_db)):
    # Check if farmer already exists
    existing_farmer = db.query(Farmer).filter(
        (Farmer.email == farmer.email) | (Farmer.phone == farmer.phone)
    ).first()
    
    if existing_farmer:
        raise HTTPException(
            status_code=400,
            detail="Farmer with this email or phone already exists"
        )
    
    # Create new farmer
    hashed_password = get_password_hash(farmer.password)
    db_farmer = Farmer(
        name=farmer.name,
        email=farmer.email,
        phone=farmer.phone,
        location=farmer.location,
        state=farmer.state,
        district=farmer.district,
        village=farmer.village,
        hashed_password=hashed_password
    )
    
    db.add(db_farmer)
    db.commit()
    db.refresh(db_farmer)
    
    return db_farmer

@router.post("/login", response_model=Token)
async def login_farmer(farmer: FarmerLogin, db: Session = Depends(get_db)):
    # Authenticate farmer
    farmer_db = db.query(Farmer).filter(Farmer.email == farmer.email).first()
    
    if not farmer_db or not verify_password(farmer.password, farmer_db.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not farmer_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive farmer account"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(farmer_db.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=FarmerResponse)
async def get_current_farmer_info(current_farmer: Farmer = Depends(get_current_farmer)):
    return current_farmer

