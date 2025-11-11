from fastapi import APIRouter, Depends
from typing import List
from uuid import UUID
from app.models.conversation import ConversationListResponse, ConversationResponse, ConversationStatusResponse, StructuredDataResponse
from app.models.message import MessageResponse
from app.services.conversation_service import ConversationService
from app.database.client import get_supabase
from app.dependencies import verify_api_key

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

@router.get("/", response_model=List[ConversationListResponse])
async def list_conversations(_: str = Depends(verify_api_key)):
    service = ConversationService()
    return await service.list_conversations()

@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = ConversationService()
    return await service.get_conversation(conversation_id)

@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = ConversationService()
    return await service.get_conversation_messages(conversation_id)

@router.get("/{conversation_id}/status", response_model=ConversationStatusResponse)
async def get_conversation_status(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = ConversationService()
    return await service.get_conversation_status(conversation_id)

@router.get("/{conversation_id}/structured-data", response_model=StructuredDataResponse)
async def get_structured_data(
    conversation_id: UUID,
    _: str = Depends(verify_api_key)
):
    supabase = get_supabase()
    result = supabase.table("conversations").select(
        "id, structured_data, recording_url, duration_ms"
    ).eq("id", str(conversation_id)).execute()
    
    if not result.data:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conv = result.data[0]
    return StructuredDataResponse(
        conversation_id=conv["id"],
        structured_data=conv.get("structured_data"),
        recording_url=conv.get("recording_url"),
        duration_ms=conv.get("duration_ms")
    )

