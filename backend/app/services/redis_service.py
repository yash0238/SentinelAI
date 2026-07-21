import json
from app.config import settings
from app.core.logging import logger

# Try importing redis
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class RedisService:
    def __init__(self):
        self.url = settings.REDIS_URL
        self.client = None
        self.use_fallback = not REDIS_AVAILABLE or settings.DEMO_MODE_FALLBACK
        self.mock_store = {} # In-memory fallback

    async def connect(self):
        if self.use_fallback:
            return
        try:
            self.client = redis.from_url(self.url)
            await self.client.ping()
        except Exception as e:
            logger.warning(f"Redis connection failed, using in-memory fallback: {e}")
            self.use_fallback = True

    async def close(self):
        if self.client:
            await self.client.close()

    async def set_session(self, session_id: str, state: dict, ttl: int = 3600):
        if self.use_fallback:
            self.mock_store[session_id] = state
            return
            
        await self.client.set(session_id, json.dumps(state), ex=ttl)

    async def get_session(self, session_id: str) -> dict:
        if self.use_fallback:
            return self.mock_store.get(session_id)
            
        data = await self.client.get(session_id)
        return json.loads(data) if data else None

    async def append_turn(self, session_id: str, turn: dict):
        state = await self.get_session(session_id) or {"turns": []}
        state["turns"] = state.get("turns", []) + [turn]
        await self.set_session(session_id, state)

    async def clear_session(self, session_id: str):
        if self.use_fallback:
            self.mock_store.pop(session_id, None)
            return
            
        await self.client.delete(session_id)

redis_service = RedisService()
