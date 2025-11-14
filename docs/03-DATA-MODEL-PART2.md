# HexaBid - Data Model (Part 2: OEM, Documents, ERP)

## OEM & Vendor Management

### 11. oem_vendors (Per Tenant)

```sql
CREATE TABLE oem_vendors (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Company Info
  company_name VARCHAR(255) NOT NULL,
  vendor_type VARCHAR(50), -- oem, distributor, manufacturer, reseller
  
  -- Contact
  primary_contact_name VARCHAR(255),
  primary_contact_email VARCHAR(255),
  primary_contact_phone VARCHAR(20),
  
  -- Additional Contacts
  contacts JSONB DEFAULT '[]',
  -- [{ name: '...', email: '...', phone: '...', designation: '...' }]
  
  -- Address
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100) DEFAULT 'India',
  pincode VARCHAR(20),
  
  -- Business Details
  gstin VARCHAR(20),
  pan VARCHAR(20),
  website VARCHAR(255),
  
  -- Performance
  rating DECIMAL(2, 1) CHECK (rating >= 0 AND rating <= 5),
  total_rfqs_sent INTEGER DEFAULT 0,
  total_quotes_received INTEGER DEFAULT 0,
  response_rate DECIMAL(5, 2) GENERATED ALWAYS AS (
    CASE WHEN total_rfqs_sent > 0 
    THEN (total_quotes_received::DECIMAL / total_rfqs_sent * 100) 
    ELSE 0 END
  ) STORED,
  
  avg_response_time_hours INTEGER,
  
  -- Payment Terms
  payment_terms VARCHAR(100), -- Net 30, Net 60, etc.
  credit_limit DECIMAL(15, 2),
  
  -- Metadata
  categories TEXT[], -- Categories they supply
  tags TEXT[],
  notes TEXT,
  
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_oem_vendors_name ON oem_vendors(company_name);
CREATE INDEX idx_oem_vendors_active ON oem_vendors(is_active);
```

### 12. vendor_price_lists (Per Tenant)

```sql
CREATE TABLE vendor_price_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  vendor_id UUID NOT NULL REFERENCES oem_vendors(id) ON DELETE CASCADE,
  
  -- Price List Info
  name VARCHAR(255) NOT NULL,
  version VARCHAR(50),
  effective_from DATE,
  effective_to DATE,
  
  -- Document
  document_url TEXT, -- S3 URL to uploaded price list
  document_type VARCHAR(50), -- pdf, xlsx, csv
  
  -- Parsed Data
  items JSONB,
  -- [{ sku: '...', product_name: '...', unit_price: 100, currency: 'INR', ... }]
  
  parsing_status VARCHAR(50) DEFAULT 'pending',
  
  is_current BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vendor_price_lists_vendor ON vendor_price_lists(vendor_id);
CREATE INDEX idx_vendor_price_lists_current ON vendor_price_lists(vendor_id, is_current);
```

### 13. vendor_quotes (Per Tenant)

```sql
CREATE TABLE vendor_quotes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
  vendor_id UUID NOT NULL REFERENCES oem_vendors(id),
  rfq_id UUID REFERENCES rfq_requests(id),
  
  -- Quote Info
  quote_number VARCHAR(100),
  quote_date DATE,
  valid_until DATE,
  
  -- Pricing
  currency VARCHAR(3) DEFAULT 'INR',
  total_amount DECIMAL(15, 2),
  
  -- Line Items
  line_items JSONB NOT NULL DEFAULT '[]',
  -- [{
  --   boq_item_id: 'uuid',
  --   description: '...',
  --   quantity: 10,
  --   unit: 'nos',
  --   unit_price: 100,
  --   total: 1000,
  --   gst: 18,
  --   delivery_time_days: 15
  -- }]
  
  -- Terms
  payment_terms VARCHAR(100),
  delivery_terms VARCHAR(255),
  warranty_terms VARCHAR(255),
  
  -- Document
  quote_document_url TEXT,
  
  -- Status
  status VARCHAR(50) DEFAULT 'received', -- received, under_review, accepted, rejected
  
  -- Notes
  internal_notes TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vendor_quotes_tender ON vendor_quotes(tender_id);
CREATE INDEX idx_vendor_quotes_vendor ON vendor_quotes(vendor_id);
CREATE INDEX idx_vendor_quotes_rfq ON vendor_quotes(rfq_id);
```

### 14. rfq_requests (Per Tenant)

```sql
CREATE TABLE rfq_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
  project_id UUID REFERENCES tender_projects(id),
  
  -- RFQ Details
  rfq_number VARCHAR(100) UNIQUE,
  subject VARCHAR(255),
  message TEXT,
  
  -- Items Requested
  boq_item_ids UUID[], -- Array of BOQ items included in this RFQ
  
  -- Recipients
  vendor_ids UUID[], -- Array of vendor IDs
  
  -- Dates
  response_deadline TIMESTAMP,
  
  -- Communication
  sent_via VARCHAR(50), -- email, whatsapp, both
  email_status JSONB DEFAULT '{}', -- { vendor_id: 'sent' | 'delivered' | 'failed' }
  whatsapp_status JSONB DEFAULT '{}',
  
  -- Responses
  total_sent INTEGER DEFAULT 0,
  total_responses INTEGER DEFAULT 0,
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft', -- draft, sent, in_progress, closed
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sent_at TIMESTAMP,
  closed_at TIMESTAMP
);

CREATE INDEX idx_rfq_requests_tender ON rfq_requests(tender_id);
CREATE INDEX idx_rfq_requests_status ON rfq_requests(status);
```

## Document Management

### 15. document_templates (Per Tenant)

```sql
CREATE TABLE document_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Template Info
  name VARCHAR(255) NOT NULL,
  template_type VARCHAR(100), -- cover_letter, technical_spec, financial_bid, compliance
  description TEXT,
  
  -- File
  file_url TEXT NOT NULL, -- S3 URL to .docx template
  file_size INTEGER,
  
  -- Merge Fields
  merge_fields JSONB DEFAULT '[]',
  -- [{ field: '{{company_name}}', description: 'Legal company name', type: 'text' }]
  
  -- Usage
  category VARCHAR(100),
  is_default BOOLEAN DEFAULT false,
  usage_count INTEGER DEFAULT 0,
  
  -- Version
  version VARCHAR(50) DEFAULT '1.0',
  
  is_active BOOLEAN DEFAULT true,
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_document_templates_type ON document_templates(template_type);
```

### 16. document_assembly_jobs (Per Tenant)

```sql
CREATE TABLE document_assembly_jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
  project_id UUID REFERENCES tender_projects(id),
  
  -- Job Configuration
  job_name VARCHAR(255),
  template_ids UUID[], -- Array of template IDs to merge
  
  -- Merge Data
  merge_data JSONB NOT NULL,
  -- All variables needed for template merging
  
  -- Output Configuration
  output_format VARCHAR(50) DEFAULT 'pdf', -- pdf, docx, both
  output_structure VARCHAR(100), -- single_file, zip_with_folders
  naming_convention VARCHAR(255),
  
  -- Status
  status VARCHAR(50) DEFAULT 'queued', -- queued, processing, completed, failed
  progress_percentage INTEGER DEFAULT 0,
  error_message TEXT,
  
  -- Output
  output_file_url TEXT, -- S3 URL to generated document/zip
  output_file_size INTEGER,
  
  -- Timestamps
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  started_at TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE INDEX idx_document_assembly_tender ON document_assembly_jobs(tender_id);
CREATE INDEX idx_document_assembly_status ON document_assembly_jobs(status);
```

## Compliance & Approvals

### 17. compliance_checklists (Per Tenant)

```sql
CREATE TABLE compliance_checklists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Template or Tender-specific
  is_template BOOLEAN DEFAULT false,
  template_name VARCHAR(255),
  
  tender_id UUID REFERENCES tenders(id) ON DELETE CASCADE,
  
  -- Checklist Items
  items JSONB NOT NULL DEFAULT '[]',
  -- [{
  --   id: 'uuid',
  --   question: 'EMD submitted?',
  --   requirement: 'Rs 50,000',
  --   type: 'yes_no' | 'text' | 'file_upload',
  --   is_mandatory: true,
  --   section: 'Financial'
  -- }]
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 18. compliance_answers (Per Tenant)

```sql
CREATE TABLE compliance_answers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  checklist_id UUID NOT NULL REFERENCES compliance_checklists(id) ON DELETE CASCADE,
  tender_id UUID NOT NULL REFERENCES tenders(id) ON DELETE CASCADE,
  item_id UUID NOT NULL, -- ID of item in checklist JSONB
  
  -- Answer
  answer TEXT,
  answer_type VARCHAR(50), -- yes/no, text, file
  
  -- Proof Documents
  proof_documents JSONB DEFAULT '[]',
  -- [{ name: 'EMD.pdf', url: 's3://...', uploaded_at: '...' }]
  
  -- Compliance Status
  is_compliant BOOLEAN,
  remarks TEXT,
  
  -- Audit
  answered_by UUID REFERENCES users(id),
  answered_at TIMESTAMP,
  verified_by UUID REFERENCES users(id),
  verified_at TIMESTAMP,
  
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_compliance_answers_tender ON compliance_answers(tender_id);
CREATE INDEX idx_compliance_answers_checklist ON compliance_answers(checklist_id);
```

### 19. approvals (Per Tenant)

```sql
CREATE TABLE approvals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  project_id UUID NOT NULL REFERENCES tender_projects(id) ON DELETE CASCADE,
  
  -- Approval Request
  approval_type VARCHAR(100) NOT NULL, -- boq_final, pricing_final, document_submission
  title VARCHAR(255),
  description TEXT,
  
  -- Multi-level Approval
  approval_levels JSONB NOT NULL,
  -- [{
  --   level: 1,
  --   approver_id: 'uuid',
  --   status: 'pending' | 'approved' | 'rejected',
  --   comments: '...',
  --   actioned_at: '...'
  -- }]
  
  current_level INTEGER DEFAULT 1,
  
  -- Overall Status
  status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected, cancelled
  
  -- Attachments
  attachments JSONB DEFAULT '[]',
  
  requested_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE INDEX idx_approvals_project ON approvals(project_id);
CREATE INDEX idx_approvals_status ON approvals(status);
```

## Communications

### 20. communications (Per Tenant)

```sql
CREATE TABLE communications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Context
  tender_id UUID REFERENCES tenders(id) ON DELETE CASCADE,
  vendor_id UUID REFERENCES oem_vendors(id),
  rfq_id UUID REFERENCES rfq_requests(id),
  
  -- Communication Details
  channel VARCHAR(50) NOT NULL, -- email, whatsapp, phone, in_person
  direction VARCHAR(20), -- inbound, outbound
  
  -- Sender/Receiver
  from_contact VARCHAR(255),
  to_contact VARCHAR(255),
  cc_contacts TEXT[],
  
  -- Content
  subject VARCHAR(500),
  body TEXT,
  
  -- Attachments
  attachments JSONB DEFAULT '[]',
  
  -- Status (for outbound)
  status VARCHAR(50), -- sent, delivered, failed, read
  
  -- External IDs
  email_message_id VARCHAR(255),
  whatsapp_message_id VARCHAR(255),
  
  -- Thread
  thread_id UUID, -- Group related messages
  in_reply_to UUID REFERENCES communications(id),
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_communications_tender ON communications(tender_id);
CREATE INDEX idx_communications_vendor ON communications(vendor_id);
CREATE INDEX idx_communications_rfq ON communications(rfq_id);
CREATE INDEX idx_communications_thread ON communications(thread_id);
```

## Pricing & History

### 21. price_history (Per Tenant)

```sql
CREATE TABLE price_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Product Reference
  product_id UUID REFERENCES products(id),
  
  -- Tender Context
  tender_id UUID REFERENCES tenders(id),
  boq_item_id UUID REFERENCES boq_items(id),
  
  -- Price Details
  price DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'INR',
  quantity DECIMAL(12, 2),
  unit VARCHAR(50),
  
  -- Source
  source VARCHAR(100), -- tender_win, vendor_quote, market_rate, manual_entry
  vendor_id UUID REFERENCES oem_vendors(id),
  
  -- Date
  price_date DATE NOT NULL,
  
  -- Metadata
  notes TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_price_history_product ON price_history(product_id, price_date DESC);
CREATE INDEX idx_price_history_tender ON price_history(tender_id);
```

### 22. bid_strategy_profiles (Per Tenant)

```sql
CREATE TABLE bid_strategy_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Margin Rules
  default_margin_percentage DECIMAL(5, 2),
  min_margin_percentage DECIMAL(5, 2),
  
  -- Category-specific Margins
  category_margins JSONB DEFAULT '{}',
  -- { "Electronics": 15, "Electrical": 12, ... }
  
  -- Pricing Strategy
  pricing_strategy VARCHAR(100), -- aggressive, competitive, premium
  
  -- Rules
  rules JSONB DEFAULT '[]',
  -- [{
  --   condition: 'tender_value > 1000000',
  --   margin: 10,
  --   apply_to: 'all' | 'category'
  -- }]
  
  is_default BOOLEAN DEFAULT false,
  is_active BOOLEAN DEFAULT true,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Notifications

### 23. notifications (Per Tenant)

```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  -- Notification Details
  type VARCHAR(100) NOT NULL, 
  -- tender_match, rfq_response, task_assigned, approval_request, deadline_reminder
  
  title VARCHAR(255) NOT NULL,
  message TEXT,
  
  -- Context
  related_resource_type VARCHAR(100), -- tender, task, approval, rfq
  related_resource_id UUID,
  
  -- Delivery
  channels VARCHAR(50)[], -- ['in_app', 'email', 'whatsapp']
  
  -- Status
  is_read BOOLEAN DEFAULT false,
  read_at TIMESTAMP,
  
  -- Action
  action_url TEXT,
  action_label VARCHAR(100),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user ON notifications(user_id, is_read, created_at DESC);
CREATE INDEX idx_notifications_type ON notifications(type);
```

### 24. saved_searches (Per Tenant)

```sql
CREATE TABLE saved_searches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  name VARCHAR(255) NOT NULL,
  
  -- Search Criteria
  filters JSONB NOT NULL,
  -- {
  --   keywords: ['laptop', 'computer'],
  --   category: 'IT Hardware',
  --   min_value: 100000,
  --   max_value: 5000000,
  --   regions: ['Delhi', 'Mumbai']
  -- }
  
  -- Alert Settings
  enable_alerts BOOLEAN DEFAULT true,
  alert_frequency VARCHAR(50) DEFAULT 'real_time', -- real_time, daily, weekly
  last_alerted_at TIMESTAMP,
  
  -- Stats
  match_count INTEGER DEFAULT 0,
  last_match_at TIMESTAMP,
  
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_saved_searches_user ON saved_searches(user_id);
CREATE INDEX idx_saved_searches_active ON saved_searches(is_active, enable_alerts);
```

## Audit Logs

### 25. audit_logs (Per Tenant)

```sql
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Who
  user_id UUID REFERENCES users(id),
  user_email VARCHAR(255),
  
  -- What
  action VARCHAR(100) NOT NULL, -- create, update, delete, approve, reject
  resource_type VARCHAR(100) NOT NULL, -- tender, boq_item, user, etc.
  resource_id UUID,
  
  -- Changes
  old_values JSONB,
  new_values JSONB,
  
  -- Where
  ip_address VARCHAR(45),
  user_agent TEXT,
  
  -- When
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id, created_at DESC);
CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(created_at DESC);
```

---

## Next: ERP Tables

See `03-DATA-MODEL-PART3.md` for ERP module tables (Sales, Purchase, Inventory, Projects, Accounting, HRMS).
