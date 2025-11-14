from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
import uuid

# User Models
class UserBase(BaseModel):
    email: EmailStr
    fullName: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    emailVerified: bool = False
    hasCompletedProfile: bool = False
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    googleId: Optional[str] = None

class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = "bearer"
    user: User

# Vendor Models
class VendorContact(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    designation: Optional[str] = None

class VendorCreate(BaseModel):
    companyName: str
    vendorType: Optional[str] = None
    primaryContactName: Optional[str] = None
    primaryContactEmail: Optional[EmailStr] = None
    primaryContactPhone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    pincode: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    website: Optional[str] = None
    paymentTerms: Optional[str] = None
    categories: List[str] = []
    tags: List[str] = []
    notes: Optional[str] = None

class VendorUpdate(BaseModel):
    companyName: Optional[str] = None
    vendorType: Optional[str] = None
    primaryContactName: Optional[str] = None
    primaryContactEmail: Optional[EmailStr] = None
    primaryContactPhone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    gstin: Optional[str] = None
    pan: Optional[str] = None
    website: Optional[str] = None
    paymentTerms: Optional[str] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None
    isActive: Optional[bool] = None

class Vendor(VendorCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    rating: float = 0.0
    totalRfqsSent: int = 0
    totalQuotesReceived: int = 0
    isActive: bool = True
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# RFQ Models
class RFQLineItem(BaseModel):
    itemName: str
    description: Optional[str] = None
    quantity: float
    unit: str
    specifications: Optional[str] = None

class RFQCreate(BaseModel):
    rfqNumber: str
    title: str
    description: Optional[str] = None
    vendorIds: List[str]
    lineItems: List[RFQLineItem]
    dueDate: datetime
    deliveryLocation: Optional[str] = None
    paymentTerms: Optional[str] = None
    notes: Optional[str] = None

class RFQUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    vendorIds: Optional[List[str]] = None
    lineItems: Optional[List[RFQLineItem]] = None
    dueDate: Optional[datetime] = None
    deliveryLocation: Optional[str] = None
    paymentTerms: Optional[str] = None
    notes: Optional[str] = None
    status: Optional[str] = None

class RFQ(RFQCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    status: str = "draft"  # draft, sent, closed
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    sentAt: Optional[datetime] = None

# Vendor Quote Models
class QuoteLineItem(BaseModel):
    itemName: str
    quantity: float
    unit: str
    unitPrice: float
    totalPrice: float
    remarks: Optional[str] = None

class VendorQuoteCreate(BaseModel):
    rfqId: str
    vendorId: str
    quoteNumber: Optional[str] = None
    totalAmount: float
    lineItems: List[QuoteLineItem]
    paymentTerms: Optional[str] = None
    deliveryTerms: Optional[str] = None
    validUntil: Optional[datetime] = None
    remarks: Optional[str] = None

class VendorQuote(VendorQuoteCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    status: str = "received"  # received, accepted, rejected
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Company Profile Models
class CompanyProfileCreate(BaseModel):
    companyName: str
    industry: str
    address: str
    taxId: str
    logoUrl: Optional[str] = None
    authorizedPersonName: str
    authorizedPersonMobile: str
    authorizedPersonEmail: EmailStr

class CompanyProfileUpdate(BaseModel):
    companyName: Optional[str] = None
    industry: Optional[str] = None
    address: Optional[str] = None
    taxId: Optional[str] = None
    logoUrl: Optional[str] = None
    authorizedPersonName: Optional[str] = None
    authorizedPersonMobile: Optional[str] = None
    authorizedPersonEmail: Optional[EmailStr] = None

class CompanyProfile(CompanyProfileCreate):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updatedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Team Member Models
class TeamMemberInvite(BaseModel):
    email: EmailStr
    role: str  # admin, manager, viewer
    name: Optional[str] = None

class TeamMember(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    companyId: str
    email: EmailStr
    name: Optional[str] = None
    role: str
    status: str = "invited"  # invited, active, inactive
    inviteToken: Optional[str] = None
    invitedAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    joinedAt: Optional[datetime] = None

# Email Verification Models
class EmailVerificationToken(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    userId: str
    token: str
    expiresAt: datetime
    createdAt: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))