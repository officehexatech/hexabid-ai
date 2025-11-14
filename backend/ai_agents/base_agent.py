from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
import uuid
import json

class BaseAgent(ABC):
    """
    Base class for all HexaBid AI Agents.
    Each agent specializes in a specific task and can communicate with other agents.
    """
    
    def __init__(self, agent_type: str, model: str = "gpt-4o-mini", provider: str = "openai"):
        self.agent_type = agent_type
        self.model = model
        self.provider = provider
        self.api_key = os.getenv('EMERGENT_LLM_KEY')
        self.session_id = f"{agent_type}_{uuid.uuid4().hex[:8]}"
        self.chat = None
        self.execution_log = []
        
    def initialize_chat(self, system_message: str):
        """Initialize the LLM chat with system message"""
        self.chat = LlmChat(
            api_key=self.api_key,
            session_id=self.session_id,
            system_message=system_message
        ).with_model(self.provider, self.model)
        
    async def execute(self, input_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute the agent's task.
        Returns structured output that can be used by other agents.
        """
        try:
            self.log_execution("started", {"input": input_data})
            
            # Agent-specific processing
            result = await self._process(input_data, context or {})
            
            # Self-correction through reasoning
            if result.get('needs_correction', False):
                result = await self._self_correct(result, input_data)
            
            self.log_execution("completed", {"output": result})
            
            return {
                "agent": self.agent_type,
                "status": "success",
                "result": result,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "execution_log": self.execution_log
            }
            
        except Exception as e:
            self.log_execution("error", {"error": str(e)})
            return {
                "agent": self.agent_type,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "execution_log": self.execution_log
            }
    
    @abstractmethod
    async def _process(self, input_data: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Agent-specific processing logic - to be implemented by subclasses"""
        pass
    
    async def _self_correct(self, result: Dict[str, Any], original_input: Dict[str, Any]) -> Dict[str, Any]:
        """Self-correction through reasoning"""
        correction_prompt = f"""
        Review the following output and correct any errors or inconsistencies:
        
        Original Input: {json.dumps(original_input, indent=2)}
        Current Output: {json.dumps(result, indent=2)}
        
        Provide the corrected output in the same format.
        """
        
        message = UserMessage(text=correction_prompt)
        response = await self.chat.send_message(message)
        
        try:
            corrected = json.loads(response)
            self.log_execution("self_corrected", {"before": result, "after": corrected})
            return corrected
        except:
            # If parsing fails, return original
            return result
    
    def log_execution(self, stage: str, data: Dict[str, Any]):
        """Log execution steps for debugging and monitoring"""
        self.execution_log.append({
            "stage": stage,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        })
    
    def format_output_for_next_agent(self, data: Any) -> str:
        """Format output for consumption by next agent"""
        return json.dumps(data, indent=2)
