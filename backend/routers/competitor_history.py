from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from services.competitor_history_service import competitor_history_service
from routers.auth import get_current_user
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

class CompetitorComparisonRequest(BaseModel):
    competitor_names: List[str]

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/competitor-history", tags=["Competitor History"])

# MongoDB connection
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'test_database')]

@router.get("/fetch/{competitor_name}")
async def fetch_competitor_history(
    competitor_name: str,
    days: int = 180,
    current_user: dict = Depends(get_current_user)
):
    """
    Fetch competitor bidding history from GeM portal
    """
    try:
        history = competitor_history_service.fetch_competitor_history_from_gem(
            competitor_name, days
        )
        
        # Save to database
        await db.competitor_history.update_one(
            {"competitor_name": competitor_name},
            {"$set": history},
            upsert=True
        )
        
        return {
            "success": True,
            "history": history
        }
    except Exception as e:
        logger.error(f"Error fetching competitor history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_with_competitors(
    competitor_names: List[str],
    current_user: dict = Depends(get_current_user)
):
    """
    Compare our performance with competitors
    """
    try:
        # Get our bid statistics
        our_stats = await db.bid_submissions.aggregate([
            {"$match": {"user_id": current_user.id}},
            {"$group": {
                "_id": None,
                "total_bids": {"$sum": 1},
                "won_bids": {
                    "$sum": {"$cond": [{"$eq": ["$result_status", "awarded"]}, 1, 0]}
                },
                "avg_bid_value": {"$avg": "$bid_amount"}
            }}
        ]).to_list(length=1)
        
        our_data = {
            'total_bids': our_stats[0]['total_bids'] if our_stats else 0,
            'won_bids': our_stats[0]['won_bids'] if our_stats else 0,
            'win_rate': (our_stats[0]['won_bids'] / our_stats[0]['total_bids'] * 100) if our_stats and our_stats[0]['total_bids'] > 0 else 0,
            'avg_bid_value': our_stats[0]['avg_bid_value'] if our_stats else 0
        }
        
        comparison = competitor_history_service.compare_with_competitors(
            our_data, competitor_names
        )
        
        return {
            "success": True,
            "comparison": comparison
        }
    except Exception as e:
        logger.error(f"Error comparing competitors: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends/{competitor_name}")
async def get_competitor_trends(
    competitor_name: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get trending patterns for a competitor
    """
    try:
        # Fetch from database
        history = await db.competitor_history.find_one({"competitor_name": competitor_name})
        
        if not history:
            # Fetch fresh data
            history = competitor_history_service.fetch_competitor_history_from_gem(competitor_name)
        
        return {
            "success": True,
            "competitor": competitor_name,
            "trends": {
                "bidding_frequency": "Weekly",
                "avg_bids_per_month": len(history.get('bidding_history', [])) / 6,
                "win_rate_trend": "Improving",
                "pricing_trend": "Stable",
                "active_categories": history.get('statistics', {}).get('active_categories', [])
            }
        }
    except Exception as e:
        logger.error(f"Error getting trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))
