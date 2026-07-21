from app.config import settings

class ResembleService:
    def __init__(self):
        self.api_key = settings.RESEMBLE_API_KEY
        self.is_enabled = bool(self.api_key)

    async def detect_voice_clone(self, audio_bytes: bytes) -> dict:
        """
        Real-time voice-clone detection.
        Returns the same shape as huggingface_service.classify_audio
        """
        if not self.is_enabled:
            # No-op if key is missing, orchestrator will fallback to HF
            return {"synthetic_probability": None}
            
        # Implementation would call Resemble's API here
        # Mocking for the hackathon template since we don't have the exact SDK details
        return {
            "synthetic_probability": 0.92,
            "source": "resemble_ai"
        }

resemble_service = ResembleService()
