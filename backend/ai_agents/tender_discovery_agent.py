from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class TenderDiscoveryAgent(BaseAgent):
    """
    Tender Discovery Agent - Discovers relevant tenders from various sources
    Uses GPT-5 for intelligent tender matching and filtering
    """
    
    def __init__(self):
        super().__init__(agent_type="tender_discovery", model="gpt-5", provider="openai")
        
        system_message = """
        You are the Tender Discovery Agent for HexaBid.
        Your role is to analyze tender requirements and discover relevant tenders from provided sources.
        
        Capabilities:
        1. Match user requirements with tender opportunities
        2. Extract key tender details (number, title, organization, deadline, value)
        3. Filter tenders by category, location, value range
        4. Prioritize tenders based on win probability
        5. Identify tender sources (GeM, eProcure, CPPP, manual entries)
        
        Output Format (JSON):
        {
            "discovered_tenders": [
                {
                    "tender_number": "string",
                    "title": "string",
                    "organization": "string",
                    "department": "string",
                    "category": "string",
                    "location": "string",
                    "publish_date": "YYYY-MM-DD",
                    "submission_deadline": "YYYY-MM-DD",
                    "tender_value": number,
                    "emd_amount": number,
                    "source": "gem|eprocure|cppp|manual",
                    "document_url": "string",
                    "match_score": number (0-100),
                    "win_probability": "high|medium|low",
                    "key_requirements": ["string"]
                }
            ],
            "search_summary": "string",
            "total_found": number,
            "recommendations": ["string"]
        }
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Discover tenders based on user requirements
        
        Input:
        {
            "search_query": "string",
            "category": "string" (optional),
            "location": "string" (optional),
            "min_value": number (optional),
            "max_value": number (optional),
            "keywords": ["string"] (optional),
            "existing_tenders_db": [] (optional - from HexaBid database)
        }
        """
        
        search_query = input_data.get('search_query', '')
        category = input_data.get('category', 'All')
        location = input_data.get('location', 'All India')
        min_value = input_data.get('min_value', 0)
        max_value = input_data.get('max_value', 10000000000)  # 1000 Cr
        keywords = input_data.get('keywords', [])
        existing_tenders = input_data.get('existing_tenders_db', [])
        
        prompt = f"""
        Discover tenders matching the following criteria:
        
        Search Query: {search_query}
        Category: {category}
        Location: {location}
        Value Range: ₹{min_value} - ₹{max_value}
        Keywords: {', '.join(keywords) if keywords else 'None'}
        
        Existing Tenders in Database:
        {json.dumps(existing_tenders, indent=2) if existing_tenders else 'None - Simulate discovery'}
        
        Task:
        1. If existing_tenders provided, filter and rank them based on match score
        2. If no existing_tenders, simulate discovering 5-10 relevant tenders from GeM/eProcure
        3. Calculate match_score (0-100) based on requirement alignment
        4. Assess win_probability (high/medium/low)
        5. Extract key_requirements from each tender
        6. Provide recommendations for best tender opportunities
        
        Return ONLY valid JSON in the specified format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'discovered_tenders' not in result:
                result['needs_correction'] = True
            
            return result
        except json.JSONDecodeError:
            # If response is not valid JSON, wrap it
            return {
                "discovered_tenders": [],
                "search_summary": response,
                "total_found": 0,
                "recommendations": ["Unable to parse tender discovery results"],
                "needs_correction": True
            }
