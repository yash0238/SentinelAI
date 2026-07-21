from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Dict, Any

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# --- Scam Detection ---

class ScamVerdict(BaseModel):
    risk_level: RiskLevel
    risk_score: int = Field(ge=0, le=100)
    scam_type: str
    explanation: str
    matched_signals: Optional[List[str]] = None
    synthetic_voice_probability: Optional[float] = None
    source: str = "ai_pipeline"

class ScamAudioRequest(BaseModel):
    # Handled via UploadFile in FastAPI, but schema can document it
    pass

class SessionRisk(BaseModel):
    session_id: str
    current_risk: RiskLevel
    score: int
    signals_detected: List[str]

# --- Citizen Shield ---

class ShieldChatRequest(BaseModel):
    message: str
    language: Optional[str] = None

class ShieldChatResponse(BaseModel):
    risk_level: RiskLevel
    risk_score: int
    scam_type: str
    explanation: str
    recommended_action: str
    reply_message: str  # The message to send back to the user in their language

# --- Counterfeit ---

class CounterfeitResult(BaseModel):
    authentic: bool
    risk_level: RiskLevel
    risk_score: int
    feature_checklist: Dict[str, bool]
    explanation: str
    source: str = "vision_pipeline"

# --- Graph Intel ---

class GraphIngestRequest(BaseModel):
    report_id: str
    victim_id: Optional[str] = None
    suspect_phone: Optional[str] = None
    suspect_upi: Optional[str] = None
    ip_address: Optional[str] = None
    device_id: Optional[str] = None

class ClusterResult(BaseModel):
    cluster_id: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]

# --- Reports ---

class FraudReport(BaseModel):
    id: str
    created_at: str
    scam_type: str
    risk_level: RiskLevel
    risk_score: int
    language: str
    source: str
    city: str
    lat: float
    lng: float
    amount_involved: int
    status: str

class Hotspot(BaseModel):
    city: str
    lat: float
    lng: float
    count: int
    risk: str
