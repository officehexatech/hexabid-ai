from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum
import uuid

# AI Credit Models
class CreditTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    amount: int  # Credits amount
    type: str  # "purchase", "usage", "refund"
    description: str
    orderId: Optional[str] = None
    paymentId: Optional[str] = None
    balance_after: int
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CreditBalance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    userId: str
    balance: int = 0  # Current credit balance
    total_purchased: int = 0
    total_used: int = 0
    lastUpdated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Payment Models
class PaymentOrderCreate(BaseModel):
    amount: int  # Amount in paise (multiply rupees by 100)
    credits: int  # Number of credits to purchase
    currency: str = "INR"

class PaymentOrder(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    orderId: str  # Razorpay order ID
    amount: int  # in paise
    credits: int
    currency: str
    status: str = "created"  # created, paid, failed
    paymentId: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    paidAt: Optional[datetime] = None

# AI Agent Execution Models
class WorkflowType(str, Enum):
    discover_and_bid = "discover_and_bid"
    parse_and_bid = "parse_and_bid"
    generate_boq = "generate_boq"
    assemble_documents = "assemble_documents"

class AgentExecutionRequest(BaseModel):
    workflow_type: WorkflowType
    input_data: Dict[str, Any]
    
class AgentExecutionStatus(str, Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class AgentExecution(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    execution_id: str
    workflow_type: str
    status: AgentExecutionStatus = AgentExecutionStatus.pending
    input_data: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None
    agents_executed: List[str] = []
    timeline: List[Dict[str, Any]] = []
    workflow_log: List[Dict[str, Any]] = []
    credits_used: int = 0
    error: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    startedAt: Optional[datetime] = None
    completedAt: Optional[datetime] = None

# Credit Pricing Configuration
CREDIT_PRICING = {
    "packages": [
        {"credits": 100, "price": 499, "bonus": 0},  # ₹499 for 100 credits
        {"credits": 500, "price": 2199, "bonus": 50},  # ₹2199 for 550 credits (10% bonus)
        {"credits": 1000, "price": 3999, "bonus": 150},  # ₹3999 for 1150 credits (15% bonus)
        {"credits": 5000, "price": 17999, "bonus": 1000},  # ₹17999 for 6000 credits (20% bonus)
    ],
    "usage_costs": {
        "tender_discovery": 10,  # credits per discovery
        "document_parser": 15,  # credits per document
        "boq_generator": 20,  # credits per BOQ
        "document_assembly": 10,  # credits per assembly
        "discover_and_bid": 55,  # total for full workflow
        "parse_and_bid": 45,  # without discovery
    }
}
