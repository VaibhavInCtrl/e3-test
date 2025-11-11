from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class AgentCreate(BaseModel):
    name: str
    prompts: str
    additional_details: Optional[str] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    prompts: Optional[str] = None
    additional_details: Optional[str] = None

class AgentResponse(BaseModel):
    id: UUID
    name: str
    prompts: str
    additional_details: Optional[str]
    created_at: datetime
    last_used_at: Optional[datetime]

class AgentListResponse(BaseModel):
    id: UUID
    name: str
    created_at: datetime
    last_used_at: Optional[datetime]
    conversation_count: int

