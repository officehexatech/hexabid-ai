from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
from models_gem import BidSubmission, BidResult
from services.gem_scraper import gem_scraper
from routers.auth import get_current_user
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/gem", tags=["GEM Integration"])

# MongoDB connection
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'test_database')]

@router.get("/tenders/search")
async def search_gem_tenders(
    keywords: str,
    category: str = None,
    max_results: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Search for tenders on GeM portal
    """
    try:
        tenders = gem_scraper.search_tenders(keywords, category, max_results)
        
        return {
            "success": True,
            "total": len(tenders),
            "tenders": tenders
        }
    except Exception as e:
        logger.error(f"Error searching tenders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tenders/{tender_number}/details")
async def get_tender_details(
    tender_number: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get detailed information about a tender
    """
    try:
        details = gem_scraper.get_tender_details(tender_number)
        
        if not details:
            raise HTTPException(status_code=404, detail="Tender not found")
        
        return {
            "success": True,
            "tender": details
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching tender details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bids/submit")
async def submit_bid(
    bid: BidSubmission,
    current_user: dict = Depends(get_current_user)
):
    """
    Submit a bid for a tender
    """
    try:
        bid.user_id = current_user['user_id']
        bid.status = 'submitted'
        
        from datetime import datetime
        bid.submission_date = datetime.utcnow().isoformat()
        
        # Save to database
        bid_dict = bid.dict()
        await db.bid_submissions.insert_one(bid_dict)
        
        return {
            "success": True,
            "message": "Bid submitted successfully",
            "bid_id": bid.bid_id
        }
    except Exception as e:
        logger.error(f"Error submitting bid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bids/my-bids")
async def get_my_bids(
    status: str = None,
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all bids submitted by current user
    """
    try:
        query = {"user_id": current_user['user_id']}
        if status:
            query["status"] = status
        
        skip = (page - 1) * limit
        
        bids_cursor = db.bid_submissions.find(query).skip(skip).limit(limit)
        bids = await bids_cursor.to_list(length=limit)
        
        total = await db.bid_submissions.count_documents(query)
        
        return {
            "success": True,
            "total": total,
            "page": page,
            "limit": limit,
            "bids": bids
        }
    except Exception as e:
        logger.error(f"Error fetching bids: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/bids/{bid_id}/status")
async def track_bid_status(
    bid_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Track the status of a submitted bid
    """
    try:
        # Get bid from database
        bid = await db.bid_submissions.find_one({"bid_id": bid_id, "user_id": current_user['user_id']})
        
        if not bid:
            raise HTTPException(status_code=404, detail="Bid not found")
        
        # Get live status from GEM
        status = gem_scraper.track_bid_status(bid_id)
        
        # Update database
        await db.bid_submissions.update_one(
            {"bid_id": bid_id},
            {"$set": {
                "status": status['status'],
                "last_updated": status['last_updated'],
                "remarks": status.get('remarks')
            }}
        )
        
        return {
            "success": True,
            "bid": bid,
            "live_status": status
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error tracking bid: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{tender_number}")
async def get_bid_results(
    tender_number: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get results for a tender
    """
    try:
        results = gem_scraper.get_bid_results(tender_number)
        
        if not results:
            raise HTTPException(status_code=404, detail="Results not available")
        
        # Save to database
        await db.bid_results.update_one(
            {"tender_number": tender_number},
            {"$set": results},
            upsert=True
        )
        
        return {
            "success": True,
            "results": results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard/stats")
async def get_bid_dashboard_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Get dashboard statistics for bids
    """
    try:
        user_id = current_user['user_id']
        
        # Count bids by status
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$status",
                "count": {"$sum": 1}
            }}
        ]
        
        status_counts = {}
        async for doc in db.bid_submissions.aggregate(pipeline):
            status_counts[doc['_id']] = doc['count']
        
        # Get won/lost stats
        total_bids = await db.bid_submissions.count_documents({"user_id": user_id})
        won_bids = await db.bid_submissions.count_documents({"user_id": user_id, "result_status": "awarded"})
        lost_bids = await db.bid_submissions.count_documents({"user_id": user_id, "result_status": "rejected"})
        
        win_rate = (won_bids / total_bids * 100) if total_bids > 0 else 0
        
        return {
            "success": True,
            "stats": {
                "total_bids": total_bids,
                "won_bids": won_bids,
                "lost_bids": lost_bids,
                "pending_bids": total_bids - won_bids - lost_bids,
                "win_rate": round(win_rate, 2),
                "status_breakdown": status_counts
            }
        }
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
