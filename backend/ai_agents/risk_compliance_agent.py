from typing import Dict, Any
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class RiskComplianceAgent(BaseAgent):
    """
    Risk & Compliance Audit Agent
    Uses GPT-5 for comprehensive risk evaluation and compliance checking
    """
    
    def __init__(self):
        super().__init__(agent_type="risk_compliance", model="gpt-5", provider="openai")
        
        system_message = """
        You are the Risk Agent. Evaluate tender eligibility, technical compliance, 
        financial viability and produce a RiskReport with risk_score, issues, and mitigation steps.
        
        Risk Categories:
        1. Eligibility: Do we meet basic tender requirements?
        2. Technical: Can we deliver per specifications?
        3. Financial: Is the project financially viable?
        4. Delivery: Can we meet deadlines and quantities?
        5. Legal: Any legal/contractual red flags?
        6. Reputational: Impact on company reputation?
        
        Risk Severity Levels:
        - Critical: Showstopper, must address before bidding
        - High: Significant risk, needs mitigation plan
        - Medium: Manageable risk, monitor closely
        - Low: Minimal risk, standard management
        
        Output Format (RiskReport schema):
        {
            "tender_id": "string",
            "overall_risk_score": number (0-100, 0=low risk, 100=high risk),
            "risk_level": "low" | "medium" | "high" | "critical",
            "identified_risks": [
                {
                    "category": "eligibility|technical|financial|delivery|legal|reputational",
                    "description": "string",
                    "severity": "critical" | "high" | "medium" | "low",
                    "probability": number (0-1),
                    "impact": "string",
                    "mitigation_steps": ["string"]
                }
            ],
            "compliance_checks": [
                {
                    "requirement": "string",
                    "status": "pass" | "fail" | "needs_clarification",
                    "evidence": "string",
                    "notes": "string"
                }
            ],
            "eligibility_status": "eligible" | "not_eligible" | "conditional",
            "financial_viability": "viable" | "marginal" | "not_viable",
            "recommendation": "string",
            "confidence_score": number (0-1),
            "assessment_timestamp": "ISO datetime"
        }
        
        Risk Scoring:
        - 0-25: Low risk (green light)
        - 26-50: Medium risk (proceed with caution)
        - 51-75: High risk (significant mitigation needed)
        - 76-100: Critical risk (consider NO-BID)
        
        Eligibility Checks:
        - Turnover requirements
        - Experience requirements
        - Technical certifications
        - Financial standing
        - Past performance
        - Blacklist status
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate risks and compliance
        
        Input:
        {
            "tender_id": "string",
            "parsed_tender": {} (from DocumentParserAgent),
            "boq": {} (from BOQAgent),
            "pricing": {} (from PricingAgent),
            "company_profile": {} (from context),
            "past_performance": [] (optional)
        }
        """
        
        tender_id = input_data.get('tender_id', 'Unknown')
        parsed_tender = input_data.get('parsed_tender', {})
        boq = input_data.get('boq', {})
        pricing = input_data.get('pricing', {})
        company_profile = context.get('company_profile', {})
        past_performance = input_data.get('past_performance', [])
        
        # Extract key data
        technical_requirements = parsed_tender.get('technical_requirements', [])
        emd_amount = parsed_tender.get('emd_details', {}).get('amount', 0)
        tender_value = boq.get('total_our_value', 0)
        compliance_gaps = boq.get('compliance_gaps', [])
        
        prompt = f"""
        Perform comprehensive risk and compliance assessment for tender:
        
        Tender ID: {tender_id}
        Organization: {parsed_tender.get('organization', 'Unknown')}
        Tender Value: ₹{tender_value:,.2f}
        EMD Amount: ₹{emd_amount:,.2f}
        
        Company Profile:
        - Name: {company_profile.get('companyName', 'Unknown')}
        - Industry: {company_profile.get('industry', 'Unknown')}
        - GST: {company_profile.get('gstin', 'Not provided')}
        
        Technical Requirements:
        {json.dumps(technical_requirements[:10], indent=2) if technical_requirements else 'Not available'}
        
        BOQ Compliance Gaps:
        {json.dumps(compliance_gaps, indent=2) if compliance_gaps else 'No gaps identified'}
        
        Pricing Analysis:
        - Recommended Scenario: {pricing.get('recommended_scenario', 'Not available')}
        - Win Probability: {pricing.get('scenarios', [{}])[0].get('win_probability', 'N/A')}
        
        Past Performance:
        {json.dumps(past_performance, indent=2) if past_performance else 'No historical data'}
        
        Task:
        Conduct comprehensive risk assessment:
        
        1. **Eligibility Risks**:
           - Check turnover requirements (assume company turnover = tender_value * 3)
           - Check experience requirements
           - Check certifications
           - EMD payment capability
           - Status: eligible / not_eligible / conditional
        
        2. **Technical Risks**:
           - Can we meet all specifications?
           - Do we have required expertise?
           - Any compliance gaps from BOQ?
           - Product availability
        
        3. **Financial Risks**:
           - Working capital requirements
           - Payment terms risk
           - Margin adequacy
           - Financial viability: viable / marginal / not_viable
        
        4. **Delivery Risks**:
           - Can we meet deadlines?
           - Supply chain reliability
           - Installation/commissioning capacity
           - Resource availability
        
        5. **Legal Risks**:
           - Penalty clauses
           - Liquidated damages
           - Warranty/AMC obligations
           - Payment terms
        
        6. **Reputational Risks**:
           - Impact of failure
           - Client importance
           - Public sector visibility
        
        For each risk:
        - Describe clearly
        - Assign severity (critical/high/medium/low)
        - Estimate probability (0-1)
        - Explain impact
        - Provide 2-3 mitigation steps
        
        Compliance Checks:
        - List each major requirement
        - Status: pass / fail / needs_clarification
        - Provide evidence or notes
        
        Calculate overall_risk_score (0-100):
        - Weight: Eligibility 25%, Technical 25%, Financial 20%, Delivery 15%, Legal 10%, Reputational 5%
        - If any CRITICAL risk exists, score >= 75
        
        Provide final recommendation:
        - If risk_score < 40 and eligible: "Proceed with bid"
        - If risk_score 40-60: "Proceed with mitigation plan"
        - If risk_score > 60: "High risk - consider carefully"
        - If critical risks: "Recommend NO-BID unless critical risks addressed"
        
        Return ONLY valid JSON in RiskReport schema format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'identified_risks' not in result or 'compliance_checks' not in result:
                result['needs_correction'] = True
            
            # Ensure timestamp
            if 'assessment_timestamp' not in result:
                from datetime import datetime, timezone
                result['assessment_timestamp'] = datetime.now(timezone.utc).isoformat()
            
            if 'confidence_score' not in result:
                result['confidence_score'] = 0.85
            
            # Map risk_score to risk_level if missing
            if 'risk_level' not in result and 'overall_risk_score' in result:
                score = result['overall_risk_score']
                if score <= 25:
                    result['risk_level'] = 'low'
                elif score <= 50:
                    result['risk_level'] = 'medium'
                elif score <= 75:
                    result['risk_level'] = 'high'
                else:
                    result['risk_level'] = 'critical'
            
            return result
            
        except json.JSONDecodeError:
            return {
                "tender_id": tender_id,
                "overall_risk_score": 75,
                "risk_level": "high",
                "identified_risks": [],
                "compliance_checks": [],
                "eligibility_status": "conditional",
                "financial_viability": "marginal",
                "recommendation": "Manual risk assessment required due to analysis failure",
                "error": "JSON parsing failed",
                "confidence_score": 0.3,
                "needs_correction": True
            }
