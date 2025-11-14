from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from datetime import datetime, timezone

# Import routers
from routers import auth, vendors, rfq, company_profile, email_verification, chatbot, settings, feedback, tenders, boq, products, alerts, analytics, ai_agents, credits, payments, tenants, super_admin, gem_integration, search, competitors, cpp_portal, buyers_history, competitor_history, pdf_tools, email_client, office365

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app
app = FastAPI(title="HexaBid API", version="1.0.0")

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Health check
@api_router.get("/")
async def root():
    return {"message": "HexaBid API - Running", "version": "1.0.0"}

@api_router.get("/health")
async def health_check():
    try:
        # Check MongoDB connection
        await db.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# Include all routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(vendors.router, prefix="/vendors", tags=["Vendors"])
api_router.include_router(rfq.router, prefix="/rfq", tags=["RFQ"])
api_router.include_router(company_profile.router, prefix="/company", tags=["Company Profile"])
api_router.include_router(email_verification.router, prefix="/email", tags=["Email Verification"])
api_router.include_router(chatbot.router, prefix="/chatbot", tags=["AI Chatbot"])
api_router.include_router(settings.router, prefix="/settings", tags=["Platform Settings"])
api_router.include_router(feedback.router, prefix="/feedback", tags=["Feedback"])
# MVP Core Modules
api_router.include_router(tenders.router, prefix="/tenders", tags=["Tenders"])
api_router.include_router(boq.router, prefix="/boq", tags=["BOQ"])
api_router.include_router(products.router, prefix="/products", tags=["Product Catalog"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["Notifications"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics & MIS"])
# AI Agents & Credits
api_router.include_router(ai_agents.router, prefix="/ai-agents", tags=["AI Agents"])
api_router.include_router(credits.router, prefix="/credits", tags=["Credits"])
api_router.include_router(payments.router, prefix="/payments", tags=["Payments"])
# Multi-Tenant & Admin
api_router.include_router(tenants.router, prefix="/tenants", tags=["Tenants"])
api_router.include_router(super_admin.router, prefix="/super-admin", tags=["Super Admin"])
# GEM Integration, Search & Competitors
api_router.include_router(gem_integration.router)
api_router.include_router(search.router)
api_router.include_router(competitors.router)
# CPP Portal, Buyers & Competitor History
api_router.include_router(cpp_portal.router)
api_router.include_router(buyers_history.router)
api_router.include_router(competitor_history.router)
# Phase 2: PDF Tools, Email, Office 365
api_router.include_router(pdf_tools.router)
api_router.include_router(email_client.router)
api_router.include_router(office365.router)

# Include the API router in the main app
app.include_router(api_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_db_client():
    logger.info("Starting HexaBid API...")
    logger.info(f"Connected to MongoDB at {mongo_url}")
    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.vendors.create_index("companyName")
    await db.companies.create_index("userId")
    logger.info("Database indexes created")

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Shutting down HexaBid API...")
    client.close()

# Export db for use in routers
app.state.db = db