from fastapi import APIRouter, HTTPException, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
from typing import Optional
import sys
sys.path.append('/app/backend')
from models_extended import Product, ProductCreate, ProductCategory
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/")
async def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(50, ge=1, le=200),
    category: Optional[str] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    skip = (page - 1) * limit
    query = {"userId": current_user.id, "isActive": True}
    
    if category:
        query["category"] = category
    if search:
        query["$or"] = [
            {"productName": {"$regex": search, "$options": "i"}},
            {"productCode": {"$regex": search, "$options": "i"}},
            {"brand": {"$regex": search, "$options": "i"}}
        ]
    
    total = await db.products.count_documents(query)
    products_cursor = db.products.find(query, {"_id": 0}).skip(skip).limit(limit).sort("productName", 1)
    products = await products_cursor.to_list(length=limit)
    
    for product in products:
        for date_field in ['createdAt', 'updatedAt']:
            if product.get(date_field) and isinstance(product[date_field], str):
                product[date_field] = datetime.fromisoformat(product[date_field])
    
    return {
        "data": products,
        "pagination": {"page": page, "limit": limit, "total": total, "totalPages": (total + limit - 1) // limit}
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Check if product code already exists
    existing = await db.products.find_one({"productCode": product_data.productCode, "userId": current_user.id})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product code already exists")
    
    product = Product(**product_data.model_dump(), userId=current_user.id)
    product_dict = product.model_dump()
    
    for date_field in ['createdAt', 'updatedAt']:
        if product_dict.get(date_field):
            product_dict[date_field] = product_dict[date_field].isoformat()
    
    await db.products.insert_one(product_dict)
    return product

@router.get("/{product_id}")
async def get_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    product_doc = await db.products.find_one({"id": product_id, "userId": current_user.id}, {"_id": 0})
    if not product_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    for date_field in ['createdAt', 'updatedAt']:
        if product_doc.get(date_field) and isinstance(product_doc[date_field], str):
            product_doc[date_field] = datetime.fromisoformat(product_doc[date_field])
    
    return Product(**product_doc)

@router.patch("/{product_id}")
async def update_product(
    product_id: str,
    updates: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    existing = await db.products.find_one({"id": product_id, "userId": current_user.id})
    if not existing:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # If updating unit price, add to price history
    if "unitPrice" in updates and updates["unitPrice"] != existing.get("unitPrice"):
        price_history = existing.get("priceHistory", [])
        price_history.append({
            "price": updates["unitPrice"],
            "changedAt": datetime.now(timezone.utc).isoformat()
        })
        updates["priceHistory"] = price_history
    
    updates["updatedAt"] = datetime.now(timezone.utc).isoformat()
    await db.products.update_one({"id": product_id}, {"$set": updates})
    
    updated = await db.products.find_one({"id": product_id}, {"_id": 0})
    for date_field in ['createdAt', 'updatedAt']:
        if updated.get(date_field) and isinstance(updated[date_field], str):
            updated[date_field] = datetime.fromisoformat(updated[date_field])
    
    return Product(**updated)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    # Soft delete
    result = await db.products.update_one(
        {"id": product_id, "userId": current_user.id},
        {"$set": {"isActive": False, "updatedAt": datetime.now(timezone.utc).isoformat()}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None
