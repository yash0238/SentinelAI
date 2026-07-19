# WhatsApp Cloud API — Setup

Step-by-step to wire the citizen interface. ~20 minutes.

## 1. Create a Meta app
1. Go to https://developers.facebook.com/ → **My Apps** → **Create App**.
2. Choose type **Business**.
3. Add the **WhatsApp** product to the app.

## 2. Get your test number & token
- In WhatsApp → **API Setup**, Meta gives you a free **test phone number**
  and a temporary **access token** (valid ~24h).
- Copy the **Phone number ID** and **access token** into `.env`:
  ```
  WHATSAPP_TOKEN=...
  WHATSAPP_PHONE_NUMBER_ID=...
  WHATSAPP_VERIFY_TOKEN=sentinelai_verify_token
  ```
- Add your own number as a **recipient** to test.

## 3. Expose your local backend
```bash
ngrok http 8000
```
Copy the HTTPS forwarding URL, e.g. `https://abcd-1234.ngrok-free.app`.

## 4. Configure the webhook
- In WhatsApp → **Configuration** → **Webhook** → **Edit**.
- Callback URL: `https://<your-ngrok>/whatsapp/webhook`
- Verify token: the same `WHATSAPP_VERIFY_TOKEN` value.
- Subscribe to the **messages** field.

## 5. Test
- Send a WhatsApp message from your registered number to the test number.
- Watch the backend logs; you should see the inbound webhook and a reply.

## Notes / gotchas
- The temporary token expires daily — for a multi-day hackathon, generate a
  **permanent** system-user token (Business Settings → System Users).
- To start a conversation (not just reply), you must use a **pre-approved
  template message**. Replies within the 24-hour window can be free-form.
- Voice notes/images arrive as media IDs — download them via the Graph API
  (see `app/services/whatsapp_service.download_media`).
