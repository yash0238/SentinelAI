# 🔑 SentinelAI — API Keys & Accounts Setup

Every credential you need, where to get it, and which `.env` variable it maps
to. All services have free tiers sufficient for the hackathon.

> Copy `.env.example` → `.env` and fill values as you go. **Never commit `.env`.**

---

## 1. HuggingFace (audio, zero-shot, vision)
1. Sign up at https://huggingface.co.
2. Go to **Settings → Access Tokens** → **New token** (role: `read`).
3. Set:
   ```
   HF_API_TOKEN=hf_...
   HF_AUDIO_MODEL=facebook/wav2vec2-base-960h
   HF_ZEROSHOT_MODEL=MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli
   HF_VISION_MODEL=google/vit-base-patch16-224
   ```
- **Free tier:** rate-limited Inference API. First call to an idle model may
  return 503 (cold start) — retry with backoff and pre-warm before the demo.

## 2. Groq (Llama 3, ultra-fast LLM)
1. Sign up at https://console.groq.com.
2. **API Keys → Create API Key.**
3. Set:
   ```
   GROQ_API_KEY=gsk_...
   GROQ_MODEL=llama3-70b-8192
   ```
- **Free tier:** generous rate limits, sub-second responses. Great for live
  multilingual replies.

## 3. Resemble AI (OPTIONAL — premium voice-clone detection)
1. https://www.resemble.ai — request API access.
2. Set `RESEMBLE_API_KEY=...`.
- Skip if unavailable; the HuggingFace audio path is the default fallback.

## 4. Neo4j (fraud-network graph)
**Option A — Sandbox (fastest):**
1. https://neo4j.com/sandbox/ → create a blank sandbox.
2. Copy the **Bolt URL**, username, password.

**Option B — Aura Free (persistent):**
1. https://neo4j.com/cloud/aura-free/ → create a free instance.
2. Download credentials on creation (shown once!).

Set:
```
NEO4J_URI=bolt://... (or neo4j+s://... for Aura)
NEO4J_USER=neo4j
NEO4J_PASSWORD=...
```

## 5. Upstash Redis (session state)
1. https://upstash.com → create a **Redis** database (free tier).
2. Copy the connection URL.
3. Set `REDIS_URL=redis://...` (or the `rediss://` TLS URL Upstash provides).

## 6. Supabase (report logging / Postgres)
1. https://supabase.com → new project.
2. **Project Settings → API** → copy **Project URL** + **anon/service key**.
3. Set:
   ```
   SUPABASE_URL=https://xxxx.supabase.co
   SUPABASE_KEY=...
   ```
4. Create the `fraud_reports` table (schema in
   `backend/app/services/supabase_service.py` docstring).

## 7. WhatsApp Cloud API (citizen interface)
Full walkthrough in [`../whatsapp-bot/SETUP.md`](../whatsapp-bot/SETUP.md).
Short version:
1. https://developers.facebook.com → create a **Business** app → add
   **WhatsApp**.
2. Copy the test **Phone number ID** + **access token**.
3. Set:
   ```
   WHATSAPP_TOKEN=...
   WHATSAPP_PHONE_NUMBER_ID=...
   WHATSAPP_VERIFY_TOKEN=sentinelai_verify_token
   ```
- The test token expires in ~24h; generate a permanent **system-user** token
  for multi-day events.

## 8. Mapbox (dashboard hotspot map)
1. https://account.mapbox.com → copy your **default public token**.
2. Set (frontend `.env.local`):
   ```
   NEXT_PUBLIC_MAPBOX_TOKEN=pk...
   ```

## 9. Deployment (Render + Vercel)
- **Render:** https://render.com — connect GitHub, add env vars in dashboard.
- **Vercel:** https://vercel.com — import repo, set frontend env vars.

---

## Verify everything
Run the connectivity check before you start building features:
```bash
python scripts/check_env.py
```
It should confirm HuggingFace, Groq, Neo4j, Redis, and Supabase are reachable.

## Security reminders
- `.env` is gitignored — keep it that way.
- Use the **service key** for Supabase only on the backend, never in the
  frontend.
- Rotate any key that was ever pasted into a chat, screen share, or commit.
