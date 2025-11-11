from fastapi import APIRouter, Depends, status
from typing import List
from uuid import UUID
from app.models.driver import DriverCreate, DriverUpdate, DriverResponse
from app.services.driver_service import DriverService
from app.dependencies import verify_api_key

router = APIRouter(prefix="/api/drivers", tags=["drivers"])

@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(
    driver: DriverCreate,
    _: str = Depends(verify_api_key)
):
    service = DriverService()
    return await service.create_driver(driver)

@router.get("/", response_model=List[DriverResponse])
async def list_drivers(_: str = Depends(verify_api_key)):
    service = DriverService()
    return await service.list_drivers()

@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = DriverService()
    return await service.get_driver(driver_id)

@router.put("/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: UUID,
    driver: DriverUpdate,
    _: str = Depends(verify_api_key)
):
    service = DriverService()
    return await service.update_driver(driver_id, driver)

@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    driver_id: UUID,
    _: str = Depends(verify_api_key)
):
    service = DriverService()
    await service.delete_driver(driver_id)

