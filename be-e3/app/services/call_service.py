from uuid import UUID
from typing import Dict
from app.services.retell_service import RetellService
from app.services.prompt_generation_service import PromptGenerationService
from app.database.client import get_supabase

class CallService:
    def __init__(self):
        self.retell_service = RetellService()
        self.prompt_service = PromptGenerationService()
        self.supabase = get_supabase()
    
    async def initiate_call(
        self,
        conversation_id: UUID,
        driver_phone: str,
        driver_name: str,
        load_number: str,
        retell_agent_id: str,
        system_prompt: str
    ) -> Dict:
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
        
        self.supabase.table("conversations").update({
            "retell_call_id": call_data["call_id"],
            "retell_access_token": call_data["access_token"],
            "call_type": "web_call"
        }).eq("id", str(conversation_id)).execute()
        
        return call_data

