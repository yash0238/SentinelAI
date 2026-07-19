# Deployment Checklist

End-to-end steps to get SentinelAI live. Do this **mid-hackathon**, not at the
buzzer.

## 0. Prep
- [ ] All secrets in `.env` locally; nothing secret committed.
- [ ] Backend runs locally (`uvicorn app.main:app --reload`).
- [ ] Frontend runs locally (`npm run dev`).

## 1. Provision managed services
- [ ] **Supabase**: create project, create `fraud_reports` table, copy URL + key.
- [ ] **Neo4j Sandbox / Aura Free**: create instance, copy bolt URI + creds.
- [ ] **Upstash Redis**: create DB, copy connection URL.
- [ ] **Groq** + **HuggingFace** tokens ready.

## 2. Deploy backend (Render)
- [ ] Push repo to GitHub.
- [ ] In Render: New → Blueprint → point at repo (reads `infra/render.yaml`).
- [ ] Add all secret env vars in the dashboard.
- [ ] Deploy; verify `https://<app>.onrender.com/health`.

## 3. Deploy frontend (Vercel)
- [ ] Import repo in Vercel, set root to `frontend/`.
- [ ] Set `NEXT_PUBLIC_API_BASE_URL` to the Render backend URL.
- [ ] Set `NEXT_PUBLIC_MAPBOX_TOKEN`.
- [ ] Deploy; open the Vercel URL.

## 4. Wire WhatsApp
- [ ] Point the Meta webhook to the Render backend `/whatsapp/webhook`.
- [ ] Send a test message; confirm a reply.

## 5. Smoke test the demo path
- [ ] Upload a voice note → get a scam verdict.
- [ ] Upload a note image → get a counterfeit result.
- [ ] Ingest a few reports → clusters appear on the network page.
- [ ] Hotspots render on the dashboard map.

## Rollback
- Render/Vercel keep previous deploys — one click to roll back if a change
  breaks the demo. Freeze changes ~1 hour before judging.
