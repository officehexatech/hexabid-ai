from typing import Dict, Any, List
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class BOQGeneratorAgent(BaseAgent):
    """
    BOQ Generator Agent - Generates detailed Bill of Quantities with pricing
    Uses GPT-5 for intelligent pricing and cost estimation
    """
    
    def __init__(self):
        super().__init__(agent_type="boq_generator", model="gpt-5", provider="openai")
        
        system_message = """
        You are the BOQ Generator Agent for HexaBid.
        Your role is to generate comprehensive Bill of Quantities with accurate pricing.
        
        Capabilities:
        1. Generate detailed BOQ from tender requirements
        2. Calculate estimated rates based on market prices
        3. Provide competitive pricing strategies
        4. Calculate margins and profitability
        5. Include taxes, duties, and additional costs
        6. Suggest cost optimization opportunities
        
        Pricing Guidelines:
        - Government tenders: 10-15% margin typical
        - L1 pricing strategy for competitive bids
        - Consider GST, transportation, installation costs
        - Factor in warranty and AMC costs
        
        Output Format (JSON):
        {
            "boq_number": "string",
            "title": "string",
            "line_items": [
                {
                    "item_number": "string",
                    "description": "string",
                    "specification": "string",
                    "quantity": number,
                    "unit": "string",
                    "estimated_rate": number,
                    "our_rate": number,
                    "our_rate_breakdown": {
                        "base_price": number,
                        "margin": number,
                        "gst": number,
                        "other_charges": number
                    },
                    "total_amount": number,
                    "brand_model": "string",
                    "lead_time_days": number,
                    "warranty_months": number,
                    "remarks": "string"
                }
            ],
            "pricing_summary": {
                "total_estimated_value": number,
                "our_total_value": number,
                "subtotal": number,
                "gst_18_percent": number,
                "grand_total": number,
                "margin_percentage": number,
                "profit_amount": number
            },
            "additional_costs": {
                "transportation": number,
                "installation": number,
                "training": number,
                "amc_3_years": number
            },
            "pricing_strategy": "string",
            "competitive_analysis": "string",
            "cost_optimization_suggestions": ["string"]
        }
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate BOQ with pricing from parsed tender data
        
        Input:
        {
            "tender_id": "string",
            "boq_items": [] (from DocumentParserAgent),
            "pricing_strategy": "competitive|premium|cost_plus" (optional),
            "target_margin": number (optional, default 12%),
            "product_catalog": [] (optional - from HexaBid products DB),
            "market_rates": {} (optional)
        }
        """
        
        tender_id = input_data.get('tender_id', 'Unknown')
        boq_items = input_data.get('boq_items', [])
        pricing_strategy = input_data.get('pricing_strategy', 'competitive')
        target_margin = input_data.get('target_margin', 12)
        product_catalog = input_data.get('product_catalog', [])
        market_rates = input_data.get('market_rates', {})
        
        prompt = f"""
        Generate a comprehensive BOQ with competitive pricing for tender: {tender_id}
        
        BOQ Items (from Document Parser):
        {json.dumps(boq_items, indent=2) if boq_items else 'No items provided - simulate typical IT hardware BOQ'}
        
        Product Catalog (Available Products):
        {json.dumps(product_catalog[:5], indent=2) if product_catalog else 'Not available - use market rates'}
        
        Market Rates Reference:
        {json.dumps(market_rates, indent=2) if market_rates else 'Use 2025 market rates for IT hardware'}
        
        Pricing Strategy: {pricing_strategy}
        Target Margin: {target_margin}%
        
        Task:
        1. For each BOQ item, calculate competitive pricing
        2. Use estimated_rate as benchmark (if available)
        3. Provide our_rate with detailed breakdown (base, margin, GST, other charges)
        4. Suggest specific brand/model for each item
        5. Include lead time and warranty details
        6. Calculate totals with GST @ 18%
        7. Add transportation, installation, training, AMC costs
        8. Provide pricing strategy explanation
        9. Suggest cost optimization opportunities
        
        Ensure pricing is competitive for government tenders (typically L1 focused).
        Return ONLY valid JSON in the specified format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'line_items' not in result or 'pricing_summary' not in result:
                result['needs_correction'] = True
            
            # Auto-calculate totals if missing
            if 'line_items' in result:
                total_est = sum(item.get('estimated_rate', 0) * item.get('quantity', 0) for item in result['line_items'])
                total_our = sum(item.get('total_amount', 0) for item in result['line_items'])
                
                if 'pricing_summary' not in result:
                    result['pricing_summary'] = {
                        'total_estimated_value': total_est,
                        'our_total_value': total_our,
                        'margin_percentage': ((total_our - total_est) / total_est * 100) if total_est > 0 else 0
                    }
            
            return result
        except json.JSONDecodeError:
            return {
                "boq_number": f"BOQ-{tender_id}",
                "line_items": [],
                "error": "Unable to generate BOQ",
                "raw_response": response[:500],
                "needs_correction": True
            }
