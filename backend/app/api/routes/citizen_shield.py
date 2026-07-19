"""
Route: Citizen Fraud Shield (conversational AI).

Endpoints (planned)
-------------------
POST /shield/chat        -> free-text or voice-note query from a citizen;
                            returns a fraud risk assessment + guided next steps
                            in the citizen's language.
POST /shield/report      -> structures a citizen complaint into an NCRB-ready
                            report payload.

Powered by Llama 3 via Groq for fast multilingual summarisation and the
zero-shot classifier for scam-type tagging. Conversation state is cached in
Redis so multi-turn context is preserved during the demo.

TODO
----
[ ] Define APIRouter(prefix="/shield", tags=["Citizen Shield"]).
[ ] Detect language, translate/normalise, classify, respond.
[ ] Persist conversation turns to Redis keyed by user id.
"""
