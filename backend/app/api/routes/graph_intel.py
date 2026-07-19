"""
Route: Fraud Network Graph Intelligence.

Endpoints (planned)
-------------------
POST /graph/ingest        -> add a fraud report (phone, UPI id, IP, device
                            fingerprint) as nodes/edges in Neo4j.
GET  /graph/clusters      -> return detected money-mule / fraud-ring clusters.
GET  /graph/entity/{id}   -> ego network for a specific entity (for the
                            law-enforcement dashboard visualisation).
GET  /graph/package/{id}  -> generate a court-admissible intelligence package
                            (auditable, timestamped, source-attributed).

Backed by Neo4j (with a NetworkX local fallback). Clustering surfaces
coordinated networks from otherwise isolated victim reports.

TODO
----
[ ] Define APIRouter(prefix="/graph", tags=["Graph Intelligence"]).
[ ] Implement ingest -> MERGE nodes/edges.
[ ] Community detection query for clusters.
[ ] Serialise intelligence package with provenance metadata.
"""
