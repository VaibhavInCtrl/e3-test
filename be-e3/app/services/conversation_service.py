import logging
from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from app.database.client import get_supabase
from app.models.conversation import ConversationCreate, ConversationResponse, ConversationListResponse, ConversationStatusResponse, ConversationStatus
from app.models.message import MessageCreate, MessageResponse

logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(self):
        self.supabase = get_supabase()
    
    async def create_conversation(self, conversation: ConversationCreate) -> ConversationResponse:
        logger.info(f"Creating conversation for agent: {conversation.agent_id}, driver: {conversation.driver_id}")
        
        try:
            result = self.supabase.table("conversations").insert({
                "agent_id": str(conversation.agent_id),
                "driver_id": str(conversation.driver_id),
                "load_number": conversation.load_number,
                "status": ConversationStatus.PENDING.value
            }).execute()
            
            if not result.data:
                logger.error("Failed to create conversation: No data returned")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create conversation"
                )
            
            logger.info(f"Successfully created conversation: {result.data[0]['id']}")
            return ConversationResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create conversation: {str(e)}"
            )
    
    async def get_conversation(self, conversation_id: UUID) -> ConversationResponse:
        result = self.supabase.table("conversations").select("*").eq("id", str(conversation_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return ConversationResponse(**result.data[0])
    
    async def list_conversations(self) -> List[ConversationListResponse]:
        result = self.supabase.table("conversations").select(
            "*, agents(name), drivers(name)"
        ).execute()
        
        conversations = []
        for conv in result.data:
            conversations.append(ConversationListResponse(
                id=conv["id"],
                agent_id=conv["agent_id"],
                agent_name=conv["agents"]["name"],
                driver_id=conv["driver_id"],
                driver_name=conv["drivers"]["name"],
                load_number=conv["load_number"],
                status=conv["status"],
                started_at=conv["started_at"],
                completed_at=conv.get("completed_at")
            ))
        
        return conversations
    
    async def get_conversation_messages(self, conversation_id: UUID) -> List[MessageResponse]:
        result = self.supabase.table("messages").select("*").eq(
            "conversation_id", str(conversation_id)
        ).order("created_at").execute()
        
        return [MessageResponse(**msg) for msg in result.data]
    
    async def get_conversation_status(self, conversation_id: UUID) -> ConversationStatusResponse:
        result = self.supabase.table("conversations").select(
            "id, status, completed_at"
        ).eq("id", str(conversation_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return ConversationStatusResponse(**result.data[0])
    
    async def update_conversation_status(self, conversation_id: UUID, new_status: ConversationStatus) -> None:
        update_data = {"status": new_status.value}
        
        if new_status in [ConversationStatus.COMPLETED, ConversationStatus.FAILED]:
            update_data["completed_at"] = datetime.utcnow().isoformat()
        
        self.supabase.table("conversations").update(update_data).eq("id", str(conversation_id)).execute()
    
    async def add_message(self, message: MessageCreate) -> MessageResponse:
        logger.debug(f"Adding message to conversation: {message.conversation_id}")
        
        try:
            result = self.supabase.table("messages").insert({
                "conversation_id": str(message.conversation_id),
                "role": message.role.value,
                "content": message.content
            }).execute()
            
            if not result.data:
                logger.error(f"Failed to add message: No data returned")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to add message"
                )
            
            return MessageResponse(**result.data[0])
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding message: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to add message: {str(e)}"
            )

