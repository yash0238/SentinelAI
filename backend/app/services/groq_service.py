from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from app.config import settings
from app.core.logging import logger

class GroqService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        if self.api_key:
            self.llm = ChatGroq(
                temperature=0.1,
                groq_api_key=self.api_key,
                model_name=settings.GROQ_MODEL
            )
        else:
            self.llm = None

    async def _invoke(self, messages: list) -> str:
        if not self.llm and settings.DEMO_MODE_FALLBACK:
            return self._mock_response(messages)
            
        if not self.llm:
            logger.warning("Groq API key missing and DEMO_MODE_FALLBACK is False")
            return "Analysis unavailable due to missing API key."
            
        try:
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Groq API error: {str(e)}")
            if settings.DEMO_MODE_FALLBACK:
                return self._mock_response(messages)
            raise

    async def summarise_message(self, text: str, lang: str = "English") -> str:
        """Summarise a panicked victim's message."""
        messages = [
            SystemMessage(content=f"You are a helpful assistant. Summarise the user's message concisely in {lang}, focusing on key facts relevant to a potential fraud case. Keep it under 3 sentences."),
            HumanMessage(content=text)
        ]
        return await self._invoke(messages)

    async def generate_verdict_explanation(self, signals: dict, lang: str = "English") -> str:
        """Human-readable explanation of a verdict."""
        prompt = f"""
        Explain why this is or isn't a scam based on these signals:
        Risk Level: {signals.get('risk_level')}
        Score: {signals.get('score')}/100
        Type: {signals.get('scam_type')}
        Detected signals: {', '.join(signals.get('detected', []))}
        
        Provide a concise, calm explanation in {lang}. Do not give legal advice.
        If high risk, tell them to call 1930.
        """
        messages = [
            SystemMessage(content="You are SentinelAI, a digital public safety assistant."),
            HumanMessage(content=prompt)
        ]
        return await self._invoke(messages)

    async def classify_scam_type(self, text: str) -> str:
        """Quick LLM tag when zero-shot is insufficient."""
        messages = [
            SystemMessage(content="Classify the following text into a scam category. Respond ONLY with the category name (e.g. 'Digital Arrest', 'Phishing', 'Safe')."),
            HumanMessage(content=text)
        ]
        return await self._invoke(messages)
        
    def _mock_response(self, messages) -> str:
        content = " ".join([m.content for m in messages]).lower()
        if "summarise" in content:
            return "The user is reporting a potential scam call from someone claiming to be an official. They are being asked to transfer money."
        elif "explain why" in content:
            if "critical" in content or "high" in content:
                return "This matches a known fraud pattern. Do not transfer any funds or share personal information. Disconnect the call immediately and contact the Cyber Crime Helpline at 1930."
            return "No strong indicators of fraud detected, but always remain cautious when sharing sensitive information."
        elif "classify" in content:
            if "arrest" in content or "cbi" in content:
                return "Digital Arrest"
            return "Suspicious Activity"
        return "Mock Groq Response"

groq_service = GroqService()
