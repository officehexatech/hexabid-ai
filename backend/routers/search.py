from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Dict, Any, Optional
from models_gem import SearchQuery
from routers.auth import get_current_user
import logging
from motor.motor_asyncio import AsyncIOMotorClient
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/search", tags=["Search"])

# MongoDB connection
client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
db = client[os.getenv('DB_NAME', 'test_database')]

@router.get("/global")
async def global_search(
    q: str = Query(..., description="Search query"),
    collection: Optional[str] = Query(None, description="Specific collection to search"),
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Global search across all collections
    """
    try:
        results = {}
        
        collections_to_search = [
            "tenders", "products", "vendors", "boq", "bid_submissions"
        ] if not collection else [collection]
        
        for coll_name in collections_to_search:
            # Create text search query
            search_results = await search_collection(coll_name, q, page, limit)
            if search_results:
                results[coll_name] = search_results
        
        total_results = sum(r['total'] for r in results.values())
        
        return {
            "success": True,
            "query": q,
            "total_results": total_results,
            "results": results
        }
    except Exception as e:
        logger.error(f"Error in global search: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def search_collection(collection_name: str, query: str, page: int, limit: int) -> Dict[str, Any]:
    """
    Search in a specific collection
    """
    try:
        collection = db[collection_name]
        
        # Build regex query for flexible searching
        search_query = {
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"organization": {"$regex": query, "$options": "i"}},
                {"tender_number": {"$regex": query, "$options": "i"}},
                {"company_name": {"$regex": query, "$options": "i"}},
                {"category": {"$regex": query, "$options": "i"}}
            ]
        }
        
        skip = (page - 1) * limit
        
        cursor = collection.find(search_query).skip(skip).limit(limit)
        items = await cursor.to_list(length=limit)
        
        total = await collection.count_documents(search_query)
        
        return {
            "total": total,
            "page": page,
            "limit": limit,
            "items": items
        }
    except Exception as e:
        logger.error(f"Error searching collection {collection_name}: {e}")
        return None

@router.get("/tenders")
async def search_tenders(
    q: str = Query(..., description="Search query"),
    category: Optional[str] = None,
    status: Optional[str] = None,
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
    page: int = 1,
    limit: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """
    Advanced tender search with filters
    """
    try:
        query_filter = {
            "$or": [
                {"title": {"$regex": q, "$options": "i"}},
                {"tender_number": {"$regex": q, "$options": "i"}},
                {"organization": {"$regex": q, "$options": "i"}}
            ]
        }
        
        if category:
            query_filter["category"] = category
        if status:
            query_filter["status"] = status
        if min_value:
            query_filter["tender_value"] = {"$gte": min_value}
        if max_value:
            if "tender_value" in query_filter:
                query_filter["tender_value"]["$lte"] = max_value
            else:
                query_filter["tender_value"] = {"$lte": max_value}
        
        skip = (page - 1) * limit
        
        cursor = db.tenders.find(query_filter).skip(skip).limit(limit)
        tenders = await cursor.to_list(length=limit)
        
        total = await db.tenders.count_documents(query_filter)
        
        return {
            "success": True,
            "total": total,
            "page": page,
            "limit": limit,
            "tenders": tenders
        }
    except Exception as e:
        logger.error(f"Error searching tenders: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=2, description="Partial query for suggestions"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get search suggestions based on partial query
    """
    try:
        suggestions = []
        
        # Get suggestions from different collections
        collections = [
            ("tenders", "title"),
            ("products", "name"),
            ("vendors", "company_name")
        ]
        
        for coll_name, field_name in collections:
            query = {field_name: {"$regex": f"^{q}", "$options": "i"}}
            cursor = db[coll_name].find(query, {field_name: 1}).limit(5)
            
            async for doc in cursor:
                if field_name in doc:
                    suggestions.append({
                        "text": doc[field_name],
                        "type": coll_name[:-1]  # Remove 's' from collection name
                    })
        
        return {
            "success": True,
            "suggestions": suggestions[:10]  # Limit to 10 suggestions
        }
    except Exception as e:
        logger.error(f"Error getting suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))
