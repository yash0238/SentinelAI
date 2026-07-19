# SentinelAI — Infrastructure & Deployment

Fastest path to a live demo. Prefer managed platforms over raw cloud.

| Component | Platform | Why |
|-----------|----------|-----|
| Backend (FastAPI) | **Render** or **Railway** | native Python, deploy from repo in minutes |
| Frontend (Next.js) | **Vercel** | zero-config Next.js hosting |
| Frontend (Streamlit alt) | **HuggingFace Spaces** | free, Python-native |
| Database | **Supabase** (Postgres) | instant REST API, easy dashboard |
| Graph DB | **Neo4j Sandbox / Aura Free** | hosted graph, no local setup |
| Cache | **Upstash Redis** (free tier) | serverless Redis |

## Files here

- `render.yaml`        — Render blueprint for the backend service.
- `railway.md`         — Railway setup notes (alternative to Render).
- `vercel.md`          — Frontend deploy notes.
- `DEPLOYMENT.md`      — full end-to-end deploy checklist.

## Golden rule for the demo

Deploy **early** (hour 6–8), not at the end. A working deployed URL removes
last-minute panic and lets you share a live link with judges.
