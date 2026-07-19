"""
SentinelAI — NetworkX in-memory graph fallback.

If Neo4j is unavailable (no sandbox, offline demo), this module provides the
same ingest/cluster/ego-network operations backed by an in-memory NetworkX
graph so the fraud-network feature still demos convincingly.

TODO
----
[ ] Mirror the neo4j_service function signatures.
[ ] Use networkx.community for cluster detection.
"""
