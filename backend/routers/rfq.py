from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from models import RFQ, RFQCreate, RFQUpdate, VendorQuote, VendorQuoteCreate, User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/", response_model=dict)
async def get_rfqs(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    skip = (page - 1) * limit
    query = {"userId": current_user.id}
    
    if status_filter:
        query["status"] = status_filter
    
    # Get total count
    total = await db.rfqs.count_documents(query)
    
    # Get RFQs
    rfqs_cursor = db.rfqs.find(query, {"_id": 0}).skip(skip).limit(limit).sort("createdAt", -1)
    rfqs = await rfqs_cursor.to_list(length=limit)
    
    # Parse dates
    for rfq in rfqs:
        if isinstance(rfq.get('createdAt'), str):
            rfq['createdAt'] = datetime.fromisoformat(rfq['createdAt'])
        if isinstance(rfq.get('updatedAt'), str):
            rfq['updatedAt'] = datetime.fromisoformat(rfq['updatedAt'])
        if rfq.get('sentAt') and isinstance(rfq.get('sentAt'), str):
            rfq['sentAt'] = datetime.fromisoformat(rfq['sentAt'])
        if isinstance(rfq.get('dueDate'), str):
            rfq['dueDate'] = datetime.fromisoformat(rfq['dueDate'])
    
    return {
        "data": rfqs,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "totalPages": (total + limit - 1) // limit
        }
    }

@router.get("/{rfq_id}", response_model=RFQ)
async def get_rfq(
    rfq_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    rfq_doc = await db.rfqs.find_one({"id": rfq_id, "userId": current_user.id}, {"_id": 0})
    if not rfq_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    
    # Parse dates
    if isinstance(rfq_doc.get('createdAt'), str):
        rfq_doc['createdAt'] = datetime.fromisoformat(rfq_doc['createdAt'])
    if isinstance(rfq_doc.get('updatedAt'), str):
        rfq_doc['updatedAt'] = datetime.fromisoformat(rfq_doc['updatedAt'])
    if rfq_doc.get('sentAt') and isinstance(rfq_doc.get('sentAt'), str):
        rfq_doc['sentAt'] = datetime.fromisoformat(rfq_doc['sentAt'])
    if isinstance(rfq_doc.get('dueDate'), str):
        rfq_doc['dueDate'] = datetime.fromisoformat(rfq_doc['dueDate'])
    
    return RFQ(**rfq_doc)

@router.post("/", response_model=RFQ, status_code=status.HTTP_201_CREATED)
async def create_rfq(
    rfq_data: RFQCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Verify vendors exist
    for vendor_id in rfq_data.vendorIds:
        vendor = await db.vendors.find_one({"id": vendor_id, "userId": current_user.id})
        if not vendor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vendor {vendor_id} not found")
    
    rfq = RFQ(**rfq_data.model_dump(), userId=current_user.id)
    rfq_dict = rfq.model_dump()
    rfq_dict["createdAt"] = rfq_dict["createdAt"].isoformat()
    rfq_dict["updatedAt"] = rfq_dict["updatedAt"].isoformat()
    rfq_dict["dueDate"] = rfq_dict["dueDate"].isoformat()
    
    await db.rfqs.insert_one(rfq_dict)
    
    # Update vendor stats
    for vendor_id in rfq_data.vendorIds:
        await db.vendors.update_one(
            {"id": vendor_id},
            {"$inc": {"totalRfqsSent": 1}}
        )
    
    return rfq

@router.patch("/{rfq_id}", response_model=RFQ)
async def update_rfq(
    rfq_id: str,
    rfq_data: RFQUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if RFQ exists
    existing_rfq = await db.rfqs.find_one({"id": rfq_id, "userId": current_user.id})
    if not existing_rfq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    
    # Update RFQ
    update_data = {k: v for k, v in rfq_data.model_dump(exclude_unset=True).items()}
    if "dueDate" in update_data and update_data["dueDate"]:
        update_data["dueDate"] = update_data["dueDate"].isoformat()
    update_data["updatedAt"] = datetime.now(timezone.utc).isoformat()
    
    # If status changed to 'sent', set sentAt
    if update_data.get("status") == "sent" and not existing_rfq.get("sentAt"):
        update_data["sentAt"] = datetime.now(timezone.utc).isoformat()
    
    await db.rfqs.update_one({"id": rfq_id}, {"$set": update_data})
    
    # Get updated RFQ
    updated_rfq = await db.rfqs.find_one({"id": rfq_id}, {"_id": 0})
    
    # Parse dates
    if isinstance(updated_rfq.get('createdAt'), str):
        updated_rfq['createdAt'] = datetime.fromisoformat(updated_rfq['createdAt'])
    if isinstance(updated_rfq.get('updatedAt'), str):
        updated_rfq['updatedAt'] = datetime.fromisoformat(updated_rfq['updatedAt'])
    if updated_rfq.get('sentAt') and isinstance(updated_rfq.get('sentAt'), str):
        updated_rfq['sentAt'] = datetime.fromisoformat(updated_rfq['sentAt'])
    if isinstance(updated_rfq.get('dueDate'), str):
        updated_rfq['dueDate'] = datetime.fromisoformat(updated_rfq['dueDate'])
    
    return RFQ(**updated_rfq)

@router.delete("/{rfq_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rfq(
    rfq_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    result = await db.rfqs.delete_one({"id": rfq_id, "userId": current_user.id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    
    return None

# Vendor Quotes
@router.get("/{rfq_id}/quotes", response_model=List[VendorQuote])
async def get_rfq_quotes(
    rfq_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Verify RFQ exists
    rfq = await db.rfqs.find_one({"id": rfq_id, "userId": current_user.id})
    if not rfq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    
    # Get quotes
    quotes_cursor = db.vendor_quotes.find({"rfqId": rfq_id, "userId": current_user.id}, {"_id": 0}).sort("createdAt", -1)
    quotes = await quotes_cursor.to_list(length=100)
    
    # Parse dates
    for quote in quotes:
        if isinstance(quote.get('createdAt'), str):
            quote['createdAt'] = datetime.fromisoformat(quote['createdAt'])
        if isinstance(quote.get('updatedAt'), str):
            quote['updatedAt'] = datetime.fromisoformat(quote['updatedAt'])
        if quote.get('validUntil') and isinstance(quote.get('validUntil'), str):
            quote['validUntil'] = datetime.fromisoformat(quote['validUntil'])
    
    return [VendorQuote(**quote) for quote in quotes]

@router.post("/{rfq_id}/quotes", response_model=VendorQuote, status_code=status.HTTP_201_CREATED)
async def create_vendor_quote(
    rfq_id: str,
    quote_data: VendorQuoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Verify RFQ exists
    rfq = await db.rfqs.find_one({"id": rfq_id, "userId": current_user.id})
    if not rfq:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="RFQ not found")
    
    # Verify vendor exists
    vendor = await db.vendors.find_one({"id": quote_data.vendorId, "userId": current_user.id})
    if not vendor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendor not found")
    
    quote = VendorQuote(**quote_data.model_dump(), userId=current_user.id)
    quote_dict = quote.model_dump()
    quote_dict["createdAt"] = quote_dict["createdAt"].isoformat()
    quote_dict["updatedAt"] = quote_dict["updatedAt"].isoformat()
    if quote_dict.get("validUntil"):
        quote_dict["validUntil"] = quote_dict["validUntil"].isoformat()
    
    await db.vendor_quotes.insert_one(quote_dict)
    
    # Update vendor stats
    await db.vendors.update_one(
        {"id": quote_data.vendorId},
        {"$inc": {"totalQuotesReceived": 1}}
    )
    
    return quote