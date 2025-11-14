from fastapi import APIRouter, HTTPException, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from typing import Optional
import sys
sys.path.append('/app/backend')
from models_extended import Tender, TenderCreate, TenderStatus
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/")
async def get_tenders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    skip = (page - 1) * limit
    query = {"userId": current_user.id}
    
    if status:
        query["status"] = status
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"tenderNumber": {"$regex": search, "$options": "i"}},
            {"organization": {"$regex": search, "$options": "i"}}
        ]
    
    total = await db.tenders.count_documents(query)
    tenders_cursor = db.tenders.find(query, {"_id": 0}).skip(skip).limit(limit).sort("createdAt", -1)
    tenders = await tenders_cursor.to_list(length=limit)
    
    for tender in tenders:
        for date_field in ['publishDate', 'submissionDeadline', 'createdAt', 'updatedAt']:
            if tender.get(date_field) and isinstance(tender[date_field], str):
                tender[date_field] = datetime.fromisoformat(tender[date_field])
    
    return {
        "data": tenders,
        "pagination": {"page": page, "limit": limit, "total": total, "totalPages": (total + limit - 1) // limit}
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_tender(
    tender_data: TenderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    tender = Tender(**tender_data.model_dump(), userId=current_user.id)
    tender_dict = tender.model_dump()
    
    for date_field in ['publishDate', 'submissionDeadline', 'createdAt', 'updatedAt']:
        if tender_dict.get(date_field):
            tender_dict[date_field] = tender_dict[date_field].isoformat()
    
    await db.tenders.insert_one(tender_dict)
    return tender

@router.get("/{tender_id}")
async def get_tender(
    tender_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    tender_doc = await db.tenders.find_one({"id": tender_id, "userId": current_user.id}, {"_id": 0})
    if not tender_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tender not found")
    
    for date_field in ['publishDate', 'submissionDeadline', 'createdAt', 'updatedAt']:
        if tender_doc.get(date_field) and isinstance(tender_doc[date_field], str):
            tender_doc[date_field] = datetime.fromisoformat(tender_doc[date_field])
    
    return Tender(**tender_doc)

@router.patch("/{tender_id}")
async def update_tender(
    tender_id: str,
    updates: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    existing = await db.tenders.find_one({"id": tender_id, "userId": current_user.id})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tender not found")
    
    updates["updatedAt"] = datetime.now(timezone.utc).isoformat()
    await db.tenders.update_one({"id": tender_id}, {"$set": updates})
    
    updated = await db.tenders.find_one({"id": tender_id}, {"_id": 0})
    for date_field in ['publishDate', 'submissionDeadline', 'createdAt', 'updatedAt']:
        if updated.get(date_field) and isinstance(updated[date_field], str):
            updated[date_field] = datetime.fromisoformat(updated[date_field])
    
    return Tender(**updated)

@router.delete("/{tender_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tender(
    tender_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    result = await db.tenders.delete_one({"id": tender_id, "userId": current_user.id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tender not found")
    return None