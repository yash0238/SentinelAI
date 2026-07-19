"""
SentinelAI — Individual LangGraph node functions.

Each node is a small, testable function that takes the shared graph State,
performs one action (call a service, transform data), and returns a partial
state update. Keeping nodes thin makes the graph easy to reason about.

Planned nodes
-------------
- classify_intent(state)
- run_audio_detection(state)
- run_script_classification(state)
- lookup_number_reputation(state)
- fuse_signals(state)
- generate_explanation(state)
- log_and_alert(state)

TODO
----
[ ] Implement each node against the corresponding service.
[ ] Keep side effects (logging/alerts) isolated to the final nodes.
"""
