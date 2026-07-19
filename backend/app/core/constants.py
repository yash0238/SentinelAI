"""
SentinelAI — Shared constants.

Planned contents
----------------
- SCAM_SCRIPT_LABELS: candidate labels for zero-shot classification, e.g.
  ["digital arrest / fake CBI-ED officer", "KYC update fraud",
   "fake courier/parcel scam", "investment / trading scam",
   "loan app extortion", "electricity bill disconnection", "legitimate"].
- SUPPORTED_LANGUAGES: the 12 regional languages for the Citizen Shield.
- RISK_THRESHOLDS: score cut-offs mapping to RiskLevel.
- ALERT_RECIPIENTS: mock MHA / helpline routing config.

TODO
----
[ ] Fill in label lists and thresholds; tune during testing.
"""
