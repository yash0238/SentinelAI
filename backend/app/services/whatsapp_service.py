"""
Service: WhatsApp Cloud API wrapper (outbound + media download).

Functions (planned)
-------------------
- send_message(to, text)         -> send a text reply.
- send_template(to, template)    -> send an approved template message.
- download_media(media_id)       -> fetch voice note / image bytes for
                                    analysis by the AI services.

Design notes
------------
- Uses WHATSAPP_TOKEN + WHATSAPP_PHONE_NUMBER_ID from settings.
- Inbound handling lives in api/routes/whatsapp_webhook.py; this module only
  handles the Graph API calls.

TODO
----
[ ] Implement send_message via POST /{phone_number_id}/messages.
[ ] Implement two-step media download (get URL, then fetch with token).
"""
