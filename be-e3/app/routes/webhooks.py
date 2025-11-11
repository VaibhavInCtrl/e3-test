from fastapi import APIRouter, Request, status
from app.services.webhook_service import WebhookService

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])

@router.post("/retell")
async def retell_webhook(request: Request):
    payload = await request.json()
    
    event_type = payload.get("event")
    
    webhook_service = WebhookService()
    
    try:
        await webhook_service.process_webhook(event_type, payload)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

