from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List
from pydantic import BaseModel
from services.office365_service import office365_service
from routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/office365", tags=["Office 365"])

class DocumentCreate(BaseModel):
    document_type: str  # word, excel, powerpoint
    title: str

class DocumentShare(BaseModel):
    document_id: str
    emails: List[str]
    permission: str = "view"  # view, edit

@router.post("/documents/create")
async def create_document(
    doc: DocumentCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new Office document (Mocked)
    """
    try:
        result = await office365_service.create_document(doc.document_type, doc.title)
        return result
    except Exception as e:
        logger.error(f"Error creating document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/list")
async def list_documents(
    folder: str = "root",
    limit: int = 50,
    current_user: dict = Depends(get_current_user)
):
    """
    List OneDrive documents (Mocked)
    """
    try:
        result = await office365_service.list_documents(folder, limit)
        return result
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get document details (Mocked)
    """
    try:
        result = await office365_service.get_document(document_id)
        return result
    except Exception as e:
        logger.error(f"Error getting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_to_onedrive(
    file: UploadFile = File(...),
    folder: str = "root",
    current_user: dict = Depends(get_current_user)
):
    """
    Upload file to OneDrive (Mocked)
    """
    try:
        # In real implementation, would upload the file
        result = await office365_service.upload_to_onedrive(file.filename, folder)
        return result
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/share")
async def share_document(
    share: DocumentShare,
    current_user: dict = Depends(get_current_user)
):
    """
    Share document with users (Mocked)
    """
    try:
        result = await office365_service.share_document(
            share.document_id, share.emails, share.permission
        )
        return result
    except Exception as e:
        logger.error(f"Error sharing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
