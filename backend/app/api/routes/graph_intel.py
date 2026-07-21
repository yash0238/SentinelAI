from fastapi import APIRouter, Depends
from app.models.schemas import ClusterResult, GraphIngestRequest
from app.services.neo4j_service import neo4j_service
from app.core.security import verify_le_token

router = APIRouter(prefix="/graph", tags=["Graph Intelligence"])

@router.post("/ingest", status_code=201)
async def ingest_report(
    req: GraphIngestRequest,
    token: str = Depends(verify_le_token)
):
    """
    Manually ingest entity relationships from a report into the Neo4j graph.
    Requires Law Enforcement API Token.
    """
    await neo4j_service.ingest_report(req.model_dump())
    return {"status": "success"}

@router.get("/clusters", response_model=ClusterResult)
async def get_clusters(token: str = Depends(verify_le_token)):
    """
    Run community detection and return active fraud rings.
    Requires Law Enforcement API Token.
    """
    data = await neo4j_service.detect_clusters()
    return ClusterResult(**data)

@router.get("/entity/{entity_id}", response_model=ClusterResult)
async def get_ego_network(
    entity_id: str,
    token: str = Depends(verify_le_token)
):
    """
    Get 1st and 2nd degree connections for a specific entity.
    Requires Law Enforcement API Token.
    """
    data = await neo4j_service.ego_network(entity_id)
    return ClusterResult(**data)

@router.get("/package/{cluster_id}")
async def generate_intel_package(
    cluster_id: str,
    token: str = Depends(verify_le_token)
):
    """
    Generate an intelligence package for prosecution.
    Requires Law Enforcement API Token.
    """
    return await neo4j_service.build_intel_package(cluster_id)
