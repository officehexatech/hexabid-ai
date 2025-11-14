from fastapi import APIRouter, HTTPException, Depends, Request, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import razorpay
import hmac
import hashlib
import os
import sys
sys.path.append('/app/backend')
from models_ai import PaymentOrderCreate, PaymentOrder, CREDIT_PRICING
from models import User
from routers.auth import get_current_user, get_db

router = APIRouter()

# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(os.getenv('RAZORPAY_KEY_ID', 'rzp_test_key'), os.getenv('RAZORPAY_KEY_SECRET', 'secret'))
)

@router.post("/create-order")
async def create_payment_order(
    order_data: PaymentOrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Create Razorpay payment order for credit purchase"""
    
    try:
        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": order_data.amount,  # Amount in paise
            "currency": order_data.currency,
            "payment_capture": 1,
            "notes": {
                "user_id": current_user.id,
                "credits": order_data.credits
            }
        })
        
        # Save order in database
        payment_order = PaymentOrder(
            userId=current_user.id,
            orderId=razorpay_order['id'],
            amount=order_data.amount,
            credits=order_data.credits,
            currency=order_data.currency,
            status="created"
        )
        
        order_dict = payment_order.model_dump()
        order_dict['createdAt'] = order_dict['createdAt'].isoformat()
        if order_dict.get('paidAt'):
            order_dict['paidAt'] = order_dict['paidAt'].isoformat()
        
        await db.payment_orders.insert_one(order_dict)
        
        return {
            "order_id": razorpay_order['id'],
            "amount": razorpay_order['amount'],
            "currency": razorpay_order['currency'],
            "key_id": os.getenv('RAZORPAY_KEY_ID', 'rzp_test_key')
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create payment order: {str(e)}"
        )

@router.post("/verify")
async def verify_payment(
    payment_data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Verify Razorpay payment and credit user account"""
    
    try:
        razorpay_order_id = payment_data['razorpay_order_id']
        razorpay_payment_id = payment_data['razorpay_payment_id']
        razorpay_signature = payment_data['razorpay_signature']
        
        # Verify signature
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }
        
        razorpay_client.utility.verify_payment_signature(params_dict)
        
        # Get order from database
        order = await db.payment_orders.find_one({
            "orderId": razorpay_order_id,
            "userId": current_user.id
        })
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        if order['status'] == 'paid':
            raise HTTPException(status_code=400, detail="Payment already processed")
        
        # Update order status
        await db.payment_orders.update_one(
            {"orderId": razorpay_order_id},
            {
                "$set": {
                    "status": "paid",
                    "paymentId": razorpay_payment_id,
                    "paidAt": datetime.now(timezone.utc).isoformat()
                }
            }
        )
        
        # Credit user account
        balance = await db.credit_balances.find_one({"userId": current_user.id})
        
        if not balance:
            balance = {
                "userId": current_user.id,
                "balance": 0,
                "total_purchased": 0,
                "total_used": 0
            }
        
        new_balance = balance['balance'] + order['credits']
        new_total_purchased = balance['total_purchased'] + order['credits']
        
        await db.credit_balances.update_one(
            {"userId": current_user.id},
            {
                "$set": {
                    "balance": new_balance,
                    "total_purchased": new_total_purchased,
                    "lastUpdated": datetime.now(timezone.utc).isoformat()
                }
            },
            upsert=True
        )
        
        # Log transaction
        await db.credit_transactions.insert_one({
            "id": str(__import__('uuid').uuid4()),
            "userId": current_user.id,
            "amount": order['credits'],
            "type": "purchase",
            "description": f"Purchased {order['credits']} credits",
            "orderId": razorpay_order_id,
            "paymentId": razorpay_payment_id,
            "balance_after": new_balance,
            "createdAt": datetime.now(timezone.utc).isoformat()
        })
        
        return {
            "status": "success",
            "message": "Payment verified and credits added",
            "credits_added": order['credits'],
            "new_balance": new_balance
        }
        
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid payment signature"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment verification failed: {str(e)}"
        )

@router.post("/webhook")
async def handle_webhook(
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Handle Razorpay webhooks"""
    
    try:
        payload = await request.body()
        signature = request.headers.get('X-Razorpay-Signature', '')
        webhook_secret = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')
        
        # Verify webhook signature
        razorpay_client.utility.verify_webhook_signature(
            payload.decode(),
            signature,
            webhook_secret
        )
        
        # Process webhook event
        import json
        event = json.loads(payload)
        
        if event.get('event') == 'payment.captured':
            payment_id = event['payload']['payment']['entity']['id']
            order_id = event['payload']['payment']['entity']['order_id']
            
            # Update order status
            await db.payment_orders.update_one(
                {"orderId": order_id},
                {"$set": {"status": "paid", "paymentId": payment_id}}
            )
        
        return {"status": "processed"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Webhook processing failed: {str(e)}"
        )

@router.get("/packages")
async def get_packages():
    """Get available credit packages"""
    return {"packages": CREDIT_PRICING['packages']}
