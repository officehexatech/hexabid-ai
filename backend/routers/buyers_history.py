from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from services.buyers_history_service import buyers_history_service
from routers.auth import get_current_user
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

class BuyersAnalysisRequest(BaseModel):
    keywords: List[str]
    days: int = 365

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/buyers", tags=["Buyers History"])

# MongoDB connection
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'test_database')]

@router.post("/analyze")
async def analyze_buyers(
    request: BuyersAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze buyer organizations based on keywords
    """
    try:
        analysis = buyers_history_service.analyze_buyers_for_keywords(request.keywords, request.days)
        
        return {
            "success": True,
            "analysis": analysis
        }
    except Exception as e:
        logger.error(f"Error analyzing buyers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommendations")
async def get_buyer_recommendations(
    current_user: dict = Depends(get_current_user)
):
    """
    Get buyer recommendations based on user's company profile
    """
    try:
        # Fetch company profile
        company = await db.companies.find_one({"userId": current_user.id})
        
        if not company:
            return {
                "success": False,
                "message": "Company profile not found. Please complete your profile first."
            }
        
        # Extract keywords from company profile
        company_profile = {
            'keywords': company.get('businessCategories', []),
            'categories': company.get('productCategories', [])
        }
        
        recommendations = buyers_history_service.get_buyer_recommendations(company_profile)
        
        return {
            "success": True,
            "total_recommendations": len(recommendations),
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"Error getting buyer recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights")
async def get_buyers_insights(
    keywords: List[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """
    Get insights about buyer market
    """
    try:
        if not keywords:
            # Get keywords from company profile
            company = await db.companies.find_one({"userId": current_user.id})
            if company:
                keywords = company.get('businessCategories', ['IT', 'Hardware'])
            else:
                keywords = ['IT', 'Hardware']
        
        analysis = buyers_history_service.analyze_buyers_for_keywords(keywords)
        
        return {
            "success": True,
            "insights": analysis['insights']
        }
    except Exception as e:
        logger.error(f"Error getting insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))
