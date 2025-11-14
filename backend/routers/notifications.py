from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import sys
sys.path.append('/app/backend')
from models_extended import Alert, AlertType, AlertChannel
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/")
async def get_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    alerts_cursor = db.alerts.find({"userId": current_user.id}, {"_id": 0}).sort("createdAt", -1).limit(50)
    alerts = await alerts_cursor.to_list(length=50)
    
    for alert in alerts:
        for date_field in ['sentAt', 'createdAt']:
            if alert.get(date_field) and isinstance(alert[date_field], str):
                alert[date_field] = datetime.fromisoformat(alert[date_field])
    
    return {"data": alerts}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_notification(
    alert_type: AlertType,
    title: str,
    message: str,
    related_id: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    alert = Alert(
        userId=current_user.id,
        alertType=alert_type,
        title=title,
        message=message,
        relatedId=related_id,
        channels=[AlertChannel.inapp]
    )
    
    alert_dict = alert.model_dump()
    alert_dict["createdAt"] = alert_dict["createdAt"].isoformat()
    
    await db.alerts.insert_one(alert_dict)
    return alert

@router.patch("/{alert_id}/read")
async def mark_as_read(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    result = await db.alerts.update_one(
        {"id": alert_id, "userId": current_user.id},
        {"$set": {"isRead": True}}
    )
    
    if result.matched_count == 0:
        return {"message": "Alert not found"}
    
    return {"message": "Marked as read"}

@router.get("/unread-count")
async def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    count = await db.alerts.count_documents({"userId": current_user.id, "isRead": False})
    return {"unreadCount": count}