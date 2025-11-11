import logging
from retell import Retell
from typing import Dict, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class RetellService:
    def __init__(self):
        self.client = Retell(api_key=settings.retell_api_key)
    
    async def create_agent(
        self,
        name: str,
        system_prompt: str,
        voice_id: Optional[str] = None,
        enable_backchanneling: bool = True,
        interruption_sensitivity: float = 0.8
    ) -> Dict:
        logger.info(f"Creating Retell agent: {name}")
        
        try:
            retell_llm = self.client.llm.create(
                general_prompt=system_prompt,
                begin_message="Hi {{driver_name}}, this is dispatch with a check call on load {{load_number}}. Can you give me an update on your status?",
                general_tools=[],
                starting_state="default",
                start_speaker="agent",
                states=[
                    {
                        "name": "default",
                        "edges": []
                    }
                ]
            )
            logger.info(f"Created Retell LLM: {retell_llm.llm_id}")
        except Exception as e:
            logger.error(f"Failed to create Retell LLM: {e}")
            raise
        
        try:
            agent = self.client.agent.create(
                agent_name=name,
                voice_id=voice_id or settings.retell_default_voice_id,
                response_engine={
                    "type": "retell-llm",
                    "llm_id": retell_llm.llm_id
                },
                enable_backchannel=enable_backchanneling,
                interruption_sensitivity=interruption_sensitivity,
                responsiveness=1,
                ambient_sound="coffee-shop",
                backchannel_frequency=0.9,
                backchannel_words=["yeah", "uh-huh", "I see", "got it"],
                end_call_after_silence_ms=30000
            )
            logger.info(f"Created Retell agent: {agent.agent_id}")
        except Exception as e:
            logger.error(f"Failed to create Retell agent: {e}")
            raise
        
        try:
            self.client.agent.publish(agent.agent_id)
            logger.info(f"Published Retell agent: {agent.agent_id}")
        except Exception as e:
            logger.error(f"Failed to publish Retell agent: {e}")
            raise
        
        return {
            "agent_id": agent.agent_id,
            "agent_name": agent.agent_name,
            "llm_id": retell_llm.llm_id
        }
    
    async def create_web_call(
        self,
        agent_id: str,
        metadata: Dict,
        retell_llm_dynamic_variables: Optional[Dict] = None
    ) -> Dict:
        logger.info(f"Creating web call for agent: {agent_id}")
        
        try:
            call = self.client.call.create_web_call(
                agent_id=agent_id,
                metadata=metadata,
                retell_llm_dynamic_variables=retell_llm_dynamic_variables or {}
            )
            logger.info(f"Created web call: {call.call_id}")
        except Exception as e:
            logger.error(f"Failed to create web call: {e}")
            raise
        
        return {
            "call_id": call.call_id,
            "access_token": call.access_token,
            "agent_id": call.agent_id
        }
    
    async def get_call_details(self, call_id: str) -> Dict:
        logger.debug(f"Retrieving call details: {call_id}")
        
        try:
            call = self.client.call.retrieve(call_id)
            logger.info(f"Retrieved call details: {call_id}")
        except Exception as e:
            logger.error(f"Failed to retrieve call details: {e}")
            raise

        return {
            "call_id": call.call_id,
            "agent_id": call.agent_id,
            "call_status": call.call_status,
            "transcript": call.transcript,
            "transcript_object": call.transcript_object,
            "recording_url": call.recording_url,
            "duration_ms": call.duration_ms,
            "disconnection_reason": call.disconnection_reason,
            "call_analysis": call.call_analysis if hasattr(call, 'call_analysis') else None
        }

