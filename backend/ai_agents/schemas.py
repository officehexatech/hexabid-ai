"""
Structured JSON Schemas for HexaBid AI Multi-Agent System
All agents must return responses conforming to these schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime, date
from enum import Enum

# ============================================================================
# DISCOVERY SCHEMAS
# ============================================================================

class TenderSource(str, Enum):
    gem = "gem"
    eprocure = "eprocure"
    cppp = "cppp"
    manual = "manual"
    scraped = "scraped"

class EligibilityFlag(BaseModel):
    criterion: str
    is_eligible: bool
    reason: str

class DiscoveredTender(BaseModel):
    tender_number: str
    title: str
    organization: str
    department: Optional[str] = None
    category: str
    location: str
    publish_date: date
    submission_deadline: datetime
    tender_value: Optional[float] = None
    emd_amount: Optional[float] = None
    source: TenderSource
    document_url: Optional[str] = None
    relevance_score: float = Field(..., ge=0, le=100)  # 0-100
    win_probability: Literal["high", "medium", "low"]
    eligibility_flags: List[EligibilityFlag] = []
    key_requirements: List[str] = []
    confidence_score: float = Field(..., ge=0, le=1)  # 0-1

class DiscoveryOutput(BaseModel):
    discovered_tenders: List[DiscoveredTender]
    search_summary: str
    total_found: int
    recommendations: List[str]
    processing_timestamp: datetime
    confidence_score: float = Field(..., ge=0, le=1)

# ============================================================================
# PARSING SCHEMAS
# ============================================================================

class BOQLineItem(BaseModel):
    item_number: str
    description: str
    specification: str
    quantity: float
    unit: str
    estimated_rate: Optional[float] = None
    confidence_score: float = Field(..., ge=0, le=1)

class TechnicalRequirement(BaseModel):
    clause_number: str
    requirement: str
    is_mandatory: bool
    compliance_needed: str
    confidence_score: float = Field(..., ge=0, le=1)

class SubmissionDetails(BaseModel):
    deadline: datetime
    submission_mode: Literal["online", "offline", "hybrid"]
    portal_link: Optional[str] = None
    physical_address: Optional[str] = None

class EvaluationCriteria(BaseModel):
    technical_score_weightage: float
    financial_score_weightage: float
    evaluation_method: str
    l1_criteria: Optional[str] = None

class EMDDetails(BaseModel):
    amount: float
    mode: List[str]  # ["DD", "BG", "NEFT", "Online"]
    exemption_clauses: List[str] = []

class KeyDate(BaseModel):
    event: str
    date: datetime

class ParsedTender(BaseModel):
    tender_number: str
    title: str
    organization: str
    description: str
    scope_of_work: str
    boq_items: List[BOQLineItem]
    technical_requirements: List[TechnicalRequirement]
    mandatory_documents: List[str]
    submission_details: SubmissionDetails
    evaluation_criteria: EvaluationCriteria
    emd_details: EMDDetails
    key_dates: List[KeyDate]
    manual_checks_needed: List[str] = []  # Items needing human review
    confidence_score: float = Field(..., ge=0, le=1)
    parsing_timestamp: datetime

# ============================================================================
# BOQ & COMPLIANCE SCHEMAS
# ============================================================================

class MappedProduct(BaseModel):
    product_code: str
    product_name: str
    brand: str
    model: str
    our_price: float
    meets_spec: bool
    compliance_notes: str

class EnhancedBOQItem(BaseModel):
    item_number: str
    description: str
    specification: str
    quantity: float
    unit: str
    estimated_rate: Optional[float] = None
    our_rate: float
    mapped_products: List[MappedProduct] = []
    compliance_status: Literal["compliant", "partial", "non_compliant"]
    compliance_notes: str
    total_amount: float
    confidence_score: float = Field(..., ge=0, le=1)

class ComplianceGap(BaseModel):
    requirement: str
    status: Literal["met", "partial", "not_met"]
    mitigation: Optional[str] = None

class BOQOutput(BaseModel):
    tender_id: str
    boq_number: str
    title: str
    line_items: List[EnhancedBOQItem]
    total_estimated_value: float
    total_our_value: float
    margin_percentage: float
    compliance_gaps: List[ComplianceGap]
    missing_specifications: List[str]
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0, le=1)
    generation_timestamp: datetime

# ============================================================================
# RFQ & VENDOR QUOTE SCHEMAS
# ============================================================================

class RFQLineItem(BaseModel):
    item_number: str
    description: str
    specification: str
    quantity: float
    unit: str
    target_price: Optional[float] = None

class GeneratedRFQ(BaseModel):
    rfq_number: str
    vendor_id: str
    vendor_name: str
    line_items: List[RFQLineItem]
    submission_deadline: datetime
    email_template: str
    whatsapp_template: str
    sent: bool = False

class VendorQuoteLine(BaseModel):
    item_number: str
    quoted_price: float
    brand: str
    model: str
    lead_time_days: int
    warranty_months: int

class VendorQuote(BaseModel):
    quote_id: str
    rfq_id: str
    vendor_id: str
    vendor_name: str
    quote_lines: List[VendorQuoteLine]
    total_quoted_value: float
    valid_until: date
    terms_and_conditions: str
    received_at: datetime
    confidence_score: float = Field(..., ge=0, le=1)

class RFQOutput(BaseModel):
    rfqs_generated: List[GeneratedRFQ]
    quotes_received: List[VendorQuote]
    summary: str
    recommendations: List[str]
    confidence_score: float = Field(..., ge=0, le=1)

# ============================================================================
# PRICING STRATEGY SCHEMAS
# ============================================================================

class PricingScenario(BaseModel):
    scenario_name: Literal["aggressive", "balanced", "conservative"]
    total_bid_value: float
    margin_percentage: float
    profit_amount: float
    win_probability: float = Field(..., ge=0, le=1)
    reasoning: str
    risks: List[str]
    advantages: List[str]

class CompetitorIntelligence(BaseModel):
    estimated_competitors: int
    likely_l1_price: Optional[float] = None
    our_rank_prediction: Optional[int] = None
    market_dynamics: str

class PricingReport(BaseModel):
    tender_id: str
    scenarios: List[PricingScenario]  # Must have exactly 3
    recommended_scenario: Literal["aggressive", "balanced", "conservative"]
    competitor_intelligence: CompetitorIntelligence
    price_optimization_suggestions: List[str]
    confidence_score: float = Field(..., ge=0, le=1)
    generation_timestamp: datetime

# ============================================================================
# RISK & COMPLIANCE SCHEMAS
# ============================================================================

class RiskCategory(str, Enum):
    eligibility = "eligibility"
    technical = "technical"
    financial = "financial"
    delivery = "delivery"
    legal = "legal"
    reputational = "reputational"

class IdentifiedRisk(BaseModel):
    category: RiskCategory
    description: str
    severity: Literal["critical", "high", "medium", "low"]
    probability: float = Field(..., ge=0, le=1)
    impact: str
    mitigation_steps: List[str]

class ComplianceCheck(BaseModel):
    requirement: str
    status: Literal["pass", "fail", "needs_clarification"]
    evidence: str
    notes: str

class RiskReport(BaseModel):
    tender_id: str
    overall_risk_score: float = Field(..., ge=0, le=100)  # 0=low risk, 100=high risk
    risk_level: Literal["low", "medium", "high", "critical"]
    identified_risks: List[IdentifiedRisk]
    compliance_checks: List[ComplianceCheck]
    eligibility_status: Literal["eligible", "not_eligible", "conditional"]
    financial_viability: Literal["viable", "marginal", "not_viable"]
    recommendation: str
    confidence_score: float = Field(..., ge=0, le=1)
    assessment_timestamp: datetime

# ============================================================================
# DOCUMENT ASSEMBLY SCHEMAS
# ============================================================================

class GeneratedDocument(BaseModel):
    document_type: Literal["cover_letter", "technical_bid", "financial_bid", 
                           "compliance_statement", "annexures", "checklist"]
    file_name: str
    file_path: str  # S3 or local path
    file_size_kb: int
    page_count: int
    requires_signature: bool
    requires_seal: bool

class DocumentManifest(BaseModel):
    item: str
    status: Literal["completed", "pending", "not_required"]
    notes: str

class DocPackage(BaseModel):
    tender_id: str
    package_id: str
    documents: List[GeneratedDocument]
    manifest: List[DocumentManifest]
    zip_file_path: str
    total_size_mb: float
    ready_for_submission: bool
    missing_items: List[str]
    instructions: str
    generation_timestamp: datetime
    confidence_score: float = Field(..., ge=0, le=1)

# ============================================================================
# STRATEGY & DECISION SCHEMAS
# ============================================================================

class DecisionFactors(BaseModel):
    discovery_score: float
    technical_feasibility: float
    pricing_competitiveness: float
    risk_score: float
    resource_availability: float
    strategic_importance: float

class StrategyDecision(BaseModel):
    tender_id: str
    decision: Literal["BID", "NO-BID", "NEEDS_INFO"]
    confidence: float = Field(..., ge=0, le=1)
    reasoning: str
    decision_factors: DecisionFactors
    key_considerations: List[str]
    recommended_actions: List[str]
    conditions: List[str] = []  # If decision is conditional
    expected_effort_hours: Optional[float] = None
    expected_cost: Optional[float] = None
    strategic_notes: str
    decision_timestamp: datetime

# ============================================================================
# AI ASSISTANT SCHEMAS
# ============================================================================

class AgentAction(BaseModel):
    agent: str
    action: str
    parameters: Dict[str, Any]

class AssistantResponse(BaseModel):
    message: str  # Human-readable response
    intent: str  # Identified user intent
    actions: List[AgentAction] = []  # Actions to execute
    data: Optional[Dict[str, Any]] = None  # Structured data
    suggestions: List[str] = []
    needs_clarification: bool = False
    clarification_questions: List[str] = []
    confidence_score: float = Field(..., ge=0, le=1)
    response_timestamp: datetime
