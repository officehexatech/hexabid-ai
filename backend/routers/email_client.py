from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from services.email_service import email_service
from routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/email", tags=["Email Client"])

class EmailSend(BaseModel):
    to: List[str]
    subject: str
    body: str
    attachments: List[str] = []

class EmailDraft(BaseModel):
    to: List[str]
    subject: str
    body: str

class EmailMarkReadRequest(BaseModel):
    email_ids: List[str]

class EmailDeleteRequest(BaseModel):
    email_ids: List[str]

@router.post("/send")
async def send_email(
    email: EmailSend,
    current_user: dict = Depends(get_current_user)
):
    """
    Send email (Gmail API / SMTP - Mocked)
    """
    try:
        result = await email_service.send_email(
            email.to, email.subject, email.body, email.attachments
        )
        return result
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/inbox")
async def get_inbox(
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch inbox emails (Mocked)
    """
    try:
        result = await email_service.fetch_emails("inbox", limit)
        return result
    except Exception as e:
        logger.error(f"Error fetching inbox: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sent")
async def get_sent(
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch sent emails (Mocked)
    """
    try:
        result = await email_service.fetch_emails("sent", limit)
        return result
    except Exception as e:
        logger.error(f"Error fetching sent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/drafts/create")
async def create_draft(
    draft: EmailDraft,
    current_user: dict = Depends(get_current_user)
):
    """
    Create email draft (Mocked)
    """
    try:
        result = await email_service.create_draft(draft.to, draft.subject, draft.body)
        return result
    except Exception as e:
        logger.error(f"Error creating draft: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mark-read")
async def mark_as_read(
    request: EmailMarkReadRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark emails as read
    """
    try:
        result = await email_service.mark_as_read(request.email_ids)
        return result
    except Exception as e:
        logger.error(f"Error marking emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete")
async def delete_emails(
    request: EmailDeleteRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete emails
    """
    try:
        result = await email_service.delete_emails(request.email_ids)
        return result
    except Exception as e:
        logger.error(f"Error deleting emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))
