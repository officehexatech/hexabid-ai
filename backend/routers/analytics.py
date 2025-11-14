from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
import sys
sys.path.append('/app/backend')
from models_extended import TenderAnalytics
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/tender-stats")
async def get_tender_statistics(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    user_id = current_user.id
    
    # Get tender statistics
    total = await db.tenders.count_documents({"userId": user_id})
    active = await db.tenders.count_documents({"userId": user_id, "status": {"$in": ["new", "in_progress"]}})
    submitted = await db.tenders.count_documents({"userId": user_id, "status": "submitted"})
    won = await db.tenders.count_documents({"userId": user_id, "status": "won"})
    lost = await db.tenders.count_documents({"userId": user_id, "status": "lost"})
    
    # Calculate win rate
    completed = won + lost
    win_rate = (won / completed * 100) if completed > 0 else 0.0
    
    # Calculate total value
    pipeline = [
        {"$match": {"userId": user_id, "tenderValue": {"$exists": True}}},
        {"$group": {"_id": None, "total": {"$sum": "$tenderValue"}, "count": {"$sum": 1}}}
    ]
    value_result = await db.tenders.aggregate(pipeline).to_list(length=1)
    
    total_value = value_result[0]["total"] if value_result else 0.0
    avg_value = value_result[0]["total"] / value_result[0]["count"] if value_result and value_result[0]["count"] > 0 else 0.0
    
    return TenderAnalytics(
        totalTenders=total,
        activeTenders=active,
        submittedTenders=submitted,
        wonTenders=won,
        lostTenders=lost,
        winRate=round(win_rate, 2),
        totalValue=total_value,
        avgTenderValue=round(avg_value, 2)
    )

@router.get("/dashboard-stats")
async def get_dashboard_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    user_id = current_user.id
    
    # Aggregate all stats
    vendors_count = await db.vendors.count_documents({"userId": user_id, "isActive": True})
    rfqs_count = await db.rfqs.count_documents({"userId": user_id})
    tenders_count = await db.tenders.count_documents({"userId": user_id})
    products_count = await db.products.count_documents({"userId": user_id, "isActive": True})
    
    # Get team members count
    profile = await db.companies.find_one({"userId": user_id})
    team_count = 0
    if profile:
        team_count = await db.team_members.count_documents({"companyId": profile["id"]})
    
    # Get active tenders
    active_tenders = await db.tenders.count_documents({"userId": user_id, "status": {"$in": ["new", "in_progress"]}})
    
    return {
        "vendors": vendors_count,
        "rfqs": rfqs_count,
        "tenders": tenders_count,
        "activeTenders": active_tenders,
        "products": products_count,
        "teamMembers": team_count
    }