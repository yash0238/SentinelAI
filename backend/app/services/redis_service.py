"""
Service: Redis wrapper — active scam-call session state & chat memory.

Why
---
During a live "digital arrest" demo the AI must remember the running context
of a call (turns so far, accumulating risk score). Redis holds this ephemeral
state keyed by session/user id with a short TTL.

Functions (planned)
-------------------
- set_session(session_id, state, ttl)
- get_session(session_id)
- append_turn(session_id, turn)
- clear_session(session_id)

TODO
----
[ ] Implement using redis-py (async) with REDIS_URL from settings.
[ ] JSON-serialise state; set a sensible TTL (e.g., 1 hour).
"""
