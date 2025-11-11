from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

class AgentCreate(BaseModel):
    name: str
    prompts: str
    additional_details: Optional[str] = None
    scenario_description: Optional[str] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    prompts: Optional[str] = None
    additional_details: Optional[str] = None
    scenario_description: Optional[str] = None

class AgentResponse(BaseModel):
    id: UUID
    name: str
    prompts: str
    additional_details: Optional[str]
    scenario_description: Optional[str]
    system_prompt: Optional[str]
    retell_agent_id: Optional[str]
    created_at: datetime
    last_used_at: Optional[datetime]

class AgentListResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    last_used_at: Optional[datetime]
    conversation_count: int

class GeneratePromptRequest(BaseModel):
    scenario_description: str
    additional_context: Optional[str] = None

class GeneratePromptResponse(BaseModel):
    system_prompt: str

