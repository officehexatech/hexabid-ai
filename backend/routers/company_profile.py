from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import uuid
from models import CompanyProfile, CompanyProfileCreate, CompanyProfileUpdate, TeamMember, TeamMemberInvite, User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/profile", response_model=CompanyProfile)
async def get_company_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    profile_doc = await db.companies.find_one({"userId": current_user.id}, {"_id": 0})
    if not profile_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found")
    
    # Parse dates
    if isinstance(profile_doc.get('createdAt'), str):
        profile_doc['createdAt'] = datetime.fromisoformat(profile_doc['createdAt'])
    if isinstance(profile_doc.get('updatedAt'), str):
        profile_doc['updatedAt'] = datetime.fromisoformat(profile_doc['updatedAt'])
    
    return CompanyProfile(**profile_doc)

@router.post("/profile", response_model=CompanyProfile, status_code=status.HTTP_201_CREATED)
async def create_company_profile(
    profile_data: CompanyProfileCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if profile already exists
    existing_profile = await db.companies.find_one({"userId": current_user.id})
    if existing_profile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company profile already exists")
    
    profile = CompanyProfile(**profile_data.model_dump(), userId=current_user.id)
    profile_dict = profile.model_dump()
    profile_dict["createdAt"] = profile_dict["createdAt"].isoformat()
    profile_dict["updatedAt"] = profile_dict["updatedAt"].isoformat()
    
    await db.companies.insert_one(profile_dict)
    
    # Mark user as having completed profile
    await db.users.update_one(
        {"id": current_user.id},
        {"$set": {"hasCompletedProfile": True}}
    )
    
    return profile

@router.patch("/profile", response_model=CompanyProfile)
async def update_company_profile(
    profile_data: CompanyProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if profile exists
    existing_profile = await db.companies.find_one({"userId": current_user.id})
    if not existing_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found")
    
    # Update profile
    update_data = {k: v for k, v in profile_data.model_dump(exclude_unset=True).items()}
    update_data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    
    await db.companies.update_one({"userId": current_user.id}, {"$set": update_data})
    
    # Get updated profile
    updated_profile = await db.companies.find_one({"userId": current_user.id}, {"_id": 0})
    
    # Parse dates
    if isinstance(updated_profile.get('createdAt'), str):
        updated_profile['createdAt'] = datetime.fromisoformat(updated_profile['createdAt'])
    if isinstance(updated_profile.get('updatedAt'), str):
        updated_profile['updatedAt'] = datetime.fromisoformat(updated_profile['updatedAt'])
    
    return CompanyProfile(**updated_profile)

# Team Members
@router.get("/team", response_model=List[TeamMember])
async def get_team_members(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Get company profile
    profile = await db.companies.find_one({"userId": current_user.id})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found")
    
    # Get team members
    members_cursor = db.team_members.find({"companyId": profile["id"]}, {"_id": 0}).sort("invitedAt", -1)
    members = await members_cursor.to_list(length=100)
    
    # Parse dates
    for member in members:
        if isinstance(member.get('invitedAt'), str):
            member['invitedAt'] = datetime.fromisoformat(member['invitedAt'])
        if member.get('joinedAt') and isinstance(member.get('joinedAt'), str):
            member['joinedAt'] = datetime.fromisoformat(member['joinedAt'])
    
    return [TeamMember(**member) for member in members]

@router.post("/team/invite", response_model=TeamMember, status_code=status.HTTP_201_CREATED)
async def invite_team_member(
    invite_data: TeamMemberInvite,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Get company profile
    profile = await db.companies.find_one({"userId": current_user.id})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found. Please complete your profile first.")
    
    # Check if member already invited
    existing_member = await db.team_members.find_one({"companyId": profile["id"], "email": invite_data.email})
    if existing_member:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already invited")
    
    # Create team member
    member = TeamMember(
        companyId=profile["id"],
        email=invite_data.email,
        name=invite_data.name,
        role=invite_data.role,
        inviteToken=str(uuid.uuid4())
    )
    member_dict = member.model_dump()
    member_dict["invitedAt"] = member_dict["invitedAt"].isoformat()
    
    await db.team_members.insert_one(member_dict)
    
    # TODO: Send invitation email in Phase 5
    
    return member

@router.delete("/team/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_team_member(
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Get company profile
    profile = await db.companies.find_one({"userId": current_user.id})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found")
    
    result = await db.team_members.delete_one({"id": member_id, "companyId": profile["id"]})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    
    return None

@router.patch("/team/{member_id}/role", response_model=TeamMember)
async def update_team_member_role(
    member_id: str,
    role: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Get company profile
    profile = await db.companies.find_one({"userId": current_user.id})
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company profile not found")
    
    # Validate role
    valid_roles = ["admin", "manager", "viewer"]
    if role not in valid_roles:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}")
    
    # Update member role
    result = await db.team_members.update_one(
        {"id": member_id, "companyId": profile["id"]},
        {"$set": {"role": role}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team member not found")
    
    # Get updated member
    member_doc = await db.team_members.find_one({"id": member_id}, {"_id": 0})
    
    # Parse dates
    if isinstance(member_doc.get('invitedAt'), str):
        member_doc['invitedAt'] = datetime.fromisoformat(member_doc['invitedAt'])
    if member_doc.get('joinedAt') and isinstance(member_doc.get('joinedAt'), str):
        member_doc['joinedAt'] = datetime.fromisoformat(member_doc['joinedAt'])
    
    return TeamMember(**member_doc)