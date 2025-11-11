from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from enum import Enum

class MessageRole(str, Enum):
    AGENT = "agent"
    HUMAN = "human"

class MessageCreate(BaseModel):
    conversation_id: UUID
    role: MessageRole
    content: str

class MessageResponse(BaseModel):
    id: UUID
    conversation_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

