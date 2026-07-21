from fastapi import APIRouter
import uuid
from app.models.schemas import ShieldChatRequest, ShieldChatResponse
from app.agents.orchestrator import orchestrator
from app.agents.citizen_shield_prompts import format_shield_response

router = APIRouter(prefix="/shield", tags=["Citizen Shield"])

@router.post("/chat", response_model=ShieldChatResponse)
async def chat_with_shield(req: ShieldChatRequest):
    """
    Public-facing endpoint for the Citizen Shield chatbot.
    Analyzes text and returns a safe, helpful response for the citizen.
    """
    session_id = f"CHAT-{uuid.uuid4().hex[:8]}"
    
    # Process through orchestrator
    state = await orchestrator.process_threat(
        session_id=session_id,
        message=req.message,
        language=req.language or "English"
    )
    
    # Format WhatsApp-friendly reply
    reply = format_shield_response(
        risk_level=state["risk_level"],
        explanation=state["explanation"],
        action=state["recommended_action"]
    )
    
    return ShieldChatResponse(
        risk_level=state["risk_level"],
        risk_score=state["risk_score"],
        scam_type=state["scam_type"],
        explanation=state["explanation"],
        recommended_action=state["recommended_action"],
        reply_message=reply
    )
