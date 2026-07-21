from fastapi import APIRouter, File, UploadFile, Depends
import uuid
from app.models.schemas import ScamVerdict
from app.agents.orchestrator import orchestrator
from app.core.security import verify_le_token, validate_file_upload
from app.core.logging import logger

router = APIRouter(prefix="/scam", tags=["Scam Detection"])

@router.post("/analyze-audio", response_model=ScamVerdict)
async def analyze_audio(
    file: UploadFile = File(...),
    token: str = Depends(verify_le_token)
):
    """
    Process an audio file (intercepted call or voice note) through the LangGraph pipeline.
    Requires Law Enforcement API Token.
    """
    # 1. Validate file
    content = await file.read()
    validate_file_upload(len(content), file.content_type)
    
    session_id = f"AUDIO-{uuid.uuid4().hex[:8]}"
    logger.bind(audit=True).info(f"Received audio analysis request {session_id} from {token}")
    
    # 2. Process through Orchestrator
    # We pass the audio directly, no text transcript required for this specific route
    state = await orchestrator.process_threat(
        session_id=session_id,
        audio_bytes=content,
        message="Voice analysis requested"
    )
    
    # 3. Format response
    return ScamVerdict(
        risk_level=state["risk_level"],
        risk_score=state["risk_score"],
        scam_type=state["scam_type"],
        explanation=state["explanation"],
        matched_signals=state["signals"],
        synthetic_voice_probability=state["synthetic_voice_probability"]
    )
