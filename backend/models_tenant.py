"""
Multi-Tenant Models for HexaBid
All tenants are isolated by tenant_id
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
from enum import Enum
import uuid

# Tenant Status
class TenantStatus(str, Enum):
    active = "active"
    suspended = "suspended"
    trial = "trial"
    cancelled = "cancelled"

# Tenant Plans
class TenantPlan(str, Enum):
    free = "free"
    startup = "startup"
    professional = "professional"
    enterprise = "enterprise"

# Tenant Model
class Tenant(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_name: str
    domain: Optional[str] = None  # Custom domain
    status: TenantStatus = TenantStatus.trial
    plan: TenantPlan = TenantPlan.free
    owner_user_id: str  # The user who created the tenant
    settings: dict = {}
    features_enabled: List[str] = []  # Feature flags
    max_users: int = 5
    max_tenders_per_month: int = 10
    max_ai_credits_per_month: int = 100
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    trial_ends_at: Optional[datetime] = None
    subscription_ends_at: Optional[datetime] = None

# Tenant Usage Tracking
class TenantUsage(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    month: str  # Format: YYYY-MM
    total_users: int = 0
    total_tenders: int = 0
    ai_credits_used: int = 0
    ai_tokens_consumed: int = 0  # OpenAI tokens
    storage_used_mb: int = 0
    api_calls: int = 0
    cost_incurred: float = 0.0  # Estimated cost
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Tenant User Roles
class TenantRole(str, Enum):
    owner = "owner"
    admin = "admin"
    manager = "manager"
    user = "user"
    viewer = "viewer"

# Tenant User Membership
class TenantMember(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    user_id: str
    role: TenantRole
    permissions: List[str] = []
    is_active: bool = True
    invited_by: Optional[str] = None
    joined_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Super Admin Actions Log
class AdminAction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    admin_user_id: str
    action_type: str  # "create_tenant", "suspend_tenant", "change_plan", etc.
    target_tenant_id: Optional[str] = None
    details: dict = {}
    performed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Tenant Billing
class TenantBilling(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: str
    plan: TenantPlan
    billing_cycle: str  # "monthly" | "yearly"
    amount: float
    currency: str = "INR"
    payment_status: str  # "paid" | "pending" | "failed"
    invoice_id: Optional[str] = None
    billing_date: datetime
    next_billing_date: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Feature Flags per Tenant
TENANT_FEATURES = {
    "free": [
        "basic_tender_management",
        "vendor_management",
        "rfq_basic"
    ],
    "startup": [
        "basic_tender_management",
        "vendor_management",
        "rfq_basic",
        "ai_discovery",
        "ai_parsing",
        "boq_generator"
    ],
    "professional": [
        "basic_tender_management",
        "vendor_management",
        "rfq_basic",
        "ai_discovery",
        "ai_parsing",
        "boq_generator",
        "ai_pricing",
        "ai_risk_assessment",
        "document_assembly",
        "analytics_advanced",
        "email_notifications"
    ],
    "enterprise": [
        "basic_tender_management",
        "vendor_management",
        "rfq_basic",
        "ai_discovery",
        "ai_parsing",
        "boq_generator",
        "ai_pricing",
        "ai_risk_assessment",
        "document_assembly",
        "analytics_advanced",
        "email_notifications",
        "whatsapp_integration",
        "custom_workflows",
        "api_access",
        "white_label",
        "dedicated_support",
        "custom_domain"
    ]
}

# Plan Limits
PLAN_LIMITS = {
    "free": {
        "max_users": 2,
        "max_tenders_per_month": 5,
        "max_ai_credits_per_month": 50,
        "max_storage_mb": 100,
        "api_rate_limit": 100
    },
    "startup": {
        "max_users": 5,
        "max_tenders_per_month": 25,
        "max_ai_credits_per_month": 250,
        "max_storage_mb": 1000,
        "api_rate_limit": 500
    },
    "professional": {
        "max_users": 20,
        "max_tenders_per_month": 100,
        "max_ai_credits_per_month": 1000,
        "max_storage_mb": 10000,
        "api_rate_limit": 2000
    },
    "enterprise": {
        "max_users": -1,  # Unlimited
        "max_tenders_per_month": -1,
        "max_ai_credits_per_month": -1,
        "max_storage_mb": -1,
        "api_rate_limit": -1
    }
}

# Plan Pricing (INR per month)
PLAN_PRICING = {
    "free": 0,
    "startup": 2999,
    "professional": 9999,
    "enterprise": 49999  # Base price, custom pricing available
}
