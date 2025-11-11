from typing import List, Optional
from uuid import UUID
from datetime import datetime
from fastapi import HTTPException, status
from app.database.client import get_supabase
from app.models.agent import AgentCreate, AgentUpdate, AgentResponse, AgentListResponse

class AgentService:
    def __init__(self):
        self.supabase = get_supabase()
    
    async def create_agent(self, agent: AgentCreate) -> AgentResponse:
        result = self.supabase.table("agents").insert({
            "name": agent.name,
            "prompts": agent.prompts,
            "additional_details": agent.additional_details
        }).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create agent"
            )
        
        return AgentResponse(**result.data[0])
    
    async def get_agent(self, agent_id: UUID) -> AgentResponse:
        result = self.supabase.table("agents").select("*").eq("id", str(agent_id)).execute()
        
        if not result.data:
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
        update_data = {k: v for k, v in agent.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        result = self.supabase.table("agents").update(update_data).eq("id", str(agent_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
        
        return AgentResponse(**result.data[0])
    
    async def delete_agent(self, agent_id: UUID) -> None:
        result = self.supabase.table("agents").delete().eq("id", str(agent_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Agent not found"
            )
    
    async def update_last_used(self, agent_id: UUID) -> None:
        self.supabase.table("agents").update({
            "last_used_at": datetime.utcnow().isoformat()
        }).eq("id", str(agent_id)).execute()

