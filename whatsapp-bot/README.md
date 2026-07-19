# SentinelAI — WhatsApp Citizen Interface

The **zero-frontend** citizen touchpoint. A citizen forwards a suspicious voice
note, phone number, or banknote photo to the SentinelAI WhatsApp number and
gets back an instant fraud risk assessment plus guided NCRB reporting steps.

## How it works

```
Citizen (WhatsApp)
   │  forwards voice note / number / image
   ▼
WhatsApp Cloud API  ──webhook──▶  backend /whatsapp/webhook
                                      │
                                      ▼
                          orchestrator (LangGraph)
                          ├─ audio → deepfake detection
                          ├─ text  → scam-script classifier
                          └─ image → counterfeit vision
                                      │
                                      ▼
                          Groq/Llama 3 → multilingual reply
                                      │
   ◀──────────── reply ──────────────┘
```

> The actual webhook + send logic lives in the backend
> (`app/api/routes/whatsapp_webhook.py` and `app/services/whatsapp_service.py`).
> This folder holds the **message templates**, **flow copy**, and **setup notes**.

## Contents

- `message-templates.md` — approved template + reply copy in target languages.
- `SETUP.md` — step-by-step WhatsApp Cloud API + Meta app configuration.

## Local testing

Expose your local backend with a tunnel (e.g. `ngrok http 8000`) and register
the HTTPS URL as the webhook callback in the Meta developer console. Use the
`WHATSAPP_VERIFY_TOKEN` from your `.env`.
