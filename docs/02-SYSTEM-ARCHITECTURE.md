# HexaBid - System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer / CDN                      │
│                      (CloudFlare / AWS ALB)                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ├─────────────────────────────────────────┐
                         │                                         │
                         ▼                                         ▼
         ┌───────────────────────────┐              ┌──────────────────────┐
         │   Frontend (React SPA)    │              │   Admin Portal       │
         │   - Multi-tenant UI       │              │   - Super Admin      │
         │   - Responsive Design     │              │   - Tenant Admin     │
         └───────────┬───────────────┘              └──────────┬───────────┘
                     │                                         │
                     └─────────────┬───────────────────────────┘
                                   │
                                   ▼
                     ┌─────────────────────────────┐
                     │   API Gateway / Ingress     │
                     │   - Tenant Routing          │
                     │   - Rate Limiting           │
                     │   - Authentication          │
                     └─────────────┬───────────────┘
                                   │
        ┏━━━━━━━━━━━━━━━━━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━┓
        ┃          Kubernetes Cluster (Application Layer)      ┃
        ┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
        ┃                                                       ┃
        ┃  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ ┃
        ┃  │   API Server │  │ Tender Engine│  │ AI Service│ ┃
        ┃  │   (NestJS)   │  │   (Workers)  │  │  (LLM)    │ ┃
        ┃  │              │  │              │  │           │ ┃
        ┃  │ - REST APIs  │  │ - Scraping   │  │ - NLP     │ ┃
        ┃  │ - GraphQL    │  │ - Parsing    │  │ - OCR     │ ┃
        ┃  │ - WebSocket  │  │ - BOQ Gen    │  │ - Chatbot │ ┃
        ┃  └──────┬───────┘  └──────┬───────┘  └─────┬─────┘ ┃
        ┃         │                  │                │       ┃
        ┃  ┌──────┴──────────────────┴────────────────┴────┐ ┃
        ┃  │           Message Queue (RabbitMQ/Bull)        │ ┃
        ┃  └──────┬──────────────────┬────────────────┬─────┘ ┃
        ┃         │                  │                │       ┃
        ┃  ┌──────┴───────┐  ┌──────┴───────┐  ┌─────┴─────┐ ┃
        ┃  │ Email Worker │  │  Doc Worker  │  │OEM Worker │ ┃
        ┃  │              │  │              │  │           │ ┃
        ┃  │ - Notif      │  │ - PDF Gen    │  │ - RFQ     │ ┃
        ┃  │ - OTP        │  │ - Merge      │  │ - Quotes  │ ┃
        ┃  └──────────────┘  └──────────────┘  └───────────┘ ┃
        ┃                                                       ┃
        ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐        ┌──────────────────┐       ┌───────────────┐
│  PostgreSQL   │        │  Elasticsearch   │       │     Redis     │
│  (Multi-DB)   │        │  (Search/Index)  │       │   (Cache +    │
│               │        │                  │       │    Queue)     │
│ - Tenant DBs  │        │ - Tender Search  │       │               │
│ - Shared Meta │        │ - Full Text      │       │ - Sessions    │
│ - Replication │        │ - Analytics      │       │ - Job Queue   │
└───────────────┘        └──────────────────┘       └───────────────┘
        │                                                     │
        │                 ┌──────────────────┐               │
        └─────────────────┤   MinIO / S3     │───────────────┘
                          │ (Object Storage) │
                          │                  │
                          │ - Documents      │
                          │ - Templates      │
                          │ - Attachments    │
                          └──────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    External Integrations                         │
├─────────────────────────────────────────────────────────────────┤
│ Gem.gov.in API │ WhatsApp (Twilio) │ Email (SendGrid/SES)       │
│ Google Drive   │ OneDrive          │ Payment (Razorpay/Stripe)  │
│ DocuSign       │ Tally/QuickBooks  │ OCR (Cloud Vision)         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                  Monitoring & Observability                      │
├─────────────────────────────────────────────────────────────────┤
│ Prometheus │ Grafana │ ELK/EFK Stack │ Jaeger (Tracing)         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. API Gateway Layer

**Responsibilities:**
- Tenant identification and routing
- Request authentication and validation
- Rate limiting per tenant/user
- Request/response logging
- SSL termination

**Technology:** Kubernetes Ingress Controller (NGINX) + Custom middleware

**Tenant Routing Strategy:**
```
tenant1.hexabid.in → Route to API with X-Tenant-ID: tenant1
tenant2.hexabid.in → Route to API with X-Tenant-ID: tenant2
hexabid.in/admin   → Super Admin portal
```

### 2. API Server (NestJS)

**Structure:**
```
src/
├── modules/
│   ├── auth/              # Authentication & Authorization
│   ├── tenants/           # Tenant management
│   ├── tenders/           # Tender CRUD operations
│   ├── boq/               # BOQ management
│   ├── products/          # Product catalog
│   ├── oem/               # OEM & vendor management
│   ├── documents/         # Document assembly
│   ├── compliance/        # Compliance checklist
│   ├── workspace/         # Project workspace
│   ├── pricing/           # Pricing engine
│   ├── erp/
│   │   ├── sales/
│   │   ├── purchase/
│   │   ├── inventory/
│   │   ├── projects/
│   │   ├── accounting/
│   │   └── hrms/
│   ├── notifications/     # Alert system
│   ├── integrations/      # External services
│   └── analytics/         # MIS & reporting
├── common/
│   ├── guards/            # Auth guards
│   ├── interceptors/      # Logging, transformation
│   ├── filters/           # Exception handling
│   ├── decorators/        # Custom decorators
│   └── middleware/        # Tenant context
├── config/                # Configuration management
└── database/
    ├── migrations/        # DB schema versions
    ├── seeds/             # Sample data
    └── entities/          # TypeORM entities
```

**Key Features:**
- **Dependency Injection**: NestJS IoC container
- **Validation**: Class-validator for DTOs
- **ORM**: TypeORM with PostgreSQL
- **API Docs**: Swagger/OpenAPI auto-generated
- **Caching**: Redis-based decorators
- **Background Jobs**: Bull queues

### 3. Tender Processing Engine (Workers)

**Workers:**

#### 3.1 Scraper Worker
- Scheduled jobs (cron) for Gem.gov.in
- Configurable portal connectors
- Change detection and alerting
- Retry logic with exponential backoff

#### 3.2 Parser Worker
- OCR pipeline (Tesseract primary, Cloud Vision fallback)
- NLP extraction (spaCy + custom models)
- BOQ table extraction
- Structured data validation

#### 3.3 BOQ Generator
- Auto-generate from parsed data
- Formula calculation engine
- Historical price lookup
- Margin application

### 4. AI Services

#### 4.1 NLP Service
```typescript
// Capabilities:
- Entity extraction (dates, amounts, specifications)
- Classification (tender categories)
- Similarity matching (product recommendations)
- Summarization (tender briefs)
```

#### 4.2 Pricing Engine
```typescript
// Inputs:
- Historical price data
- OEM quotes
- Market indices
- Competitor intelligence
- Margin rules

// Output:
- Per-line rate suggestions
- Confidence scores
- Explanation/reasoning
```

#### 4.3 AI Chatbot
```typescript
// Features:
- Context-aware responses (tenant data)
- Query tender information
- Generate draft documents
- Explain MIS reports
- Data entry assistance
```

**LLM Integration:** Via Emergent LLM Key (supports OpenAI, Anthropic, Gemini)

### 5. Database Architecture

#### Multi-Tenant Strategy: Schema-per-Tenant

```sql
-- Shared schema: public
CREATE TABLE public.tenants (
  id UUID PRIMARY KEY,
  subdomain VARCHAR(100) UNIQUE,
  company_name VARCHAR(255),
  subscription_plan VARCHAR(50),
  status VARCHAR(20),
  created_at TIMESTAMP
);

-- Per-tenant schema
CREATE SCHEMA tenant_abc123;

-- Tenant tables
CREATE TABLE tenant_abc123.users (...);
CREATE TABLE tenant_abc123.tenders (...);
CREATE TABLE tenant_abc123.boq_items (...);
-- ... all tenant-specific tables
```

**Benefits:**
- Strong data isolation
- Easy backup/restore per tenant
- Schema evolution flexibility
- Query performance (no tenant_id filtering)

**Connection Management:**
- Connection pool per schema
- Middleware sets search_path based on tenant
- ORM context switching

#### Key Tables (Per Tenant Schema)

See `03-DATA-MODEL.md` for complete schema.

### 6. Caching Strategy

#### L1: Redis Cache
```
- User sessions: 24 hours
- Tender search results: 15 minutes
- Product catalog: 1 hour
- OEM price lists: 6 hours
- API rate limit counters: 1 minute windows
- Background job status: Until completion
```

#### L2: Application Cache
```
- Tenant configuration: In-memory (invalidate on update)
- User permissions: In-memory (invalidate on role change)
```

#### L3: Database Cache
```
- Materialized views for analytics
- Refresh strategy: Incremental (hourly)
```

### 7. Message Queue Architecture

**Queue Types:**

```typescript
// High Priority Queue
- OTP emails (immediate)
- Critical notifications
- Real-time updates

// Standard Queue
- Tender scraping
- Document generation
- Email notifications
- RFQ sends

// Low Priority Queue  
- Analytics processing
- Report generation
- Data cleanup tasks
```

**Technology:** Bull (Redis-backed) for Node.js simplicity

**Job Configuration:**
```typescript
{
  attempts: 3,
  backoff: {
    type: 'exponential',
    delay: 2000
  },
  removeOnComplete: 100, // Keep last 100
  removeOnFail: false    // Keep failures for debugging
}
```

### 8. Search Architecture (Elasticsearch)

**Indices:**

```
tenders_v1              # Main tender index
products_v1             # Product catalog
oem_vendors_v1          # OEM/vendor directory
documents_v1            # Document content (OCR text)
audit_logs_v1           # Audit trail (time-series)
```

**Indexing Pipeline:**
```
PostgreSQL (Source) 
  → Change Data Capture (Debezium/Logical Replication)
  → Kafka/RabbitMQ
  → Elasticsearch Bulk Indexer
  → Elasticsearch
```

**Search Features:**
- Full-text search with relevance scoring
- Fuzzy matching for typos
- Faceted search (filters)
- Aggregations for analytics
- Geo-search for regional tenders

### 9. Object Storage (MinIO / S3)

**Bucket Structure:**
```
hexabid-documents/
  ├── {tenant_id}/
  │   ├── tenders/
  │   │   └── {tender_id}/
  │   │       ├── original/      # Uploaded PDFs
  │   │       ├── parsed/        # Extracted text/JSON
  │   │       └── attachments/   # Supporting docs
  │   ├── templates/
  │   │   └── {template_id}.docx
  │   ├── generated/
  │   │   └── {job_id}/
  │   │       └── submission_package.zip
  │   └── oem_quotes/
  │       └── {quote_id}.pdf
  └── shared/                    # Shared assets
      └── logos/
```

**Access Control:**
- Pre-signed URLs (time-limited)
- Tenant-based path restrictions
- Encryption at rest (AES-256)

### 10. Security Architecture

#### Authentication Flow

```
1. User enters email → Backend generates 6-digit OTP
2. OTP sent via email (SendGrid/SES)
3. OTP stored in Redis (5 min TTL, max 3 attempts)
4. User submits OTP → Verified against Redis
5. JWT token issued (access + refresh)
6. Subsequent requests use JWT (Bearer token)
```

#### Authorization (RBAC)

```typescript
// Permission model
Role → Permissions → Resources

// Example:
BidManager → [
  'tender:read',
  'tender:write',
  'boq:read',
  'boq:write',
  'oem:read',
  'document:generate'
]

// Enforcement:
@UseGuards(JwtAuthGuard, RolesGuard)
@RequirePermissions('tender:write')
async createTender(@CurrentUser() user, @Body() dto) {
  // Tenant context auto-injected
}
```

#### Encryption

- **In Transit**: TLS 1.3 (all communications)
- **At Rest**: 
  - PostgreSQL: Transparent Data Encryption (TDE)
  - MinIO: Server-side encryption (SSE)
  - Sensitive fields: Application-layer encryption (AES-256-GCM)

#### Audit Logging

```typescript
AuditLog {
  id: UUID
  tenant_id: UUID
  user_id: UUID
  action: string        // 'tender:created', 'boq:updated'
  resource_type: string
  resource_id: string
  changes: JSONB        // Old/new values
  ip_address: string
  user_agent: string
  timestamp: DateTime
}
```

All write operations automatically logged.

### 11. Monitoring & Observability

#### Metrics (Prometheus)

```yaml
# Application Metrics
- http_requests_total (counter)
- http_request_duration_seconds (histogram)
- active_connections (gauge)
- background_jobs_processed (counter)
- cache_hit_rate (gauge)

# Business Metrics
- tenders_ingested_total
- boq_generated_total
- documents_assembled_total
- ai_chatbot_queries

# Infrastructure Metrics
- node_cpu_usage
- node_memory_usage
- postgres_connection_pool
- redis_memory_usage
```

#### Logging (ELK Stack)

```
Application Logs → Fluent Bit → Elasticsearch → Kibana

Log Format (JSON):
{
  "timestamp": "2025-01-15T10:30:00Z",
  "level": "info",
  "service": "api-server",
  "tenant_id": "abc123",
  "user_id": "user456",
  "trace_id": "xyz789",
  "message": "Tender created",
  "context": { "tender_id": "tender123" }
}
```

#### Tracing (Jaeger)

- Distributed tracing for request flows
- End-to-end visibility (API → Workers → Database)
- Performance bottleneck identification

#### Alerting Rules

```yaml
# Critical
- API error rate > 5% (5 min window)
- Database connection pool exhausted
- Worker queue size > 10,000
- Disk usage > 85%

# Warning
- API p95 latency > 500ms
- Cache hit rate < 70%
- Failed background jobs > 10/hour
```

### 12. Deployment Architecture

See `04-INFRASTRUCTURE.md` for K8s and Terraform details.

## Scalability Considerations

### Horizontal Scaling

- **API Servers**: Stateless, auto-scale based on CPU/memory
- **Workers**: Scale based on queue depth
- **Database**: Read replicas for read-heavy workloads
- **Elasticsearch**: Cluster with multiple data nodes

### Vertical Scaling

- **PostgreSQL**: Scale up primary (CPU/RAM/IOPS)
- **Redis**: Scale up for larger cache

### Sharding Strategy (Future)

When single PostgreSQL instance limits reached:

```
Shard by tenant_id hash:
- Shard 1: Tenants 0-999
- Shard 2: Tenants 1000-1999
- ...

Router service: Maps tenant → shard
```

## Disaster Recovery

### Backup Strategy

- **PostgreSQL**: Daily full backups + WAL archiving (PITR)
- **Elasticsearch**: Daily snapshots to S3
- **MinIO**: Cross-region replication
- **Retention**: 30 days

### Recovery Procedures

- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 15 minutes
- **Failover**: Automated to replica region

## Compliance & Privacy

### GDPR Considerations

- **Right to Access**: API endpoint for user data export
- **Right to Erasure**: Soft delete with cleanup job
- **Data Portability**: Export in JSON/CSV format
- **Consent Management**: Explicit opt-in for communications

### Data Residency

- Tenant can specify data region (India/EU/US)
- Provision K8s cluster in specified region
- Ensure data never crosses boundaries

## Technology Choices - Rationale

### Why NestJS?
- Enterprise-grade architecture (DI, modularity)
- TypeScript for type safety
- Excellent ecosystem (TypeORM, Bull, Swagger)
- Scalable and maintainable

### Why PostgreSQL?
- ACID compliance for financial data
- JSON support for flexible schemas
- Schema-per-tenant for isolation
- Mature replication and backup tools

### Why Elasticsearch?
- Best-in-class full-text search
- Aggregations for analytics
- Scales horizontally
- Real-time indexing

### Why Redis?
- Fastest caching layer
- Native support for Bull queues
- Pub/Sub for real-time features
- Simple and reliable

### Why Kubernetes?
- Industry standard for orchestration
- Multi-cloud portability
- Rich ecosystem (Helm, operators)
- Auto-scaling and self-healing
