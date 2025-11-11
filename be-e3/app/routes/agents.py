from fastapi import APIRouter, Depends, status
from typing import List
from uuid import UUID
from app.models.agent import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse
from app.services.agent_service import AgentService
from app.dependencies import verify_api_key

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    _: str = Depends(verify_api_key)
):
    service = AgentService()
    return await service.create_agent(agent)

@router.get("/", response_model=List[AgentListResponse])
async def list_agents(_: str = Depends(verify_api_key)):
    service = AgentService()
    return await service.list_agents()

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = AgentService()
    return await service.get_agent(agent_id)

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent: AgentUpdate,
    _: str = Depends(verify_api_key)
):
    service = AgentService()
    return await service.update_agent(agent_id, agent)

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = AgentService()
    await service.delete_agent(agent_id)

