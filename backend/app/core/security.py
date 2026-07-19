"""
SentinelAI — Security helpers.

Covers:
- API key / token verification for protected law-enforcement endpoints.
- WhatsApp webhook signature verification.
- Input sanitisation helpers (media size/type limits).
- PII redaction utilities for logs.

SECURITY NOTE
-------------
The law-enforcement dashboard and graph-intelligence endpoints MUST be
authenticated before any real deployment. For the hackathon demo a simple
shared-token guard is acceptable, but this gap must be called out in the pitch
and README disclaimer.

TODO
----
[ ] Implement a dependency that checks a bearer token.
[ ] Implement verify_whatsapp_signature(request).
[ ] Add file validation (max size, allowed mime types).
"""
