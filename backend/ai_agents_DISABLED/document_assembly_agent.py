from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class DocumentAssemblyAgent(BaseAgent):
    """
    Document Assembly Agent - Assembles complete tender submission documents
    Uses GPT-4o-mini for document generation (cost-effective for text generation)
    """
    
    def __init__(self):
        super().__init__(agent_type="document_assembly", model="gpt-4o-mini", provider="openai")
        
        system_message = """
        You are the Document Assembly Agent for HexaBid.
        Your role is to assemble professional tender submission documents.
        
        Capabilities:
        1. Generate cover letter with company credentials
        2. Create technical compliance statement
        3. Format financial bid (BOQ) professionally
        4. Generate supporting documents list
        5. Create submission checklist
        6. Format documents as per tender requirements
        
        Document Standards:
        - Professional business formatting
        - Government tender language and tone
        - Include company letterhead placeholders
        - Proper numbering and references
        - Clear section headings
        - Signature placeholders
        
        Output Format (JSON):
        {
            "documents": [
                {
                    "document_type": "cover_letter|technical_bid|financial_bid|compliance_statement|checklist",
                    "title": "string",
                    "content": "string (formatted markdown or HTML)",
                    "page_count": number,
                    "requires_signature": boolean,
                    "requires_seal": boolean
                }
            ],
            "submission_package_summary": {
                "total_documents": number,
                "ready_to_submit": boolean,
                "missing_items": ["string"],
                "instructions": "string"
            },
            "checklist": [
                {
                    "item": "string",
                    "status": "completed|pending|not_required",
                    "notes": "string"
                }
            ]
        }
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assemble complete tender submission documents
        
        Input:
        {
            "tender_info": {} (from DocumentParserAgent),
            "boq": {} (from BOQGeneratorAgent),
            "company_profile": {} (from HexaBid DB),
            "technical_requirements": [] (from DocumentParserAgent),
            "mandatory_documents": [] (from DocumentParserAgent)
        }
        """
        
        tender_info = input_data.get('tender_info', {})
        boq = input_data.get('boq', {})
        company_profile = input_data.get('company_profile', {})
        technical_requirements = input_data.get('technical_requirements', [])
        mandatory_documents = input_data.get('mandatory_documents', [])
        
        prompt = f"""
        Assemble complete tender submission documents for:
        
        Tender Information:
        {json.dumps(tender_info, indent=2) if tender_info else 'Simulate typical government IT tender'}
        
        Company Profile:
        {json.dumps(company_profile, indent=2) if company_profile else 'Use placeholder company details'}
        
        BOQ Summary:
        {json.dumps(boq.get('pricing_summary', {}), indent=2) if boq else 'BOQ not available'}
        
        Technical Requirements:
        {json.dumps(technical_requirements[:5], indent=2) if technical_requirements else 'Not specified'}
        
        Mandatory Documents:
        {json.dumps(mandatory_documents, indent=2) if mandatory_documents else 'Standard documents'}
        
        Task:
        Generate the following documents:
        
        1. **Cover Letter**: Professional introduction, company credentials, bid submission
        2. **Technical Compliance Statement**: Clause-by-clause compliance with YES/NO/PARTIAL
        3. **Financial Bid (BOQ)**: Professionally formatted price bid with all line items
        4. **Submission Checklist**: All documents and their status
        
        Format each document professionally with:
        - Proper headers and company letterhead placeholder
        - Professional business language
        - Government tender appropriate tone
        - Clear sections and numbering
        - Signature and seal placeholders
        
        Return ONLY valid JSON in the specified format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'documents' not in result:
                result['needs_correction'] = True
            
            return result
        except json.JSONDecodeError:
            return {
                "documents": [
                    {
                        "document_type": "error",
                        "title": "Document Generation Error",
                        "content": response[:1000]
                    }
                ],
                "error": "Unable to generate documents",
                "needs_correction": True
            }
