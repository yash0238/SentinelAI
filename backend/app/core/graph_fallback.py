"""
A pure Python fallback for Graph operations when Neo4j is not available.
Uses mock data shaped like the frontend's expected output.
"""
import uuid
from typing import Dict, Any, List

class NetworkXFallback:
    def __init__(self):
        self.reports = []
        self.entities = {}
        
    def ingest_report(self, report: dict):
        self.reports.append(report)
        return True

    def get_clusters(self) -> Dict[str, Any]:
        """Returns the exact same mock shape as the Streamlit app for the hackathon demo."""
        return {
            "cluster_id": "RING-007",
            "nodes": [
                {"id": "V1", "label": "Victim A", "type": "victim"},
                {"id": "V2", "label": "Victim B", "type": "victim"},
                {"id": "V3", "label": "Victim C", "type": "victim"},
                {"id": "P1", "label": "+91 98••• 210", "type": "phone"},
                {"id": "P2", "label": "+91 90••• 774", "type": "phone"},
                {"id": "U1", "label": "mule1@upi", "type": "upi"},
                {"id": "U2", "label": "mule2@upi", "type": "upi"},
                {"id": "U3", "label": "collector@upi", "type": "upi"},
                {"id": "D1", "label": "Device 4F:A2", "type": "device"},
                {"id": "S1", "label": "Suspect X", "type": "suspect"},
            ],
            "edges": [
                {"source": "V1", "target": "P1", "label": "received call"},
                {"source": "V2", "target": "P1", "label": "received call"},
                {"source": "V3", "target": "P2", "label": "received call"},
                {"source": "P1", "target": "D1", "label": "linked device"},
                {"source": "P2", "target": "D1", "label": "linked device"},
                {"source": "V1", "target": "U1", "label": "transferred"},
                {"source": "V2", "target": "U2", "label": "transferred"},
                {"source": "V3", "target": "U2", "label": "transferred"},
                {"source": "U1", "target": "U3", "label": "funneled"},
                {"source": "U2", "target": "U3", "label": "funneled"},
                {"source": "D1", "target": "S1", "label": "operated by"},
                {"source": "U3", "target": "S1", "label": "controlled by"},
            ],
        }

    def ego_network(self, entity_id: str) -> Dict[str, Any]:
        cluster = self.get_clusters()
        # Find all edges connected to this entity
        connected_edges = [e for e in cluster["edges"] if e["source"] == entity_id or e["target"] == entity_id]
        
        # Find all connected nodes
        connected_node_ids = set([entity_id])
        for e in connected_edges:
            connected_node_ids.add(e["source"])
            connected_node_ids.add(e["target"])
            
        connected_nodes = [n for n in cluster["nodes"] if n["id"] in connected_node_ids]
        
        return {
            "cluster_id": f"EGO-{entity_id}",
            "nodes": connected_nodes,
            "edges": connected_edges
        }

networkx_fallback = NetworkXFallback()
