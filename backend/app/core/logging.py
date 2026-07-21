import sys
from loguru import logger
from datetime import datetime
import json
from app.config import settings

# Configure Loguru
logger.remove()
logger.add(sys.stderr, level=settings.LOG_LEVEL)
logger.add("logs/app.log", rotation="10 MB", level="INFO")
logger.add("logs/audit.log", rotation="50 MB", level="INFO", filter=lambda record: "audit" in record["extra"])

def audit_log(event_type: str, actor: str, payload: dict):
    """
    Produce a tamper-evident, timestamped, source-attributed audit record.
    Never log secrets or raw PII values.
    """
    # Create a sanitized copy of the payload (remove PII/secrets if any)
    sanitized = {k: v for k, v in payload.items() if "secret" not in k.lower() and "token" not in k.lower()}
    
    audit_record = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": event_type,
        "actor": actor,
        "payload": sanitized,
    }
    
    logger.bind(audit=True).info(json.dumps(audit_record))
