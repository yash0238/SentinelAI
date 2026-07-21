from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.core.logging import logger
from app.services.redis_service import redis_service
from app.services.neo4j_service import neo4j_service
from app.services.supabase_service import supabase_service

from app.api.routes import (
    scam_detection,
    citizen_shield,
    counterfeit,
    graph_intel,
    reports,
    whatsapp_webhook
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting SentinelAI backend...")
    await redis_service.connect()
    await neo4j_service.connect()
    supabase_service.connect()
    
    yield
    
    # Shutdown
    logger.info("Shutting down SentinelAI backend...")
    await redis_service.close()
    await neo4j_service.close()

app = FastAPI(
    title="SentinelAI Core Engine",
    description="Proactive Intelligence for Digital Public Safety",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For hackathon demo. In prod: restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(scam_detection.router)
app.include_router(citizen_shield.router)
app.include_router(counterfeit.router)
app.include_router(graph_intel.router)
app.include_router(reports.router)
app.include_router(whatsapp_webhook.router)

@app.get("/health", tags=["System"])
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "demo_fallback": settings.DEMO_MODE_FALLBACK
    }
