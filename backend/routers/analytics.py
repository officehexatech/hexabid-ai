from fastapi import APIRouter, HTTPException, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from typing import Optional
import sys
sys.path.append('/app/backend')
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Tender metrics
    total_tenders = await db.tenders.count_documents({"userId": current_user.id})
    active_tenders = await db.tenders.count_documents({"userId": current_user.id, "status": {"$in": ["new", "in_progress"]}})
    submitted_tenders = await db.tenders.count_documents({"userId": current_user.id, "status": "submitted"})
    won_tenders = await db.tenders.count_documents({"userId": current_user.id, "status": "won"})
    lost_tenders = await db.tenders.count_documents({"userId": current_user.id, "status": "lost"})
    
    # Calculate win rate
    closed_tenders = won_tenders + lost_tenders
    win_rate = (won_tenders / closed_tenders * 100) if closed_tenders > 0 else 0.0
    
    # Total tender value (sum of tenderValue field)
    tender_pipeline = [
        {"$match": {"userId": current_user.id, "tenderValue": {"$exists": True}}},
        {"$group": {"_id": None, "totalValue": {"$sum": "$tenderValue"}}}
    ]
    tender_value_result = await db.tenders.aggregate(tender_pipeline).to_list(length=1)
    total_value = tender_value_result[0]["totalValue"] if tender_value_result else 0.0
    avg_tender_value = total_value / total_tenders if total_tenders > 0 else 0.0
    
    # Vendor metrics
    total_vendors = await db.vendors.count_documents({"userId": current_user.id, "isActive": True})
    
    # RFQ metrics
    total_rfqs = await db.rfqs.count_documents({"userId": current_user.id})
    open_rfqs = await db.rfqs.count_documents({"userId": current_user.id, "status": {"$in": ["draft", "sent"]}})
    
    # Product metrics
    total_products = await db.products.count_documents({"userId": current_user.id, "isActive": True})
    
    # BOQ metrics
    total_boqs = await db.boqs.count_documents({"userId": current_user.id})
    
    # Team size
    team_result = await db.companies.find_one({"userId": current_user.id}, {"teamMembers": 1})
    team_size = len(team_result.get("teamMembers", [])) if team_result else 0
    
    return {
        "tenders": {
            "total": total_tenders,
            "active": active_tenders,
            "submitted": submitted_tenders,
            "won": won_tenders,
            "lost": lost_tenders,
            "winRate": round(win_rate, 2),
            "totalValue": round(total_value, 2),
            "avgValue": round(avg_tender_value, 2)
        },
        "vendors": {
            "total": total_vendors
        },
        "rfqs": {
            "total": total_rfqs,
            "open": open_rfqs
        },
        "products": {
            "total": total_products
        },
        "boqs": {
            "total": total_boqs
        },
        "team": {
            "size": team_size
        }
    }

@router.get("/tender-stats")
async def get_tender_stats(
    period: str = Query("month", regex="^(week|month|quarter|year)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Calculate date range based on period
    now = datetime.now(timezone.utc)
    if period == "week":
        days = 7
    elif period == "month":
        days = 30
    elif period == "quarter":
        days = 90
    else:  # year
        days = 365
    
    from datetime import timedelta
    start_date = now - timedelta(days=days)
    
    # Get tenders grouped by status
    pipeline = [
        {
            "$match": {
                "userId": current_user.id,
                "createdAt": {"$gte": start_date.isoformat()}
            }
        },
        {
            "$group": {
                "_id": "$status",
                "count": {"$sum": 1},
                "totalValue": {"$sum": "$tenderValue"}
            }
        }
    ]
    
    results = await db.tenders.aggregate(pipeline).to_list(length=100)
    
    status_breakdown = {}
    for result in results:
        status_breakdown[result["_id"]] = {
            "count": result["count"],
            "totalValue": round(result.get("totalValue", 0), 2)
        }
    
    return {
        "period": period,
        "statusBreakdown": status_breakdown
    }

@router.get("/recent-activity")
async def get_recent_activity(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Get recent tenders
    recent_tenders = await db.tenders.find(
        {"userId": current_user.id},
        {"_id": 0, "id": 1, "title": 1, "status": 1, "createdAt": 1, "updatedAt": 1}
    ).sort("updatedAt", -1).limit(limit).to_list(length=limit)
    
    # Get recent RFQs
    recent_rfqs = await db.rfqs.find(
        {"userId": current_user.id},
        {"_id": 0, "id": 1, "rfqNumber": 1, "title": 1, "status": 1, "createdAt": 1}
    ).sort("createdAt", -1).limit(limit).to_list(length=limit)
    
    # Combine and sort by date
    activities = []
    
    for tender in recent_tenders:
        activities.append({
            "type": "tender",
            "id": tender["id"],
            "title": tender["title"],
            "status": tender["status"],
            "timestamp": tender.get("updatedAt", tender.get("createdAt"))
        })
    
    for rfq in recent_rfqs:
        activities.append({
            "type": "rfq",
            "id": rfq["id"],
            "title": rfq.get("title", rfq["rfqNumber"]),
            "status": rfq["status"],
            "timestamp": rfq["createdAt"]
        })
    
    # Sort by timestamp
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return {
        "activities": activities[:limit]
    }
