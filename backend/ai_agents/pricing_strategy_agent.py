from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class PricingStrategyAgent(BaseAgent):
    """
    Pricing Strategy & Bid Optimization Agent
    Uses GPT-5 for intelligent pricing scenarios and win probability prediction
    """
    
    def __init__(self):
        super().__init__(agent_type="pricing_strategy", model="gpt-5", provider="openai")
        
        system_message = """
        You are the Pricing Strategy Agent. Use BOQ, OEM quotes, price_history, 
        competitor intelligence to generate 3 pricing scenarios (aggressive, balanced, conservative). 
        Return PricingReport schema with reasoning and predicted win probability.
        
        Pricing Philosophy:
        - Aggressive: Minimize margin (5-8%), maximize win probability
        - Balanced: Standard margin (10-15%), good win probability
        - Conservative: Higher margin (18-25%), lower risk
        
        Consider:
        - Government tenders typically L1 (lowest bidder wins)
        - EMD amount as indicator of competition
        - Historical win rates at different price points
        - Competitor pricing patterns
        - Risk vs reward tradeoff
        
        Output Format (PricingReport schema):
        {
            "tender_id": "string",
            "scenarios": [
                {
                    "scenario_name": "aggressive" | "balanced" | "conservative",
                    "total_bid_value": number,
                    "margin_percentage": number,
                    "profit_amount": number,
                    "win_probability": number (0-1),
                    "reasoning": "string",
                    "risks": ["string"],
                    "advantages": ["string"]
                }
            ],
            "recommended_scenario": "aggressive" | "balanced" | "conservative",
            "competitor_intelligence": {
                "estimated_competitors": number,
                "likely_l1_price": number,
                "our_rank_prediction": number,
                "market_dynamics": "string"
            },
            "price_optimization_suggestions": ["string"],
            "confidence_score": number (0-1),
            "generation_timestamp": "ISO datetime"
        }
        
        Win Probability Estimation:
        - Aggressive (below market by 5-10%): 0.7-0.9
        - Balanced (at market rate): 0.5-0.7
        - Conservative (above market by 10-20%): 0.2-0.4
        
        Adjust based on:
        - Tender complexity (high = fewer bidders)
        - EMD amount (high = fewer bidders)
        - Technical requirements (stringent = fewer bidders)
        - Our past performance with this organization
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate pricing scenarios and recommendations
        
        Input:
        {
            "tender_id": "string",
            "boq": {} (from BOQAgent),
            "vendor_quotes": [] (from RFQAgent),
            "estimated_value": number (tender's estimated value),
            "emd_amount": number,
            "price_history": [] (past similar tenders),
            "target_margin": number (optional, default 12%)
        }
        """
        
        tender_id = input_data.get('tender_id', 'Unknown')
        boq = input_data.get('boq', {})
        vendor_quotes = input_data.get('vendor_quotes', [])
        estimated_value = input_data.get('estimated_value', 0)
        emd_amount = input_data.get('emd_amount', 0)
        price_history = input_data.get('price_history', [])
        target_margin = input_data.get('target_margin', 12)
        
        # Extract costs from BOQ
        our_total_cost = boq.get('total_our_value', 0)
        if not our_total_cost and boq.get('line_items'):
            our_total_cost = sum(item.get('total_amount', 0) for item in boq.get('line_items', []))
        
        # Get lowest vendor quotes if available
        if vendor_quotes:
            vendor_prices = [q.get('total_quoted_value', 0) for q in vendor_quotes]
            lowest_vendor_quote = min(vendor_prices) if vendor_prices else 0
        else:
            lowest_vendor_quote = 0
        
        prompt = f"""
        Generate pricing strategy for tender:
        
        Tender ID: {tender_id}
        Estimated Tender Value: ₹{estimated_value:,.2f}
        EMD Amount: ₹{emd_amount:,.2f}
        Our Base Cost: ₹{our_total_cost:,.2f}
        Lowest Vendor Quote: ₹{lowest_vendor_quote:,.2f if lowest_vendor_quote else 0}
        Target Margin: {target_margin}%
        
        BOQ Summary:
        - Total Items: {len(boq.get('line_items', []))}
        - BOQ Total: ₹{boq.get('total_our_value', 0):,.2f}
        
        Vendor Quotes Received: {len(vendor_quotes)}
        {json.dumps([{'vendor': q.get('vendor_name'), 'total': q.get('total_quoted_value')} for q in vendor_quotes], indent=2) if vendor_quotes else 'No vendor quotes'}
        
        Historical Data:
        {json.dumps(price_history, indent=2) if price_history else 'No historical data - use industry benchmarks'}
        
        Task:
        Generate 3 pricing scenarios:
        
        1. **Aggressive Scenario**:
           - Minimize margin to maximize win probability
           - Target L1 position
           - Margin: 5-8%
           - Calculate bid value, profit, win probability (0.7-0.9)
           - List risks (low margin, tight delivery, price pressure)
           - List advantages (high win chance, market share, future business)
        
        2. **Balanced Scenario**:
           - Standard industry margin
           - Good profitability with reasonable win chance
           - Margin: 10-15%
           - Calculate bid value, profit, win probability (0.5-0.7)
           - List risks and advantages
        
        3. **Conservative Scenario**:
           - Higher margin for risk buffer
           - Lower win probability but better profitability if won
           - Margin: 18-25%
           - Calculate bid value, profit, win probability (0.2-0.4)
           - List risks and advantages
        
        Recommend ONE scenario based on:
        - EMD amount (high = fewer competitors)
        - Tender complexity
        - Our capacity and resources
        - Strategic importance
        
        Provide competitor intelligence:
        - Estimate number of bidders (based on EMD, complexity)
        - Predict likely L1 price
        - Predict our rank in each scenario
        - Market dynamics assessment
        
        Add price optimization suggestions.
        
        Return ONLY valid JSON in PricingReport schema format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'scenarios' not in result or len(result.get('scenarios', [])) != 3:
                result['needs_correction'] = True
            
            # Ensure generation_timestamp
            if 'generation_timestamp' not in result:
                from datetime import datetime, timezone
                result['generation_timestamp'] = datetime.now(timezone.utc).isoformat()
            
            if 'confidence_score' not in result:
                result['confidence_score'] = 0.85
            
            return result
            
        except json.JSONDecodeError:
            return {
                "tender_id": tender_id,
                "scenarios": [],
                "recommended_scenario": "balanced",
                "competitor_intelligence": {
                    "estimated_competitors": 0,
                    "market_dynamics": "Unable to analyze"
                },
                "price_optimization_suggestions": ["Manual pricing analysis required"],
                "error": "JSON parsing failed",
                "confidence_score": 0.3,
                "needs_correction": True
            }
