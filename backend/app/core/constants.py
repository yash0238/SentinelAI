# Shared constants

SCAM_SCRIPT_LABELS = [
    "digital arrest / fake CBI or ED officer",
    "KYC / bank account update fraud",
    "fake courier or parcel scam",
    "investment or stock trading scam",
    "loan app extortion",
    "electricity bill disconnection scam",
    "SIM swap / telecom fraud",
    "legitimate / not a scam",
]

SUPPORTED_LANGUAGES = [
    "Hindi",
    "English",
    "Marathi",
    "Tamil",
    "Telugu",
    "Bengali",
    "Kannada",
    "Gujarati",
    "Malayalam",
    "Odia",
    "Punjabi",
    "Assamese"
]

# Risk score thresholds mapping to RiskLevel enum
RISK_THRESHOLDS = {
    "CRITICAL": 85,
    "HIGH": 65,
    "MEDIUM": 40,
    "LOW": 0
}

def get_risk_level(score: int) -> str:
    if score >= RISK_THRESHOLDS["CRITICAL"]:
        return "CRITICAL"
    if score >= RISK_THRESHOLDS["HIGH"]:
        return "HIGH"
    if score >= RISK_THRESHOLDS["MEDIUM"]:
        return "MEDIUM"
    return "LOW"

# Mock recipients for alerts
ALERT_RECIPIENTS = {
    "mha_nodal_officer": "mha.alerts@gov.in",
    "cyber_helpline": "1930"
}
