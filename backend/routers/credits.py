from fastapi import APIRouter, HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import sys
sys.path.append('/app/backend')
from models_ai import CreditBalance, CreditTransaction
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/balance")
async def get_balance(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user's credit balance"""
    balance = await db.credit_balances.find_one({"userId": current_user.id}, {"_id": 0})
    
    if not balance:
        # Initialize balance
        balance = {
            "userId": current_user.id,
            "balance": 0,
            "total_purchased": 0,
            "total_used": 0,
            "lastUpdated": datetime.now(timezone.utc).isoformat()
        }
        await db.credit_balances.insert_one(balance)
    
    return balance

@router.get("/transactions")
async def get_transactions(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user's credit transaction history"""
    transactions = await db.credit_transactions.find(
        {"userId": current_user.id},
        {"_id": 0}
    ).sort("createdAt", -1).limit(100).to_list(length=100)
    
    return {"transactions": transactions}
