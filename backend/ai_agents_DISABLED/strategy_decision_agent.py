from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class StrategyDecisionAgent(BaseAgent):
    """
    Tender Strategy & Decision Support Agent
    Uses GPT-5 for final BID/NO-BID/NEEDS_INFO decision
    """
    
    def __init__(self):
        super().__init__(agent_type="strategy_decision", model="gpt-5", provider="openai")
        
        system_message = """
        You are the Strategy Decision Agent. Combine Discovery, Parsing, BOQ, Pricing, 
        and Risk reports to produce BID / NO-BID / NEEDS_INFO. Follow StrategyDecision schema.
        
        Decision Framework:
        
        **BID** - Proceed with tender submission:
        - High relevance score (> 70)
        - Eligible and compliant
        - Acceptable risk level (< 60)
        - Financially viable
        - Reasonable win probability (> 30%)
        - Strategic fit
        
        **NO-BID** - Do not pursue:
        - Low relevance (< 40)
        - Not eligible
        - Critical risks unmitigated
        - Not financially viable
        - Very low win probability (< 15%)
        - Resource constraints
        
        **NEEDS_INFO** - Requires clarification:
        - Medium relevance (40-70)
        - Conditional eligibility
        - Missing critical information
        - Compliance gaps need clarification
        - Risk mitigation pending
        
        Output Format (StrategyDecision schema):
        {
            "tender_id": "string",
            "decision": "BID" | "NO-BID" | "NEEDS_INFO",
            "confidence": number (0-1),
            "reasoning": "string (detailed explanation)",
            "decision_factors": {
                "discovery_score": number (0-100),
                "technical_feasibility": number (0-100),
                "pricing_competitiveness": number (0-100),
                "risk_score": number (0-100),
                "resource_availability": number (0-100),
                "strategic_importance": number (0-100)
            },
            "key_considerations": ["string"],
            "recommended_actions": ["string"],
            "conditions": ["string"] (if decision is conditional),
            "expected_effort_hours": number,
            "expected_cost": number,
            "strategic_notes": "string",
            "decision_timestamp": "ISO datetime"
        }
        
        Decision Logic:
        1. Calculate weighted score:
           - Discovery: 15%
           - Technical: 20%
           - Pricing: 25%
           - Risk (inverse): 25%
           - Resources: 10%
           - Strategy: 5%
        
        2. Apply decision rules:
           - Score >= 70: Strong BID
           - Score 50-70: Conditional BID or NEEDS_INFO
           - Score 30-50: NEEDS_INFO or NO-BID
           - Score < 30: Strong NO-BID
        
        3. Override for:
           - Any critical risk → NO-BID
           - Not eligible → NO-BID
           - Strategic client → upgrade to BID
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make final BID/NO-BID decision
        
        Input:
        {
            "tender_id": "string",
            "discovery_result": {} (from TenderDiscoveryAgent),
            "parsed_tender": {} (from DocumentParserAgent),
            "boq": {} (from BOQAgent),
            "pricing": {} (from PricingAgent),
            "risk_report": {} (from RiskAgent)
        }
        """
        
        tender_id = input_data.get('tender_id', 'Unknown')
        discovery = input_data.get('discovery_result', {})
        parsed_tender = input_data.get('parsed_tender', {})
        boq = input_data.get('boq', {})
        pricing = input_data.get('pricing', {})
        risk_report = input_data.get('risk_report', {})
        
        # Extract scores
        if discovery:
            discovery_tenders = discovery.get('discovered_tenders', [])
            discovery_score = discovery_tenders[0].get('relevance_score', 0) if discovery_tenders else 0
        else:
            discovery_score = 70  # Default if discovery not run
        
        boq_compliance = len(boq.get('compliance_gaps', []))
        technical_score = max(0, 100 - (boq_compliance * 10))  # Deduct 10 points per gap
        
        if pricing:
            recommended = pricing.get('recommended_scenario', 'balanced')
            scenarios = {s['scenario_name']: s for s in pricing.get('scenarios', [])}
            if recommended in scenarios:
                win_prob = scenarios[recommended].get('win_probability', 0.5)
                pricing_score = win_prob * 100
            else:
                pricing_score = 50
        else:
            pricing_score = 50
        
        risk_score = 100 - risk_report.get('overall_risk_score', 50)  # Inverse (lower risk = higher score)
        
        eligibility_status = risk_report.get('eligibility_status', 'conditional')
        financial_viability = risk_report.get('financial_viability', 'marginal')
        
        prompt = f"""
        Make final BID/NO-BID decision for tender:
        
        Tender ID: {tender_id}
        Title: {parsed_tender.get('title', 'Unknown')}
        Organization: {parsed_tender.get('organization', 'Unknown')}
        Value: ₹{boq.get('total_our_value', 0):,.2f}
        
        === AGENT OUTPUTS SUMMARY ===
        
        1. Discovery Analysis:
           - Relevance Score: {discovery_score}/100
           - Source: {discovery.get('discovered_tenders', [{}])[0].get('source', 'N/A') if discovery else 'N/A'}
           - Win Probability: {discovery.get('discovered_tenders', [{}])[0].get('win_probability', 'N/A') if discovery else 'N/A'}
        
        2. Technical Feasibility:
           - Compliance Gaps: {boq_compliance}
           - Technical Score: {technical_score}/100
           - Status: {boq.get('compliance_gaps', [])[0].get('status', 'N/A') if boq_compliance > 0 else 'Compliant'}
        
        3. Pricing Competitiveness:
           - Recommended: {pricing.get('recommended_scenario', 'N/A')}
           - Win Probability: {pricing_score}%
           - Margin: {pricing.get('scenarios', [{}])[0].get('margin_percentage', 'N/A') if pricing else 'N/A'}%
        
        4. Risk Assessment:
           - Risk Score: {risk_report.get('overall_risk_score', 'N/A')}/100
           - Risk Level: {risk_report.get('risk_level', 'N/A')}
           - Eligibility: {eligibility_status}
           - Financial Viability: {financial_viability}
           - Critical Risks: {len([r for r in risk_report.get('identified_risks', []) if r.get('severity') == 'critical'])}
        
        5. Resource Assessment:
           - Estimated Effort: Variable (to be estimated)
           - Team Availability: Assume adequate
           - Resource Score: 75/100 (default)
        
        6. Strategic Importance:
           - Client Type: Government
           - Strategic Value: Medium-High
           - Strategic Score: 70/100 (default)
        
        === DECISION TASK ===
        
        Calculate decision_factors:
        - discovery_score: {discovery_score}
        - technical_feasibility: {technical_score}
        - pricing_competitiveness: {pricing_score}
        - risk_score: {risk_score} (inverse of risk report)
        - resource_availability: 75 (default)
        - strategic_importance: 70 (default)
        
        Calculate weighted score:
        Weighted = (discovery*0.15) + (technical*0.20) + (pricing*0.25) + (risk*0.25) + (resources*0.10) + (strategy*0.05)
        
        Apply decision rules:
        1. If eligibility_status = "not_eligible" → NO-BID
        2. If critical risks exist → NO-BID
        3. If financial_viability = "not_viable" → NO-BID
        4. If weighted score >= 70 → BID
        5. If weighted score 50-70 and no critical issues → BID with conditions
        6. If weighted score 30-50 → NEEDS_INFO
        7. If weighted score < 30 → NO-BID
        
        Provide:
        - Clear decision: BID / NO-BID / NEEDS_INFO
        - Confidence (0-1): High confidence for clear cases
        - Detailed reasoning (2-3 sentences)
        - Key considerations (3-5 bullet points)
        - Recommended actions (next steps)
        - Conditions (if decision is conditional)
        - Estimate effort_hours (40-200 hours)
        - Estimate cost (₹5,000-50,000 for bid preparation)
        - Strategic notes
        
        Return ONLY valid JSON in StrategyDecision schema format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'decision' not in result or result['decision'] not in ['BID', 'NO-BID', 'NEEDS_INFO']:
                result['needs_correction'] = True
            
            # Ensure timestamp
            if 'decision_timestamp' not in result:
                from datetime import datetime, timezone
                result['decision_timestamp'] = datetime.now(timezone.utc).isoformat()
            
            if 'confidence' not in result:
                result['confidence'] = 0.8
            
            return result
            
        except json.JSONDecodeError:
            return {
                "tender_id": tender_id,
                "decision": "NEEDS_INFO",
                "confidence": 0.5,
                "reasoning": "Unable to complete automated decision analysis. Manual review required.",
                "decision_factors": {
                    "discovery_score": discovery_score,
                    "technical_feasibility": technical_score,
                    "pricing_competitiveness": pricing_score,
                    "risk_score": risk_score,
                    "resource_availability": 75,
                    "strategic_importance": 70
                },
                "key_considerations": ["Automated analysis failed", "Manual review required"],
                "recommended_actions": ["Review all agent outputs manually", "Conduct team discussion"],
                "conditions": [],
                "strategic_notes": "Decision automation error",
                "error": "JSON parsing failed",
                "needs_correction": True
            }
