from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from app.config import settings
from app.agents.orchestrator import orchestrator
from app.services.whatsapp_service import whatsapp_service
from app.agents.citizen_shield_prompts import format_shield_response
from app.core.logging import logger

router = APIRouter(prefix="/webhook", tags=["WhatsApp Webhook"])

@router.get("/whatsapp")
async def verify_webhook(request: Request):
    """Webhook verification for Meta."""
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    
    if mode and token:
        if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
            return int(challenge)
        raise HTTPException(status_code=403, detail="Verification token mismatch")
    raise HTTPException(status_code=400, detail="Missing parameters")

@router.post("/whatsapp")
async def receive_message(request: Request, bg_tasks: BackgroundTasks):
    """Receive and process inbound WhatsApp messages."""
    payload = await request.json()
    
    # Log raw payload for debugging (safely)
    logger.debug("Received WhatsApp Webhook event")
    
    try:
        # Extract message details
        # Meta's payload structure is deeply nested
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return {"status": "ok"} # Ack status updates
            
        msg = messages[0]
        from_number = msg.get("from")
        msg_type = msg.get("type")
        
        # Only process text for now (audio would require downloading media from FB servers)
        if msg_type == "text":
            text = msg.get("text", {}).get("body", "")
            
            # Fire and forget processing to avoid blocking the webhook response
            bg_tasks.add_task(process_whatsapp_message, from_number, text)
            
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        # Always return 200 to WhatsApp so they don't retry endlessly
        return {"status": "ok"}

async def process_whatsapp_message(phone: str, text: str):
    """Background task to process the message and send a reply."""
    try:
        # 1. Analyze via Orchestrator
        state = await orchestrator.process_threat(
            session_id=f"WA-{phone}", # Using phone as session ID for continuity
            message=text
        )
        
        # 2. Format reply
        reply = format_shield_response(
            risk_level=state["risk_level"],
            explanation=state["explanation"],
            action=state["recommended_action"]
        )
        
        # 3. Send reply via WhatsApp API
        await whatsapp_service.send_message(phone, reply)
        
    except Exception as e:
        logger.error(f"Error in process_whatsapp_message: {str(e)}")
