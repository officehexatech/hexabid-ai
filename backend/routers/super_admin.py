from fastapi import APIRouter, HTTPException, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from typing import Optional
import sys
sys.path.append('/app/backend')
from models_tenant import Tenant, TenantStatus, TenantPlan, AdminAction, PLAN_PRICING
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

# Super Admin User IDs (hardcoded for now - should be in env/config)
SUPER_ADMIN_IDS = ["super_admin_user_id"]  # Update with actual super admin user IDs

def is_super_admin(user: User) -> bool:
    """Check if user is super admin"""
    return user.id in SUPER_ADMIN_IDS or user.email.endswith("@hexabid.com")  # Or your domain

async def require_super_admin(current_user: User = Depends(get_current_user)):
    """Dependency to require super admin access"""
    if not is_super_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user

@router.get("/tenants")
async def list_all_tenants(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    status_filter: Optional[str] = None,
    plan_filter: Optional[str] = None,
    admin: User = Depends(require_super_admin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """List all tenants (Super Admin)"""
    
    skip = (page - 1) * limit
    query = {}
    
    if status_filter:
        query["status"] = status_filter
    if plan_filter:
        query["plan"] = plan_filter
    
    total = await db.tenants.count_documents(query)
    tenants = await db.tenants.find(query, {"_id": 0}).skip(skip).limit(limit).sort("created_at", -1).to_list(length=limit)
    
    # Add member count and usage for each tenant
    for tenant in tenants:
        member_count = await db.tenant_members.count_documents({"tenant_id": tenant["id"], "is_active": True})
        tenant["member_count"] = member_count
        
        current_month = datetime.now(timezone.utc).strftime('%Y-%m')
        usage = await db.tenant_usage.find_one(
            {"tenant_id": tenant["id"], "month": current_month},
            {"_id": 0}
        )
        tenant["current_usage"] = usage
    
    return {
        "tenants": tenants,
        "pagination": {"page": page, "limit": limit, "total": total, "totalPages": (total + limit - 1) // limit}
    }

@router.get("/tenants/{tenant_id}")
async def get_tenant_details(
    tenant_id: str,
    admin: User = Depends(require_super_admin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get detailed tenant information (Super Admin)"""
    
    tenant = await db.tenants.find_one({"id": tenant_id}, {"_id": 0})
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Get all members
    members = await db.tenant_members.find({"tenant_id": tenant_id}, {"_id": 0}).to_list(length=100)
    
    # Get usage history (last 6 months)
    usage_history = await db.tenant_usage.find(
        {"tenant_id": tenant_id},
        {"_id": 0}
    ).sort("month", -1).limit(6).to_list(length=6)
    
    # Get billing history
    billing_history = await db.tenant_billing.find(
        {"tenant_id": tenant_id},
        {"_id": 0}
    ).sort("billing_date", -1).limit(12).to_list(length=12)
    
    return {
        "tenant": tenant,
        "members": members,
        "usage_history": usage_history,
        "billing_history": billing_history
    }

@router.patch("/tenants/{tenant_id}/status")
async def update_tenant_status(
    tenant_id: str,
    status_data: dict,
    admin: User = Depends(require_super_admin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update tenant status (Super Admin)"""
    
    new_status = status_data.get("status")
    if new_status not in [s.value for s in TenantStatus]:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    result = await db.tenants.update_one(
        {"id": tenant_id},
        {"$set": {"status": new_status}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Log admin action
    action = AdminAction(
        admin_user_id=admin.id,
        action_type="update_tenant_status",
        target_tenant_id=tenant_id,
        details={"new_status": new_status, "reason": status_data.get("reason", "")}
    )
    action_dict = action.model_dump()
    action_dict['performed_at'] = action_dict['performed_at'].isoformat()
    await db.admin_actions.insert_one(action_dict)
    
    return {"message": f"Tenant status updated to {new_status}"}

@router.patch("/tenants/{tenant_id}/plan")
async def update_tenant_plan(
    tenant_id: str,
    plan_data: dict,
    admin: User = Depends(require_super_admin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Update tenant plan (Super Admin)"""
    
    new_plan = plan_data.get("plan")
    if new_plan not in [p.value for p in TenantPlan]:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    result = await db.tenants.update_one(
        {"id": tenant_id},
        {"$set": {"plan": new_plan}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Log admin action
    action = AdminAction(
        admin_user_id=admin.id,
        action_type="update_tenant_plan",
        target_tenant_id=tenant_id,
        details={"new_plan": new_plan, "reason": plan_data.get("reason", "")}
    )
    action_dict = action.model_dump()
    action_dict['performed_at'] = action_dict['performed_at'].isoformat()
    await db.admin_actions.insert_one(action_dict)
    
    return {"message": f"Tenant plan updated to {new_plan}"}

@router.get("/dashboard")
async def get_admin_dashboard(
    admin: User = Depends(require_super_admin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get super admin dashboard metrics"""
    
    # Count tenants by status
    total_tenants = await db.tenants.count_documents({})
    active_tenants = await db.tenants.count_documents({"status": "active"})
    trial_tenants = await db.tenants.count_documents({"status": "trial"})
    suspended_tenants = await db.tenants.count_documents({"status": "suspended"})
    
    # Count by plan
    free_plan = await db.tenants.count_documents({"plan": "free"})
    startup_plan = await db.tenants.count_documents({"plan": "startup"})
    professional_plan = await db.tenants.count_documents({"plan": "professional"})
    enterprise_plan = await db.tenants.count_documents({"plan": "enterprise"})
    
    # Calculate MRR (Monthly Recurring Revenue)
    plan_counts = {
        "free": free_plan,
        "startup": startup_plan,
        "professional": professional_plan,
        "enterprise": enterprise_plan
    }
    
    mrr = sum(count * PLAN_PRICING[plan] for plan, count in plan_counts.items())
    
    # Get recent signups (last 30 days)
    thirty_days_ago = (datetime.now(timezone.utc) - __import__('datetime').timedelta(days=30)).isoformat()
    recent_signups = await db.tenants.count_documents({"created_at": {"$gte": thirty_days_ago}})
    
    # Get total users across all tenants
    total_users = await db.tenant_members.count_documents({"is_active": True})
    
    # Get current month usage aggregates
    current_month = datetime.now(timezone.utc).strftime('%Y-%m')
    usage_pipeline = [
        {"$match": {"month": current_month}},
        {"$group": {
            "_id": None,
            "total_ai_credits": {"$sum": "$ai_credits_used"},
            "total_tokens": {"$sum": "$ai_tokens_consumed"},
            "total_cost": {"$sum": "$cost_incurred"}
        }}
    ]
    
    usage_aggregate = await db.tenant_usage.aggregate(usage_pipeline).to_list(length=1)
    usage_summary = usage_aggregate[0] if usage_aggregate else {
        "total_ai_credits": 0,
        "total_tokens": 0,
        "total_cost": 0
    }
    
    return {
        "tenants": {
            "total": total_tenants,
            "active": active_tenants,
            "trial": trial_tenants,
            "suspended": suspended_tenants
        },
        "plans": {
            "free": free_plan,
            "startup": startup_plan,
            "professional": professional_plan,
            "enterprise": enterprise_plan
        },
        "revenue": {
            "mrr": mrr,
            "currency": "INR"
        },
        "growth": {
            "recent_signups_30d": recent_signups
        },
        "users": {
            "total": total_users
        },
        "usage": {
            "current_month": current_month,
            "total_ai_credits_used": usage_summary.get("total_ai_credits", 0),
            "total_tokens_consumed": usage_summary.get("total_tokens", 0),
            "total_cost_incurred": usage_summary.get("total_cost", 0)
        }
    }

@router.get("/actions")
async def get_admin_actions(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    admin: User = Depends(require_super_admin),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get admin action log"""
    
    skip = (page - 1) * limit
    
    total = await db.admin_actions.count_documents({})
    actions = await db.admin_actions.find({}, {"_id": 0}).skip(skip).limit(limit).sort("performed_at", -1).to_list(length=limit)
    
    return {
        "actions": actions,
        "pagination": {"page": page, "limit": limit, "total": total}
    }
