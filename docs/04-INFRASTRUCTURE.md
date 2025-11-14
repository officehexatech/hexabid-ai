# HexaBid - Infrastructure & Deployment

## Infrastructure Overview

### Target Cloud Providers
- **Primary**: AWS (Amazon Web Services)
- **Alternative**: GCP (Google Cloud Platform) / Azure
- **On-Premise**: Kubernetes on bare metal (optional)

### Infrastructure Components

```
┌─────────────────────────────────────────────────────────────────┐
│                        AWS Cloud (Region: ap-south-1)                   │
└───────────────────────────────┬─────────────────────────────────┘
                                 │
                 ┌────────────────┴────────────────┐
                 │   VPC (10.0.0.0/16)     │
                 └──────────┬───────────────────┘
                            │
       ┌────────────────┼────────────────┐
       │                │                │
       ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│Public Subnet  │  │Private Subnet│  │Database Subnet│
│(10.0.1.0/24) │  │(10.0.2.0/24) │  │(10.0.3.0/24) │
│               │  │               │  │               │
│ - NAT Gateway │  │ - EKS Nodes   │  │ - RDS         │
│ - ALB         │  │ - App Pods    │  │ - ElastiCache │
│               │  │               │  │               │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Terraform Infrastructure Code

### Directory Structure

```
terraform/
├── environments/
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── terraform.tfvars
│   └── production/
│       ├── main.tf
│       ├── variables.tf
│       └── terraform.tfvars
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── eks/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── elasticache/
│   ├── s3/
│   └── elasticsearch/
└── README.md
```

### Key Terraform Modules

See `/terraform` directory in project for complete implementation.

**Highlights**:
- **VPC Module**: Creates VPC with public/private/database subnets across 3 AZs
- **EKS Module**: Provisions managed Kubernetes cluster with node groups
- **RDS Module**: PostgreSQL 14 with multi-AZ, automated backups
- **ElastiCache Module**: Redis cluster for caching
- **S3 Module**: Object storage buckets with lifecycle policies
- **Elasticsearch Module**: AWS Elasticsearch Service (OpenSearch)

---

## Kubernetes Architecture

### Cluster Configuration

**Control Plane**: AWS EKS Managed
**Node Groups**:
- **Application Nodes**: t3.xlarge (4 vCPU, 16 GB RAM) - Auto-scaling 3-10 nodes
- **Worker Nodes**: t3.large (2 vCPU, 8 GB RAM) - Auto-scaling 2-5 nodes

### Namespaces

```yaml
# Namespace structure
namespaces:
  - hexabid-prod          # Production application
  - hexabid-staging       # Staging environment
  - hexabid-system        # System services (monitoring, logging)
  - cert-manager          # SSL certificate management
  - ingress-nginx         # Ingress controller
```

---

## Helm Charts

### Directory Structure

```
helm/
├── hexabid/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── values-staging.yaml
│   ├── values-production.yaml
│   └── templates/
│       ├── deployment-api.yaml
│       ├── deployment-worker.yaml
│       ├── deployment-frontend.yaml
│       ├── service-api.yaml
│       ├── service-frontend.yaml
│       ├── ingress.yaml
│       ├── configmap.yaml
│       ├── secrets.yaml
│       ├── hpa.yaml              # Horizontal Pod Autoscaler
│       ├── pdb.yaml              # Pod Disruption Budget
│       └── cronjob-scraper.yaml  # Tender scraping jobs
└── README.md
```

### Sample Helm Values (Production)

```yaml
# values-production.yaml
replicaCount:
  api: 3
  worker: 2
  frontend: 2

image:
  api:
    repository: hexabid/api
    tag: "1.0.0"
    pullPolicy: IfNotPresent
  worker:
    repository: hexabid/worker
    tag: "1.0.0"
  frontend:
    repository: hexabid/frontend
    tag: "1.0.0"

resources:
  api:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "2000m"
  worker:
    requests:
      memory: "1Gi"
      cpu: "1000m"
    limits:
      memory: "4Gi"
      cpu: "2000m"

autoscaling:
  api:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
  worker:
    enabled: true
    minReplicas: 2
    maxReplicas: 8
    targetCPUUtilizationPercentage: 80

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/rate-limit: "100"
  hosts:
    - host: hexabid.in
      paths:
        - path: /
          pathType: Prefix
          backend: frontend
        - path: /api
          pathType: Prefix
          backend: api
    - host: "*.hexabid.in"
      paths:
        - path: /
          pathType: Prefix
          backend: frontend
  tls:
    - secretName: hexabid-tls
      hosts:
        - hexabid.in
        - "*.hexabid.in"

postgresql:
  enabled: false  # Using external RDS
  external:
    host: hexabid-prod.cluster-xxx.ap-south-1.rds.amazonaws.com
    port: 5432
    database: hexabid
    username: hexabid_admin
    passwordSecret: hexabid-db-secret

redis:
  enabled: false  # Using external ElastiCache
  external:
    host: hexabid-prod.xxx.cache.amazonaws.com
    port: 6379
    passwordSecret: hexabid-redis-secret

elasticsearch:
  enabled: false
  external:
    host: https://search-hexabid-prod-xxx.ap-south-1.es.amazonaws.com
    port: 443

minio:
  enabled: false
  external:
    endpoint: https://s3.ap-south-1.amazonaws.com
    bucket: hexabid-prod-documents
    accessKeySecret: hexabid-s3-secret

env:
  NODE_ENV: production
  LOG_LEVEL: info
  ENABLE_CORS: "true"
  
  # Emergent LLM Key (injected from secret)
  EMERGENT_LLM_KEY:
    secretKeyRef:
      name: hexabid-llm-secret
      key: api-key

secrets:
  # Managed via external secrets operator or manual creation
  - hexabid-db-secret
  - hexabid-redis-secret
  - hexabid-s3-secret
  - hexabid-llm-secret
  - hexabid-sendgrid-secret
  - hexabid-twilio-secret
```

---

## Kubernetes Manifests Highlights

### API Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hexabid-api
  namespace: hexabid-prod
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hexabid-api
  template:
    metadata:
      labels:
        app: hexabid-api
    spec:
      containers:
      - name: api
        image: hexabid/api:1.0.0
        ports:
        - containerPort: 3000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: hexabid-db-secret
              key: url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: hexabid-redis-secret
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Horizontal Pod Autoscaler

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hexabid-api-hpa
  namespace: hexabid-prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hexabid-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
```

### Ingress Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: hexabid-ingress
  namespace: hexabid-prod
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - hexabid.in
    - "*.hexabid.in"
    secretName: hexabid-tls
  rules:
  - host: hexabid.in
    http:
      paths:
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: hexabid-api
            port:
              number: 3000
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hexabid-frontend
            port:
              number: 80
  - host: "*.hexabid.in"  # Tenant subdomains
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: hexabid-frontend
            port:
              number: 80
```

---

## CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Build and Deploy

on:
  push:
    branches:
      - main       # Production
      - staging    # Staging
      - develop    # Development

env:
  AWS_REGION: ap-south-1
  EKS_CLUSTER_NAME: hexabid-prod

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.DOCKER_REGISTRY }}
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build and push API image
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: |
            hexabid/api:${{ github.sha }}
            hexabid/api:latest
          cache-from: type=registry,ref=hexabid/api:latest
          cache-to: type=inline

      - name: Build and push Worker image
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          file: ./backend/Dockerfile.worker
          push: true
          tags: |
            hexabid/worker:${{ github.sha }}
            hexabid/worker:latest

      - name: Build and push Frontend image
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: |
            hexabid/frontend:${{ github.sha }}
            hexabid/frontend:latest

  test:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run backend tests
        run: |
          cd backend
          npm install
          npm run test

      - name: Run frontend tests
        run: |
          cd frontend
          npm install
          npm run test

      - name: Run integration tests
        run: npm run test:integration

  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Update kubeconfig
        run: |
          aws eks update-kubeconfig --name ${{ env.EKS_CLUSTER_NAME }} --region ${{ env.AWS_REGION }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install hexabid ./helm/hexabid \
            --namespace hexabid-prod \
            --values ./helm/hexabid/values-production.yaml \
            --set image.api.tag=${{ github.sha }} \
            --set image.worker.tag=${{ github.sha }} \
            --set image.frontend.tag=${{ github.sha }} \
            --wait --timeout 10m

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/hexabid-api -n hexabid-prod
          kubectl rollout status deployment/hexabid-worker -n hexabid-prod
          kubectl rollout status deployment/hexabid-frontend -n hexabid-prod

      - name: Run smoke tests
        run: |
          curl -f https://hexabid.in/health || exit 1
          curl -f https://hexabid.in/api/health || exit 1

      - name: Notify on success
        if: success()
        run: echo "Deployment successful!"

      - name: Rollback on failure
        if: failure()
        run: |
          helm rollback hexabid -n hexabid-prod
          echo "Deployment failed, rolled back"
```

---

## Monitoring Setup

### Prometheus Configuration

```yaml
# prometheus-values.yaml
serverFiles:
  prometheus.yml:
    scrape_configs:
      - job_name: 'hexabid-api'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - hexabid-prod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            regex: hexabid-api
            action: keep

      - job_name: 'hexabid-worker'
        kubernetes_sd_configs:
          - role: pod
            namespaces:
              names:
                - hexabid-prod
        relabel_configs:
          - source_labels: [__meta_kubernetes_pod_label_app]
            regex: hexabid-worker
            action: keep

      - job_name: 'postgresql'
        static_configs:
          - targets: ['postgres-exporter:9187']

      - job_name: 'redis'
        static_configs:
          - targets: ['redis-exporter:9121']
```

### Grafana Dashboards

Pre-configured dashboards:
- **Application Overview**: Request rates, latencies, error rates
- **Database Performance**: Connection pool, query performance, slow queries
- **Redis Metrics**: Hit rate, memory usage, operations/sec
- **Kubernetes Cluster**: Node resources, pod status, network traffic
- **Business Metrics**: Tenders ingested, BOQs generated, documents assembled

---

## Cost Estimation

### Development Environment

```
EKS Control Plane:        $73/month
EC2 Nodes (2x t3.medium): $60/month
RDS (db.t3.small):        $30/month
ElastiCache (cache.t3.micro): $15/month
S3 Storage (100 GB):      $2/month
Data Transfer:            $10/month

Total: ~$190/month
```

### Staging Environment

```
EKS Control Plane:        $73/month
EC2 Nodes (3x t3.large):  $180/month
RDS (db.t3.medium):       $65/month
ElastiCache (cache.t3.small): $30/month
Elasticsearch (t3.small): $40/month
S3 Storage (500 GB):      $12/month
Data Transfer:            $30/month

Total: ~$430/month
```

### Production Environment (Initial)

```
EKS Control Plane:        $73/month
EC2 Nodes (5x t3.xlarge): $750/month
RDS (db.r5.xlarge, Multi-AZ): $580/month
RDS Read Replica:         $290/month
ElastiCache (cache.r5.large): $180/month
Elasticsearch (r5.large, 3 nodes): $450/month
S3 Storage (5 TB):        $115/month
CloudFront CDN:           $50/month
Data Transfer:            $150/month
Backup Storage:           $100/month
ALB:                      $25/month
Route53:                  $5/month

Total: ~$2,768/month (~$33,000/year)
```

### Production (Scaled for 1000 Tenants)

```
EKS Control Plane:        $73/month
EC2 Nodes (15x t3.xlarge): $2,250/month
RDS (db.r5.4xlarge, Multi-AZ): $2,320/month
RDS Read Replicas (2x):   $1,160/month
ElastiCache (cache.r5.2xlarge): $720/month
Elasticsearch (r5.2xlarge, 6 nodes): $3,600/month
S3 Storage (50 TB):       $1,150/month
CloudFront CDN:           $300/month
Data Transfer:            $800/month
Backup Storage:           $500/month

Total: ~$12,873/month (~$154,000/year)
```

---

## Disaster Recovery

### Backup Strategy

1. **Database (PostgreSQL)**:
   - Automated daily snapshots (RDS)
   - WAL archiving to S3 for PITR
   - Retention: 30 days

2. **Object Storage (S3)**:
   - Versioning enabled
   - Cross-region replication to DR region
   - Lifecycle policies (30-day retention for deleted objects)

3. **Elasticsearch**:
   - Daily snapshots to S3
   - Retention: 14 days

4. **Redis**:
   - AOF (Append-Only File) persistence
   - Daily snapshots

### Recovery Procedures

**RTO (Recovery Time Objective)**: 4 hours
**RPO (Recovery Point Objective)**: 15 minutes

**Failover Process**:
1. DNS failover to DR region (Route53 health checks)
2. Promote RDS read replica in DR region
3. Deploy application to DR Kubernetes cluster
4. Restore Elasticsearch from latest snapshot
5. Redirect traffic via load balancer

---

## Security Hardening

### Network Security
- VPC with private subnets for application and database
- Security groups: Least privilege access
- Network ACLs for subnet-level filtering
- VPN/Bastion host for administrative access

### Secrets Management
- AWS Secrets Manager or HashiCorp Vault
- Kubernetes External Secrets Operator
- Encrypted at rest and in transit
- Automatic rotation for database credentials

### SSL/TLS
- Let's Encrypt certificates via cert-manager
- TLS 1.3 only
- HSTS headers enforced

### IAM & RBAC
- Kubernetes RBAC for fine-grained permissions
- AWS IAM roles for service accounts (IRSA)
- Pod security policies

---

## Runbook

See `/docs/05-RUNBOOK.md` for operational procedures:
- Deployment procedures
- Rollback procedures
- Scaling operations
- Incident response
- Database migrations
- Backup/restore procedures
- Log analysis
- Performance troubleshooting

---

## Next Steps

1. Provision infrastructure using Terraform
2. Deploy monitoring stack (Prometheus + Grafana)
3. Deploy application using Helm
4. Configure CI/CD pipeline
5. Load testing and performance tuning
6. Security audit and penetration testing
7. Documentation and knowledge transfer
