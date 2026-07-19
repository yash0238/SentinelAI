"""
SentinelAI — Pydantic request/response schemas (the shared data contracts).

Grouping all schemas here keeps the API contract in one place and lets the
frontend generate types from the OpenAPI spec.

Planned models
--------------
- ScamAudioRequest / ScamVerdict
- SessionMetadata / SessionRisk
- ShieldChatRequest / ShieldChatResponse
- CounterfeitResult (feature checklist + score)
- GraphIngestRequest / ClusterResult / IntelPackage
- FraudReport / ReportStats / Hotspot
- RiskLevel enum: LOW | MEDIUM | HIGH | CRITICAL

TODO
----
[ ] Define each BaseModel with field types, examples, and validation.
[ ] Reuse RiskLevel across scam, shield, and counterfeit responses.
"""
