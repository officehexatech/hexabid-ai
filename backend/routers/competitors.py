from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any, Optional
from models_gem import CompetitorProfile
from services.gem_scraper import gem_scraper
from routers.auth import get_current_user
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/competitors", tags=["Competitor Analysis"])

# MongoDB connection
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'test_database')]

@router.get("/analysis")
async def get_competitor_analysis(
    category: Optional[str] = None,
    days: int = 90,
    current_user: dict = Depends(get_current_user)
):
    """
    Get competitor analysis data
    """
    try:
        # Fetch competitor data from GEM
        competitor_data = gem_scraper.get_competitor_bids(category, days)
        
        # Save/update in database
        for competitor in competitor_data:
            await db.competitors.update_one(
                {"company_name": competitor['company_name']},
                {"$set": competitor},
                upsert=True
            )
        
        return {
            "success": True,
            "total_competitors": len(competitor_data),
            "competitors": competitor_data
        }
    except Exception as e:
        logger.error(f"Error fetching competitor analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list")
async def list_competitors(
    page: int = 1,
    limit: int = 20,
    sort_by: str = "win_rate",
    current_user: dict = Depends(get_current_user)
):
    """
    List all tracked competitors
    """
    try:
        skip = (page - 1) * limit
        
        # Sort options
        sort_order = -1 if sort_by in ['win_rate', 'total_bids', 'won_bids'] else 1
        
        cursor = db.competitors.find().sort(sort_by, sort_order).skip(skip).limit(limit)
        competitors = await cursor.to_list(length=limit)
        
        total = await db.competitors.count_documents({})
        
        return {
            "success": True,
            "total": total,
            "page": page,
            "limit": limit,
            "competitors": competitors
        }
    except Exception as e:
        logger.error(f"Error listing competitors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{competitor_id}/profile")
async def get_competitor_profile(
    competitor_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed profile of a competitor
    """
    try:
        competitor = await db.competitors.find_one({"competitor_id": competitor_id})
        
        if not competitor:
            raise HTTPException(status_code=404, detail="Competitor not found")
        
        return {
            "success": True,
            "competitor": competitor
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching competitor profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/compare/{tender_id}")
async def compare_competitors_for_tender(
    tender_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Compare competitors who bid on a specific tender
    """
    try:
        # Get bid submissions for this tender
        bids = await db.bid_submissions.find({"tender_id": tender_id}).to_list(length=100)
        
        if not bids:
            return {
                "success": True,
                "message": "No bids found for this tender",
                "comparison": []
            }
        
        # Get competitor profiles
        comparison = []
        for bid in bids:
            competitor = await db.competitors.find_one({"company_name": bid.get('company_name')})
            
            if competitor:
                comparison.append({
                    "company_name": competitor['company_name'],
                    "bid_amount": bid.get('bid_amount'),
                    "win_rate": competitor.get('win_rate', 0),
                    "avg_bid_amount": competitor.get('avg_bid_amount', 0),
                    "total_bids": competitor.get('total_bids', 0),
                    "won_bids": competitor.get('won_bids', 0)
                })
        
        # Sort by bid amount
        comparison.sort(key=lambda x: x['bid_amount'])
        
        return {
            "success": True,
            "tender_id": tender_id,
            "total_bidders": len(comparison),
            "comparison": comparison
        }
    except Exception as e:
        logger.error(f"Error comparing competitors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/insights")
async def get_competitor_insights(
    current_user: dict = Depends(get_current_user)
):
    """
    Get key insights about competitors
    """
    try:
        # Top competitors by win rate
        top_competitors = await db.competitors.find().sort("win_rate", -1).limit(5).to_list(length=5)
        
        # Most aggressive competitors (lowest avg bid)
        aggressive_competitors = await db.competitors.find().sort("avg_bid_amount", 1).limit(5).to_list(length=5)
        
        # Most active competitors (highest total bids)
        active_competitors = await db.competitors.find().sort("total_bids", -1).limit(5).to_list(length=5)
        
        # Overall stats
        total_competitors = await db.competitors.count_documents({})
        
        pipeline = [
            {"$group": {
                "_id": None,
                "avg_win_rate": {"$avg": "$win_rate"},
                "avg_bid_amount": {"$avg": "$avg_bid_amount"}
            }}
        ]
        
        stats = await db.competitors.aggregate(pipeline).to_list(length=1)
        overall_stats = stats[0] if stats else {}
        
        return {
            "success": True,
            "insights": {
                "total_competitors": total_competitors,
                "avg_market_win_rate": round(overall_stats.get('avg_win_rate', 0), 2),
                "avg_market_bid_amount": round(overall_stats.get('avg_bid_amount', 0), 2),
                "top_performers": top_competitors,
                "most_aggressive": aggressive_competitors,
                "most_active": active_competitors
            }
        }
    except Exception as e:
        logger.error(f"Error fetching competitor insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))
