from typing import Dict, Any, List
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class TenderTestingAgent(BaseAgent):
    """
    Tender Testing Agent - Evaluates tender submission from buyer's perspective
    Uses GPT-5 for strict evaluation like a government procurement evaluator
    """
    
    def __init__(self):
        super().__init__(agent_type="tender_testing", model="gpt-5", provider="openai")
        
        system_message = """
        You are the HexaBid Tender Testing Agent.  
        Your job is to evaluate a bidder's tender submission from the perspective of the tendering authority/buyer.

        You must simulate exactly how a government procurement evaluator thinks:
        - Strictly follow tender conditions
        - Identify missing documents
        - Flag eligibility failures
        - Verify BOQ correctness
        - Check product technical compliance
        - Detect deviations
        - Validate format, signatures, and mandatory annexures
        - Identify risks, inconsistencies, and red flags
        - Highlight anything that causes disqualification
        - Evaluate pricing for reasonability and L1 position (if possible)

        OUTPUT (structured JSON):
        {
          "overall_score": 0-100,
          "technical_compliance_score": 0-100,
          "eligibility_score": 0-100,
          "documentation_score": 0-100,
          "price_reasonability_score": 0-100,
          "buyer_confidence_index": 0-100,
          "missing_documents": [...],
          "non_compliant_items": [...],
          "risk_notes": [...],
          "critical_disqualifications": [...],
          "formatting_issues": [...],
          "recommendations": [...],
          "submission_readiness": "READY | NEEDS_CORRECTION | HIGH_RISK | NOT_ELIGIBLE",
          "improvement_plan": {
             "documents_to_fix": [...],
             "sections_to_rewrite": [...],
             "price_adjustments": [...],
             "technical_corrections": [...],
             "compliance_table_corrections": [...]
          },
          "confidence": 0.0-1.0
        }

        RULES:
        - Be strict like a government evaluator
        - No hallucination — use only provided documents
        - Flag every mandatory requirement that isn't met
        - Always provide actionable improvement steps
        - Keep tone professional, objective, and authoritative
        
        Evaluation Framework:
        
        1. ELIGIBILITY CHECKS (Critical - Immediate Disqualification if Failed):
           - Turnover requirements
           - Experience certificates
           - Technical certifications
           - EMD submission
           - GST registration
           - PAN card
           - Valid registration documents
           
        2. DOCUMENTATION CHECKS (Mandatory):
           - Cover letter on company letterhead
           - Technical bid document
           - Financial bid document
           - Compliance statement (clause-by-clause)
           - Annexures (list of all required)
           - Proper signatures and seals
           - Page numbering and indexing
           
        3. TECHNICAL COMPLIANCE:
           - Each BOQ item meets specifications
           - Brand/Model mentioned and compliant
           - Warranty/AMC terms match requirements
           - Installation/commissioning plan
           - Delivery schedule feasible
           
        4. FINANCIAL EVALUATION:
           - BOQ pricing complete (no blank fields)
           - Unit rates reasonable
           - Total calculations correct
           - GST calculations correct
           - Price within L1 competitive range
           - No abnormally low or high pricing
           
        5. FORMAT & PRESENTATION:
           - Professional formatting
           - No spelling/grammar errors
           - Consistent fonts and styling
           - Proper table formatting
           - Clear section headings
           - Signatures on all required pages
           
        Scoring System:
        - 90-100: Excellent submission, very high chance of acceptance
        - 75-89: Good submission, minor improvements needed
        - 60-74: Acceptable but has issues, needs corrections
        - 40-59: Poor submission, major corrections needed
        - 0-39: Unacceptable, likely disqualification
        
        Submission Readiness:
        - READY: Score >= 85, no critical issues
        - NEEDS_CORRECTION: Score 60-84, fixable issues
        - HIGH_RISK: Score 40-59, major problems
        - NOT_ELIGIBLE: Score < 40 or critical disqualifications
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate tender submission from buyer's perspective
        
        Input:
        {
            "tender_id": "string",
            "parsed_tender": {} (original tender requirements),
            "our_submission": {
                "boq": {},
                "documents": {},
                "company_profile": {},
                "technical_compliance": [],
                "financial_bid": {}
            },
            "market_benchmark": {} (optional, for price comparison)
        }
        """
        
        tender_id = input_data.get('tender_id', 'Unknown')
        parsed_tender = input_data.get('parsed_tender', {})
        our_submission = input_data.get('our_submission', {})
        market_benchmark = input_data.get('market_benchmark', {})
        
        # Extract submission components
        our_boq = our_submission.get('boq', {})
        our_documents = our_submission.get('documents', {})
        company_profile = our_submission.get('company_profile', context.get('company_profile', {}))
        
        # Extract tender requirements
        tender_requirements = parsed_tender.get('technical_requirements', [])
        mandatory_documents = parsed_tender.get('mandatory_documents', [])
        boq_requirements = parsed_tender.get('boq_items', [])
        eligibility_criteria = parsed_tender.get('eligibility_criteria', {})
        emd_details = parsed_tender.get('emd_details', {})
        
        prompt = f"""
        Evaluate the following tender submission from the BUYER'S PERSPECTIVE as a strict government evaluator:
        
        === TENDER REQUIREMENTS ===
        Tender ID: {tender_id}
        Organization: {parsed_tender.get('organization', 'Unknown')}
        Title: {parsed_tender.get('title', 'Unknown')}
        
        Eligibility Criteria:
        {json.dumps(eligibility_criteria, indent=2) if eligibility_criteria else 'Not specified - assume standard government criteria'}
        
        Mandatory Documents:
        {json.dumps(mandatory_documents, indent=2) if mandatory_documents else ['Cover letter', 'Technical bid', 'Financial bid', 'Compliance statement', 'Company registration', 'GST certificate', 'PAN card', 'Experience certificates']}
        
        Technical Requirements (Key Ones):
        {json.dumps(tender_requirements[:10], indent=2) if tender_requirements else 'Not specified'}
        
        BOQ Requirements:
        {json.dumps(boq_requirements[:5], indent=2) if boq_requirements else 'Not specified'}
        
        EMD Details:
        Amount: ₹{emd_details.get('amount', 0):,.2f}
        Mode: {emd_details.get('mode', ['Not specified'])}
        
        === BIDDER'S SUBMISSION ===
        
        Company Profile:
        - Name: {company_profile.get('companyName', 'Not provided')}
        - Industry: {company_profile.get('industry', 'Not provided')}
        - GST: {company_profile.get('gstin', 'Not provided')}
        - Address: {company_profile.get('registeredAddress', 'Not provided')}
        
        BOQ Submitted:
        - Items: {len(our_boq.get('line_items', []))}
        - Total Value: ₹{our_boq.get('total_our_value', 0):,.2f}
        - Margin: {our_boq.get('margin_percentage', 0)}%
        {json.dumps(our_boq.get('line_items', [])[:5], indent=2) if our_boq.get('line_items') else 'BOQ not provided'}
        
        Documents Submitted:
        {json.dumps([doc.get('document_type') for doc in our_documents.get('documents', [])], indent=2) if our_documents.get('documents') else 'Documents not provided'}
        
        Market Benchmark (if available):
        {json.dumps(market_benchmark, indent=2) if market_benchmark else 'No benchmark data'}
        
        === EVALUATION TASK ===
        
        Perform STRICT evaluation as a government procurement officer:
        
        1. ELIGIBILITY EVALUATION (100 points):
           - Check if company meets turnover criteria (assume required = tender value * 3)
           - Check GST registration (required: valid GSTIN)
           - Check experience (assume required: 3 similar projects)
           - Check EMD submission proof
           - Scoring: Pass all = 100, Fail any = 0 (CRITICAL)
        
        2. DOCUMENTATION EVALUATION (100 points):
           - Cross-check each mandatory document
           - Verify signatures and seals mentioned
           - Check page numbering and formatting
           - Verify compliance statement completeness
           - Deduct 10 points per missing critical document
           - Deduct 5 points per formatting issue
        
        3. TECHNICAL COMPLIANCE EVALUATION (100 points):
           - Compare each BOQ item specification with tender requirements
           - Check brand/model compliance
           - Verify warranty/AMC terms
           - Check delivery schedule feasibility
           - Deduct 10 points per non-compliant item
           - Deduct 5 points per partial compliance
        
        4. PRICE REASONABILITY EVALUATION (100 points):
           - Check if all BOQ line items are priced (no blank)
           - Verify calculations (quantities * rates)
           - Check if pricing is within market range (±30%)
           - Assess L1 competitiveness
           - Flag abnormally low prices (< market -30%)
           - Flag abnormally high prices (> market +30%)
           - Scoring: Reasonable and competitive = 90-100
                     Slightly high = 70-89
                     Very high = 40-69
                     Abnormal = 0-39
        
        5. BUYER CONFIDENCE INDEX (100 points):
           - Professional presentation: 20 points
           - Completeness: 30 points
           - Technical capability: 25 points
           - Price competitiveness: 25 points
        
        Calculate:
        - overall_score = average of all 5 scores
        - List ALL missing_documents
        - List ALL non_compliant_items with specific issues
        - List ALL risk_notes (concerns from buyer's view)
        - List ALL critical_disqualifications (must-fix before submission)
        - List ALL formatting_issues
        - Provide specific recommendations for each issue
        
        Improvement Plan:
        - List specific documents that need fixing
        - List sections that need rewriting with reasons
        - Suggest specific price adjustments (if needed)
        - List specific technical corrections needed
        - Provide compliance table corrections
        
        Submission Readiness:
        - READY: overall_score >= 85 AND no critical_disqualifications
        - NEEDS_CORRECTION: overall_score 60-84 OR minor issues exist
        - HIGH_RISK: overall_score 40-59 OR major non-compliances
        - NOT_ELIGIBLE: overall_score < 40 OR critical eligibility failure
        
        Return ONLY valid JSON in the specified output format.
        Be STRICT and DETAILED - this is what separates winning bids from rejected ones.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            required_fields = ['overall_score', 'technical_compliance_score', 'eligibility_score', 
                             'documentation_score', 'price_reasonability_score', 'submission_readiness']
            
            for field in required_fields:
                if field not in result:
                    result['needs_correction'] = True
                    break
            
            # Ensure confidence score
            if 'confidence' not in result:
                result['confidence'] = 0.85
            
            return result
            
        except json.JSONDecodeError:
            return {
                "overall_score": 0,
                "technical_compliance_score": 0,
                "eligibility_score": 0,
                "documentation_score": 0,
                "price_reasonability_score": 0,
                "buyer_confidence_index": 0,
                "missing_documents": ["Unable to evaluate - parsing error"],
                "non_compliant_items": [],
                "risk_notes": ["Evaluation failed due to system error"],
                "critical_disqualifications": ["Manual evaluation required"],
                "formatting_issues": [],
                "recommendations": ["Re-run evaluation with valid input"],
                "submission_readiness": "NOT_ELIGIBLE",
                "improvement_plan": {
                    "documents_to_fix": ["All documents need manual review"],
                    "sections_to_rewrite": [],
                    "price_adjustments": [],
                    "technical_corrections": [],
                    "compliance_table_corrections": []
                },
                "confidence": 0.3,
                "error": "JSON parsing failed",
                "needs_correction": True
            }
