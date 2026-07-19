"""
Route: WhatsApp Cloud API webhook (citizen interface).

Endpoints (planned)
-------------------
GET  /whatsapp/webhook   -> verification handshake (echo hub.challenge).
POST /whatsapp/webhook   -> inbound messages (text / voice note / image).
                           Routes the payload to the Citizen Shield pipeline
                           and replies with a fraud risk assessment.

This is the "no-frontend" citizen touchpoint: users forward a suspicious voice
note, number, or note image and get an instant verdict.

TODO
----
[ ] Define APIRouter(prefix="/whatsapp", tags=["WhatsApp"]).
[ ] Implement GET verification against WHATSAPP_VERIFY_TOKEN.
[ ] Parse inbound message types, download media, dispatch to services.
[ ] Send reply via whatsapp_service.send_message(...).
"""
