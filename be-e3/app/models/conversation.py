from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID
from enum import Enum

class ConversationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ConversationCreate(BaseModel):
    agent_id: UUID
    driver_id: UUID
    load_number: str

class ConversationResponse(BaseModel):
    id: UUID
    agent_id: UUID
    driver_id: UUID
    load_number: str
    status: ConversationStatus
    started_at: datetime
    completed_at: Optional[datetime]

class ConversationListResponse(BaseModel):
    id: UUID
    agent_id: UUID
    agent_name: str
    driver_id: UUID
    driver_name: str
    load_number: str
    status: ConversationStatus
    started_at: datetime
    completed_at: Optional[datetime]

class ConversationStatusResponse(BaseModel):
    id: UUID
    status: ConversationStatus
    completed_at: Optional[datetime]

