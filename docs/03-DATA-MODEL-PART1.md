# HexaBid - Data Model (Part 1: Core Tables)

## ER Diagram Overview

```
[Tenants] ───< has many >─── [Users]
    │                              │
    │                              │
    └──< has many >── [Tenders] ──< belongs to >──┘
                         │
                         ├──< has one >── [TenderProjects]
                         │                     │
                         │                     ├──< has many >── [ProjectTasks]
                         │                     ├──< has many >── [Approvals]
                         │                     └──< has many >── [Documents]
                         │
                         ├──< has many >── [BOQItems]
                         │                     │
                         │                     ├──< links to >── [Products]
                         │                     └──< has many >── [VendorQuotes]
                         │
                         ├──< has many >── [ComplianceAnswers]
                         ├──< has many >── [Communications]
                         └──< has many >── [DocumentJobs]

[OEMVendors] ──< has many >── [VendorQuotes]
      │
      └──< has many >── [VendorPriceLists]

[Products] ──< belongs to >── [OEMVendors]
     │
     └──< has many >── [PriceHistory]
```

## Schema Organization

### Shared Schema (public)

**Purpose**: System-wide metadata, not tenant-specific

**Tables**:
- `tenants`: Tenant master
- `subscription_plans`: Plan definitions
- `system_settings`: Global configuration
- `migration_history`: Schema version tracking

### Per-Tenant Schema (tenant_{id})

**Purpose**: Complete isolation of tenant data

**All tables listed below reside in tenant schema**

---

## Core Tables

### 1. public.tenants (Shared)

```sql
CREATE TABLE public.tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subdomain VARCHAR(100) UNIQUE NOT NULL,
  company_name VARCHAR(255) NOT NULL,
  company_email VARCHAR(255),
  company_phone VARCHAR(20),
  
  -- Subscription
  subscription_plan_id UUID REFERENCES public.subscription_plans(id),
  subscription_status VARCHAR(20) DEFAULT 'active', -- active, suspended, cancelled
  billing_cycle VARCHAR(20), -- monthly, annual
  subscription_start_date TIMESTAMP,
  subscription_end_date TIMESTAMP,
  
  -- Usage & Limits
  user_limit INTEGER DEFAULT 10,
  storage_limit_gb INTEGER DEFAULT 50,
  api_rate_limit INTEGER DEFAULT 1000, -- requests per minute
  
  -- Technical
  database_schema VARCHAR(100), -- e.g., 'tenant_abc123'
  status VARCHAR(20) DEFAULT 'active', -- active, inactive, suspended
  
  -- Metadata
  settings JSONB DEFAULT '{}', -- Tenant-specific settings
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP -- Soft delete
);

CREATE INDEX idx_tenants_subdomain ON public.tenants(subdomain);
CREATE INDEX idx_tenants_status ON public.tenants(status);
```

### 2. public.subscription_plans (Shared)

```sql
CREATE TABLE public.subscription_plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) NOT NULL, -- Starter, Pro, Enterprise
  display_name VARCHAR(255),
  description TEXT,
  
  -- Pricing
  price_monthly DECIMAL(10, 2),
  price_annual DECIMAL(10, 2),
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Limits
  max_users INTEGER,
  max_storage_gb INTEGER,
  max_tenders_per_month INTEGER,
  api_rate_limit INTEGER,
  
  -- Features
  features JSONB DEFAULT '[]', -- ['ai_assistant', 'advanced_analytics', ...]
  
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## Tenant Schema Tables

### 3. users (Per Tenant)

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Identity
  email VARCHAR(255) UNIQUE NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  avatar_url TEXT,
  
  -- Authentication
  otp_hash VARCHAR(255), -- Hashed OTP for current session
  otp_expires_at TIMESTAMP,
  otp_attempts INTEGER DEFAULT 0,
  
  last_login_at TIMESTAMP,
  last_login_ip VARCHAR(45),
  
  -- Authorization
  role_id UUID REFERENCES roles(id),
  permissions JSONB DEFAULT '[]', -- Additional permissions beyond role
  
  -- Status
  status VARCHAR(20) DEFAULT 'active', -- active, inactive, suspended
  email_verified BOOLEAN DEFAULT false,
  
  -- Preferences
  preferences JSONB DEFAULT '{}', -- UI settings, notifications, etc.
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
```

### 4. roles (Per Tenant)

```sql
CREATE TABLE roles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) UNIQUE NOT NULL, -- BidManager, TechLead, Finance, Approver
  display_name VARCHAR(255),
  description TEXT,
  
  permissions JSONB NOT NULL DEFAULT '[]',
  -- Example: [
  --   "tender:read", "tender:write", "tender:delete",
  --   "boq:read", "boq:write",
  --   "oem:read", "document:generate"
  -- ]
  
  is_system BOOLEAN DEFAULT false, -- System roles can't be deleted
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 5. company_profile (Per Tenant)

```sql
CREATE TABLE company_profile (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Basic Info
  legal_name VARCHAR(255),
  trade_name VARCHAR(255),
  registration_number VARCHAR(100),
  pan VARCHAR(20),
  gstin VARCHAR(20),
  
  -- Address
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  pincode VARCHAR(20),
  
  -- Contact
  primary_email VARCHAR(255),
  primary_phone VARCHAR(20),
  website VARCHAR(255),
  
  -- Tender Configuration
  master_keywords TEXT[], -- Array of keywords for tender alerts
  business_categories TEXT[], -- Categories of interest
  target_regions TEXT[], -- Preferred tender regions
  
  -- Digital Signatures
  digital_signature_certificate JSONB, -- Store cert metadata
  signature_authorized_persons JSONB DEFAULT '[]',
  
  -- Mailbox Config
  tender_inbox_email VARCHAR(255),
  whatsapp_api_config JSONB,
  
  -- Branding
  logo_url TEXT,
  letterhead_url TEXT,
  
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_by UUID REFERENCES users(id)
);
```

### 6. tenders (Per Tenant)

```sql
CREATE TABLE tenders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Source
  source VARCHAR(50) NOT NULL, -- gem, manual_upload, paste_url, csv_import
  source_url TEXT,
  external_tender_id VARCHAR(255), -- ID from source portal
  
  -- Basic Info
  title TEXT NOT NULL,
  tender_number VARCHAR(255),
  buyer_organization VARCHAR(255),
  buyer_department VARCHAR(255),
  
  -- Metadata
  category VARCHAR(255),
  sub_category VARCHAR(255),
  tender_type VARCHAR(100), -- Open, Limited, EOI
  tender_value DECIMAL(15, 2),
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Dates
  published_date DATE,
  bid_submission_start_date TIMESTAMP,
  bid_submission_end_date TIMESTAMP,
  technical_bid_opening_date TIMESTAMP,
  financial_bid_opening_date TIMESTAMP,
  
  -- Location
  tender_location VARCHAR(255),
  state VARCHAR(100),
  region VARCHAR(100),
  
  -- Documents
  documents JSONB DEFAULT '[]',
  -- [{ name: 'NIT.pdf', url: 's3://...', size: 1024, uploaded_at: '...' }]
  
  -- Parsing Status
  parsing_status VARCHAR(50) DEFAULT 'pending', -- pending, in_progress, completed, failed
  parsed_data JSONB, -- Extracted structured data
  parsing_confidence DECIMAL(3, 2), -- 0.00 to 1.00
  
  -- Eligibility & Requirements
  eligibility_criteria TEXT,
  technical_requirements TEXT,
  special_conditions TEXT,
  
  -- Status & Tracking
  status VARCHAR(50) DEFAULT 'discovered', 
  -- discovered, evaluated, workspace_created, bid_in_progress, submitted, won, lost, abandoned
  
  match_score DECIMAL(3, 2), -- Relevance score based on keywords
  is_starred BOOLEAN DEFAULT false,
  tags TEXT[],
  
  -- Assignment
  assigned_to UUID REFERENCES users(id),
  assigned_at TIMESTAMP,
  
  -- Audit
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  deleted_at TIMESTAMP
);

CREATE INDEX idx_tenders_status ON tenders(status);
CREATE INDEX idx_tenders_submission_end ON tenders(bid_submission_end_date);
CREATE INDEX idx_tenders_buyer ON tenders(buyer_organization);
CREATE INDEX idx_tenders_category ON tenders(category);
CREATE INDEX idx_tenders_source ON tenders(source);
CREATE INDEX idx_tenders_match_score ON tenders(match_score DESC);
```

### 7. tender_projects (Per Tenant)

```sql
CREATE TABLE tender_projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tender_id UUID UNIQUE NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
  
  -- Project Info
  project_name VARCHAR(255) NOT NULL,
  project_code VARCHAR(100) UNIQUE,
  
  -- Team
  bid_manager_id UUID REFERENCES users(id),
  tech_lead_id UUID REFERENCES users(id),
  finance_lead_id UUID REFERENCES users(id),
  team_members UUID[], -- Array of user IDs
  
  -- Configuration
  bid_strategy_profile_id UUID REFERENCES bid_strategy_profiles(id),
  target_margin_percentage DECIMAL(5, 2),
  
  -- Status & Milestones
  status VARCHAR(50) DEFAULT 'initiated',
  -- initiated, requirements_review, boq_preparation, vendor_rfq, 
  -- pricing_finalization, document_assembly, ready_for_submission, submitted
  
  milestones JSONB DEFAULT '[]',
  -- [{ name: 'BOQ Finalization', due_date: '...', status: 'pending', completed_at: null }]
  
  -- Workspace Settings
  workspace_settings JSONB DEFAULT '{}',
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE INDEX idx_tender_projects_tender ON tender_projects(tender_id);
CREATE INDEX idx_tender_projects_status ON tender_projects(status);
```

### 8. project_tasks (Per Tenant)

```sql
CREATE TABLE project_tasks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id UUID NOT NULL REFERENCES tender_projects(id) ON DELETE CASCADE,
  
  title VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Assignment
  assigned_to UUID REFERENCES users(id),
  assigned_by UUID REFERENCES users(id),
  
  -- Priority & Status
  priority VARCHAR(20) DEFAULT 'medium', -- low, medium, high, urgent
  status VARCHAR(50) DEFAULT 'todo', -- todo, in_progress, review, completed
  
  -- Dates
  due_date TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  
  -- Dependencies
  depends_on UUID[], -- Array of task IDs that must complete first
  
  -- Attachments & Comments
  attachments JSONB DEFAULT '[]',
  comments JSONB DEFAULT '[]',
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_project_tasks_project ON project_tasks(project_id);
CREATE INDEX idx_project_tasks_assigned ON project_tasks(assigned_to);
CREATE INDEX idx_project_tasks_status ON project_tasks(status);
```

### 9. boq_items (Per Tenant)

```sql
CREATE TABLE boq_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
  
  -- Item Info
  item_number VARCHAR(50),
  description TEXT NOT NULL,
  specifications TEXT,
  hsn_code VARCHAR(20),
  
  -- Quantity
  quantity DECIMAL(12, 2) NOT NULL,
  unit VARCHAR(50) NOT NULL, -- nos, kg, liters, etc.
  
  -- Pricing
  suggested_rate DECIMAL(15, 2), -- AI-suggested rate
  suggested_rate_source VARCHAR(100), -- historical, oem_quote, market_index
  manual_rate DECIMAL(15, 2), -- User-overridden rate
  final_rate DECIMAL(15, 2), -- Actual rate used (manual or suggested)
  
  amount DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * COALESCE(final_rate, 0)) STORED,
  
  -- Tax
  gst_percentage DECIMAL(5, 2) DEFAULT 18.00,
  gst_amount DECIMAL(15, 2) GENERATED ALWAYS AS (amount * gst_percentage / 100) STORED,
  total_amount DECIMAL(15, 2) GENERATED ALWAYS AS (amount + (amount * gst_percentage / 100)) STORED,
  
  -- Product Mapping
  matched_product_id UUID REFERENCES products(id),
  matching_confidence DECIMAL(3, 2), -- 0.00 to 1.00
  
  -- Vendor Quotes
  selected_vendor_quote_id UUID, -- References vendor_quotes(id)
  
  -- Metadata
  notes TEXT,
  formula VARCHAR(500), -- Excel-style formula if calculated
  row_order INTEGER, -- Display order
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_boq_items_tender ON boq_items(tender_id);
CREATE INDEX idx_boq_items_product ON boq_items(matched_product_id);
CREATE INDEX idx_boq_items_order ON boq_items(tender_id, row_order);
```

### 10. products (Per Tenant)

```sql
CREATE TABLE products (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Product Info
  sku VARCHAR(100),
  product_name VARCHAR(255) NOT NULL,
  brand VARCHAR(100),
  model VARCHAR(100),
  
  -- OEM
  oem_vendor_id UUID REFERENCES oem_vendors(id),
  
  -- Specifications
  category VARCHAR(100),
  sub_category VARCHAR(100),
  specifications JSONB NOT NULL DEFAULT '{}',
  -- { "power": "1000W", "voltage": "220V", "dimensions": "10x20x30cm" }
  
  technical_description TEXT,
  hsn_code VARCHAR(20),
  
  -- Embedding for similarity search
  specification_embedding VECTOR(384), -- PostgreSQL pgvector extension
  
  -- Pricing
  list_price DECIMAL(15, 2),
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Availability
  lead_time_days INTEGER,
  stock_status VARCHAR(50), -- in_stock, out_of_stock, on_order
  
  -- Metadata
  images JSONB DEFAULT '[]',
  datasheets JSONB DEFAULT '[]',
  certifications JSONB DEFAULT '[]',
  
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_oem ON products(oem_vendor_id);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_sku ON products(sku);
-- For vector similarity search:
-- CREATE INDEX idx_products_embedding ON products USING ivfflat (specification_embedding vector_cosine_ops);
```
