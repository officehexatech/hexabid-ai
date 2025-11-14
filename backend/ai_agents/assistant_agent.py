from typing import Dict, Any, List
from .base_agent import BaseAgent
from emergentintegrations.llm.chat import UserMessage
import json

class AssistantAgent(BaseAgent):
    """
    AI Assistant Agent - Conversational agent for chat, commands, and guidance
    Uses GPT-4o-mini for cost-effective conversational AI
    """
    
    def __init__(self):
        super().__init__(agent_type="ai_assistant", model="gpt-4o-mini", provider="openai")
        
        system_message = """
        You are the HexaBid AI Assistant. Act as conversational agent, execute commands, 
        trigger agents, summarize results, and guide users. Provide structured responses with actions.
        
        Capabilities:
        1. Answer questions about HexaBid features
        2. Explain tender processes and workflows
        3. Summarize agent outputs in plain language
        4. Execute commands ("run discovery", "generate BOQ", "check risks")
        5. Guide users through tender bidding process
        6. Provide recommendations and best practices
        7. Trigger specific agents based on user requests
        
        Available Commands:
        - "discover tenders [category] [location]" → Trigger TenderDiscoveryAgent
        - "parse tender [tender_id]" → Trigger DocumentParserAgent
        - "generate boq [tender_id]" → Trigger BOQAgent
        - "create rfq [tender_id]" → Trigger RFQAgent
        - "analyze pricing [tender_id]" → Trigger PricingAgent
        - "check risks [tender_id]" → Trigger RiskAgent
        - "assemble documents [tender_id]" → Trigger DocumentAssemblyAgent
        - "make decision [tender_id]" → Trigger StrategyAgent
        - "run full workflow [query]" → Run complete pipeline
        
        Output Format (AssistantResponse schema):
        {
            "message": "string (human-readable response)",
            "intent": "string (identified user intent)",
            "actions": [
                {
                    "agent": "string (agent name)",
                    "action": "string (action to perform)",
                    "parameters": {"key": "value"}
                }
            ],
            "data": {"any": "structured data"},
            "suggestions": ["string (next steps suggestions)"],
            "needs_clarification": boolean,
            "clarification_questions": ["string"],
            "confidence_score": number (0-1),
            "response_timestamp": "ISO datetime"
        }
        
        Intent Categories:
        - question: User asking for information
        - command: User requesting action
        - summary: User wants summary of data
        - guidance: User needs help/guidance
        - clarification: Response to assistant's question
        
        Response Style:
        - Friendly and professional
        - Concise but informative
        - Use bullet points for clarity
        - Provide specific next steps
        - Ask clarifying questions when needed
        
        When user intent is unclear:
        - Set needs_clarification = true
        - Ask 2-3 clarifying questions
        - Suggest possible interpretations
        """
        self.initialize_chat(system_message)
    
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process user message and respond with actions
        
        Input:
        {
            "user_message": "string",
            "conversation_history": [] (optional),
            "user_context": {} (user profile, active tenders, etc.)
        }
        """
        
        user_message = input_data.get('user_message', '')
        conversation_history = input_data.get('conversation_history', [])
        user_context = input_data.get('user_context', {})
        
        # Build context for the assistant
        context_summary = f"""
        User Context:
        - Active Tenders: {len(user_context.get('active_tenders', []))}
        - Company: {user_context.get('company_name', 'Unknown')}
        - Credit Balance: {user_context.get('credit_balance', 0)}
        
        Recent Conversation:
        {json.dumps(conversation_history[-5:], indent=2) if conversation_history else 'First message'}
        """
        
        prompt = f"""
        {context_summary}
        
        User Message: "{user_message}"
        
        Task:
        1. Understand user intent
        2. Provide helpful response
        3. If user wants to execute an action, return appropriate agent actions
        4. Suggest next steps
        
        Examples:
        
        User: "Find me tenders for IT hardware in Delhi"
        Response:
        {
            "message": "I'll search for IT hardware tenders in Delhi for you. This will use 10 credits.",
            "intent": "command",
            "actions": [{
                "agent": "tender_discovery",
                "action": "discover",
                "parameters": {"search_query": "IT hardware", "location": "Delhi"}
            }],
            "suggestions": ["Review discovered tenders", "Parse selected tender document"],
            "needs_clarification": false,
            "confidence_score": 0.95
        }
        
        User: "What's the status of my tenders?"
        Response:
        {
            "message": "You have {X} active tenders. [Summary of each]. Would you like details on any specific tender?",
            "intent": "question",
            "actions": [],
            "data": {"active_tenders": [...]},
            "suggestions": ["View tender details", "Check pending actions"],
            "needs_clarification": false,
            "confidence_score": 0.9
        }
        
        User: "Help me bid"
        Response:
        {
            "message": "I can help you with the tender bidding process. Do you want to:\n1. Discover new tenders\n2. Work on an existing tender\n3. Learn about the bidding process?",
            "intent": "guidance",
            "actions": [],
            "suggestions": ["Discover new tenders", "View existing tenders", "Learn workflow"],
            "needs_clarification": true,
            "clarification_questions": ["Which tender would you like to work on?", "What stage are you at?"],
            "confidence_score": 0.7
        }
        
        Return ONLY valid JSON in AssistantResponse schema format.
        """
        
        message = UserMessage(text=prompt)
        response = await self.chat.send_message(message)
        
        try:
            result = json.loads(response)
            
            # Validation
            if 'message' not in result or 'intent' not in result:
                result['needs_correction'] = True
            
            # Ensure timestamp
            if 'response_timestamp' not in result:
                from datetime import datetime, timezone
                result['response_timestamp'] = datetime.now(timezone.utc).isoformat()
            
            if 'confidence_score' not in result:
                result['confidence_score'] = 0.85
            
            # Ensure required fields have defaults
            if 'actions' not in result:
                result['actions'] = []
            if 'suggestions' not in result:
                result['suggestions'] = []
            if 'needs_clarification' not in result:
                result['needs_clarification'] = False
            if 'clarification_questions' not in result:
                result['clarification_questions'] = []
            
            return result
            
        except json.JSONDecodeError:
            return {
                "message": "I apologize, I'm having trouble processing your request. Could you please rephrase?",
                "intent": "error",
                "actions": [],
                "suggestions": ["Try rephrasing your question", "Use specific commands"],
                "needs_clarification": true,
                "clarification_questions": ["What would you like help with?"],
                "confidence_score": 0.3,
                "error": "JSON parsing failed"
            }
