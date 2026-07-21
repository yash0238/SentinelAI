from app.config import settings
from app.core.logging import logger

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

class SupabaseService:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self.client = None
        self.use_fallback = not SUPABASE_AVAILABLE or not self.url or not self.key or settings.DEMO_MODE_FALLBACK
        self.mock_store = {}

    def connect(self):
        if self.use_fallback:
            return
        try:
            self.client = create_client(self.url, self.key)
        except Exception as e:
            logger.warning(f"Supabase connection failed, using in-memory fallback: {e}")
            self.use_fallback = True

    async def log_fraud_report(self, report_data: dict):
        """Insert a verified fraud report into Supabase."""
        if self.use_fallback:
            report_id = report_data.get("id", f"MOCK-{len(self.mock_store)}")
            self.mock_store[report_id] = report_data
            return {"status": "success", "id": report_id, "mock": True}
            
        try:
            data, count = self.client.table("fraud_reports").insert(report_data).execute()
            return {"status": "success", "data": data[1]}
        except Exception as e:
            logger.error(f"Failed to log to Supabase: {e}")
            # Fallback for hackathon continuity
            return {"status": "error", "message": str(e), "mock": True}

    async def get_hotspots(self):
        if self.use_fallback:
            # Return some mock data matching the frontend
            return [
                {"city": "Mumbai", "lat": 19.076, "lng": 72.8777, "count": 120, "risk": "CRITICAL"},
                {"city": "Delhi", "lat": 28.6139, "lng": 77.209, "count": 85, "risk": "HIGH"}
            ]
            
        # In a real app, this would be an RPC call or aggregation query
        pass

supabase_service = SupabaseService()
