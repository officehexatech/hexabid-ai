# HexaBid - Multi-tenant Tender & ERP Platform

## 🚀 Complete Enterprise SaaS Platform

HexaBid is a comprehensive multi-tenant SaaS application for tender discovery, preparation, and complete ERP lifecycle management.

## 📋 What's Been Built

### ✅ Complete Architecture & Documentation
- **7 Comprehensive Documents** in `/app/docs/`
- Executive Summary
- System Architecture
- Complete Data Model (49 tables)
- Infrastructure Specifications (K8s, Terraform, Helm)
- API Specification (all endpoints)

### ✅ Backend (NestJS + TypeScript)
- **Complete project structure** with all 17 modules
- **Multi-tenant architecture** with tenant middleware
- **Authentication system** (OTP-based login with JWT)
- **16 Database entities** created
- **Tender module** fully functional (CRUD operations)
- **Module stubs** for all 17 features

**Modules**:
1. ✅ Auth (OTP login, JWT tokens)
2. ✅ Tender Management (complete)
3. 🔧 BOQ Module
4. 🔧 Product Catalog
5. 🔧 OEM/Vendor Management
6. 🔧 RFQ Module
7. 🔧 Document Assembly
8. 🔧 Compliance
9. 🔧 Workspace
10. 🔧 AI Assistant
11. 🔧 ERP - Sales
12. 🔧 ERP - Purchase
13. 🔧 ERP - Inventory
14. 🔧 ERP - Projects
15. 🔧 ERP - Accounting
16. 🔧 ERP - HRMS
17. 🔧 Analytics
18. 🔧 Notifications
19. 🔧 Admin

### ✅ Frontend (React + TypeScript)
- **Complete application structure**
- **Authentication UI** (OTP login flow)
- **Dashboard** with stats and recent tenders
- **Tenders page** with search and filters
- **Tender detail page**
- **Layout with sidebar navigation**
- **Stub pages** for all modules
- **Responsive design** with Tailwind CSS

### ✅ Infrastructure
- **Docker Compose** for local development
- **PostgreSQL** database
- **Redis** caching
- **MinIO** object storage
- **Elasticsearch** search engine
- **Database initialization** script

---

## 🏗️ Tech Stack

### Backend
- **Framework**: NestJS (Node.js + TypeScript)
- **Database**: PostgreSQL 14
- **Cache**: Redis
- **Search**: Elasticsearch
- **Queue**: Bull (Redis-based)
- **Auth**: JWT with OTP
- **ORM**: TypeORM

### Frontend
- **Framework**: React 18 + TypeScript
- **Routing**: React Router v6
- **State**: Zustand + React Query
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Forms**: React Hook Form + Zod

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Orchestration**: Kubernetes (production)
- **IaC**: Terraform
- **Package Management**: Helm

---

## 🚦 Quick Start

### Prerequisites
- Node.js 18+
- Docker & Docker Compose
- PostgreSQL (or use Docker)

### 1. Clone and Setup

```bash
# Install backend dependencies
cd backend-nestjs
npm install
cp .env.example .env

# Install frontend dependencies
cd ../frontend-react
npm install
```

### 2. Start Infrastructure (Option A: Docker)

```bash
# From root directory
docker-compose up -d

# Wait for services to be ready
docker-compose ps
```

### 3. Start Infrastructure (Option B: Local)

```bash
# Start PostgreSQL
psql -U postgres
CREATE DATABASE hexabid;

# Start Redis
redis-server
```

### 4. Run Database Migrations

```bash
cd backend-nestjs
npm run migration:run
```

### 5. Start Applications

```bash
# Terminal 1: Backend
cd backend-nestjs
npm run start:dev

# Terminal 2: Frontend
cd frontend-react
npm start
```

### 6. Access Application

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:3000/api
- **API Docs**: http://localhost:3000/api/docs

---

## 📦 Project Structure

```
hexabid/
├── docs/                          # Complete architecture docs
│   ├── 01-EXECUTIVE-SUMMARY.md
│   ├── 02-SYSTEM-ARCHITECTURE.md
│   ├── 03-DATA-MODEL-PART1.md
│   ├── 03-DATA-MODEL-PART2.md
│   ├── 03-DATA-MODEL-PART3.md
│   ├── 04-INFRASTRUCTURE.md
│   └── 05-API-SPECIFICATION.md
├── backend-nestjs/                # NestJS backend
│   ├── src/
│   │   ├── modules/              # 17 feature modules
│   │   │   ├── auth/
│   │   │   ├── tender/
│   │   │   ├── boq/
│   │   │   ├── product/
│   │   │   └── ...
│   │   ├── database/
│   │   │   └── entities/         # 16 database entities
│   │   ├── common/
│   │   │   ├── guards/
│   │   │   ├── decorators/
│   │   │   └── middleware/
│   │   ├── app.module.ts
│   │   └── main.ts
│   ├── package.json
│   ├── tsconfig.json
│   └── .env
├── frontend-react/                # React frontend
│   ├── src/
│   │   ├── pages/                # 11 pages
│   │   ├── components/           # Reusable components
│   │   ├── store/                # Zustand stores
│   │   ├── lib/                  # Utilities
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
├── scripts/
│   └── init-db.sql               # Database initialization
├── docker-compose.yml            # Local development setup
├── BUILD_STATUS.md               # Detailed build status
└── README.md                     # This file
```

---

## 🔐 Authentication Flow

1. User enters email
2. Backend generates 6-digit OTP
3. OTP sent via email (console log in dev mode)
4. User enters OTP
5. Backend verifies OTP
6. JWT tokens issued (access + refresh)
7. User authenticated

**Demo Login**: Use any email address. OTP will be printed in backend console.

---

## 🛠️ Development

### Backend Development

```bash
cd backend-nestjs

# Start dev server with hot reload
npm run start:dev

# Run tests
npm test

# Generate migration
npm run migration:generate -- src/database/migrations/MigrationName

# Run migrations
npm run migration:run

# Lint
npm run lint
```

### Frontend Development

```bash
cd frontend-react

# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test
```

---

## 📊 Database Schema

See `/app/docs/03-DATA-MODEL-*.md` for complete schema.

**Key Tables**:
- `tenants` - Multi-tenant configuration
- `users` - User accounts
- `roles` - RBAC roles
- `tenders` - Tender records
- `boq_items` - Bill of Quantities
- `products` - Product catalog
- `oem_vendors` - Vendor management
- `rfq_requests` - RFQ tracking
- `vendor_quotes` - Vendor quotations
- ... (49 tables total)

---

## 🔧 Configuration

### Backend Environment Variables

Edit `backend-nestjs/.env`:

```env
# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=hexabid
DATABASE_PASSWORD=hexabid123
DATABASE_NAME=hexabid

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-secret-key
JWT_EXPIRES_IN=1h

# Emergent LLM Key (for AI features)
EMERGENT_LLM_KEY=your-key

# Email (SendGrid)
SENDGRID_API_KEY=your-key

# Storage
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
```

### Frontend Environment Variables

Create `frontend-react/.env`:

```env
REACT_APP_API_URL=http://localhost:3000/api
```

---

## 📖 API Documentation

Swagger documentation available at:
- **Local**: http://localhost:3000/api/docs
- **Complete API spec**: `/app/docs/05-API-SPECIFICATION.md`

### Key Endpoints

```
POST   /api/auth/request-otp    # Request OTP
POST   /api/auth/verify-otp     # Verify OTP & login
GET    /api/tenders              # List tenders
POST   /api/tenders              # Create tender
GET    /api/tenders/:id          # Get tender details
PATCH  /api/tenders/:id          # Update tender
DELETE /api/tenders/:id          # Delete tender
```

---

## 🧪 Testing

```bash
# Backend unit tests
cd backend-nestjs
npm test

# Frontend tests
cd frontend-react
npm test

# E2E tests (to be implemented)
npm run test:e2e
```

---

## 🚀 Deployment

### Production Deployment

See `/app/docs/04-INFRASTRUCTURE.md` for complete deployment guide.

**Key Steps**:
1. Provision infrastructure using Terraform
2. Set up Kubernetes cluster
3. Configure Helm values
4. Deploy using Helm charts
5. Set up CI/CD pipelines
6. Configure monitoring (Prometheus + Grafana)

### Docker Deployment

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## 📝 Development Roadmap

### ✅ Phase 1: Foundation (Complete)
- [x] Project setup
- [x] Authentication system
- [x] Multi-tenant architecture
- [x] Database entities
- [x] Basic tender module
- [x] Frontend foundation

### 🔧 Phase 2: Core Features (In Progress)
- [ ] Complete BOQ module
- [ ] Product catalog with search
- [ ] OEM/Vendor management
- [ ] RFQ automation
- [ ] Document assembly
- [ ] Tender parsing (OCR + NLP)

### 📋 Phase 3: Advanced Features
- [ ] AI pricing engine
- [ ] AI chatbot assistant
- [ ] Workspace collaboration
- [ ] Compliance checklist
- [ ] Analytics dashboard

### 🏢 Phase 4: ERP Integration
- [ ] Sales module
- [ ] Purchase module
- [ ] Inventory management
- [ ] Project management
- [ ] Accounting basics
- [ ] HRMS basics

### 🔒 Phase 5: Production Readiness
- [ ] Security hardening
- [ ] Performance optimization
- [ ] Load testing
- [ ] Monitoring & alerting
- [ ] Documentation
- [ ] User training

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

---

## 📄 License

Proprietary - All rights reserved

---

## 📞 Support

For questions or support:
- Email: support@hexabid.in
- Documentation: `/app/docs/`
- API Docs: http://localhost:3000/api/docs

---

## 🎯 Next Steps

1. **Review Documentation**: Read `/app/docs/` for complete architecture
2. **Start Development**: Follow Quick Start guide above
3. **Implement Features**: Pick a module from the roadmap
4. **Test Thoroughly**: Write tests for new features
5. **Deploy**: Follow deployment guide in docs

---

**Built with ❤️ for enterprise tender management**
