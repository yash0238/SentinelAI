"""
Service: Neo4j graph database wrapper (fraud-network intelligence).

Graph model (proposed)
----------------------
Nodes:  (:Victim), (:Suspect), (:Phone), (:UPI), (:IP), (:Device), (:Report)
Edges:  (:Victim)-[:FILED]->(:Report)
        (:Report)-[:INVOLVES]->(:Phone|:UPI|:IP|:Device)
        (:Phone)-[:LINKED_TO]->(:Device)  etc.

Functions (planned)
-------------------
- ingest_report(report)      -> MERGE nodes + relationships.
- detect_clusters()          -> community detection to surface fraud rings.
- ego_network(entity_id)     -> subgraph for dashboard visualisation.
- build_intel_package(cluster_id) -> auditable, source-attributed export.

Design notes
------------
- Use the official neo4j driver; connection from settings.NEO4J_*.
- Provide a NetworkX fallback (see graph_fallback.py) when Neo4j is offline.

TODO
----
[ ] Implement connection pool + context-managed sessions.
[ ] Write parameterised Cypher (never string-format user input).
"""
