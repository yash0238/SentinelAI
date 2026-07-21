from typing import Dict, Any
from app.services.huggingface_service import hf_service
from app.services.groq_service import groq_service
from app.services.resemble_service import resemble_service
from app.core.constants import SCAM_SCRIPT_LABELS, get_risk_level
from app.core.logging import logger

async def classify_intent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node 1: Determine the type of input and the likely scam category."""
    logger.debug("Entering classify_intent_node")
    
    message = state.get("message", "")
    if not message:
        return state
        
    # 1. Zero-shot classification via HF
    hf_result = await hf_service.zero_shot_classify(message, SCAM_SCRIPT_LABELS)
    top_label = hf_result.get("top_label", "unknown")
    confidence = hf_result.get("confidence", 0.0)
    
    # 2. If confidence is low, fallback to LLM
    if confidence < 0.5:
        top_label = await groq_service.classify_scam_type(message)
        
    state["scam_type"] = top_label
    state["signals"].append(f"Intent classified as {top_label}")
    
    # Simple risk scoring heuristic based on keywords for the pipeline
    score = 10
    lower_msg = message.lower()
    
    if any(k in lower_msg for k in ["arrest", "cbi", "police", "fir", "warrant"]):
        score += 40
        state["signals"].append("Law enforcement coercion detected")
        
    if any(k in lower_msg for k in ["otp", "pin", "cvv", "password"]):
        score += 30
        state["signals"].append("Credential harvesting detected")
        
    if any(k in lower_msg for k in ["urgent", "immediately", "block", "freeze"]):
        score += 20
        state["signals"].append("Urgency/Threat detected")
        
    state["risk_score"] = min(100, score)
    state["risk_level"] = get_risk_level(state["risk_score"])
    
    return state

async def audio_analysis_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node 2: If audio is present, detect voice cloning."""
    logger.debug("Entering audio_analysis_node")
    
    audio_bytes = state.get("audio_bytes")
    if not audio_bytes:
        return state
        
    # Primary: Resemble AI
    result = await resemble_service.detect_voice_clone(audio_bytes)
    prob = result.get("synthetic_probability")
    
    # Fallback: HF Wav2Vec
    if prob is None:
        result = await hf_service.classify_audio(audio_bytes)
        prob = result.get("synthetic_probability", 0.0)
        
    state["synthetic_voice_probability"] = prob
    
    if prob > 0.7:
        state["signals"].append("High probability of synthetic/cloned voice")
        state["risk_score"] = min(100, state.get("risk_score", 0) + 50)
        state["risk_level"] = get_risk_level(state["risk_score"])
        
    return state

async def generate_response_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Node 3: Generate explainable verdict and response."""
    logger.debug("Entering generate_response_node")
    
    # Generate user-friendly explanation
    explanation = await groq_service.generate_verdict_explanation({
        "risk_level": state.get("risk_level"),
        "score": state.get("risk_score"),
        "scam_type": state.get("scam_type"),
        "detected": state.get("signals", [])
    }, lang=state.get("language", "English"))
    
    state["explanation"] = explanation
    
    risk = state.get("risk_level", "LOW")
    if risk in ["CRITICAL", "HIGH"]:
        state["recommended_action"] = "Do not comply. Disconnect and report to 1930."
    elif risk == "MEDIUM":
        state["recommended_action"] = "Verify independently before taking action."
    else:
        state["recommended_action"] = "Stay alert. Never share OTPs."
        
    return state
