"""
Route: Digital Arrest Scam Alerting.

Endpoints (planned)
-------------------
POST /scam/analyze-audio    -> accepts a voice note, returns synthetic-voice
                               probability + scam-script classification + verdict.
POST /scam/analyze-session  -> accepts call-flow metadata (numbers, timing,
                               spoofing signature) and returns a live-session
                               risk score.
GET  /scam/session/{id}     -> current state of an active monitored scam call
                               (backed by Redis).

Flow
----
This route delegates to the LangGraph orchestrator (app.agents.orchestrator)
which fuses the audio deepfake service + scam-script classifier + number
reputation lookup into a single verdict.

TODO
----
[ ] Define APIRouter(prefix="/scam", tags=["Scam Detection"]).
[ ] Wire request/response schemas from app.models.schemas.
[ ] Call orchestrator.run_scam_pipeline(...).
"""
