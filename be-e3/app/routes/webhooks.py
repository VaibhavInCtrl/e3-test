import logging
from fastapi import APIRouter, Request, status
from app.services.webhook_service import WebhookService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

@router.post("/retell")
async def retell_webhook(request: Request):
    logger.info("Received Retell webhook")
    
    try:
        payload = await request.json()
        event_type = payload.get("event")
        
        logger.info(f"Processing Retell webhook event: {event_type}")
        
        webhook_service = WebhookService()
        await webhook_service.process_webhook(event_type, payload)
        
        logger.info(f"Successfully processed Retell webhook: {event_type}")
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing Retell webhook: {e}")
        return {"status": "error", "message": str(e)}

