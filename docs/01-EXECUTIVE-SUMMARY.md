# HexaBid - Executive Summary

## Project Overview

**HexaBid** is an enterprise-grade, multi-tenant SaaS platform for tender discovery, preparation, and complete ERP lifecycle management.

### Platform URL
hexabid.in

### Core Value Proposition
- **Automated Tender Discovery**: Ingest from Gem.gov.in and other portals
- **AI-Powered Processing**: OCR, NLP extraction, intelligent BOQ generation
- **Complete Tender Lifecycle**: From discovery to submission-ready packages
- **Integrated ERP**: Sales, Purchase, Inventory, Projects, Finance, HRMS
- **OEM Management**: RFQ automation, quote tracking, vendor communications
- **Document Assembly**: Template-based generation of submission packages
- **AI Assistant**: Chatbot for queries, data entry, and analytics

## Technical Stack

### Backend
- **Framework**: Node.js with NestJS
- **Language**: TypeScript
- **API**: RESTful + GraphQL (optional)

### Database & Storage
- **Primary DB**: PostgreSQL 14+ (multi-tenant isolation)
- **Cache**: Redis 7+
- **Search**: Elasticsearch 8+
- **Object Storage**: MinIO (S3-compatible)
- **Message Queue**: RabbitMQ / Bull (Redis-based)

### Frontend
- **Framework**: React 18+ with TypeScript
- **Styling**: Tailwind CSS + Shadcn UI
- **State Management**: Redux Toolkit / Zustand
- **Forms**: React Hook Form + Zod validation

### Infrastructure
- **Container Orchestration**: Kubernetes 1.28+
- **IaC**: Terraform
- **Package Manager**: Helm
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana + ELK Stack

### AI & ML
- **LLM**: Via Emergent LLM Key (OpenAI/Anthropic/Gemini)
- **OCR**: Tesseract + Cloud Vision API fallback
- **Embeddings**: Sentence Transformers for product matching
- **NLP**: spaCy + custom extractors

## Architecture Principles

### Multi-Tenancy
- **Isolation Level**: Database-per-schema (PostgreSQL schemas)
- **Tenant Routing**: Subdomain-based (tenant.hexabid.in)
- **Data Segregation**: Row-level security + application-layer enforcement

### Security
- **Authentication**: OTP via email (primary), optional 2FA
- **Authorization**: RBAC with fine-grained permissions
- **Encryption**: TLS 1.3 in transit, AES-256 at rest
- **Secrets**: HashiCorp Vault / Kubernetes Secrets
- **Compliance**: OWASP Top 10, GDPR-ready

### Scalability
- **Horizontal Scaling**: Stateless services, HPA in K8s
- **Caching Strategy**: Redis L1, PostgreSQL materialized views L2
- **Async Processing**: Background jobs for heavy tasks
- **CDN**: CloudFlare for static assets

## Module Overview

### Core Modules (17)
1. **Tenant & Company Management** - Multi-tenant onboarding, user management
2. **Tender Ingestion** - Automated scraping, manual upload, API integration
3. **Tender Parsing & NLP** - OCR, extraction, structured data
4. **Tender Workspace** - Collaborative project management
5. **BOQ & Costing** - Spreadsheet editor, pricing engine
6. **Product Catalog** - OEM database, technical matching
7. **OEM RFQ** - Email/WhatsApp automation, quote tracking
8. **Document Assembly** - Template merging, submission packages
9. **Compliance** - Checklist, approvals, audit trail
10. **Bid Price Engine** - AI suggestions, margin analysis
11. **Competitor Analysis** - MIS, pipeline, forecasting
12. **OCR & Intelligence** - Document processing pipeline
13. **AI Assistant** - Chatbot, data entry help
14. **ERP Suite** - Sales, Purchase, Inventory, Projects, Accounting, HRMS
15. **Notifications** - Email, in-app, WhatsApp alerts
16. **Integrations** - Storage, communication, payment gateways
17. **Admin & Billing** - Super admin, subscription management

## Deployment Model

### Environments
- **Development**: Local Docker Compose
- **Staging**: Kubernetes cluster (minimal resources)
- **Production**: Multi-region Kubernetes with HA

### Deployment Strategy
- **Blue-Green**: Zero-downtime deployments
- **Canary**: Gradual rollout for critical updates
- **Rollback**: Automated on health check failures

## Performance Targets

- **API Response**: p95 < 300ms for CRUD, < 1s for complex queries
- **Search**: < 200ms for typical tender searches
- **Concurrent Users**: 10,000+ per tenant cluster
- **Tenant Capacity**: 1,000+ tenants (initial), 10,000+ (scaling plan)
- **Uptime SLA**: 99.9% (43.8 min downtime/month)

## Project Phases

### Phase 1: Foundation (Weeks 1-4)
- Infrastructure setup
- Multi-tenant architecture
- Authentication & RBAC
- Basic tender ingestion

### Phase 2: Core Features (Weeks 5-10)
- Tender parsing & NLP
- BOQ editor & workspace
- Product catalog
- Document assembly

### Phase 3: Automation (Weeks 11-16)
- OEM RFQ flows
- AI pricing engine
- AI assistant/chatbot
- Notifications

### Phase 4: ERP Integration (Weeks 17-22)
- Sales, Purchase, Inventory
- Projects & Accounting
- HRMS basics

### Phase 5: Hardening (Weeks 23-28)
- Security audit
- Performance optimization
- Documentation
- Production rollout

## Success Metrics

- **Technical**: All modules functional with sample data, >80% test coverage
- **Performance**: Meets SLA targets under load testing
- **Security**: Passes OWASP scan, pen test cleared
- **Deployment**: Successful K8s deployment with monitoring
- **Handover**: Complete documentation, knowledge transfer sessions

## Team Composition (Recommended)

- **Backend Engineers**: 3-4 (NestJS, PostgreSQL, integrations)
- **Frontend Engineers**: 2-3 (React, UI/UX)
- **DevOps Engineer**: 1-2 (K8s, Terraform, CI/CD)
- **ML/AI Engineer**: 1 (NLP, pricing models, chatbot)
- **QA Engineer**: 1-2 (automated testing, security)
- **Project Manager**: 1

**Total**: 9-13 person-months for MVP, 24-36 for complete system

## Risk Register

### High Risk
1. **Tender Parsing Accuracy** - Mitigation: Hybrid approach (auto + manual correction)
2. **Multi-tenant Data Isolation** - Mitigation: Schema-per-tenant + row-level security
3. **AI Cost Management** - Mitigation: Caching, batch processing, usage limits

### Medium Risk
4. **Gem.gov.in API Changes** - Mitigation: Scraper fallback, change detection
5. **Scale at 1000+ Tenants** - Mitigation: Horizontal scaling, database sharding plan
6. **Integration Failures** - Mitigation: Retry logic, fallback modes, alerting

### Low Risk
7. **Third-party Service Outages** - Mitigation: Graceful degradation, status pages

## Acceptance Criteria

✅ Multi-tenant isolation verified (security testing)
✅ Complete tender flow demonstrated (ingestion → submission package)
✅ All 17 modules functional with sample data
✅ Email OTP login working
✅ At least 3 integrations working (Gem.gov.in, storage, WhatsApp)
✅ >80% test coverage with passing CI/CD
✅ Security scan passed (critical issues resolved)
✅ K8s deployment successful with monitoring
✅ Documentation complete (deployment, API, user manuals)
✅ 2 tenant pilot runs completed successfully

## Next Steps

1. Review and approve architecture
2. Provision infrastructure (cloud accounts, K8s cluster)
3. Begin Phase 1 implementation
4. Weekly progress reviews
5. Staging deployment at milestone completions
6. Production rollout post Phase 5
