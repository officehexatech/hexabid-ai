from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime, timezone
import sys
sys.path.append('/app/backend')
from models_ai import AgentExecutionRequest, AgentExecution, AgentExecutionStatus, CREDIT_PRICING
from models import User
from routers.auth import get_current_user, get_db
from ai_agents.orchestrator import AgentOrchestrator

router = APIRouter()

async def deduct_credits(db: AsyncIOMotorDatabase, user_id: str, workflow_type: str, tenant_id: str = None) -> bool:
    """Deduct credits for AI agent execution and track usage"""
    cost = CREDIT_PRICING['usage_costs'].get(workflow_type, 50)
    
    # Get user's credit balance
    balance_doc = await db.credit_balances.find_one({"userId": user_id})
    if not balance_doc:
        # Initialize balance
        await db.credit_balances.insert_one({
            "userId": user_id,
            "balance": 0,
            "total_purchased": 0,
            "total_used": 0,
            "lastUpdated": datetime.now(timezone.utc).isoformat()
        })
        return False
    
    if balance_doc['balance'] < cost:
        return False
    
    # Deduct credits
    new_balance = balance_doc['balance'] - cost
    await db.credit_balances.update_one(
        {"userId": user_id},
        {
            "$set": {
                "balance": new_balance,
                "total_used": balance_doc['total_used'] + cost,
                "lastUpdated": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    # Log transaction
    await db.credit_transactions.insert_one({
        "id": str(__import__('uuid').uuid4()),
        "userId": user_id,
        "amount": -cost,
        "type": "usage",
        "description": f"AI Agent Execution: {workflow_type}",
        "balance_after": new_balance,
        "createdAt": datetime.now(timezone.utc).isoformat()
    })
    
    return True

async def execute_agent_workflow(
    execution_id: str,
    request_data: AgentExecutionRequest,
    user_id: str,
    db: AsyncIOMotorDatabase
):
    """Background task to execute AI agent workflow"""
    try:
        # Update status to running
        await db.agent_executions.update_one(
            {"id": execution_id},
            {"$set": {
                "status": "running",
                "startedAt": datetime.now(timezone.utc).isoformat()
            }}
        )
        
        # Get user context (company profile, products)
        company = await db.companies.find_one({"userId": user_id}, {"_id": 0})
        products = await db.products.find({"userId": user_id, "isActive": True}, {"_id": 0}).to_list(length=100)
        tenders = await db.tenders.find({"userId": user_id}, {"_id": 0}).to_list(length=50)
        
        user_context = {
            "company_profile": company,
            "product_catalog": products,
            "existing_tenders_db": tenders
        }
        
        # Execute workflow
        orchestrator = AgentOrchestrator()
        results = await orchestrator.execute_phase1_workflow(
            workflow_type=request_data.workflow_type,
            input_data=request_data.input_data,
            user_context=user_context
        )
        
        # Calculate estimated tokens (approximate based on agents used)
        estimated_tokens = len(results.get('agents_executed', [])) * 2000  # ~2k tokens per agent
        
        # Update execution record
        await db.agent_executions.update_one(
            {"id": execution_id},
            {"$set": {
                "status": "completed" if results['status'] == 'completed' else "failed",
                "results": results.get('results', {}),
                "agents_executed": results.get('agents_executed', []),
                "timeline": results.get('timeline', []),
                "workflow_log": results.get('workflow_log', []),
                "completedAt": datetime.now(timezone.utc).isoformat(),
                "credits_used": CREDIT_PRICING['usage_costs'].get(request_data.workflow_type, 50),
                "tokens_consumed": estimated_tokens
            }}
        )
        
        # Update tenant usage if tenant exists
        membership = await db.tenant_members.find_one({"user_id": user_id, "is_active": True})
        if membership:
            current_month = datetime.now(timezone.utc).strftime('%Y-%m')
            await db.tenant_usage.update_one(
                {"tenant_id": membership["tenant_id"], "month": current_month},
                {
                    "$inc": {
                        "ai_credits_used": CREDIT_PRICING['usage_costs'].get(request_data.workflow_type, 50),
                        "ai_tokens_consumed": estimated_tokens,
                        "cost_incurred": estimated_tokens * 0.00002  # Approximate $0.00002 per token
                    },
                    "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
                },
                upsert=True
            )
        
    except Exception as e:
        # Update with error
        await db.agent_executions.update_one(
            {"id": execution_id},
            {"$set": {
                "status": "failed",
                "error": str(e),
                "completedAt": datetime.now(timezone.utc).isoformat()
            }}
        )

@router.post("/execute", status_code=status.HTTP_202_ACCEPTED)
async def execute_agents(
    request: AgentExecutionRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Execute AI agent workflow (async)"""
    
    # Get tenant_id if multi-tenant enabled
    membership = await db.tenant_members.find_one({"user_id": current_user.id, "is_active": True})
    tenant_id = membership.get("tenant_id") if membership else None
    
    # Check and deduct credits
    has_credits = await deduct_credits(db, current_user.id, request.workflow_type, tenant_id)
    if not has_credits:
        cost = CREDIT_PRICING['usage_costs'].get(request.workflow_type, 50)
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=f"Insufficient credits. Need {cost} credits for this workflow."
        )
    
    # Create execution record
    execution = AgentExecution(
        userId=current_user.id,
        execution_id=str(__import__('uuid').uuid4()),
        workflow_type=request.workflow_type,
        input_data=request.input_data,
        status=AgentExecutionStatus.pending
    )
    
    execution_dict = execution.model_dump()
    for date_field in ['createdAt', 'startedAt', 'completedAt']:
        if execution_dict.get(date_field):
            execution_dict[date_field] = execution_dict[date_field].isoformat()
    
    await db.agent_executions.insert_one(execution_dict)
    
    # Execute in background
    background_tasks.add_task(
        execute_agent_workflow,
        execution.id,
        request,
        current_user.id,
        db
    )
    
    return {
        "execution_id": execution.id,
        "status": "pending",
        "message": "Workflow execution started",
        "credits_deducted": CREDIT_PRICING['usage_costs'].get(request.workflow_type, 50)
    }

@router.get("/executions")
async def get_executions(
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get user's agent execution history"""
    executions = await db.agent_executions.find(
        {"userId": current_user.id},
        {"_id": 0}
    ).sort("createdAt", -1).limit(50).to_list(length=50)
    
    return {"executions": executions}

@router.get("/executions/{execution_id}")
async def get_execution(
    execution_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db)
):
    """Get specific execution details"""
    execution = await db.agent_executions.find_one(
        {"id": execution_id, "userId": current_user.id},
        {"_id": 0}
    )
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution

@router.get("/pricing")
async def get_pricing():
    """Get AI agent pricing and credit packages"""
    return CREDIT_PRICING
