"""
SentinelAI — Central configuration.

Loads environment variables (see .env.example) into a typed Settings object
using pydantic-settings. Import `settings` anywhere in the app instead of
reading os.environ directly.

TODO
----
[ ] Define a Settings(BaseSettings) class mapping every env var:
    HF_API_TOKEN, GROQ_API_KEY, NEO4J_*, REDIS_URL, SUPABASE_*, WHATSAPP_*.
[ ] Provide sensible defaults for local development.
[ ] Expose a cached `get_settings()` accessor.
"""
