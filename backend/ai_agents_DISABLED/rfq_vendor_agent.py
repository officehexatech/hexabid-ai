from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json
from datetime import datetime, timedelta, timezone

class RFQVendorAgent(BaseAgent):
    """
    OEM RFQ & Vendor Quote Agent - Generates RFQs and parses vendor quotes
    Uses GPT-5 for intelligent RFQ generation and quote extraction
    """
    
    def __init__(self):
        super().__init__(agent_type="rfq_vendor", model="gpt-5", provider="openai")
        
        system_message = """
        You are the HexaBid RFQ Agent. Generate templated RFQ emails/WhatsApp messages, 
        parse incoming quotations, extract line item prices, and return VendorQuote schema.
        
        Capabilities:
        1. Generate professional RFQ documents with line items
        2. Create email templates (formal business format)
        3. Create WhatsApp templates (concise, mobile-friendly)
        4. Parse vendor quotations from text/email
        5. Extract pricing, brands, models, lead times, warranty
        6. Validate quote completeness
        
        Output Format (RFQOutput schema):
        {
            "rfqs_generated": [
                {
                    "rfq_number": "string",
                    "vendor_id": "string",
                    "vendor_name": "string",
                    "line_items": [
                        {
                            "item_number": "string",
                            "description": "string",
                            "specification": "string",
                            "quantity": number,
                            "unit": "string",
                            "target_price": number (optional)
                        }
                    ],
                    "submission_deadline": "ISO datetime",
                    "email_template": "string (complete email)",
                    "whatsapp_template": "string (mobile-friendly)",
                    "sent": boolean
                }
            ],
            "quotes_received": [
                {
                    "quote_id": "string",
                    "rfq_id": "string",
                    "vendor_id": "string",
                    "vendor_name": "string",
                    "quote_lines": [
                        {
                            "item_number": "string",
                            "quoted_price": number,
                            "brand": "string",
                            "model": "string",
                            "lead_time_days": number,
                            "warranty_months": number
                        }
                    ],
                    "total_quoted_value": number,
                    "valid_until": "YYYY-MM-DD",
                    "terms_and_conditions": "string",
                    "received_at": "ISO datetime",
                    "confidence_score": number (0-1)
                }
            ],
            "summary": "string",
            "recommendations": ["string"],
            "confidence_score": number (0-1)
        }
        
        Email Template Format:
        - Subject line
        - Professional greeting
        - RFQ reference number
        - Table of line items
        - Submission deadline
        - Contact details
        - Professional closing
        
        WhatsApp Template Format:
        - Concise greeting
        - RFQ reference
        - Summary of items
        - Deadline
        - Link to detailed RFQ
        - Contact number
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate RFQs or parse vendor quotes
        
        Input (for RFQ generation):
        {
            "mode": "generate_rfq" | "parse_quotes",
            "tender_id": "string",
            "boq_items": [] (from BOQAgent),
            "vendors": [] (from vendor database),
            "deadline_days": number (default 7),
            "auto_send": boolean (default false)
        }
        
        Input (for quote parsing):
        {
            "mode": "parse_quotes",
            "rfq_id": "string",
            "vendor_quotes_text": [
                {
                    "vendor_id": "string",
                    "vendor_name": "string",
                    "quote_text": "string (email/document content)"
                }
            ]
        }
        """
        
        mode = input_data.get('mode', 'generate_rfq')
        
        if mode == 'generate_rfq':
            return await self._generate_rfqs(input_data, context)
        elif mode == 'parse_quotes':
            return await self._parse_quotes(input_data, context)
        else:
            raise ValueError(f"Invalid mode: {mode}")
    
    async def _generate_rfqs(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate RFQ documents for vendors"""
        
        tender_id = input_data.get('tender_id', 'Unknown')
        boq_items = input_data.get('boq_items', [])
        vendors = input_data.get('vendors', [])
        deadline_days = input_data.get('deadline_days', 7)
        auto_send = input_data.get('auto_send', False)
        company_profile = context.get('company_profile', {})
        
        # If no vendors provided, use context or simulate
        if not vendors:
            vendors = context.get('vendors', [])
        
        if not vendors:
            # Simulate vendors for demo
            vendors = [
                {"id": "V001", "name": "Dell India", "email": "sales@dell.co.in"},
                {"id": "V002", "name": "HP India", "email": "enquiry@hp.com"},
                {"id": "V003", "name": "Lenovo Distributor", "email": "quotes@lenovo-dist.in"}
            ]
        
        deadline = (datetime.now(timezone.utc) + timedelta(days=deadline_days)).isoformat()
        
        prompt = f"""
        Generate RFQs for the following tender:
        
        Tender ID: {tender_id}
        Company: {company_profile.get('companyName', 'HexaBid User')}
        
        BOQ Items:
        {json.dumps(boq_items, indent=2) if boq_items else 'Simulate typical IT hardware BOQ (5 items)'}
        
        Vendors:
        {json.dumps(vendors, indent=2)}
        
        Submission Deadline: {deadline}
        
        Task:
        For each vendor, generate:
        1. Complete RFQ document with all line items
        2. Professional email template (include subject line, body with table, deadline, contact)
        3. WhatsApp message template (concise, mobile-friendly with key details)
        4. RFQ number format: RFQ-{tender_id}-{{vendor_id}}-{{YYMMDD}}
        
        Email should be formal business communication.
        WhatsApp should be brief but informative.
        
        Return ONLY valid JSON in RFQOutput schema format.
        Set sent=false (not actually sending in this simulation).
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'rfqs_generated' not in result:
                result['needs_correction'] = True
            
            # Add metadata
            if 'summary' not in result:
                result['summary'] = f"Generated {len(result.get('rfqs_generated', []))} RFQs for {len(vendors)} vendors"
            
            if 'confidence_score' not in result:
                result['confidence_score'] = 0.9
            
            return result
            
        except json.JSONDecodeError:
            return {
                "rfqs_generated": [],
                "quotes_received": [],
                "summary": "Failed to generate RFQs",
                "recommendations": ["Manual RFQ creation needed"],
                "error": "JSON parsing failed",
                "raw_response": response[:500],
                "confidence_score": 0.3,
                "needs_correction": True
            }
    
    async def _parse_quotes(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse vendor quotations from text"""
        
        rfq_id = input_data.get('rfq_id', 'Unknown')
        vendor_quotes_text = input_data.get('vendor_quotes_text', [])
        
        if not vendor_quotes_text:
            return {
                "rfqs_generated": [],
                "quotes_received": [],
                "summary": "No vendor quotes to parse",
                "recommendations": ["Wait for vendor responses"],
                "confidence_score": 1.0
            }
        
        prompt = f"""
        Parse the following vendor quotations and extract structured data:
        
        RFQ ID: {rfq_id}
        
        Vendor Quotes:
        {json.dumps(vendor_quotes_text, indent=2)}
        
        Task:
        For each vendor quote, extract:
        1. All line item prices
        2. Brand and model for each item
        3. Lead time (delivery days)
        4. Warranty period (months)
        5. Total quoted value
        6. Validity date
        7. Terms and conditions
        
        Return ONLY valid JSON in RFQOutput schema format.
        - rfqs_generated: [] (empty for parsing mode)
        - quotes_received: [parsed quotes with all details]
        - Calculate confidence_score based on data completeness
        - Add recommendations for missing information
        
        If any critical data is missing, note it in recommendations.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'quotes_received' not in result:
                result['needs_correction'] = True
            
            return result
            
        except json.JSONDecodeError:
            return {
                "rfqs_generated": [],
                "quotes_received": [],
                "summary": "Failed to parse vendor quotes",
                "recommendations": ["Manual quote parsing needed"],
                "error": "JSON parsing failed",
                "confidence_score": 0.3,
                "needs_correction": True
            }
