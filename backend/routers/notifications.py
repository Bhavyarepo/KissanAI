from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Farmer, Notification
from schemas import NotificationCreate, NotificationResponse
from auth import get_current_farmer
from twilio.rest import Client
import os
from datetime import datetime
from typing import List

router = APIRouter()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Initialize Twilio client if credentials are available
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    twilio_client = None

@router.post("/send", response_model=NotificationResponse)
async def send_notification(
    notification: NotificationCreate,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Send notification to farmer"""
    try:
        # Create notification record
        db_notification = Notification(
            farmer_id=current_farmer.id,
            message=notification.message,
            notification_type=notification.notification_type,
            priority=notification.priority
        )
        
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        
        # Send SMS if Twilio is configured
        if twilio_client and current_farmer.phone:
            try:
                message = twilio_client.messages.create(
                    body=notification.message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=current_farmer.phone
                )
                
                # Update notification status
                db_notification.is_sent = True
                db_notification.sent_at = datetime.now()
                db.commit()
                
            except Exception as e:
                print(f"Failed to send SMS: {str(e)}")
        
        return db_notification
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")

@router.get("/history")
async def get_notification_history(
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Get farmer's notification history"""
    notifications = db.query(Notification).filter(
        Notification.farmer_id == current_farmer.id
    ).order_by(Notification.created_at.desc()).all()
    
    return notifications

@router.post("/weather-alert")
async def send_weather_alert(
    location: str,
    alert_type: str,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Send weather alert to farmer"""
    try:
        # Create weather alert message
        alert_messages = {
            'rain': f"Weather Alert: Heavy rainfall expected in {location}. Please take necessary precautions for your crops.",
            'drought': f"Weather Alert: Drought conditions expected in {location}. Consider irrigation planning.",
            'storm': f"Weather Alert: Storm warning for {location}. Secure your crops and equipment.",
            'heat': f"Weather Alert: High temperature warning for {location}. Monitor crop health closely."
        }
        
        message = alert_messages.get(alert_type, f"Weather Alert: {alert_type} expected in {location}")
        
        # Create notification
        notification = NotificationCreate(
            message=message,
            notification_type="weather",
            priority="high"
        )
        
        return await send_notification(notification, current_farmer, db)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending weather alert: {str(e)}")

@router.post("/market-alert")
async def send_market_alert(
    crop_name: str,
    price_change: str,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: Session = Depends(get_db)
):
    """Send market price alert to farmer"""
    try:
        message = f"Market Alert: {crop_name} prices have {price_change}. Check current market rates for better selling opportunities."
        
        notification = NotificationCreate(
            message=message,
            notification_type="market",
            priority="medium"
        )
        
        return await send_notification(notification, current_farmer, db)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending market alert: {str(e)}")





