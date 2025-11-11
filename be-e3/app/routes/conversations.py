import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.models.conversation import ConversationListResponse, ConversationResponse, ConversationStatusResponse, StructuredDataResponse
from app.models.message import MessageResponse
from app.services.conversation_service import ConversationService
from app.database.client import get_supabase
from app.dependencies import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/conversations", tags=["conversations"])

@router.get("/", response_model=List[ConversationListResponse])
async def list_conversations(_: str = Depends(verify_api_key)):
    logger.debug("API request to list conversations")
    try:
        service = ConversationService()
        return await service.list_conversations()
    except Exception as e:
        logger.error(f"Error in list_conversations endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list conversations: {str(e)}"
        )

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.debug(f"API request to get conversation: {conversation_id}")
    try:
        service = ConversationService()
        return await service.get_conversation(conversation_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_conversation endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation: {str(e)}"
        )

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.debug(f"API request to get messages for conversation: {conversation_id}")
    try:
        service = ConversationService()
        return await service.get_conversation_messages(conversation_id)
    except Exception as e:
        logger.error(f"Error in get_conversation_messages endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get messages: {str(e)}"
        )

@router.get("/{conversation_id}/status", response_model=ConversationStatusResponse)
async def get_conversation_status(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.debug(f"API request to get status for conversation: {conversation_id}")
    try:
        service = ConversationService()
        return await service.get_conversation_status(conversation_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_conversation_status endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get conversation status: {str(e)}"
        )

@router.get("/{conversation_id}/structured-data", response_model=StructuredDataResponse)
async def get_structured_data(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.debug(f"API request to get structured data for conversation: {conversation_id}")
    try:
        supabase = get_supabase()
        result = supabase.table("conversations").select(
            "id, structured_data, recording_url, duration_ms"
        ).eq("id", str(conversation_id)).execute()
        
        if not result.data:
            logger.warning(f"Conversation not found: {conversation_id}")
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conv = result.data[0]
        return StructuredDataResponse(
            conversation_id=conv["id"],
            structured_data=conv.get("structured_data"),
            recording_url=conv.get("recording_url"),
            duration_ms=conv.get("duration_ms")
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_structured_data endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get structured data: {str(e)}"
        )

