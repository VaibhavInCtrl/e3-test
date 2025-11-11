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
from app.dependencies import verify_api_key

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
    agent_service = AgentService()
    driver_service = DriverService()
    conversation_service = ConversationService()
    call_service = CallService()
    
    agent = await agent_service.get_agent(request.agent_id)
    
    if request.driver_id:
        driver = await driver_service.get_driver(request.driver_id)
    else:
        if not request.driver_name or not request.driver_phone:
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
    
    await call_service.initiate_call(
        conversation.id,
        driver.phone_number,
        agent.prompts
    )
    
    return conversation

