from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from app.database.client import get_supabase
from app.models.driver import DriverCreate, DriverUpdate, DriverResponse

class DriverService:
    def __init__(self):
        self.supabase = get_supabase()
    
    async def create_driver(self, driver: DriverCreate) -> DriverResponse:
        result = self.supabase.table("drivers").insert({
            "name": driver.name,
            "phone_number": driver.phone_number
        }).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create driver"
            )
        
        return DriverResponse(**result.data[0])
    
    async def get_driver(self, driver_id: UUID) -> DriverResponse:
        result = self.supabase.table("drivers").select("*").eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        return DriverResponse(**result.data[0])
    
    async def list_drivers(self) -> List[DriverResponse]:
        result = self.supabase.table("drivers").select("*").execute()
        return [DriverResponse(**driver) for driver in result.data]
    
    async def update_driver(self, driver_id: UUID, driver: DriverUpdate) -> DriverResponse:
        update_data = {k: v for k, v in driver.model_dump().items() if v is not None}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        result = self.supabase.table("drivers").update(update_data).eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )
        
        return DriverResponse(**result.data[0])
    
    async def delete_driver(self, driver_id: UUID) -> None:
        result = self.supabase.table("drivers").delete().eq("id", str(driver_id)).execute()
        
        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Driver not found"
            )

