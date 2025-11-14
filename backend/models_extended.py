from pydantic import BaseModel, Field, EmailStr, ConfigDict, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from enum import Enum
import uuid

# Tender Models
class TenderStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    submitted = "submitted"
    won = "won"
    lost = "lost"
    archived = "archived"

class TenderSource(str, Enum):
    gem = "gem"
    cppp = "cppp"
    eprocure = "eprocure"
    manual = "manual"

class TenderCreate(BaseModel):
    tenderNumber: str
    title: str
    description: Optional[str] = None
    source: TenderSource = TenderSource.manual
    organization: str
    department: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    publishDate: Optional[datetime] = None
    submissionDeadline: datetime
    tenderValue: Optional[float] = None
    emdAmount: Optional[float] = None
    documentUrl: Optional[str] = None
    tags: List[str] = []
    notes: Optional[str] = None

class Tender(TenderCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    status: TenderStatus = TenderStatus.new
    workspaceId: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# BOQ Models
class BOQLineItem(BaseModel):
    itemNumber: str
    description: str
    specification: Optional[str] = None
    quantity: float
    unit: str
    estimatedRate: Optional[float] = None
    ourRate: Optional[float] = None
    totalAmount: Optional[float] = None
    remarks: Optional[str] = None
    productId: Optional[str] = None

class BOQCreate(BaseModel):
    tenderId: str
    boqNumber: str
    title: str
    lineItems: List[BOQLineItem]
    totalEstimatedValue: Optional[float] = None
    totalOurValue: Optional[float] = None
    marginPercentage: Optional[float] = None
    notes: Optional[str] = None

class BOQ(BOQCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    version: int = 1
    status: str = "draft"  # draft, approved, submitted
    approvedBy: Optional[str] = None
    approvedAt: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Product Catalog Models
class ProductCategory(str, Enum):
    hardware = "hardware"
    software = "software"
    service = "service"
    material = "material"
    equipment = "equipment"

class ProductCreate(BaseModel):
    productCode: str
    productName: str
    category: ProductCategory
    brand: str
    model: Optional[str] = None
    specifications: Dict[str, Any] = {}
    unitPrice: Optional[float] = None
    unit: str = "pcs"
    oemVendorId: Optional[str] = None
    leadTimeDays: Optional[int] = None
    warrantyMonths: Optional[int] = None
    description: Optional[str] = None
    imageUrl: Optional[str] = None
    datasheet: Optional[str] = None
    tags: List[str] = []

class Product(ProductCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    isActive: bool = True
    priceHistory: List[Dict[str, Any]] = []
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Compliance Models
class ComplianceClause(BaseModel):
    clauseNumber: str
    requirement: str
    ourCompliance: str
    supportingDocuments: List[str] = []
    status: str = "pending"  # pending, compliant, non_compliant

class TechnicalCompliance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenderId: str
    userId: str
    clauses: List[ComplianceClause]
    overallStatus: str = "in_progress"
    aiSuggestions: Optional[Dict[str, Any]] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Document Template Models
class DocumentType(str, Enum):
    cover_letter = "cover_letter"
    company_profile = "company_profile"
    experience = "experience"
    technical_bid = "technical_bid"
    financial_bid = "financial_bid"
    compliance = "compliance"

class GeneratedDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenderId: str
    userId: str
    documentType: DocumentType
    content: str
    fileName: str
    fileUrl: Optional[str] = None
    version: int = 1
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# MIS & Analytics Models
class TenderAnalytics(BaseModel):
    totalTenders: int = 0
    activeTenders: int = 0
    submittedTenders: int = 0
    wonTenders: int = 0
    lostTenders: int = 0
    winRate: float = 0.0
    totalValue: float = 0.0
    avgTenderValue: float = 0.0

class CompetitorEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tenderId: str
    userId: str
    competitorName: str
    quotedPrice: Optional[float] = None
    won: bool = False
    remarks: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Alert Models
class AlertType(str, Enum):
    deadline = "deadline"
    rfq_response = "rfq_response"
    approval = "approval"
    tender_match = "tender_match"
    status_update = "status_update"

class AlertChannel(str, Enum):
    email = "email"
    whatsapp = "whatsapp"
    inapp = "inapp"

class Alert(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    alertType: AlertType
    title: str
    message: str
    relatedId: Optional[str] = None
    channels: List[AlertChannel]
    isRead: bool = False
    sentAt: Optional[datetime] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ERP Models - Sales
class LeadStatus(str, Enum):
    new = "new"
    contacted = "contacted"
    qualified = "qualified"
    proposal = "proposal"
    negotiation = "negotiation"
    won = "won"
    lost = "lost"

class Lead(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    companyName: str
    contactPerson: str
    email: EmailStr
    phone: Optional[str] = None
    status: LeadStatus = LeadStatus.new
    source: Optional[str] = None
    estimatedValue: Optional[float] = None
    expectedClosingDate: Optional[datetime] = None
    notes: Optional[str] = None
    assignedTo: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ERP Models - Purchase
class PurchaseOrderStatus(str, Enum):
    draft = "draft"
    sent = "sent"
    confirmed = "confirmed"
    partially_received = "partially_received"
    received = "received"
    cancelled = "cancelled"

class POLineItem(BaseModel):
    productId: Optional[str] = None
    description: str
    quantity: float
    unit: str
    unitPrice: float
    totalPrice: float

class PurchaseOrder(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    poNumber: str
    vendorId: str
    orderDate: datetime
    deliveryDate: Optional[datetime] = None
    status: PurchaseOrderStatus = PurchaseOrderStatus.draft
    lineItems: List[POLineItem]
    subtotal: float
    tax: float = 0.0
    totalAmount: float
    notes: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ERP Models - Inventory
class StockMovementType(str, Enum):
    in_receipt = "in_receipt"
    out_issue = "out_issue"
    transfer = "transfer"
    adjustment = "adjustment"

class StockMovement(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    productId: str
    movementType: StockMovementType
    quantity: float
    unit: str
    fromLocation: Optional[str] = None
    toLocation: Optional[str] = None
    reference: Optional[str] = None
    remarks: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ERP Models - Projects
class ProjectStatus(str, Enum):
    planning = "planning"
    in_progress = "in_progress"
    on_hold = "on_hold"
    completed = "completed"
    cancelled = "cancelled"

class ProjectTask(BaseModel):
    taskName: str
    description: Optional[str] = None
    assignedTo: Optional[str] = None
    startDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    status: str = "pending"
    progress: float = 0.0

class Project(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    projectCode: str
    projectName: str
    clientName: str
    status: ProjectStatus = ProjectStatus.planning
    startDate: datetime
    endDate: Optional[datetime] = None
    budget: Optional[float] = None
    actualCost: Optional[float] = None
    tasks: List[ProjectTask] = []
    teamMembers: List[str] = []
    notes: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ERP Models - Finance
class InvoiceStatus(str, Enum):
    draft = "draft"
    sent = "sent"
    paid = "paid"
    partially_paid = "partially_paid"
    overdue = "overdue"
    cancelled = "cancelled"

class InvoiceLineItem(BaseModel):
    description: str
    quantity: float
    unitPrice: float
    totalPrice: float

class Invoice(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    invoiceNumber: str
    clientId: str
    invoiceDate: datetime
    dueDate: datetime
    status: InvoiceStatus = InvoiceStatus.draft
    lineItems: List[InvoiceLineItem]
    subtotal: float
    tax: float = 0.0
    totalAmount: float
    paidAmount: float = 0.0
    notes: Optional[str] = None
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# ERP Models - HRMS
class EmployeeStatus(str, Enum):
    active = "active"
    on_leave = "on_leave"
    resigned = "resigned"
    terminated = "terminated"

class Employee(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    employeeCode: str
    fullName: str
    email: EmailStr
    phone: str
    designation: str
    department: str
    joiningDate: datetime
    status: EmployeeStatus = EmployeeStatus.active
    salary: Optional[float] = None
    address: Optional[str] = None
    emergencyContact: Optional[str] = None
    documents: List[str] = []
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))