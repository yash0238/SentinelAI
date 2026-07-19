"""
SentinelAI — LangGraph multi-agent orchestrator (the "Brain").

This is the fusion layer that routes a query through the right sequence of
tools and produces a single, explainable verdict. Example scam pipeline:

    START
      -> classify_intent        (is this a scam query? what modality?)
      -> [branch] audio?        -> audio_deepfake_service
                  text?         -> scam_script_classifier
                  number?       -> number_reputation_lookup
      -> fuse_signals           (weight + combine into a risk score)
      -> generate_explanation   (Groq/Llama 3 human-readable verdict)
      -> log_and_alert          (Supabase log; MHA alert if high risk)
    END

Keeping orchestration here (not in routes) means every interface — REST,
WhatsApp, IVR — reuses the exact same decision logic.

TODO
----
[ ] Define the LangGraph StateGraph and shared State TypedDict.
[ ] Register nodes wrapping each service in app.services.
[ ] Add conditional edges for modality branching.
[ ] Expose run_scam_pipeline(), run_citizen_shield(), run_counterfeit().
"""
