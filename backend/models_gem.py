from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

class BidSubmission(BaseModel):
    """Model for tracking bid submissions"""
    bid_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    tender_id: str
    tender_number: str
    tender_title: str
    organization: str
    
    # Bid details
    bid_amount: float
    technical_bid_file: Optional[str] = None
    financial_bid_file: Optional[str] = None
    emd_proof_file: Optional[str] = None
    
    # Status tracking
    status: str = 'draft'  # draft, submitted, under_evaluation, awarded, rejected
    submission_date: Optional[str] = None
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    # Results
    result_status: Optional[str] = None
    ranking: Optional[int] = None
    total_bidders: Optional[int] = None
    winner_company: Optional[str] = None
    winner_amount: Optional[float] = None
    remarks: Optional[str] = None
    
    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class BidResult(BaseModel):
    """Model for bid results"""
    result_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    tender_number: str
    tender_title: str
    bid_id: Optional[str] = None
    
    # Result details
    result_date: str
    status: str  # awarded, rejected, cancelled
    winner_company: str
    winner_amount: float
    
    # Our bid info
    our_ranking: Optional[int] = None
    our_amount: Optional[float] = None
    our_status: Optional[str] = None
    
    # Competition data
    total_bidders: int
    all_bids: List[Dict[str, Any]] = []
    
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class CompetitorProfile(BaseModel):
    """Model for competitor analysis"""
    competitor_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company_name: str
    
    # Stats
    total_bids: int = 0
    won_bids: int = 0
    win_rate: float = 0.0
    avg_bid_amount: float = 0.0
    
    # Categories they bid in
    categories: List[str] = []
    
    # Recent activity
    recent_tenders: List[Dict[str, Any]] = []
    
    # Pricing analysis
    pricing_strategy: Optional[str] = None  # aggressive, competitive, premium
    avg_discount_percentage: Optional[float] = None
    
    # Metadata
    first_seen: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class SearchQuery(BaseModel):
    """Model for search queries"""
    query: str
    collection: Optional[str] = None  # tenders, products, vendors, boqs
    filters: Dict[str, Any] = {}
    page: int = 1
    limit: int = 20
