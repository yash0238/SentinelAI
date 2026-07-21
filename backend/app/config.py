from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    # HuggingFace
    HF_API_TOKEN: str = ""
    HF_AUDIO_MODEL: str = "facebook/wav2vec2-base-960h"
    HF_ZEROSHOT_MODEL: str = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"
    HF_VISION_MODEL: str = "google/vit-base-patch16-224"

    # Groq (Llama 3)
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192"

    # Resemble AI (Optional)
    RESEMBLE_API_KEY: str = ""

    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "changeme"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Supabase
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""

    # WhatsApp
    WHATSAPP_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    WHATSAPP_VERIFY_TOKEN: str = "sentinelai_verify_token"

    # For hackathon/demo mode where API keys might be missing
    DEMO_MODE_FALLBACK: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Cache the settings
settings = Settings()
