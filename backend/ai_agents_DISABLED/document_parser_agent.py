from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class DocumentParserAgent(BaseAgent):
    """
    Document Parser Agent - Extracts structured data from tender documents
    Uses GPT-5 for intelligent document understanding and extraction
    """
    
    def __init__(self):
        super().__init__(agent_type="document_parser", model="gpt-5", provider="openai")
        
        system_message = """
        You are the Document Parser Agent for HexaBid.
        Your role is to parse tender documents and extract structured information.
        
        Capabilities:
        1. Extract tender specifications and requirements
        2. Identify BOQ items and quantities
        3. Parse technical compliance clauses
        4. Extract submission instructions and deadlines
        5. Identify mandatory documents required
        6. Extract evaluation criteria and scoring methods
        
        Output Format (JSON):
        {
            "tender_info": {
                "tender_number": "string",
                "title": "string",
                "organization": "string",
                "description": "string"
            },
            "scope_of_work": "string",
            "boq_items": [
                {
                    "item_number": "string",
                    "description": "string",
                    "specification": "string",
                    "quantity": number,
                    "unit": "string",
                    "estimated_rate": number (optional)
                }
            ],
            "technical_requirements": [
                {
                    "clause_number": "string",
                    "requirement": "string",
                    "mandatory": boolean,
                    "compliance_needed": "string"
                }
            ],
            "mandatory_documents": ["string"],
            "submission_details": {
                "deadline": "YYYY-MM-DD HH:MM",
                "submission_mode": "online|offline|hybrid",
                "address": "string" (if offline),
                "portal_link": "string" (if online)
            },
            "evaluation_criteria": {
                "technical_score": number,
                "financial_score": number,
                "method": "string"
            },
            "emd_details": {
                "amount": number,
                "mode": "string",
                "exemption_clauses": ["string"]
            },
            "key_dates": [
                {
                    "event": "string",
                    "date": "YYYY-MM-DD"
                }
            ]
        }
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse tender document and extract structured information
        
        Input:
        {
            "document_text": "string" (full tender document text),
            "document_url": "string" (optional),
            "tender_number": "string" (optional)
        }
        """
        
        document_text = input_data.get('document_text', '')
        document_url = input_data.get('document_url', '')
        tender_number = input_data.get('tender_number', 'Unknown')
        
        # Truncate if too long (keep first 15000 chars for context)
        if len(document_text) > 15000:
            document_text = document_text[:15000] + "\n\n[Document truncated for processing...]"
        
        prompt = f"""
        Parse the following tender document and extract all relevant information:
        
        Tender Number: {tender_number}
        Document URL: {document_url if document_url else 'Not provided'}
        
        Document Content:
        {document_text if document_text else 'Document content not provided. Please simulate a typical IT hardware tender document parsing.'}
        
        Task:
        1. Extract tender basic information
        2. Parse scope of work
        3. Extract all BOQ line items with specifications
        4. Identify technical compliance requirements
        5. List mandatory documents needed for submission
        6. Extract submission details and deadlines
        7. Parse evaluation criteria
        8. Extract EMD details
        9. Identify all key dates
        
        Return ONLY valid JSON in the specified format.
        If document text is not provided, simulate parsing a typical government IT hardware procurement tender.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'tender_info' not in result or 'boq_items' not in result:
                result['needs_correction'] = True
            
            return result
        except json.JSONDecodeError:
            return {
                "tender_info": {"tender_number": tender_number, "title": "Parsing Error"},
                "boq_items": [],
                "error": "Unable to parse document",
                "raw_response": response[:500],
                "needs_correction": True
            }
