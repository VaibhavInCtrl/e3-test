import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.models.driver import DriverCreate, DriverUpdate, DriverResponse
from app.services.driver_service import DriverService
from app.dependencies import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/drivers", tags=["drivers"])

@router.post("/", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
async def create_driver(
    driver: DriverCreate,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to create driver: {driver.name}")
    try:
        service = DriverService()
        result = await service.create_driver(driver)
        logger.info(f"Successfully created driver via API: {result.id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_driver endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create driver: {str(e)}"
        )

@router.get("/", response_model=List[DriverResponse])
async def list_drivers(_: str = Depends(verify_api_key)):
    logger.debug("API request to list drivers")
    try:
        service = DriverService()
        return await service.list_drivers()
    except Exception as e:
        logger.error(f"Error in list_drivers endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list drivers: {str(e)}"
        )

@router.get("/{driver_id}", response_model=DriverResponse)
async def get_driver(
    driver_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.debug(f"API request to get driver: {driver_id}")
    try:
        service = DriverService()
        return await service.get_driver(driver_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_driver endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get driver: {str(e)}"
        )

@router.put("/{driver_id}", response_model=DriverResponse)
async def update_driver(
    driver_id: UUID,
    driver: DriverUpdate,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to update driver: {driver_id}")
    try:
        service = DriverService()
        result = await service.update_driver(driver_id, driver)
        logger.info(f"Successfully updated driver via API: {driver_id}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_driver endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update driver: {str(e)}"
        )

@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_driver(
    driver_id: UUID,
    _: str = Depends(verify_api_key)
):
    logger.info(f"API request to delete driver: {driver_id}")
    try:
        service = DriverService()
        await service.delete_driver(driver_id)
        logger.info(f"Successfully deleted driver via API: {driver_id}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_driver endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete driver: {str(e)}"
        )

