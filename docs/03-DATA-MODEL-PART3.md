# HexaBid - Data Model (Part 3: ERP Modules)

## ERP Integration Overview

The ERP modules integrate with the tender lifecycle:
- **Won Tender** → Creates **Project** in Projects module
- **Project** → Generates **Sales Order** → **Invoices** → **Revenue Recognition**
- **BOQ Items** → **Purchase Orders** → **Inventory** tracking
- **Project Team** → Linked to **HRMS** employees

---

## Sales Module

### 26. sales_orders (Per Tenant)

```sql
CREATE TABLE sales_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Reference
  tender_id UUID REFERENCES tenders(id),
  project_id UUID REFERENCES erp_projects(id),
  
  -- Order Info
  order_number VARCHAR(100) UNIQUE NOT NULL,
  order_date DATE NOT NULL,
  
  -- Customer (Buyer)
  customer_name VARCHAR(255) NOT NULL,
  customer_organization VARCHAR(255),
  customer_gstin VARCHAR(20),
  customer_pan VARCHAR(20),
  
  -- Customer Address
  billing_address TEXT,
  shipping_address TEXT,
  
  -- Amounts
  subtotal DECIMAL(15, 2),
  tax_amount DECIMAL(15, 2),
  total_amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Payment Terms
  payment_terms VARCHAR(255),
  payment_due_date DATE,
  
  -- Delivery
  expected_delivery_date DATE,
  delivery_status VARCHAR(50) DEFAULT 'pending',
  -- pending, partial, completed
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft',
  -- draft, confirmed, in_progress, completed, cancelled
  
  -- Line Items stored in separate table
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sales_orders_tender ON sales_orders(tender_id);
CREATE INDEX idx_sales_orders_project ON sales_orders(project_id);
CREATE INDEX idx_sales_orders_status ON sales_orders(status);
CREATE INDEX idx_sales_orders_date ON sales_orders(order_date DESC);
```

### 27. sales_order_items (Per Tenant)

```sql
CREATE TABLE sales_order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  sales_order_id UUID NOT NULL REFERENCES sales_orders(id) ON DELETE CASCADE,
  boq_item_id UUID REFERENCES boq_items(id),
  product_id UUID REFERENCES products(id),
  
  -- Item Details
  description TEXT NOT NULL,
  hsn_code VARCHAR(20),
  
  quantity DECIMAL(12, 2) NOT NULL,
  unit VARCHAR(50) NOT NULL,
  
  unit_price DECIMAL(15, 2) NOT NULL,
  amount DECIMAL(15, 2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
  
  gst_percentage DECIMAL(5, 2) DEFAULT 18.00,
  gst_amount DECIMAL(15, 2) GENERATED ALWAYS AS (amount * gst_percentage / 100) STORED,
  total_amount DECIMAL(15, 2) GENERATED ALWAYS AS (amount + (amount * gst_percentage / 100)) STORED,
  
  -- Fulfillment
  quantity_fulfilled DECIMAL(12, 2) DEFAULT 0,
  fulfillment_status VARCHAR(50) DEFAULT 'pending',
  
  row_order INTEGER,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sales_order_items_order ON sales_order_items(sales_order_id);
```

### 28. invoices (Per Tenant)

```sql
CREATE TABLE invoices (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  sales_order_id UUID REFERENCES sales_orders(id),
  
  -- Invoice Info
  invoice_number VARCHAR(100) UNIQUE NOT NULL,
  invoice_date DATE NOT NULL,
  invoice_type VARCHAR(50) DEFAULT 'tax_invoice', -- tax_invoice, proforma, credit_note, debit_note
  
  -- Customer
  customer_name VARCHAR(255) NOT NULL,
  customer_gstin VARCHAR(20),
  billing_address TEXT,
  
  -- Amounts
  subtotal DECIMAL(15, 2),
  tax_amount DECIMAL(15, 2),
  total_amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Payment
  payment_status VARCHAR(50) DEFAULT 'unpaid',
  -- unpaid, partially_paid, paid, overdue
  payment_due_date DATE,
  amount_paid DECIMAL(15, 2) DEFAULT 0,
  amount_due DECIMAL(15, 2) GENERATED ALWAYS AS (total_amount - amount_paid) STORED,
  
  -- Document
  invoice_pdf_url TEXT,
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft', -- draft, sent, paid, cancelled
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sent_at TIMESTAMP,
  paid_at TIMESTAMP
);

CREATE INDEX idx_invoices_sales_order ON invoices(sales_order_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_invoices_payment_status ON invoices(payment_status);
CREATE INDEX idx_invoices_date ON invoices(invoice_date DESC);
```

### 29. invoice_items (Per Tenant)

```sql
CREATE TABLE invoice_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  invoice_id UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  sales_order_item_id UUID REFERENCES sales_order_items(id),
  
  description TEXT NOT NULL,
  hsn_code VARCHAR(20),
  
  quantity DECIMAL(12, 2) NOT NULL,
  unit VARCHAR(50),
  
  unit_price DECIMAL(15, 2) NOT NULL,
  amount DECIMAL(15, 2),
  
  gst_percentage DECIMAL(5, 2),
  gst_amount DECIMAL(15, 2),
  total_amount DECIMAL(15, 2),
  
  row_order INTEGER
);

CREATE INDEX idx_invoice_items_invoice ON invoice_items(invoice_id);
```

### 30. payments (Per Tenant)

```sql
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  invoice_id UUID REFERENCES invoices(id),
  sales_order_id UUID REFERENCES sales_orders(id),
  
  -- Payment Info
  payment_number VARCHAR(100) UNIQUE,
  payment_date DATE NOT NULL,
  
  amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Method
  payment_method VARCHAR(50), -- bank_transfer, cheque, cash, upi, card
  
  -- Transaction Details
  transaction_reference VARCHAR(255),
  bank_name VARCHAR(255),
  cheque_number VARCHAR(100),
  cheque_date DATE,
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending', -- pending, cleared, bounced, cancelled
  cleared_date DATE,
  
  notes TEXT,
  
  recorded_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_payments_invoice ON payments(invoice_id);
CREATE INDEX idx_payments_date ON payments(payment_date DESC);
```

---

## Purchase Module

### 31. purchase_orders (Per Tenant)

```sql
CREATE TABLE purchase_orders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Reference
  tender_id UUID REFERENCES tenders(id),
  sales_order_id UUID REFERENCES sales_orders(id),
  
  -- Vendor
  vendor_id UUID NOT NULL REFERENCES oem_vendors(id),
  vendor_quote_id UUID REFERENCES vendor_quotes(id),
  
  -- PO Info
  po_number VARCHAR(100) UNIQUE NOT NULL,
  po_date DATE NOT NULL,
  
  -- Delivery
  delivery_address TEXT,
  expected_delivery_date DATE,
  delivery_status VARCHAR(50) DEFAULT 'pending',
  
  -- Amounts
  subtotal DECIMAL(15, 2),
  tax_amount DECIMAL(15, 2),
  total_amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Payment Terms
  payment_terms VARCHAR(255),
  advance_percentage DECIMAL(5, 2),
  advance_amount DECIMAL(15, 2),
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft',
  -- draft, sent, acknowledged, in_transit, received, cancelled
  
  -- Documents
  po_pdf_url TEXT,
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  sent_at TIMESTAMP,
  received_at TIMESTAMP
);

CREATE INDEX idx_purchase_orders_vendor ON purchase_orders(vendor_id);
CREATE INDEX idx_purchase_orders_tender ON purchase_orders(tender_id);
CREATE INDEX idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX idx_purchase_orders_date ON purchase_orders(po_date DESC);
```

### 32. purchase_order_items (Per Tenant)

```sql
CREATE TABLE purchase_order_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  purchase_order_id UUID NOT NULL REFERENCES purchase_orders(id) ON DELETE CASCADE,
  product_id UUID REFERENCES products(id),
  boq_item_id UUID REFERENCES boq_items(id),
  
  description TEXT NOT NULL,
  hsn_code VARCHAR(20),
  
  quantity DECIMAL(12, 2) NOT NULL,
  unit VARCHAR(50),
  
  unit_price DECIMAL(15, 2) NOT NULL,
  amount DECIMAL(15, 2),
  
  gst_percentage DECIMAL(5, 2),
  gst_amount DECIMAL(15, 2),
  total_amount DECIMAL(15, 2),
  
  -- Receipt Tracking
  quantity_received DECIMAL(12, 2) DEFAULT 0,
  receipt_status VARCHAR(50) DEFAULT 'pending',
  
  row_order INTEGER
);

CREATE INDEX idx_purchase_order_items_po ON purchase_order_items(purchase_order_id);
```

### 33. goods_receipts (Per Tenant)

```sql
CREATE TABLE goods_receipts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  purchase_order_id UUID NOT NULL REFERENCES purchase_orders(id),
  
  -- Receipt Info
  receipt_number VARCHAR(100) UNIQUE NOT NULL,
  receipt_date DATE NOT NULL,
  
  -- Delivery Details
  delivered_by VARCHAR(255),
  vehicle_number VARCHAR(50),
  lr_number VARCHAR(100), -- Lorry Receipt
  
  -- Quality Check
  inspection_status VARCHAR(50) DEFAULT 'pending', -- pending, passed, failed, partial
  inspected_by UUID REFERENCES users(id),
  inspection_date DATE,
  inspection_notes TEXT,
  
  -- Items received (in separate table)
  
  status VARCHAR(50) DEFAULT 'received', -- received, inspected, accepted, rejected
  
  notes TEXT,
  received_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_goods_receipts_po ON goods_receipts(purchase_order_id);
CREATE INDEX idx_goods_receipts_date ON goods_receipts(receipt_date DESC);
```

### 34. goods_receipt_items (Per Tenant)

```sql
CREATE TABLE goods_receipt_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  goods_receipt_id UUID NOT NULL REFERENCES goods_receipts(id) ON DELETE CASCADE,
  purchase_order_item_id UUID NOT NULL REFERENCES purchase_order_items(id),
  
  quantity_received DECIMAL(12, 2) NOT NULL,
  quantity_accepted DECIMAL(12, 2),
  quantity_rejected DECIMAL(12, 2),
  
  rejection_reason TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_goods_receipt_items_receipt ON goods_receipt_items(goods_receipt_id);
```

---

## Inventory Module

### 35. warehouses (Per Tenant)

```sql
CREATE TABLE warehouses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  code VARCHAR(50) UNIQUE,
  
  -- Location
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  pincode VARCHAR(20),
  
  -- Contact
  manager_name VARCHAR(255),
  contact_phone VARCHAR(20),
  contact_email VARCHAR(255),
  
  -- Capacity
  total_capacity_sqft DECIMAL(10, 2),
  
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 36. inventory_items (Per Tenant)

```sql
CREATE TABLE inventory_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  product_id UUID NOT NULL REFERENCES products(id),
  warehouse_id UUID NOT NULL REFERENCES warehouses(id),
  
  -- Stock Levels
  quantity_on_hand DECIMAL(12, 2) DEFAULT 0,
  quantity_reserved DECIMAL(12, 2) DEFAULT 0, -- Reserved for sales orders
  quantity_available DECIMAL(12, 2) GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved) STORED,
  
  -- Reorder
  reorder_level DECIMAL(12, 2),
  reorder_quantity DECIMAL(12, 2),
  
  -- Costing
  unit_cost DECIMAL(15, 2), -- Weighted average cost
  total_value DECIMAL(15, 2) GENERATED ALWAYS AS (quantity_on_hand * unit_cost) STORED,
  
  -- Tracking
  last_stock_take_date DATE,
  last_movement_date TIMESTAMP,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(product_id, warehouse_id)
);

CREATE INDEX idx_inventory_items_product ON inventory_items(product_id);
CREATE INDEX idx_inventory_items_warehouse ON inventory_items(warehouse_id);
```

### 37. inventory_movements (Per Tenant)

```sql
CREATE TABLE inventory_movements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  product_id UUID NOT NULL REFERENCES products(id),
  warehouse_id UUID NOT NULL REFERENCES warehouses(id),
  
  -- Movement Type
  movement_type VARCHAR(50) NOT NULL,
  -- receipt, issue, transfer, adjustment, return
  
  -- Quantity
  quantity DECIMAL(12, 2) NOT NULL,
  unit VARCHAR(50),
  
  -- Direction
  direction VARCHAR(20) NOT NULL, -- in, out
  
  -- Reference
  reference_type VARCHAR(100), -- goods_receipt, sales_order, adjustment
  reference_id UUID,
  
  -- Before/After Snapshot
  quantity_before DECIMAL(12, 2),
  quantity_after DECIMAL(12, 2),
  
  -- Costing
  unit_cost DECIMAL(15, 2),
  total_cost DECIMAL(15, 2),
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_inventory_movements_product ON inventory_movements(product_id, created_at DESC);
CREATE INDEX idx_inventory_movements_warehouse ON inventory_movements(warehouse_id, created_at DESC);
CREATE INDEX idx_inventory_movements_reference ON inventory_movements(reference_type, reference_id);
```

---

## Projects Module

### 38. erp_projects (Per Tenant)

```sql
CREATE TABLE erp_projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Link to Tender
  tender_project_id UUID REFERENCES tender_projects(id),
  tender_id UUID REFERENCES tenders(id),
  sales_order_id UUID REFERENCES sales_orders(id),
  
  -- Project Info
  project_code VARCHAR(100) UNIQUE NOT NULL,
  project_name VARCHAR(255) NOT NULL,
  project_type VARCHAR(100), -- tender_execution, internal, maintenance
  
  -- Client
  client_name VARCHAR(255),
  client_organization VARCHAR(255),
  
  -- Dates
  start_date DATE,
  planned_end_date DATE,
  actual_end_date DATE,
  
  -- Budget
  budget_amount DECIMAL(15, 2),
  actual_cost DECIMAL(15, 2) DEFAULT 0,
  revenue DECIMAL(15, 2) DEFAULT 0,
  
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Team
  project_manager_id UUID REFERENCES users(id),
  team_member_ids UUID[],
  
  -- Status
  status VARCHAR(50) DEFAULT 'planned',
  -- planned, in_progress, on_hold, completed, cancelled
  completion_percentage DECIMAL(5, 2) DEFAULT 0,
  
  -- Location
  project_location VARCHAR(255),
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_erp_projects_tender ON erp_projects(tender_id);
CREATE INDEX idx_erp_projects_status ON erp_projects(status);
CREATE INDEX idx_erp_projects_manager ON erp_projects(project_manager_id);
```

### 39. project_expenses (Per Tenant)

```sql
CREATE TABLE project_expenses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  project_id UUID NOT NULL REFERENCES erp_projects(id) ON DELETE CASCADE,
  
  -- Expense Details
  expense_date DATE NOT NULL,
  expense_category VARCHAR(100), -- material, labor, travel, equipment, overhead
  description TEXT,
  
  amount DECIMAL(15, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Reference
  purchase_order_id UUID REFERENCES purchase_orders(id),
  invoice_number VARCHAR(100),
  
  -- Reimbursement
  is_reimbursable BOOLEAN DEFAULT false,
  reimbursed BOOLEAN DEFAULT false,
  reimbursed_date DATE,
  
  -- Approval
  approval_status VARCHAR(50) DEFAULT 'pending',
  approved_by UUID REFERENCES users(id),
  approved_at TIMESTAMP,
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_project_expenses_project ON project_expenses(project_id, expense_date DESC);
```

### 40. project_milestones (Per Tenant)

```sql
CREATE TABLE project_milestones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  project_id UUID NOT NULL REFERENCES erp_projects(id) ON DELETE CASCADE,
  
  milestone_name VARCHAR(255) NOT NULL,
  description TEXT,
  
  -- Dates
  planned_date DATE,
  actual_date DATE,
  
  -- Billing
  billing_percentage DECIMAL(5, 2), -- % of total project value
  billing_amount DECIMAL(15, 2),
  invoice_id UUID REFERENCES invoices(id),
  
  -- Status
  status VARCHAR(50) DEFAULT 'pending',
  -- pending, in_progress, completed, delayed
  
  completion_notes TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  completed_at TIMESTAMP
);

CREATE INDEX idx_project_milestones_project ON project_milestones(project_id);
```

---

## Accounting Module (Basic)

### 41. chart_of_accounts (Per Tenant)

```sql
CREATE TABLE chart_of_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  account_code VARCHAR(50) UNIQUE NOT NULL,
  account_name VARCHAR(255) NOT NULL,
  
  -- Account Type
  account_type VARCHAR(50) NOT NULL,
  -- asset, liability, equity, revenue, expense
  
  account_category VARCHAR(100),
  -- current_asset, fixed_asset, current_liability, long_term_liability, 
  -- operating_revenue, non_operating_revenue, operating_expense, etc.
  
  -- Hierarchy
  parent_account_id UUID REFERENCES chart_of_accounts(id),
  level INTEGER DEFAULT 1,
  
  -- Balance
  opening_balance DECIMAL(15, 2) DEFAULT 0,
  current_balance DECIMAL(15, 2) DEFAULT 0,
  
  currency VARCHAR(3) DEFAULT 'INR',
  
  is_active BOOLEAN DEFAULT true,
  is_system BOOLEAN DEFAULT false,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_chart_of_accounts_type ON chart_of_accounts(account_type);
CREATE INDEX idx_chart_of_accounts_parent ON chart_of_accounts(parent_account_id);
```

### 42. journal_entries (Per Tenant)

```sql
CREATE TABLE journal_entries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  entry_number VARCHAR(100) UNIQUE NOT NULL,
  entry_date DATE NOT NULL,
  
  entry_type VARCHAR(50) DEFAULT 'manual',
  -- manual, system_generated, opening_balance, closing, adjustment
  
  -- Reference
  reference_type VARCHAR(100), -- invoice, payment, purchase_order, salary
  reference_id UUID,
  
  description TEXT,
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft', -- draft, posted, voided
  posted_at TIMESTAMP,
  
  -- Audit
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  notes TEXT
);

CREATE INDEX idx_journal_entries_date ON journal_entries(entry_date DESC);
CREATE INDEX idx_journal_entries_reference ON journal_entries(reference_type, reference_id);
```

### 43. journal_entry_lines (Per Tenant)

```sql
CREATE TABLE journal_entry_lines (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  journal_entry_id UUID NOT NULL REFERENCES journal_entries(id) ON DELETE CASCADE,
  account_id UUID NOT NULL REFERENCES chart_of_accounts(id),
  
  -- Debit/Credit
  debit_amount DECIMAL(15, 2) DEFAULT 0,
  credit_amount DECIMAL(15, 2) DEFAULT 0,
  
  currency VARCHAR(3) DEFAULT 'INR',
  
  description TEXT,
  
  line_order INTEGER
);

CREATE INDEX idx_journal_entry_lines_entry ON journal_entry_lines(journal_entry_id);
CREATE INDEX idx_journal_entry_lines_account ON journal_entry_lines(account_id);

-- Constraint: Total debits must equal total credits
-- Enforced at application level
```

---

## HRMS Module

### 44. employees (Per Tenant)

```sql
CREATE TABLE employees (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Link to User (if they have system access)
  user_id UUID UNIQUE REFERENCES users(id),
  
  -- Personal Info
  employee_code VARCHAR(50) UNIQUE NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100),
  full_name VARCHAR(255) GENERATED ALWAYS AS (first_name || ' ' || COALESCE(last_name, '')) STORED,
  
  date_of_birth DATE,
  gender VARCHAR(20),
  
  -- Contact
  personal_email VARCHAR(255),
  work_email VARCHAR(255),
  mobile_phone VARCHAR(20),
  
  -- Address
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  country VARCHAR(100),
  pincode VARCHAR(20),
  
  -- Employment
  department VARCHAR(100),
  designation VARCHAR(100),
  employment_type VARCHAR(50), -- full_time, part_time, contract, intern
  
  date_of_joining DATE,
  date_of_leaving DATE,
  
  -- Reporting
  reports_to UUID REFERENCES employees(id),
  
  -- Compensation
  salary_amount DECIMAL(15, 2),
  salary_currency VARCHAR(3) DEFAULT 'INR',
  salary_frequency VARCHAR(50) DEFAULT 'monthly',
  
  -- Bank Details
  bank_name VARCHAR(255),
  bank_account_number VARCHAR(50),
  bank_ifsc VARCHAR(20),
  
  -- Statutory
  pan VARCHAR(20),
  aadhar VARCHAR(20),
  uan VARCHAR(20), -- PF UAN
  esic_number VARCHAR(20),
  
  -- Documents
  documents JSONB DEFAULT '[]',
  
  -- Status
  status VARCHAR(50) DEFAULT 'active', -- active, inactive, terminated, on_leave
  
  notes TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employees_code ON employees(employee_code);
CREATE INDEX idx_employees_user ON employees(user_id);
CREATE INDEX idx_employees_status ON employees(status);
CREATE INDEX idx_employees_department ON employees(department);
```

### 45. attendance (Per Tenant)

```sql
CREATE TABLE attendance (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  
  attendance_date DATE NOT NULL,
  
  -- Status
  status VARCHAR(50) NOT NULL,
  -- present, absent, half_day, on_leave, holiday, week_off
  
  -- Timing
  check_in_time TIME,
  check_out_time TIME,
  
  work_hours DECIMAL(4, 2), -- Calculated hours
  
  -- Leave Reference
  leave_request_id UUID REFERENCES leave_requests(id),
  
  remarks TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(employee_id, attendance_date)
);

CREATE INDEX idx_attendance_employee ON attendance(employee_id, attendance_date DESC);
CREATE INDEX idx_attendance_date ON attendance(attendance_date);
```

### 46. leave_requests (Per Tenant)

```sql
CREATE TABLE leave_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  
  -- Leave Details
  leave_type VARCHAR(50) NOT NULL, -- casual, sick, earned, unpaid
  from_date DATE NOT NULL,
  to_date DATE NOT NULL,
  total_days DECIMAL(3, 1), -- Can be half day (0.5)
  
  reason TEXT,
  
  -- Approval
  status VARCHAR(50) DEFAULT 'pending',
  -- pending, approved, rejected, cancelled
  
  approved_by UUID REFERENCES users(id),
  approval_date TIMESTAMP,
  approval_remarks TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_leave_requests_employee ON leave_requests(employee_id, from_date DESC);
CREATE INDEX idx_leave_requests_status ON leave_requests(status);
```

### 47. payroll (Per Tenant)

```sql
CREATE TABLE payroll (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  
  -- Period
  payroll_month INTEGER NOT NULL, -- 1-12
  payroll_year INTEGER NOT NULL,
  
  -- Earnings
  basic_salary DECIMAL(15, 2),
  hra DECIMAL(15, 2),
  other_allowances DECIMAL(15, 2),
  gross_salary DECIMAL(15, 2),
  
  -- Deductions
  pf_deduction DECIMAL(15, 2),
  esic_deduction DECIMAL(15, 2),
  tds_deduction DECIMAL(15, 2),
  other_deductions DECIMAL(15, 2),
  total_deductions DECIMAL(15, 2),
  
  -- Net
  net_salary DECIMAL(15, 2),
  
  -- Attendance
  days_worked DECIMAL(4, 1),
  days_absent DECIMAL(4, 1),
  days_on_leave DECIMAL(4, 1),
  
  -- Status
  status VARCHAR(50) DEFAULT 'draft', -- draft, processed, paid
  payment_date DATE,
  payment_reference VARCHAR(255),
  
  -- Payslip
  payslip_pdf_url TEXT,
  
  notes TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(employee_id, payroll_month, payroll_year)
);

CREATE INDEX idx_payroll_employee ON payroll(employee_id, payroll_year DESC, payroll_month DESC);
CREATE INDEX idx_payroll_period ON payroll(payroll_year, payroll_month);
```

### 48. recruitment (Per Tenant)

```sql
CREATE TABLE recruitment (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Position
  position_title VARCHAR(255) NOT NULL,
  department VARCHAR(100),
  required_skills TEXT[],
  
  -- Details
  job_description TEXT,
  qualifications TEXT,
  experience_required VARCHAR(100),
  
  -- Openings
  number_of_openings INTEGER DEFAULT 1,
  
  -- Compensation
  salary_range_min DECIMAL(15, 2),
  salary_range_max DECIMAL(15, 2),
  currency VARCHAR(3) DEFAULT 'INR',
  
  -- Status
  status VARCHAR(50) DEFAULT 'open',
  -- open, on_hold, closed, filled
  
  -- Posted
  posted_date DATE,
  closing_date DATE,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_recruitment_status ON recruitment(status);
```

### 49. job_applications (Per Tenant)

```sql
CREATE TABLE job_applications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  recruitment_id UUID NOT NULL REFERENCES recruitment(id) ON DELETE CASCADE,
  
  -- Candidate Info
  candidate_name VARCHAR(255) NOT NULL,
  candidate_email VARCHAR(255) NOT NULL,
  candidate_phone VARCHAR(20),
  
  -- Application
  resume_url TEXT,
  cover_letter TEXT,
  
  -- Experience
  total_experience_years DECIMAL(3, 1),
  current_ctc DECIMAL(15, 2),
  expected_ctc DECIMAL(15, 2),
  
  notice_period_days INTEGER,
  
  -- Status
  status VARCHAR(50) DEFAULT 'applied',
  -- applied, screening, interview_scheduled, interviewed, selected, rejected, offer_extended, joined
  
  -- Interview
  interview_date TIMESTAMP,
  interview_notes TEXT,
  interviewer_ids UUID[],
  
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_job_applications_recruitment ON job_applications(recruitment_id);
CREATE INDEX idx_job_applications_status ON job_applications(status);
```

---

## Summary

**Total Tables**: 49 (across shared + tenant schemas)

### Shared Schema (public): 2 tables
- tenants
- subscription_plans

### Per-Tenant Schema: 47 tables

**Core Tender System (25)**:
- users, roles, company_profile
- tenders, tender_projects, project_tasks
- boq_items, products, price_history
- oem_vendors, vendor_price_lists, vendor_quotes, rfq_requests
- document_templates, document_assembly_jobs
- compliance_checklists, compliance_answers, approvals
- communications, saved_searches, notifications
- bid_strategy_profiles, audit_logs

**ERP Modules (22)**:
- **Sales (6)**: sales_orders, sales_order_items, invoices, invoice_items, payments
- **Purchase (4)**: purchase_orders, purchase_order_items, goods_receipts, goods_receipt_items
- **Inventory (4)**: warehouses, inventory_items, inventory_movements
- **Projects (3)**: erp_projects, project_expenses, project_milestones
- **Accounting (3)**: chart_of_accounts, journal_entries, journal_entry_lines
- **HRMS (6)**: employees, attendance, leave_requests, payroll, recruitment, job_applications

---

**Next**: See `04-INFRASTRUCTURE.md` for Kubernetes and Terraform specifications.
