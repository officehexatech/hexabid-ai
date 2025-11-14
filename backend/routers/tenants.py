from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone, timedelta
import sys
sys.path.append('/app/backend')
from models_tenant import Tenant, TenantMember, TenantUsage, TenantRole, TenantStatus, PLAN_LIMITS
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tenant(
    tenant_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create new tenant"""
    
    # Check if user already has a tenant
    existing_membership = await db.tenant_members.find_one({"user_id": current_user.id, "is_active": True})
    if existing_membership:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already belongs to a tenant"
        )
    
    # Create tenant
    tenant = Tenant(
        tenant_name=tenant_data['tenant_name'],
        owner_user_id=current_user.id,
        status=TenantStatus.trial,
        trial_ends_at=datetime.now(timezone.utc) + timedelta(days=30)
    )
    
    tenant_dict = tenant.model_dump()
    for date_field in ['created_at', 'trial_ends_at', 'subscription_ends_at']:
        if tenant_dict.get(date_field):
            tenant_dict[date_field] = tenant_dict[date_field].isoformat()
    
    await db.tenants.insert_one(tenant_dict)
    
    # Add owner as member
    member = TenantMember(
        tenant_id=tenant.id,
        user_id=current_user.id,
        role=TenantRole.owner
    )
    
    member_dict = member.model_dump()
    member_dict['joined_at'] = member_dict['joined_at'].isoformat()
    await db.tenant_members.insert_one(member_dict)
    
    # Initialize usage tracking
    current_month = datetime.now(timezone.utc).strftime('%Y-%m')
    usage = TenantUsage(
        tenant_id=tenant.id,
        month=current_month
    )
    usage_dict = usage.model_dump()
    for date_field in ['created_at', 'updated_at']:
        usage_dict[date_field] = usage_dict[date_field].isoformat()
    await db.tenant_usage.insert_one(usage_dict)
    
    return {"tenant": tenant, "message": "Tenant created successfully. 30-day trial started."}

@router.get("/current")
async def get_current_tenant(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get current user's tenant"""
    
    membership = await db.tenant_members.find_one({"user_id": current_user.id, "is_active": True})
    if not membership:
        raise HTTPException(status_code=404, detail="No tenant found for user")
    
    tenant = await db.tenants.find_one({"id": membership['tenant_id']}, {"_id": 0})
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {"tenant": tenant, "role": membership['role']}

@router.get("/usage")
async def get_tenant_usage(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get tenant usage for current month"""
    
    membership = await db.tenant_members.find_one({"user_id": current_user.id, "is_active": True})
    if not membership:
        raise HTTPException(status_code=404, detail="No tenant found")
    
    tenant = await db.tenants.find_one({"id": membership['tenant_id']}, {"_id": 0})
    current_month = datetime.now(timezone.utc).strftime('%Y-%m')
    
    usage = await db.tenant_usage.find_one(
        {"tenant_id": membership['tenant_id'], "month": current_month},
        {"_id": 0}
    )
    
    if not usage:
        # Initialize usage
        usage = {
            "tenant_id": membership['tenant_id'],
            "month": current_month,
            "total_users": 0,
            "total_tenders": 0,
            "ai_credits_used": 0,
            "ai_tokens_consumed": 0,
            "storage_used_mb": 0,
            "api_calls": 0,
            "cost_incurred": 0.0
        }
    
    limits = PLAN_LIMITS[tenant['plan']]
    
    return {
        "usage": usage,
        "limits": limits,
        "plan": tenant['plan'],
        "status": tenant['status']
    }

@router.get("/members")
async def get_tenant_members(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get all tenant members"""
    
    membership = await db.tenant_members.find_one({"user_id": current_user.id, "is_active": True})
    if not membership:
        raise HTTPException(status_code=404, detail="No tenant found")
    
    members = await db.tenant_members.find(
        {"tenant_id": membership['tenant_id'], "is_active": True},
        {"_id": 0}
    ).to_list(length=100)
    
    # Fetch user details
    for member in members:
        user = await db.users.find_one({"id": member['user_id']}, {"_id": 0, "password": 0})
        member['user_details'] = user
    
    return {"members": members}
