from typing import Dict
from uuid import UUID
from app.services.retell_service import RetellService
from app.services.conversation_service import ConversationService
from app.services.agent_service import AgentService
from app.services.post_processing_service import PostProcessingService
from app.models.conversation import ConversationStatus
from app.models.message import MessageCreate, MessageRole
from app.database.client import get_supabase

class WebhookService:
    def __init__(self):
        self.retell_service = RetellService()
        self.conversation_service = ConversationService()
        self.agent_service = AgentService()
        self.post_processing_service = PostProcessingService()
        self.supabase = get_supabase()
    
    async def process_webhook(self, event_type: str, payload: Dict) -> None:
        if event_type == "call_started":
            await self.handle_call_started(payload)
        elif event_type == "call_ended":
            await self.handle_call_ended(payload)
        elif event_type == "call_analyzed":
            await self.handle_call_analyzed(payload)
    
    async def handle_call_started(self, payload: Dict) -> None:
        call_id = payload.get("call_id")
        
        conversation = self.supabase.table("conversations").select("*").eq(
            "retell_call_id", call_id
        ).execute()
        
        if conversation.data:
            await self.conversation_service.update_conversation_status(
                UUID(conversation.data[0]["id"]),
                ConversationStatus.IN_PROGRESS
            )
    
    async def handle_call_ended(self, payload: Dict) -> None:
        call_id = payload.get("call_id")
        
        conversation_result = self.supabase.table("conversations").select("*").eq(
            "retell_call_id", call_id
        ).execute()
        
        if not conversation_result.data:
            return
        
        conversation = conversation_result.data[0]
        conversation_id = UUID(conversation["id"])
        
        call_details = await self.retell_service.get_call_details(call_id)
        
        call_analysis = call_details.get("call_analysis")
        if call_analysis and not isinstance(call_analysis, dict):
            if hasattr(call_analysis, 'model_dump'):
                call_analysis = call_analysis.model_dump()
            elif hasattr(call_analysis, 'dict'):
                call_analysis = call_analysis.dict()
            else:
                call_analysis = None
        
        try:
            self.supabase.table("conversations").update({
                "transcript": call_details.get("transcript"),
                "recording_url": call_details.get("recording_url"),
                "duration_ms": call_details.get("duration_ms"),
                "disconnection_reason": call_details.get("disconnection_reason"),
                "call_analysis": call_analysis
            }).eq("id", str(conversation_id)).execute()
        except Exception as e:
            print(f"Error updating conversation: {e}")
        transcript_object = call_details.get("transcript_object", [])
        for msg in transcript_object:
            if isinstance(msg, dict):
                msg_role = msg.get("role")
                msg_content = msg.get("content", "")
            else:
                msg_role = getattr(msg, "role", None)
                msg_content = getattr(msg, "content", "")
            
            role = MessageRole.AGENT if msg_role == "agent" else MessageRole.HUMAN
            
            if msg_content:
                await self.conversation_service.add_message(
                    MessageCreate(
                        conversation_id=conversation_id,
                        role=role,
                        content=msg_content
                    )
                )
        
        agent = await self.agent_service.get_agent(UUID(conversation["agent_id"]))
        
        structured_data = await self.post_processing_service.extract_structured_data(
            transcript=call_details.get("transcript", ""),
            scenario_description=agent.prompts
        )
        print(structured_data)
        self.supabase.table("conversations").update({
            "structured_data": structured_data,
            "status": ConversationStatus.COMPLETED.value
        }).eq("id", str(conversation_id)).execute()
    
    async def handle_call_analyzed(self, payload: Dict) -> None:
        call_id = payload.get("call_id")
        call_analysis = payload.get("call_analysis")
        
        if call_analysis:
            self.supabase.table("conversations").update({
                "call_analysis": call_analysis
            }).eq("retell_call_id", call_id).execute()

