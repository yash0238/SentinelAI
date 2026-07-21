import httpx
from app.config import settings
from app.core.logging import logger

class WhatsAppService:
    def __init__(self):
        self.token = settings.WHATSAPP_TOKEN
        self.phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID
        self.base_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
        self.is_enabled = bool(self.token and self.phone_number_id)

    async def send_message(self, to_phone: str, message: str) -> bool:
        """Send a plain text reply to a user."""
        if not self.is_enabled and settings.DEMO_MODE_FALLBACK:
            logger.info(f"[MOCK WA] Sent to {to_phone}: {message}")
            return True
            
        if not self.is_enabled:
            logger.warning("WhatsApp not configured")
            return False

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }
        
        payload = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message}
        }
        
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.post(self.base_url, json=payload, headers=headers)
                resp.raise_for_status()
                return True
            except httpx.HTTPError as e:
                logger.error(f"WhatsApp API error: {e}")
                return False

whatsapp_service = WhatsAppService()
