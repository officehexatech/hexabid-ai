# HexaBid - API Specification

## Base URL

```
Production: https://hexabid.in/api
Staging: https://staging.hexabid.in/api
Development: http://localhost:3000/api
```

## Authentication

All API endpoints (except auth endpoints) require authentication via JWT token.

```http
Authorization: Bearer <jwt_token>
X-Tenant-ID: <tenant_id>  # Auto-extracted from subdomain
```

---

## Authentication APIs

### POST /auth/request-otp

Request OTP for email-based login.

**Request**:
```json
{
  "email": "user@example.com"
}
```

**Response** (200):
```json
{
  "success": true,
  "message": "OTP sent to your email",
  "expiresIn": 300
}
```

### POST /auth/verify-otp

Verify OTP and get JWT tokens.

**Request**:
```json
{
  "email": "user@example.com",
  "otp": "123456"
}
```

**Response** (200):
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "John Doe",
    "role": "BidManager"
  },
  "accessToken": "jwt_access_token",
  "refreshToken": "jwt_refresh_token",
  "expiresIn": 3600
}
```

### POST /auth/refresh

Refresh access token.

**Request**:
```json
{
  "refreshToken": "jwt_refresh_token"
}
```

**Response** (200):
```json
{
  "accessToken": "new_jwt_access_token",
  "expiresIn": 3600
}
```

---

## Tender APIs

### GET /tenders

List tenders with search and filters.

**Query Parameters**:
- `page` (number, default: 1)
- `limit` (number, default: 20)
- `search` (string): Full-text search
- `status` (string): Filter by status
- `category` (string): Filter by category
- `minValue` (number): Minimum tender value
- `maxValue` (number): Maximum tender value
- `region` (string): Filter by region
- `source` (string): gem, manual_upload, etc.
- `sortBy` (string, default: 'created_at')
- `sortOrder` (string, default: 'desc')

**Response** (200):
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "title": "Supply of Laptops",
      "tenderNumber": "GEM/2024/B/1234567",
      "buyerOrganization": "Ministry of Education",
      "category": "IT Hardware",
      "tenderValue": 5000000,
      "currency": "INR",
      "bidSubmissionEndDate": "2024-03-15T17:00:00Z",
      "status": "discovered",
      "matchScore": 0.85,
      "isStarred": false,
      "createdAt": "2024-01-10T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

### GET /tenders/:id

Get tender details.

**Response** (200):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "source": "gem",
    "externalTenderId": "GEM/2024/B/1234567",
    "title": "Supply of Laptops for Schools",
    "tenderNumber": "GEM/2024/B/1234567",
    "buyerOrganization": "Ministry of Education",
    "buyerDepartment": "Digital Education Division",
    "category": "IT Hardware",
    "subCategory": "Laptops",
    "tenderType": "Open",
    "tenderValue": 5000000,
    "currency": "INR",
    "publishedDate": "2024-01-10",
    "bidSubmissionStartDate": "2024-01-15T09:00:00Z",
    "bidSubmissionEndDate": "2024-03-15T17:00:00Z",
    "technicalBidOpeningDate": "2024-03-16T11:00:00Z",
    "tenderLocation": "Delhi",
    "state": "Delhi",
    "documents": [
      {
        "name": "NIT.pdf",
        "url": "https://s3.../NIT.pdf",
        "size": 204800,
        "uploadedAt": "2024-01-10T10:30:00Z"
      }
    ],
    "parsingStatus": "completed",
    "parsingConfidence": 0.92,
    "eligibilityCriteria": "Registered company with 5+ years experience",
    "status": "workspace_created",
    "matchScore": 0.85,
    "tags": ["electronics", "education"],
    "assignedTo": {
      "id": "uuid",
      "fullName": "Jane Smith"
    },
    "createdAt": "2024-01-10T10:30:00Z",
    "updatedAt": "2024-01-12T14:20:00Z"
  }
}
```

### POST /tenders

Create tender (manual upload/paste URL).

**Request**:
```json
{
  "source": "manual_upload",
  "sourceUrl": "https://eprocure.gov.in/...",
  "title": "Supply of Office Equipment",
  "tenderNumber": "ABC/2024/001",
  "buyerOrganization": "XYZ Corporation",
  "category": "Office Supplies",
  "tenderValue": 1000000,
  "bidSubmissionEndDate": "2024-04-30T17:00:00Z",
  "documents": [
    {
      "name": "tender_notice.pdf",
      "url": "https://s3.../document.pdf"
    }
  ]
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Supply of Office Equipment",
    "status": "discovered",
    "parsingStatus": "pending"
  }
}
```

### PATCH /tenders/:id

Update tender details.

**Request**:
```json
{
  "status": "evaluated",
  "assignedTo": "user_uuid",
  "tags": ["priority", "q2-2024"]
}
```

### DELETE /tenders/:id

Soft delete tender.

---

## Tender Project (Workspace) APIs

### POST /tenders/:id/workspace

Create workspace for tender.

**Request**:
```json
{
  "projectName": "Ministry of Education - Laptop Supply Bid",
  "bidManagerId": "uuid",
  "techLeadId": "uuid",
  "financeLeadId": "uuid",
  "targetMarginPercentage": 12.5
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "projectCode": "PRJ-2024-001",
    "projectName": "Ministry of Education - Laptop Supply Bid",
    "status": "initiated"
  }
}
```

### GET /tender-projects/:id

Get workspace details.

### GET /tender-projects/:id/tasks

List tasks for workspace.

### POST /tender-projects/:id/tasks

Create task.

**Request**:
```json
{
  "title": "Finalize BOQ pricing",
  "description": "Review all line items and confirm rates",
  "assignedTo": "uuid",
  "priority": "high",
  "dueDate": "2024-03-10T17:00:00Z"
}
```

---

## BOQ APIs

### GET /tenders/:id/boq

Get BOQ for tender.

**Response** (200):
```json
{
  "success": true,
  "data": {
    "tenderId": "uuid",
    "items": [
      {
        "id": "uuid",
        "itemNumber": "1",
        "description": "Dell Latitude 5420 Laptop",
        "specifications": "14\" FHD, Intel i5-11th Gen, 8GB RAM, 256GB SSD",
        "quantity": 500,
        "unit": "nos",
        "suggestedRate": 48000,
        "manualRate": null,
        "finalRate": 48000,
        "amount": 24000000,
        "gstPercentage": 18,
        "gstAmount": 4320000,
        "totalAmount": 28320000,
        "matchedProduct": {
          "id": "uuid",
          "productName": "Dell Latitude 5420",
          "confidence": 0.95
        },
        "notes": "Check for bulk discount"
      }
    ],
    "summary": {
      "totalItems": 10,
      "subtotal": 50000000,
      "totalGst": 9000000,
      "grandTotal": 59000000
    }
  }
}
```

### POST /tenders/:id/boq/items

Add BOQ item.

### PATCH /tenders/:id/boq/items/:itemId

Update BOQ item.

**Request**:
```json
{
  "manualRate": 47500,
  "notes": "Negotiated rate with vendor"
}
```

### POST /tenders/:id/boq/generate

Auto-generate BOQ from parsed tender.

---

## Product Catalog APIs

### GET /products

List products with search.

**Query Parameters**:
- `search`: Product name/SKU
- `category`: Filter by category
- `oemId`: Filter by OEM vendor

### GET /products/:id

Get product details.

### POST /products

Add product to catalog.

**Request**:
```json
{
  "sku": "DELL-LAT-5420",
  "productName": "Dell Latitude 5420 Laptop",
  "brand": "Dell",
  "model": "Latitude 5420",
  "oemVendorId": "uuid",
  "category": "Laptops",
  "specifications": {
    "processor": "Intel Core i5-11th Gen",
    "ram": "8GB DDR4",
    "storage": "256GB SSD",
    "display": "14-inch FHD",
    "os": "Windows 11 Pro"
  },
  "listPrice": 50000,
  "leadTimeDays": 15
}
```

### POST /products/:id/match

Find similar products for BOQ item.

**Request**:
```json
{
  "description": "Laptop with Intel i5, 8GB RAM, 256GB SSD",
  "specifications": "14-inch display, Windows OS"
}
```

**Response** (200):
```json
{
  "success": true,
  "matches": [
    {
      "product": {
        "id": "uuid",
        "productName": "Dell Latitude 5420",
        "sku": "DELL-LAT-5420"
      },
      "confidence": 0.95,
      "matchingAttributes": ["processor", "ram", "storage"]
    }
  ]
}
```

---

## OEM/Vendor APIs

### GET /oem-vendors

List OEM vendors.

### POST /oem-vendors

Add OEM vendor.

### GET /oem-vendors/:id/quotes

Get quotes from vendor.

---

## RFQ APIs

### POST /rfq/create

Create RFQ request.

**Request**:
```json
{
  "tenderId": "uuid",
  "projectId": "uuid",
  "subject": "RFQ for Laptop Supply - Ministry of Education Tender",
  "message": "Please provide your best quote for the following items...",
  "boqItemIds": ["uuid1", "uuid2"],
  "vendorIds": ["uuid1", "uuid2", "uuid3"],
  "responseDeadline": "2024-03-05T17:00:00Z",
  "sendVia": ["email", "whatsapp"]
}
```

**Response** (201):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "rfqNumber": "RFQ-2024-001",
    "status": "sent",
    "totalSent": 3
  }
}
```

### GET /rfq/:id

Get RFQ details.

### POST /rfq/:id/quotes

Submit vendor quote (can be used by vendor or internally).

---

## Document Assembly APIs

### GET /document-templates

List document templates.

### POST /document-templates

Upload document template.

### POST /tenders/:id/generate-document

Generate submission package.

**Request**:
```json
{
  "templateIds": ["uuid1", "uuid2", "uuid3"],
  "outputFormat": "pdf",
  "outputStructure": "zip_with_folders",
  "mergeData": {
    "companyName": "ABC Corp",
    "authorizedSignatory": "John Doe",
    "date": "2024-03-14"
  }
}
```

**Response** (202):
```json
{
  "success": true,
  "jobId": "uuid",
  "status": "queued",
  "estimatedTime": 120
}
```

### GET /document-jobs/:id

Check document generation status.

**Response** (200):
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "status": "completed",
    "progressPercentage": 100,
    "outputFileUrl": "https://s3.../submission_package.zip",
    "completedAt": "2024-03-14T10:35:00Z"
  }
}
```

---

## Compliance APIs

### GET /tenders/:id/compliance

Get compliance checklist.

### POST /tenders/:id/compliance/answers

Submit compliance answer.

**Request**:
```json
{
  "itemId": "uuid",
  "answer": "yes",
  "proofDocuments": [
    {
      "name": "EMD_receipt.pdf",
      "url": "https://s3.../emd.pdf"
    }
  ],
  "remarks": "EMD paid via NEFT on 2024-01-15"
}
```

---

## Approval APIs

### POST /approvals/request

Request approval.

**Request**:
```json
{
  "projectId": "uuid",
  "approvalType": "boq_final",
  "title": "Final BOQ Approval - Ministry of Education Tender",
  "description": "Please approve the finalized BOQ with total value of Rs 5.9 Cr",
  "approvalLevels": [
    {
      "level": 1,
      "approverId": "uuid",
      "approverName": "Finance Head"
    },
    {
      "level": 2,
      "approverId": "uuid",
      "approverName": "CEO"
    }
  ]
}
```

### POST /approvals/:id/action

Approve or reject.

**Request**:
```json
{
  "action": "approve",
  "comments": "Approved. Ensure timely submission."
}
```

---

## AI Assistant APIs

### POST /ai/chat

Chat with AI assistant.

**Request**:
```json
{
  "message": "Summarize the eligibility criteria for tender GEM/2024/B/1234567",
  "context": {
    "tenderId": "uuid"
  }
}
```

**Response** (200):
```json
{
  "success": true,
  "response": "The eligibility criteria for this tender includes: 1) Registered company with valid GSTIN, 2) Minimum 5 years of experience in IT hardware supply, 3) Annual turnover of at least Rs 10 Cr...",
  "sources": [
    {
      "type": "tender_document",
      "name": "NIT.pdf",
      "page": 3
    }
  ]
}
```

### POST /ai/suggest-pricing

Get AI pricing suggestions.

**Request**:
```json
{
  "boqItemId": "uuid",
  "tenderId": "uuid"
}
```

**Response** (200):
```json
{
  "success": true,
  "suggestion": {
    "suggestedRate": 48000,
    "confidence": 0.87,
    "reasoning": [
      {
        "source": "historical_price",
        "value": 47500,
        "weight": 0.4,
        "context": "Similar tender in 2023"
      },
      {
        "source": "oem_quote",
        "value": 48500,
        "weight": 0.6,
        "context": "Recent quote from Dell India"
      }
    ],
    "priceRange": {
      "min": 46000,
      "max": 52000
    }
  }
}
```

---

## Analytics & MIS APIs

### GET /analytics/dashboard

Get dashboard metrics.

**Response** (200):
```json
{
  "success": true,
  "data": {
    "tendersPipeline": {
      "discovered": 45,
      "evaluated": 12,
      "bidInProgress": 8,
      "submitted": 15,
      "won": 5,
      "lost": 3
    },
    "revenueForecas

t": 125000000,
    "avgWinRate": 62.5,
    "activeProjects": 8,
    "pendingApprovals": 3
  }
}
```

### GET /analytics/tender-trends

Get tender trends.

### GET /analytics/vendor-performance

Get vendor performance metrics.

---

## ERP APIs

### Sales Orders

#### GET /erp/sales/orders
#### POST /erp/sales/orders
#### GET /erp/sales/orders/:id

### Invoices

#### GET /erp/sales/invoices
#### POST /erp/sales/invoices
#### GET /erp/sales/invoices/:id
#### POST /erp/sales/invoices/:id/send

### Purchase Orders

#### GET /erp/purchase/orders
#### POST /erp/purchase/orders
#### GET /erp/purchase/orders/:id

### Inventory

#### GET /erp/inventory/items
#### GET /erp/inventory/movements
#### POST /erp/inventory/adjustments

### Projects

#### GET /erp/projects
#### POST /erp/projects
#### GET /erp/projects/:id
#### GET /erp/projects/:id/expenses

### HRMS

#### GET /erp/hrms/employees
#### POST /erp/hrms/employees
#### GET /erp/hrms/attendance
#### POST /erp/hrms/leave-requests

---

## Notifications APIs

### GET /notifications

Get user notifications.

### PATCH /notifications/:id/read

Mark as read.

### GET /notifications/settings

Get notification preferences.

### PATCH /notifications/settings

Update preferences.

---

## Admin APIs

### Tenant Management (Super Admin)

#### GET /admin/tenants
#### POST /admin/tenants
#### PATCH /admin/tenants/:id
#### GET /admin/tenants/:id/usage

### User Management (Tenant Admin)

#### GET /admin/users
#### POST /admin/users
#### PATCH /admin/users/:id
#### DELETE /admin/users/:id

### Role Management

#### GET /admin/roles
#### POST /admin/roles
#### PATCH /admin/roles/:id

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  }
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions"
  }
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  }
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "requestId": "req-123456"
  }
}
```

---

## Rate Limiting

- **Default**: 1000 requests per hour per user
- **Auth endpoints**: 10 requests per 15 minutes per IP
- **Document generation**: 50 requests per hour per tenant

Headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1641024000
```

---

## Pagination

All list endpoints support pagination.

**Query Parameters**:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response Headers**:
```
X-Total-Count: 150
X-Page: 1
X-Per-Page: 20
X-Total-Pages: 8
```

---

## Webhooks

### Available Events

- `tender.discovered`
- `tender.workspace_created`
- `boq.generated`
- `rfq.sent`
- `vendor_quote.received`
- `document.generated`
- `approval.requested`
- `approval.approved`
- `tender.submitted`
- `tender.won`
- `tender.lost`

### Webhook Payload

```json
{
  "event": "tender.discovered",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "tenderId": "uuid",
    "title": "Supply of Laptops",
    "matchScore": 0.85
  }
}
```

---

**Complete OpenAPI 3.0 specification**: See `/docs/openapi.yaml`
