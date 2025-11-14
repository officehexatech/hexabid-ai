from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from models import Vendor, VendorCreate, VendorUpdate, User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/", response_model=dict)
async def get_vendors(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    skip = (page - 1) * limit
    query = {"userId": current_user.id, "isActive": True}
    
    if search:
        query["companyName"] = {"$regex": search, "$options": "i"}
    
    if category:
        query["categories"] = category
    
    # Get total count
    total = await db.vendors.count_documents(query)
    
    # Get vendors
    vendors_cursor = db.vendors.find(query, {"_id": 0}).skip(skip).limit(limit).sort("companyName", 1)
    vendors = await vendors_cursor.to_list(length=limit)
    
    # Parse dates
    for vendor in vendors:
        if isinstance(vendor.get('createdAt'), str):
            vendor['createdAt'] = datetime.fromisoformat(vendor['createdAt'])
        if isinstance(vendor.get('updatedAt'), str):
            vendor['updatedAt'] = datetime.fromisoformat(vendor['updatedAt'])
    
    return {
        "data": vendors,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": (total + limit - 1) // limit
        }
    }

@router.get("/{vendor_id}", response_model=Vendor)
async def get_vendor(
    vendor_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    vendor_doc = await db.vendors.find_one({"id": vendor_id, "userId": current_user.id}, {"_id": 0})
    if not vendor_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    
    # Parse dates
    if isinstance(vendor_doc.get('createdAt'), str):
        vendor_doc['createdAt'] = datetime.fromisoformat(vendor_doc['createdAt'])
    if isinstance(vendor_doc.get('updatedAt'), str):
        vendor_doc['updatedAt'] = datetime.fromisoformat(vendor_doc['updatedAt'])
    
    return Vendor(**vendor_doc)

@router.post("/", response_model=Vendor, status_code=status.HTTP_201_CREATED)
async def create_vendor(
    vendor_data: VendorCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    vendor = Vendor(**vendor_data.model_dump(), userId=current_user.id)
    vendor_dict = vendor.model_dump()
    vendor_dict["createdAt"] = vendor_dict["createdAt"].isoformat()
    vendor_dict["updatedAt"] = vendor_dict["updatedAt"].isoformat()
    
    await db.vendors.insert_one(vendor_dict)
    
    return vendor

@router.patch("/{vendor_id}", response_model=Vendor)
async def update_vendor(
    vendor_id: str,
    vendor_data: VendorUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if vendor exists
    existing_vendor = await db.vendors.find_one({"id": vendor_id, "userId": current_user.id})
    if not existing_vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    
    # Update vendor
    update_data = {k: v for k, v in vendor_data.model_dump(exclude_unset=True).items()}
    update_data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    
    await db.vendors.update_one({"id": vendor_id}, {"$set": update_data})
    
    # Get updated vendor
    updated_vendor = await db.vendors.find_one({"id": vendor_id}, {"_id": 0})
    
    # Parse dates
    if isinstance(updated_vendor.get('createdAt'), str):
        updated_vendor['createdAt'] = datetime.fromisoformat(updated_vendor['createdAt'])
    if isinstance(updated_vendor.get('updatedAt'), str):
        updated_vendor['updatedAt'] = datetime.fromisoformat(updated_vendor['updatedAt'])
    
    return Vendor(**updated_vendor)

@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vendor(
    vendor_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Soft delete - set isActive to False
    result = await db.vendors.update_one(
        {"id": vendor_id, "userId": current_user.id},
        {"$set": {"isActive": False, "updatedAt": datetime.now(timezone.utc).isoformat()}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    
    return None