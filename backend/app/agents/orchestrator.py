from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict
import asyncio

from app.agents.nodes import classify_intent_node, audio_analysis_node, generate_response_node
from app.services.supabase_service import supabase_service
from app.services.neo4j_service import neo4j_service
from app.core.logging import logger

# Define the state shape
class AgentState(TypedDict):
    session_id: str
    message: str
    language: str
    audio_bytes: Optional[bytes]
    
    # Computed fields
    scam_type: str
    risk_score: int
    risk_level: str
    signals: List[str]
    synthetic_voice_probability: Optional[float]
    explanation: str
    recommended_action: str

# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("classify", classify_intent_node)
workflow.add_node("audio", audio_analysis_node)
workflow.add_node("response", generate_response_node)

# Add edges (Simple linear flow for the prototype)
workflow.add_edge("classify", "audio")
workflow.add_edge("audio", "response")
workflow.add_edge("response", END)

# Set entry point
workflow.set_entry_point("classify")

# Compile graph
app_graph = workflow.compile()

class Orchestrator:
    """
    The central brain coordinating the multi-agent pipeline.
    Thin routes call this orchestrator.
    """
    
    async def process_threat(self, session_id: str, message: str = "", audio_bytes: bytes = None, language: str = "English") -> Dict[str, Any]:
        """Main entry point for threat processing."""
        logger.bind(audit=True).info(f"Starting threat processing for session {session_id}")
        
        # Initialize state
        initial_state = {
            "session_id": session_id,
            "message": message,
            "language": language,
            "audio_bytes": audio_bytes,
            "scam_type": "unknown",
            "risk_score": 0,
            "risk_level": "LOW",
            "signals": [],
            "synthetic_voice_probability": None,
            "explanation": "",
            "recommended_action": ""
        }
        
        # Execute the LangGraph pipeline
        # invoke is sync in langgraph 0.0.x, but we have async nodes. 
        # Using ainvoke for newer langgraph versions.
        final_state = await app_graph.ainvoke(initial_state)
        
        # Post-processing: Log to DBs if high risk
        if final_state["risk_level"] in ["HIGH", "CRITICAL"]:
            await self._dispatch_alerts(final_state)
            
        return final_state

    async def _dispatch_alerts(self, state: Dict[str, Any]):
        """Background task to log high-risk events to Supabase and Neo4j."""
        logger.info(f"Dispatching alerts for high-risk session {state['session_id']}")
        
        report_data = {
            "id": state["session_id"],
            "scam_type": state["scam_type"],
            "risk_level": state["risk_level"],
            "risk_score": state["risk_score"],
            "language": state["language"],
            "source": "api_pipeline",
            # Mocking location for demo if missing
            "city": "Unknown", 
            "lat": 0.0,
            "lng": 0.0,
            "amount_involved": 0,
            "status": "New"
        }
        
        # Fire and forget DB inserts
        asyncio.create_task(supabase_service.log_fraud_report(report_data))
        
        # Extract entities for graph (simplified for demo)
        graph_data = {
            "report_id": state["session_id"],
            "victim_id": f"V-{state['session_id'][-4:]}",
        }
        asyncio.create_task(neo4j_service.ingest_report(graph_data))

orchestrator = Orchestrator()
