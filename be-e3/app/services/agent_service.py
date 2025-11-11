import logging
from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from app.database.client import get_supabase
from app.models.agent import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse
from app.services.prompt_generation_service import PromptGenerationService
from app.services.retell_service import RetellService

logger = logging.getLogger(__name__)

class AgentService:
    def __init__(self):
        self.supabase = get_supabase()
        self.prompt_service = PromptGenerationService()
        self.retell_service = RetellService()
    
    async def create_agent(self, agent: AgentCreate) -> AgentResponse:
        logger.info(f"Creating agent: {agent.name}")
        scenario_desc = agent.scenario_description or agent.prompts
        
        try:
            system_prompt = await self.prompt_service.generate_system_prompt(
                scenario_description=scenario_desc,
                additional_context=agent.additional_details
            )
            logger.info(f"Generated system prompt for agent: {agent.name}")
        except Exception as e:
            logger.error(f"Failed to generate system prompt: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate system prompt: {str(e)}"
            )
        
        try:
            retell_agent = await self.retell_service.create_agent(
                name=agent.name,
                system_prompt=system_prompt
            )
            logger.info(f"Created Retell agent: {retell_agent['agent_id']}")
        except Exception as e:
            logger.error(f"Failed to create Retell agent: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create Retell agent: {str(e)}"
            )
        
        result = self.supabase.table("agents").insert({
            "name": agent.name,
            "prompts": agent.prompts,
            "additional_details": agent.additional_details,
            "scenario_description": scenario_desc,
            "system_prompt": system_prompt,
            "retell_agent_id": retell_agent["agent_id"]
        }).execute()
        
        if not result.data:
            logger.error(f"Failed to insert agent into database: {agent.name}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create agent"
            )
        
        logger.info(f"Successfully created agent: {result.data[0]['id']}")
        return AgentResponse(**result.data[0])
    
    async def get_agent(self, agent_id: UUID) -> AgentResponse:
        logger.debug(f"Fetching agent: {agent_id}")
        result = self.supabase.table("agents").select("*").eq("id", str(agent_id)).execute()
        
        if not result.data:
            logger.warning(f"Agent not found: {agent_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        return AgentResponse(**result.data[0])
    
    async def list_agents(self) -> List[AgentListResponse]:
        agents_result = self.supabase.table("agents").select("*").execute()
        
        agents_list = []
        for agent in agents_result.data:
            conv_result = self.supabase.table("conversations").select("id", count="exact").eq("agent_id", agent["id"]).execute()
            conversation_count = conv_result.count if conv_result.count else 0
            
            agents_list.append(AgentListResponse(
                id=agent["id"],
                name=agent["name"],
                created_at=agent["created_at"],
                last_used_at=agent.get("last_used_at"),
                conversation_count=conversation_count
            ))
        
        return agents_list
    
    async def update_agent(self, agent_id: UUID, agent: AgentUpdate) -> AgentResponse:
        logger.info(f"Updating agent: {agent_id}")
        update_data = {k: v for k, v in agent.model_dump().items() if v is not None}
        
        if not update_data:
            logger.warning(f"No fields to update for agent: {agent_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        if 'prompts' in update_data or 'scenario_description' in update_data:
            logger.info(f"Regenerating system prompt for agent: {agent_id}")
            current_agent = await self.get_agent(agent_id)
            scenario_desc = update_data.get('scenario_description') or update_data.get('prompts') or current_agent.scenario_description or current_agent.prompts
            additional_details = update_data.get('additional_details', current_agent.additional_details)
            
            try:
                system_prompt = await self.prompt_service.generate_system_prompt(
                    scenario_description=scenario_desc,
                    additional_context=additional_details
                )
                logger.info(f"Regenerated system prompt for agent: {agent_id}")
            except Exception as e:
                logger.error(f"Failed to regenerate system prompt: {e}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to regenerate system prompt: {str(e)}"
                )
            
            if current_agent.retell_agent_id:
                try:
                    retell_agent = await self.retell_service.create_agent(
                        name=update_data.get('name', current_agent.name),
                        system_prompt=system_prompt
                    )
                    update_data['retell_agent_id'] = retell_agent['agent_id']
                    logger.info(f"Updated Retell agent: {retell_agent['agent_id']}")
                except Exception as e:
                    logger.error(f"Error updating Retell agent: {e}")
            
            update_data['system_prompt'] = system_prompt
            update_data['scenario_description'] = scenario_desc
        
        result = self.supabase.table("agents").update(update_data).eq("id", str(agent_id)).execute()
        
        if not result.data:
            logger.warning(f"Agent not found for update: {agent_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        logger.info(f"Successfully updated agent: {agent_id}")
        return AgentResponse(**result.data[0])
    
    async def delete_agent(self, agent_id: UUID) -> None:
        logger.info(f"Deleting agent: {agent_id}")
        result = self.supabase.table("agents").delete().eq("id", str(agent_id)).execute()
        
        if not result.data:
            logger.warning(f"Agent not found for deletion: {agent_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        logger.info(f"Successfully deleted agent: {agent_id}")
    
    async def update_last_used(self, agent_id: UUID) -> None:
        self.supabase.table("agents").update({
            "last_used_at": datetime.utcnow().isoformat()
        }).eq("id", str(agent_id)).execute()

