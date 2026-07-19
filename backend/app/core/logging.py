"""
SentinelAI — Logging & audit configuration.

Two concerns:
1. Application logging (loguru) with LOG_LEVEL from settings.
2. **Audit logging** — because intelligence packages must be court-admissible,
   every verdict and data-ingest action should produce a tamper-evident,
   timestamped, source-attributed audit record.

TODO
----
[ ] Configure loguru sinks (console + rotating file).
[ ] Provide audit_log(event, actor, payload) writing to a dedicated store.
[ ] Never log secrets or raw PII values.
"""
