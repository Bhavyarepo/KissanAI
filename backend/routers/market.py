from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Farmer, MarketData
from schemas import MarketDataResponse, MarketRecommendationResponse
from auth import get_current_farmer
from typing import List
import random
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/prices/{crop_name}", response_model=MarketRecommendationResponse)
async def get_market_prices(
    crop_name: str,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Get market prices and recommendations for a specific crop"""
    try:
        # Get market data for the crop
        market_data = db.query(MarketData).filter(
            MarketData.crop_name.ilike(f"%{crop_name}%")
        ).order_by(MarketData.date.desc()).limit(10).all()
        
        if not market_data:
            # Generate sample market data if none exists
            market_data = await _generate_sample_market_data(crop_name, db)
        
        # Calculate average price
        prices = [data.price_per_kg for data in market_data]
        average_price = sum(prices) / len(prices) if prices else 0
        
        # Determine price trend
        if len(prices) >= 2:
            recent_avg = sum(prices[:3]) / min(3, len(prices))
            older_avg = sum(prices[3:6]) / min(3, len(prices[3:6])) if len(prices) > 3 else recent_avg
            if recent_avg > older_avg * 1.05:
                price_trend = "increasing"
            elif recent_avg < older_avg * 0.95:
                price_trend = "decreasing"
            else:
                price_trend = "stable"
        else:
            price_trend = "stable"
        
        # Get best markets (top 3 by price)
        best_markets = sorted(market_data, key=lambda x: x.price_per_kg, reverse=True)[:3]
        
        return MarketRecommendationResponse(
            crop_name=crop_name,
            best_markets=best_markets,
            average_price=round(average_price, 2),
            price_trend=price_trend
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting market data: {str(e)}")

async def _generate_sample_market_data(crop_name: str, db: Session) -> List[MarketData]:
    """Generate sample market data for demonstration"""
    markets = [
        {"name": "Amaravathi Market", "location": "Amaravathi, AP"},
        {"name": "Guntur Market", "location": "Guntur, AP"},
        {"name": "Vijayawada Market", "location": "Vijayawada, AP"},
        {"name": "Hyderabad Market", "location": "Hyderabad, TS"},
        {"name": "Bangalore Market", "location": "Bangalore, KA"}
    ]
    
    # Base prices for different crops
    base_prices = {
        'rice': 25, 'wheat': 20, 'maize': 18, 'sugarcane': 3,
        'cotton': 60, 'millets': 15, 'tomato': 30, 'onion': 25
    }
    
    base_price = base_prices.get(crop_name.lower(), 20)
    
    market_data = []
    for i in range(5):
        market = random.choice(markets)
        price = base_price + random.uniform(-5, 10)
        
        db_market = MarketData(
            crop_name=crop_name,
            market_name=market['name'],
            location=market['location'],
            price_per_kg=round(price, 2),
            date=datetime.now() - timedelta(days=i),
            quality_grade=random.choice(['A', 'B', 'C'])
        )
        
        db.add(db_market)
        market_data.append(db_market)
    
    db.commit()
    return market_data

@router.get("/trends")
async def get_market_trends(
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Get market trends for all crops"""
    try:
        # Get all market data
        all_market_data = db.query(MarketData).order_by(MarketData.date.desc()).all()
        
        # Group by crop
        crop_trends = {}
        for data in all_market_data:
            if data.crop_name not in crop_trends:
                crop_trends[data.crop_name] = []
            crop_trends[data.crop_name].append(data.price_per_kg)
        
        # Calculate trends
        trends = []
        for crop, prices in crop_trends.items():
            if len(prices) >= 2:
                recent_avg = sum(prices[:3]) / min(3, len(prices))
                older_avg = sum(prices[3:6]) / min(3, len(prices[3:6])) if len(prices) > 3 else recent_avg
                
                if recent_avg > older_avg * 1.05:
                    trend = "increasing"
                elif recent_avg < older_avg * 0.95:
                    trend = "decreasing"
                else:
                    trend = "stable"
            else:
                trend = "stable"
            
            trends.append({
                'crop_name': crop,
                'current_price': round(prices[0], 2) if prices else 0,
                'trend': trend,
                'data_points': len(prices)
            })
        
        return trends
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting market trends: {str(e)}")





