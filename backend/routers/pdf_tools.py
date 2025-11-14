from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Dict, Any
from pydantic import BaseModel
from services.pdf_tools_service import pdf_tools_service
from routers.auth import get_current_user
import logging
import os

class PDFMergeRequest(BaseModel):
    file_paths: List[str]

class PDFSplitRequest(BaseModel):
    file_path: str
    page_ranges: List[Dict[str, Any]]

class PDFCompressRequest(BaseModel):
    file_path: str
    quality: str = "medium"

class PDFRotateRequest(BaseModel):
    file_path: str
    angle: int
    pages: str = "all"

class PDFWatermarkRequest(BaseModel):
    file_path: str
    watermark_text: str

class PDFProtectRequest(BaseModel):
    file_path: str
    password: str

class PDFExtractTextRequest(BaseModel):
    file_path: str

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/pdf-tools", tags=["PDF Tools"])

@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload PDF file for processing
    """
    try:
        # Save uploaded file
        file_path = os.path.join(pdf_tools_service.UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Get PDF info
        info = await pdf_tools_service.get_pdf_info(file_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "file_path": file_path,
            "info": info.get('info', {})
        }
    except Exception as e:
        logger.error(f"Error uploading PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/merge")
async def merge_pdfs(
    request: PDFMergeRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Merge multiple PDF files
    """
    try:
        result = await pdf_tools_service.merge_pdfs(request.file_paths)
        return result
    except Exception as e:
        logger.error(f"Error merging PDFs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/split")
async def split_pdf(
    request: PDFSplitRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Split PDF into multiple files
    """
    try:
        result = await pdf_tools_service.split_pdf(request.file_path, request.page_ranges)
        return result
    except Exception as e:
        logger.error(f"Error splitting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compress")
async def compress_pdf(
    request: PDFCompressRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Compress PDF file
    """
    try:
        result = await pdf_tools_service.compress_pdf(request.file_path, request.quality)
        return result
    except Exception as e:
        logger.error(f"Error compressing PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/rotate")
async def rotate_pdf(
    request: PDFRotateRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Rotate PDF pages
    """
    try:
        result = await pdf_tools_service.rotate_pdf(request.file_path, request.angle, request.pages)
        return result
    except Exception as e:
        logger.error(f"Error rotating PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/watermark")
async def add_watermark(
    request: PDFWatermarkRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Add watermark to PDF
    """
    try:
        result = await pdf_tools_service.add_watermark(file_path, watermark_text)
        return result
    except Exception as e:
        logger.error(f"Error adding watermark: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/protect")
async def protect_pdf(
    file_path: str,
    password: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Password protect PDF
    """
    try:
        result = await pdf_tools_service.protect_pdf(file_path, password)
        return result
    except Exception as e:
        logger.error(f"Error protecting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract-text")
async def extract_text(
    file_path: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Extract text from PDF
    """
    try:
        result = await pdf_tools_service.extract_text(file_path)
        return result
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/to-images")
async def pdf_to_images(
    file_path: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Convert PDF to images
    """
    try:
        result = await pdf_tools_service.pdf_to_images(file_path)
        return result
    except Exception as e:
        logger.error(f"Error converting PDF: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info")
async def get_pdf_info(
    file_path: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get PDF metadata and information
    """
    try:
        result = await pdf_tools_service.get_pdf_info(file_path)
        return result
    except Exception as e:
        logger.error(f"Error getting PDF info: {e}")
        raise HTTPException(status_code=500, detail=str(e))
