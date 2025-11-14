from fastapi import APIRouter, HTTPException, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from typing import Optional
import sys
sys.path.append('/app/backend')
from models_extended import Alert, AlertType, AlertChannel
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/")
async def get_alerts(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    alert_type: Optional[str] = None,
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    skip = (page - 1) * limit
    query = {"userId": current_user.id}
    
    if alert_type:
        query["alertType"] = alert_type
    if unread_only:
        query["isRead"] = False
    
    total = await db.alerts.count_documents(query)
    alerts_cursor = db.alerts.find(query, {"_id": 0}).skip(skip).limit(limit).sort("createdAt", -1)
    alerts = await alerts_cursor.to_list(length=limit)
    
    for alert in alerts:
        for date_field in ['sentAt', 'createdAt']:
            if alert.get(date_field) and isinstance(alert[date_field], str):
                alert[date_field] = datetime.fromisoformat(alert[date_field])
    
    # Count unread
    unread_count = await db.alerts.count_documents({"userId": current_user.id, "isRead": False})
    
    return {
        "data": alerts,
        "unreadCount": unread_count,
        "pagination": {"page": page, "limit": limit, "total": total, "totalPages": (total + limit - 1) // limit}
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Create alert using the Alert model
    alert = Alert(
        userId=current_user.id,
        alertType=alert_data.get("alertType", "status_update"),
        title=alert_data["title"],
        message=alert_data["message"],
        relatedId=alert_data.get("relatedId"),
        channels=alert_data.get("channels", ["inapp"])
    )
    
    alert_dict = alert.model_dump()
    
    # Convert datetime to ISO string for MongoDB storage
    for date_field in ['sentAt', 'createdAt']:
        if alert_dict.get(date_field):
            alert_dict[date_field] = alert_dict[date_field].isoformat()
    
    await db.alerts.insert_one(alert_dict)
    
    return alert

@router.patch("/{alert_id}/read")
async def mark_alert_read(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    result = await db.alerts.update_one(
        {"id": alert_id, "userId": current_user.id},
        {"$set": {"isRead": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return {"message": "Alert marked as read"}

@router.patch("/mark-all-read")
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    result = await db.alerts.update_many(
        {"userId": current_user.id, "isRead": False},
        {"$set": {"isRead": True}}
    )
    return {"message": f"Marked {result.modified_count} alerts as read"}

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    result = await db.alerts.delete_one({"id": alert_id, "userId": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    return None
