import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.models.agent import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse, GeneratePromptRequest, GeneratePromptResponse
from app.services.agent_service import AgentService
from app.services.prompt_generation_service import PromptGenerationService
from app.dependencies import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.post("/generate-prompt", response_model=GeneratePromptResponse)
async def generate_prompt(
    request: GeneratePromptRequest,
    _: str = Depends(verify_api_key)
):
    logger.info("Generating prompt from scenario description")
    try:
        service = PromptGenerationService()
        system_prompt = await service.generate_system_prompt(
            scenario_description=request.scenario_description,
            additional_context=request.additional_context
        )
        logger.info("Successfully generated prompt")
        return GeneratePromptResponse(system_prompt=system_prompt)
    except Exception as e:
        logger.error(f"Error generating prompt: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate prompt: {str(e)}"
        )

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent: AgentCreate,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to create agent: {agent.name}")
    try:
        service = AgentService()
        result = await service.create_agent(agent)
        logger.info(f"Successfully created agent via API: {result.id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_agent endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )

@router.get("/", response_model=List[AgentListResponse])
async def list_agents(_: str = Depends(verify_api_key)):
    logger.debug("API request to list agents")
    try:
        service = AgentService()
        return await service.list_agents()
    except Exception as e:
        logger.error(f"Error in list_agents endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list agents: {str(e)}"
        )

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.debug(f"API request to get agent: {agent_id}")
    try:
        service = AgentService()
        return await service.get_agent(agent_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_agent endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent: {str(e)}"
        )

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    agent: AgentUpdate,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to update agent: {agent_id}")
    try:
        service = AgentService()
        result = await service.update_agent(agent_id, agent)
        logger.info(f"Successfully updated agent via API: {agent_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_agent endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update agent: {str(e)}"
        )

@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to delete agent: {agent_id}")
    try:
        service = AgentService()
        await service.delete_agent(agent_id)
        logger.info(f"Successfully deleted agent via API: {agent_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_agent endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete agent: {str(e)}"
        )

