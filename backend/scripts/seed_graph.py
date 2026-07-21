"""
Script to seed Neo4j with a mock fraud network for the network graph demo.
"""
import asyncio
from app.services.neo4j_service import neo4j_service

async def seed_graph():
    await neo4j_service.connect()
    
    if neo4j_service.use_fallback:
        print("Neo4j is not configured or available. Using Python fallback for graph intel.")
        return
        
    print("Seeding graph (MERGE queries would go here)...")
    
    # Example Cypher to create a cluster
    query = """
    MERGE (v1:Victim {id: 'V1', name: 'Victim A'})
    MERGE (v2:Victim {id: 'V2', name: 'Victim B'})
    MERGE (p1:Phone {id: 'P1', number: '+91 98XXX 210'})
    MERGE (d1:Device {id: 'D1', mac: '4F:A2'})
    MERGE (s1:Suspect {id: 'S1', name: 'Suspect X'})
    
    MERGE (v1)-[:RECEIVED_CALL]->(p1)
    MERGE (v2)-[:RECEIVED_CALL]->(p1)
    MERGE (p1)-[:LINKED_DEVICE]->(d1)
    MERGE (d1)-[:OPERATED_BY]->(s1)
    """
    
    if neo4j_service.driver:
        async with neo4j_service.driver.session() as session:
            await session.run(query)
            print("Graph seeded.")
    
    await neo4j_service.close()

if __name__ == "__main__":
    asyncio.run(seed_graph())
