"""
SentinelAI — FastAPI application entry point.

Responsibilities
----------------
- Create the FastAPI app instance and apply middleware (CORS, logging).
- Mount all API routers from `app.api.routes`.
- Expose a `/health` endpoint for uptime checks (used by Render/Railway).
- Initialise shared clients (Redis, Neo4j, Supabase) on startup and
  gracefully close them on shutdown.

Run locally:
    uvicorn app.main:app --reload

TODO
----
[ ] Instantiate FastAPI(app_title="SentinelAI", version=...).
[ ] Add CORSMiddleware allowing the frontend origin.
[ ] include_router() for: scam_detection, citizen_shield, counterfeit,
    graph_intel, whatsapp_webhook, reports.
[ ] Startup/shutdown lifespan handlers for external clients.
"""
