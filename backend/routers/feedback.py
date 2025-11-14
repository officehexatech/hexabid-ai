from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel, EmailStr
from datetime import datetime, timezone
import uuid

router = APIRouter()

def get_db():
    from server import db
    return db

class FeedbackSubmission(BaseModel):
    name: str
    email: EmailStr
    category: str
    subject: str
    message: str
    submittedAt: str

@router.post("/")
async def submit_feedback(
    feedback: FeedbackSubmission,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Submit user feedback"""
    feedback_doc = {
        "id": str(uuid.uuid4()),
        **feedback.model_dump(),
        "status": "pending",
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    await db.feedback.insert_one(feedback_doc)
    
    return {
        "success": True,
        "message": "Feedback submitted successfully"
    }
