from typing import Dict, Any, List
from datetime import datetime, timezone
import uuid
from .tender_discovery_agent import TenderDiscoveryAgent
from .document_parser_agent import DocumentParserAgent
from .boq_generator_agent import BOQGeneratorAgent
from .document_assembly_agent import DocumentAssemblyAgent
from .rfq_vendor_agent import RFQVendorAgent
from .pricing_strategy_agent import PricingStrategyAgent
from .risk_compliance_agent import RiskComplianceAgent
from .strategy_decision_agent import StrategyDecisionAgent
from .assistant_agent import AssistantAgent

class AgentOrchestrator:
    """
    Orchestrates the multi-agent workflow for tender processing.
    Manages agent communication, data flow, and overall execution.
    """
    
    def __init__(self):
        self.execution_id = str(uuid.uuid4())
        self.workflow_log = []
        self.agents = {}
        
    async def execute_phase1_workflow(
        self,
        workflow_type: str,
        input_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute AI Agent workflow with all 9 agents
        
        Workflow Types:
        - "discover_and_bid": Complete workflow (Discovery -> Parse -> BOQ -> RFQ -> Pricing -> Risk -> Strategy -> Assembly)
        - "parse_and_bid": Start from document parsing
        - "generate_boq": Just generate BOQ from parsed data
        - "assemble_documents": Just assemble final documents
        - "full_analysis": Discovery -> Parse -> BOQ -> RFQ -> Pricing -> Risk -> Strategy (no assembly)
        - "rfq_only": Generate RFQs and parse vendor quotes
        - "pricing_analysis": Analyze pricing scenarios
        - "risk_assessment": Perform risk and compliance audit
        - "decision_support": Make BID/NO-BID decision
        - "chat_assistant": AI assistant conversation
        """
        
        self.log_workflow("workflow_started", {
            "execution_id": self.execution_id,
            "workflow_type": workflow_type,
            "input": input_data
        })
        
        try:
            results = {
                "execution_id": self.execution_id,
                "workflow_type": workflow_type,
                "status": "in_progress",
                "agents_executed": [],
                "results": {},
                "timeline": []
            }
            
            # Execute workflow based on type
            if workflow_type == "discover_and_bid":
                results = await self._execute_full_workflow(input_data, user_context)
            
            elif workflow_type == "parse_and_bid":
                results = await self._execute_parse_workflow(input_data, user_context)
            
            elif workflow_type == "generate_boq":
                results = await self._execute_boq_workflow(input_data, user_context)
            
            elif workflow_type == "assemble_documents":
                results = await self._execute_assembly_workflow(input_data, user_context)
            
            elif workflow_type == "full_analysis":
                results = await self._execute_full_analysis_workflow(input_data, user_context)
            
            elif workflow_type == "rfq_only":
                results = await self._execute_rfq_workflow(input_data, user_context)
            
            elif workflow_type == "pricing_analysis":
                results = await self._execute_pricing_workflow(input_data, user_context)
            
            elif workflow_type == "risk_assessment":
                results = await self._execute_risk_workflow(input_data, user_context)
            
            elif workflow_type == "decision_support":
                results = await self._execute_decision_workflow(input_data, user_context)
            
            elif workflow_type == "chat_assistant":
                results = await self._execute_chat_workflow(input_data, user_context)
            
            else:
                raise ValueError(f"Unknown workflow type: {workflow_type}")
            
            results["status"] = "completed"
            results["workflow_log"] = self.workflow_log
            
            self.log_workflow("workflow_completed", {"results": results})
            
            return results
            
        except Exception as e:
            error_result = {
                "execution_id": self.execution_id,
                "workflow_type": workflow_type,
                "status": "error",
                "error": str(e),
                "workflow_log": self.workflow_log
            }
            self.log_workflow("workflow_error", {"error": str(e)})
            return error_result
    
    async def _execute_full_workflow(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute complete workflow: Discovery -> Parsing -> BOQ -> Assembly"""
        
        results = {
            "agents_executed": [],
            "results": {},
            "timeline": []
        }
        
        # Step 1: Tender Discovery
        discovery_agent = TenderDiscoveryAgent()
        discovery_result = await discovery_agent.execute(input_data, context)
        results["agents_executed"].append("tender_discovery")
        results["results"]["discovery"] = discovery_result
        results["timeline"].append(self._create_timeline_entry("Tender Discovery", discovery_result))
        
        if discovery_result["status"] != "success":
            return results
        
        # Select best tender for processing
        discovered_tenders = discovery_result["result"].get("discovered_tenders", [])
        if not discovered_tenders:
            results["results"]["message"] = "No suitable tenders found"
            return results
        
        best_tender = discovered_tenders[0]  # Highest match_score
        
        # Step 2: Document Parsing
        parser_input = {
            "tender_number": best_tender.get("tender_number"),
            "document_url": best_tender.get("document_url"),
            "document_text": input_data.get("document_text", "")  # If provided
        }
        
        parser_agent = DocumentParserAgent()
        parser_result = await parser_agent.execute(parser_input, context)
        results["agents_executed"].append("document_parser")
        results["results"]["parsing"] = parser_result
        results["timeline"].append(self._create_timeline_entry("Document Parsing", parser_result))
        
        if parser_result["status"] != "success":
            return results
        
        # Step 3: BOQ Generation
        boq_input = {
            "tender_id": best_tender.get("tender_number"),
            "boq_items": parser_result["result"].get("boq_items", []),
            "pricing_strategy": input_data.get("pricing_strategy", "competitive"),
            "target_margin": input_data.get("target_margin", 12),
            "product_catalog": context.get("product_catalog", [])
        }
        
        boq_agent = BOQGeneratorAgent()
        boq_result = await boq_agent.execute(boq_input, context)
        results["agents_executed"].append("boq_generator")
        results["results"]["boq"] = boq_result
        results["timeline"].append(self._create_timeline_entry("BOQ Generation", boq_result))
        
        if boq_result["status"] != "success":
            return results
        
        # Step 4: Document Assembly
        assembly_input = {
            "tender_info": parser_result["result"].get("tender_info"),
            "boq": boq_result["result"],
            "company_profile": context.get("company_profile"),
            "technical_requirements": parser_result["result"].get("technical_requirements", []),
            "mandatory_documents": parser_result["result"].get("mandatory_documents", [])
        }
        
        assembly_agent = DocumentAssemblyAgent()
        assembly_result = await assembly_agent.execute(assembly_input, context)
        results["agents_executed"].append("document_assembly")
        results["results"]["documents"] = assembly_result
        results["timeline"].append(self._create_timeline_entry("Document Assembly", assembly_result))
        
        return results
    
    async def _execute_parse_workflow(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute from parsing onwards (tender already selected)"""
        
        results = {
            "agents_executed": [],
            "results": {},
            "timeline": []
        }
        
        # Start from Document Parsing
        parser_agent = DocumentParserAgent()
        parser_result = await parser_agent.execute(input_data, context)
        results["agents_executed"].append("document_parser")
        results["results"]["parsing"] = parser_result
        results["timeline"].append(self._create_timeline_entry("Document Parsing", parser_result))
        
        if parser_result["status"] != "success":
            return results
        
        # Continue with BOQ and Assembly
        boq_input = {
            "tender_id": input_data.get("tender_number", "Unknown"),
            "boq_items": parser_result["result"].get("boq_items", []),
            "pricing_strategy": input_data.get("pricing_strategy", "competitive"),
            "target_margin": input_data.get("target_margin", 12),
            "product_catalog": context.get("product_catalog", [])
        }
        
        boq_agent = BOQGeneratorAgent()
        boq_result = await boq_agent.execute(boq_input, context)
        results["agents_executed"].append("boq_generator")
        results["results"]["boq"] = boq_result
        results["timeline"].append(self._create_timeline_entry("BOQ Generation", boq_result))
        
        if boq_result["status"] != "success":
            return results
        
        assembly_input = {
            "tender_info": parser_result["result"].get("tender_info"),
            "boq": boq_result["result"],
            "company_profile": context.get("company_profile"),
            "technical_requirements": parser_result["result"].get("technical_requirements", []),
            "mandatory_documents": parser_result["result"].get("mandatory_documents", [])
        }
        
        assembly_agent = DocumentAssemblyAgent()
        assembly_result = await assembly_agent.execute(assembly_input, context)
        results["agents_executed"].append("document_assembly")
        results["results"]["documents"] = assembly_result
        results["timeline"].append(self._create_timeline_entry("Document Assembly", assembly_result))
        
        return results
    
    async def _execute_boq_workflow(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute BOQ generation only"""
        
        results = {
            "agents_executed": [],
            "results": {},
            "timeline": []
        }
        
        boq_agent = BOQGeneratorAgent()
        boq_result = await boq_agent.execute(input_data, context)
        results["agents_executed"].append("boq_generator")
        results["results"]["boq"] = boq_result
        results["timeline"].append(self._create_timeline_entry("BOQ Generation", boq_result))
        
        return results
    
    async def _execute_assembly_workflow(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute document assembly only"""
        
        results = {
            "agents_executed": [],
            "results": {},
            "timeline": []
        }
        
        assembly_agent = DocumentAssemblyAgent()
        assembly_result = await assembly_agent.execute(input_data, context)
        results["agents_executed"].append("document_assembly")
        results["results"]["documents"] = assembly_result
        results["timeline"].append(self._create_timeline_entry("Document Assembly", assembly_result))
        
        return results
    
    def _create_timeline_entry(self, agent_name: str, result: Dict[str, Any]) -> Dict[str, Any]:
        """Create timeline entry for workflow tracking"""
        return {
            "agent": agent_name,
            "timestamp": result.get("timestamp"),
            "status": result.get("status"),
            "duration": "N/A"  # Can be calculated from logs
        }
    
    def log_workflow(self, stage: str, data: Dict[str, Any]):
        """Log workflow execution steps"""
        self.workflow_log.append({
            "stage": stage,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        })
