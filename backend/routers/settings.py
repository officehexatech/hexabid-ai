from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime, timezone
from models import User
from routers.auth import get_current_user

router = APIRouter()

def get_db():
    from server import db
    return db

class SocialMediaLink(BaseModel):
    platform: str  # facebook, twitter, linkedin, instagram, youtube
    url: HttpUrl
    icon: Optional[str] = None

class ContactInfo(BaseModel):
    phone1: str = "+91 8806106575"
    phone2: str = "+91 9607500750"
    email: str = "support@cctverp.com"
    whatsappNumber: str = "+918806106575"

class PlatformSettings(BaseModel):
    contactInfo: ContactInfo
    socialMediaLinks: List[SocialMediaLink] = []
    enableChatbot: bool = True

class SettingsUpdate(BaseModel):
    contactInfo: Optional[ContactInfo] = None
    socialMediaLinks: Optional[List[SocialMediaLink]] = None
    enableChatbot: Optional[bool] = None

@router.get("/public", response_model=PlatformSettings)
async def get_public_settings(db: AsyncIOMotorDatabase = Depends(get_db)):
    """Get public platform settings (no auth required)"""
    settings_doc = await db.platform_settings.find_one({"type": "public"}, {"_id": 0})
    
    if not settings_doc:
        # Return default settings
        default_settings = PlatformSettings(
            contactInfo=ContactInfo(),
            socialMediaLinks=[
                {"platform": "facebook", "url": "https://facebook.com/hexabid"},
                {"platform": "twitter", "url": "https://twitter.com/hexabid"},
                {"platform": "linkedin", "url": "https://linkedin.com/company/hexabid"},
            ],
            enableChatbot=True
        )
        return default_settings
    
    return PlatformSettings(**settings_doc)

@router.patch("/admin", response_model=PlatformSettings)
async def update_settings(
    settings_update: SettingsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update platform settings (admin only)"""
    # TODO: Add admin role check
    # For now, any authenticated user can update
    
    existing_settings = await db.platform_settings.find_one({"type": "public"})
    
    if existing_settings:
        # Update existing settings
        update_data = {k: v for k, v in settings_update.model_dump(exclude_unset=True).items()}
        update_data["updatedAt"] = datetime.now(timezone.utc).isoformat()
        update_data["updatedBy"] = current_user.id
        
        # Convert nested models to dict
        if "contactInfo" in update_data:
            update_data["contactInfo"] = update_data["contactInfo"].model_dump()
        if "socialMediaLinks" in update_data:
            update_data["socialMediaLinks"] = [link.model_dump() for link in update_data["socialMediaLinks"]]
        
        await db.platform_settings.update_one(
            {"type": "public"},
            {"$set": update_data}
        )
    else:
        # Create new settings
        settings_doc = {
            "type": "public",
            "contactInfo": settings_update.contactInfo.model_dump() if settings_update.contactInfo else ContactInfo().model_dump(),
            "socialMediaLinks": [link.model_dump() for link in settings_update.socialMediaLinks] if settings_update.socialMediaLinks else [],
            "enableChatbot": settings_update.enableChatbot if settings_update.enableChatbot is not None else True,
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "createdBy": current_user.id
        }
        await db.platform_settings.insert_one(settings_doc)
    
    # Return updated settings
    updated = await db.platform_settings.find_one({"type": "public"}, {"_id": 0})
    return PlatformSettings(**updated)