from fastapi import APIRouter, HTTPException, Depends
from typing import List
from services.cpp_portal_scraper import cpp_scraper
from routers.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cpp", tags=["CPP Portal"])

@router.get("/tenders/search")
async def search_cpp_tenders(
    keywords: str,
    category: str = None,
    max_results: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for tenders on CPP Portal
    """
    try:
        tenders = cpp_scraper.search_tenders(keywords, category, max_results)
        
        return {
            "success": True,
            "source": "CPP Portal",
            "total": len(tenders),
            "tenders": tenders
        }
    except Exception as e:
        logger.error(f"Error searching CPP tenders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/ministry/{ministry_name}/tenders")
async def get_ministry_tenders(
    ministry_name: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all active tenders from a specific ministry
    """
    try:
        tenders = cpp_scraper.get_ministry_tenders(ministry_name)
        
        return {
            "success": True,
            "ministry": ministry_name,
            "total": len(tenders),
            "tenders": tenders
        }
    except Exception as e:
        logger.error(f"Error fetching ministry tenders: {e}")
        raise HTTPException(status_code=500, detail=str(e))
