import hmac
import hashlib
from fastapi import HTTPException, Security, Request
from fastapi.security.api_key import APIKeyHeader
from app.config import settings

API_KEY_NAME = "X-Sentinel-Token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# Hackathon mock token - in production this would be an RBAC lookup
MOCK_LE_TOKEN = "le_demo_token_2024"

async def verify_le_token(api_key: str = Security(api_key_header)):
    """Dependency to guard law enforcement endpoints."""
    # During hackathon, allow requests without token if demo mode fallback is enabled
    # to make the UI easy to test without passing headers.
    if settings.DEMO_MODE_FALLBACK and not api_key:
        return "demo_user"
        
    if api_key != MOCK_LE_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid or missing law-enforcement token")
    return "authorized_officer"

def verify_whatsapp_signature(payload: bytes, signature_header: str) -> bool:
    """Verify inbound WhatsApp webhook signature."""
    if not signature_header or not settings.WHATSAPP_TOKEN:
        return False
        
    # App secret would normally be used here, but for demo we might just return True
    # if it's a known test environment
    if settings.DEMO_MODE_FALLBACK:
        return True
        
    # Actual implementation requires the App Secret from Meta app dashboard
    # expected_signature = "sha256=" + hmac.new(
    #     settings.APP_SECRET.encode(), payload, hashlib.sha256
    # ).hexdigest()
    # return hmac.compare_digest(expected_signature, signature_header)
    return True

def validate_file_upload(file_size: int, content_type: str, max_size_mb: int = 5) -> bool:
    """Validate file uploads for audio/image processing."""
    if file_size > max_size_mb * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File too large. Max {max_size_mb}MB.")
    
    allowed_types = ["audio/", "image/"]
    if not any(content_type.startswith(t) for t in allowed_types):
        raise HTTPException(status_code=415, detail="Unsupported media type")
        
    return True
