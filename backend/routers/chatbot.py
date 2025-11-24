from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class ChatMessage(BaseModel):
    message: str
    sessionId: str

def get_db():
    from server import db
    return db

# Marketing chatbot system message
MARKETING_SYSTEM_MESSAGE = """You are HexaBid's AI Marketing Assistant. You help potential customers understand HexaBid's features and benefits.

HexaBid is India's premier AI-powered tender management platform that offers:

1. **Tender Discovery**: Auto-fetch tenders from GeM and government portals
2. **AI Parsing**: Smart extraction of BOQ, specifications, and requirements
3. **BOQ Generator**: AI-powered Bill of Quantities creation in minutes
4. **Compliance Checker**: Automated technical compliance validation
5. **OEM/Vendor Management**: Complete vendor database with RFQ automation
6. **Document Assembly**: One-click generation of all tender documents
7. **AI Pricing**: Smart price suggestions based on market data
8. **Analytics & MIS**: Comprehensive reports and competitor analysis
9. **ERP Integration**: Complete project execution modules
10. **Multi-Tenant**: Team collaboration with role-based access

Key Benefits:
- 10x faster tender preparation
- Zero manual errors
- 100% FREE forever - no trial, no credit card
- 24/7 availability
- Make in India initiative
- GeM portal ready
- SSL secure

Target Users:
- Government contractors
- Tender consultants
- OEMs & distributors
- EPC companies
- Service contractors
- Large enterprises

Contact:
- Phone: +91 8806106575, +91 9607500750
- Email: support@hexabid.in

Be friendly, helpful, and emphasize the FREE forever nature of the platform. Answer questions about features, pricing, implementation, and help guide users to sign up."""

@router.post("/chat")
async def chat_with_bot(message: ChatMessage, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        api_key = os.getenv("EMERGENT_LLM_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        # Create chat instance
        chat = LlmChat(
            api_key=api_key,
            session_id=message.sessionId,
            system_message=MARKETING_SYSTEM_MESSAGE
        ).with_model("openai", "gpt-4o-mini")
        
        # Create user message
        user_msg = UserMessage(text=message.message)
        
        # Get response
        response = await chat.send_message(user_msg)
        
        # Store in database
        chat_doc = {
            "id": str(uuid.uuid4()),
            "sessionId": message.sessionId,
            "userMessage": message.message,
            "botResponse": response,
            "createdAt": datetime.now(timezone.utc).isoformat()
        }
        await db.chat_history.insert_one(chat_doc)
        
        return {
            "response": response,
            "sessionId": message.sessionId
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@router.get("/history/{session_id}")
async def get_chat_history(session_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        history_cursor = db.chat_history.find(
            {"sessionId": session_id},
            {"_id": 0}
        ).sort("createdAt", 1)
        
        history = await history_cursor.to_list(length=100)
        
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")