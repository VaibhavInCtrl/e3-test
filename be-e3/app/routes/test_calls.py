import logging
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from app.models.conversation import ConversationResponse, ConversationStatus
from app.models.driver import DriverCreate
from app.services.agent_service import AgentService
from app.services.driver_service import DriverService
from app.services.conversation_service import ConversationService
from app.services.call_service import CallService
from app.services.webhook_service import WebhookService
from app.dependencies import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/test-calls", tags=["test-calls"])

class StartTestCallRequest(BaseModel):
    agent_id: UUID
    driver_id: Optional[UUID] = None
    driver_name: Optional[str] = None
    driver_phone: Optional[str] = None
    load_number: str

@router.post("/start", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def start_test_call(
    request: StartTestCallRequest,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to start test call for agent: {request.agent_id}")
    
    try:
        agent_service = AgentService()
        driver_service = DriverService()
        conversation_service = ConversationService()
        call_service = CallService()
        
        agent = await agent_service.get_agent(request.agent_id)
        
        if request.driver_id:
            driver = await driver_service.get_driver(request.driver_id)
        else:
            if not request.driver_name or not request.driver_phone:
                logger.warning("Missing driver information in test call request")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Either driver_id or both driver_name and driver_phone must be provided"
                )
            driver = await driver_service.create_driver(
                DriverCreate(name=request.driver_name, phone_number=request.driver_phone)
            )
        
        from app.models.conversation import ConversationCreate
        conversation = await conversation_service.create_conversation(
            ConversationCreate(
                agent_id=agent.id,
                driver_id=driver.id,
                load_number=request.load_number
            )
        )
        
        await agent_service.update_last_used(agent.id)
        
        await conversation_service.update_conversation_status(
            conversation.id,
            ConversationStatus.IN_PROGRESS
        )
        
        if not agent.retell_agent_id:
            logger.error(f"Agent missing Retell agent ID: {agent.id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Agent does not have a Retell agent ID. Please recreate the agent."
            )
        
        call_data = await call_service.initiate_call(
            conversation.id,
            driver.name,
            request.load_number,
            agent.retell_agent_id
        )
        
        updated_conversation = await conversation_service.get_conversation(conversation.id)
        logger.info(f"Successfully started test call: {conversation.id}")
        return updated_conversation
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in start_test_call endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start test call: {str(e)}"
        )

@router.post("/{conversation_id}/end", dependencies=[Depends(verify_api_key)])
async def end_test_call(conversation_id: UUID):
    logger.info(f"API request to end test call: {conversation_id}")
    
    from app.database.client import get_supabase
    import asyncio
    
    try:
        supabase = get_supabase()
        
        conversation_result = supabase.table("conversations").select("*").eq(
            "id", str(conversation_id)
        ).execute()
        
        if not conversation_result.data:
            logger.warning(f"Conversation not found for end call: {conversation_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        conversation = conversation_result.data[0]
        retell_call_id = conversation.get("retell_call_id")
        
        if retell_call_id:
            logger.info(f"Ending call with Retell call ID: {retell_call_id}")
            await asyncio.sleep(2)
            
            try:
                webhook_service = WebhookService()
                await webhook_service.handle_call_ended({"call_id": retell_call_id})
            except Exception as e:
                logger.error(f"Error processing call end via webhook: {e}")
                supabase.table("conversations").update({
                    "status": ConversationStatus.COMPLETED.value
                }).eq("id", str(conversation_id)).execute()
        else:
            logger.info(f"No Retell call ID found, marking conversation as completed: {conversation_id}")
            supabase.table("conversations").update({
                "status": ConversationStatus.COMPLETED.value
            }).eq("id", str(conversation_id)).execute()
        
        logger.info(f"Successfully ended test call: {conversation_id}")
        return {"status": "success", "message": "Call ended and processing initiated"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in end_test_call endpoint: {e}")
        return {"status": "error", "message": f"Call ended but processing may be delayed: {str(e)}"}
