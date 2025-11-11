from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from uuid import UUID

class DriverCreate(BaseModel):
    name: str
    phone_number: str

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone_number: Optional[str] = None

class DriverResponse(BaseModel):
    id: UUID
    name: str
    phone_number: str
    created_at: datetime

