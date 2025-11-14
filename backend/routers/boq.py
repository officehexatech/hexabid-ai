from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import sys
sys.path.append('/app/backend')
from models_extended import BOQ, BOQCreate
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/tender/{tender_id}")
async def get_boqs_by_tender(
    tender_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    boqs_cursor = db.boqs.find({"tenderId": tender_id, "userId": current_user.id}, {"_id": 0}).sort("version", -1)
    boqs = await boqs_cursor.to_list(length=100)
    
    for boq in boqs:
        for date_field in ['approvedAt', 'createdAt', 'updatedAt']:
            if boq.get(date_field) and isinstance(boq[date_field], str):
                boq[date_field] = datetime.fromisoformat(boq[date_field])
    
    return {"data": boqs}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_boq(
    boq_data: BOQCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    boq = BOQ(**boq_data.model_dump(), userId=current_user.id)
    boq_dict = boq.model_dump()
    
    for date_field in ['approvedAt', 'createdAt', 'updatedAt']:
        if boq_dict.get(date_field):
            boq_dict[date_field] = boq_dict[date_field].isoformat()
    
    await db.boqs.insert_one(boq_dict)
    return boq

@router.get("/{boq_id}")
async def get_boq(
    boq_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    boq_doc = await db.boqs.find_one({"id": boq_id, "userId": current_user.id}, {"_id": 0})
    if not boq_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BOQ not found")
    
    for date_field in ['approvedAt', 'createdAt', 'updatedAt']:
        if boq_doc.get(date_field) and isinstance(boq_doc[date_field], str):
            boq_doc[date_field] = datetime.fromisoformat(boq_doc[date_field])
    
    return BOQ(**boq_doc)

@router.patch("/{boq_id}")
async def update_boq(
    boq_id: str,
    updates: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    existing = await db.boqs.find_one({"id": boq_id, "userId": current_user.id})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="BOQ not found")
    
    updates["updatedAt"] = datetime.now(timezone.utc).isoformat()
    await db.boqs.update_one({"id": boq_id}, {"$set": updates})
    
    updated = await db.boqs.find_one({"id": boq_id}, {"_id": 0})
    for date_field in ['approvedAt', 'createdAt', 'updatedAt']:
        if updated.get(date_field) and isinstance(updated[date_field], str):
            updated[date_field] = datetime.fromisoformat(updated[date_field])
    
    return BOQ(**updated)