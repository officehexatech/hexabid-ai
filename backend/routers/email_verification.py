from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timedelta, timezone
import uuid
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.post("/send-verification")
async def send_verification_email(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if already verified
    if current_user.emailVerified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already verified")
    
    # Generate verification token
    token = str(uuid.uuid4())
    expires_at = datetime.now(timezone.utc) + timedelta(hours=24)
    
    # Store token
    token_doc = {
        "id": str(uuid.uuid4()),
        "userId": current_user.id,
        "token": token,
        "expiresAt": expires_at.isoformat(),
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    await db.email_verification_tokens.insert_one(token_doc)
    
    # TODO: Send email with verification link in Phase 5
    # For now, return the token for testing
    verification_link = f"https://hexabid.in/verify-email?token={token}"
    
    return {
        "message": "Verification email sent",
        "token": token,  # Remove this in production
        "verificationLink": verification_link  # Remove this in production
    }

@router.post("/verify")
async def verify_email(
    token: str,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Find token
    token_doc = await db.email_verification_tokens.find_one({"token": token})
    if not token_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid verification token")
    
    # Check if expired
    expires_at = datetime.fromisoformat(token_doc["expiresAt"])
    if expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification token expired")
    
    # Mark user as verified
    await db.users.update_one(
        {"id": token_doc["userId"]},
        {"$set": {"emailVerified": True}}
    )
    
    # Delete token
    await db.email_verification_tokens.delete_one({"token": token})
    
    return {"message": "Email verified successfully"}

@router.get("/status")
async def get_verification_status(
    current_user: User = Depends(get_current_user)
):
    return {
        "emailVerified": current_user.emailVerified,
        "email": current_user.email
    }