import logging
from uuid import UUID
from typing import Dict
from app.services.retell_service import RetellService
from app.database.client import get_supabase

logger = logging.getLogger(__name__)

class CallService:
    def __init__(self):
        self.retell_service = RetellService()
        self.supabase = get_supabase()
    
    async def initiate_call(
        self,
        conversation_id: UUID,
        driver_name: str,
        load_number: str,
        retell_agent_id: str
    ) -> Dict:
        logger.info(f"Initiating call for conversation: {conversation_id}")
        
        try:
            call_data = await self.retell_service.create_web_call(
                agent_id=retell_agent_id,
                metadata={
                    "conversation_id": str(conversation_id),
                    "driver_name": driver_name,
                    "load_number": load_number
                },
                retell_llm_dynamic_variables={
                    "driver_name": driver_name,
                    "load_number": load_number
                }
            )
            logger.info(f"Created web call: {call_data['call_id']}")
        except Exception as e:
            logger.error(f"Failed to create web call: {e}")
            raise
        
        self.supabase.table("conversations").update({
            "retell_call_id": call_data["call_id"],
            "retell_access_token": call_data["access_token"],
            "call_type": "web_call"
        }).eq("id", str(conversation_id)).execute()
        
        logger.info(f"Successfully initiated call for conversation: {conversation_id}")
        return call_data

