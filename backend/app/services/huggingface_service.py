import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.config import settings
from app.core.logging import logger

class HuggingFaceService:
    def __init__(self):
        self.headers = {"Authorization": f"Bearer {settings.HF_API_TOKEN}"}
        self.base_url = "https://api-inference.huggingface.co/models"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def _request(self, model: str, data, is_json=True):
        if settings.DEMO_MODE_FALLBACK and not settings.HF_API_TOKEN:
            return self._mock_response(model, data)
            
        url = f"{self.base_url}/{model}"
        async with httpx.AsyncClient() as client:
            if is_json:
                response = await client.post(url, headers=self.headers, json=data)
            else:
                response = await client.post(url, headers=self.headers, data=data)
                
            response.raise_for_status()
            return response.json()

    async def classify_audio(self, audio_bytes: bytes) -> dict:
        """Synthetic vs. human voice classification."""
        result = await self._request(settings.HF_AUDIO_MODEL, audio_bytes, is_json=False)
        # Assuming the model returns a list of dicts with 'label' and 'score'
        # e.g. [{"label": "fake", "score": 0.95}, {"label": "real", "score": 0.05}]
        if isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], list): # sometimes HF returns nested list
                result = result[0]
            
            synthetic_score = 0.0
            for item in result:
                label = item.get("label", "").lower()
                if "fake" in label or "synthetic" in label or "spoof" in label:
                    synthetic_score += item.get("score", 0.0)
                    
            # If no explicit fake label, just take top label if it's suspicious
            if synthetic_score == 0.0 and len(result) > 0:
                # Naive fallback for demo if model shape is unexpected
                pass
                
            return {"synthetic_probability": synthetic_score, "raw": result}
            
        return {"synthetic_probability": 0.0, "raw": result}

    async def zero_shot_classify(self, text: str, labels: list[str]) -> dict:
        """Scam-script category + confidence."""
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": labels}
        }
        result = await self._request(settings.HF_ZEROSHOT_MODEL, payload)
        
        if isinstance(result, dict) and "labels" in result and "scores" in result:
            return {
                "top_label": result["labels"][0],
                "confidence": result["scores"][0],
                "all_scores": dict(zip(result["labels"], result["scores"]))
            }
        return {"top_label": "unknown", "confidence": 0.0}

    async def classify_image(self, image_bytes: bytes) -> dict:
        """Banknote authenticity signal."""
        result = await self._request(settings.HF_VISION_MODEL, image_bytes, is_json=False)
        return {"raw": result}

    def _mock_response(self, model, data):
        """Fallback for when API keys are not present."""
        if model == settings.HF_AUDIO_MODEL:
            # We don't have the filename here to do clever mocking like the frontend,
            # so we'll just return a random-ish value
            return [{"label": "fake", "score": 0.85}, {"label": "real", "score": 0.15}]
            
        elif model == settings.HF_ZEROSHOT_MODEL:
            text = data.get("inputs", "").lower()
            labels = data.get("parameters", {}).get("candidate_labels", [])
            
            top_label = "digital arrest / fake CBI or ED officer" if "arrest" in text or "cbi" in text else \
                        "fake courier or parcel scam" if "parcel" in text else \
                        "OTP / UPI PIN phishing" if "otp" in text else \
                        "legitimate / not a scam"
                        
            return {
                "labels": [top_label] + [l for l in labels if l != top_label],
                "scores": [0.95] + [0.01] * (len(labels) - 1)
            }
            
        elif model == settings.HF_VISION_MODEL:
            return [{"label": "counterfeit", "score": 0.9}]
            
        return []

hf_service = HuggingFaceService()
