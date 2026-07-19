# 📘 SentinelAI — Complete Build Guideline (Start to Finish)

This is your single source of truth for building SentinelAI from an empty repo
to a live, judge-ready demo. Read it once end-to-end, then follow the phases in
order.

> **Problem Statement 6:** AI for Digital Public Safety — Defeating
> Counterfeiting, Fraud & Digital Arrest Scams.

---

## 0. Philosophy — Win with ONE Killer Feature

You cannot build all five features well in a hackathon. Judges reward **one
feature that works flawlessly and demos live** over five half-broken ones.

**Recommended killer feature: the Digital Arrest Scam Alerting + Citizen Fraud
Shield over WhatsApp.** It is the most emotional, most current, and most
demoable. Everything else (counterfeit vision, graph intelligence, dashboard)
is a *supporting cast* that makes the story complete.

Build in this priority order:

1. 🥇 **Citizen Fraud Shield + Scam Detection** (the killer demo)
2. 🥈 **Law-enforcement dashboard** (the "wow" visual — hotspot map)
3. 🥉 **Fraud-network graph** (the "technical excellence" flourish)
4. 🎖️ **Counterfeit currency check** (breadth — shows the converged platform)

If you run low on time, cut from the bottom up. Never sacrifice #1.

---

## 1. Golden Rules

1. **Don't train models.** Use HuggingFace Inference API + Groq. Zero GPU.
2. **Deploy early** (hour 6–8), not at the buzzer.
3. **Mock aggressively.** Seed realistic data so screens look alive.
4. **Every claim must demo.** If you can't show it live, cut it from the pitch.
5. **Be honest about limits.** A clear model card beats an overclaimed one.
6. **Thin routes, fat orchestrator.** All logic in `agents/orchestrator.py`.
7. **Fail gracefully.** Fallbacks (NetworkX, in-memory) keep the demo alive.

---

## 2. Prerequisites & Accounts

Create these free accounts first (details in
[`API_KEYS_SETUP.md`](API_KEYS_SETUP.md)):

- [ ] HuggingFace (Inference API token)
- [ ] Groq (API key — free, very fast)
- [ ] Neo4j Sandbox or Aura Free
- [ ] Upstash Redis (free serverless)
- [ ] Supabase (free Postgres)
- [ ] Meta developer account (WhatsApp Cloud API test number)
- [ ] Mapbox (public token for the dashboard map)
- [ ] Render + Vercel (deployment)

Local tooling:
- [ ] Python 3.11+
- [ ] Node 18+ (if using the Next.js frontend)
- [ ] `ngrok` (for WhatsApp webhook testing)
- [ ] Git

---

## 3. Repository Tour

See [`PROJECT_STRUCTURE.md`](PROJECT_STRUCTURE.md) for the annotated tree. Key
folders:

- `backend/` — FastAPI + LangGraph orchestrator + service wrappers.
- `frontend/` — Next.js dashboard (**or** `frontend-streamlit/` — pick one).
- `whatsapp-bot/` — templates + setup for the citizen interface.
- `ml/` — model cards, labels, sample data.
- `infra/` — deployment blueprints.
- `scripts/` — seed & health-check helpers.
- `docs/` — this and other planning docs.

---

## 4. Build Phases

### Phase A — Foundation (get a heartbeat)
Goal: backend boots, `/health` returns 200, frontend renders a shell.

1. `backend/app/config.py` — implement the typed `Settings` from `.env`.
2. `backend/app/main.py` — create the app, add CORS, mount an empty router,
   add `/health`.
3. Run `uvicorn app.main:app --reload`; confirm `/docs` loads.
4. Frontend: `npm install`, get `app/layout.jsx` + `app/page.jsx` rendering a
   placeholder.

### Phase B — The Killer Feature (Scam Detection + Citizen Shield)
Goal: submit a voice note / text and get an explainable verdict.

1. `services/huggingface_service.py` — implement `classify_audio` and
   `zero_shot_classify`.
2. `services/groq_service.py` — implement `summarise_message` and
   `generate_verdict_explanation`.
3. `agents/nodes.py` + `agents/orchestrator.py` — build the LangGraph pipeline
   (classify → run models → fuse → explain).
4. `api/routes/scam_detection.py` + `api/routes/citizen_shield.py` — wire the
   endpoints to the orchestrator.
5. Test with `ml/data/` fixtures. Tune thresholds in `core/constants.py`.

### Phase C — WhatsApp Citizen Interface
Goal: forward a voice note on WhatsApp → get a reply.

1. `services/whatsapp_service.py` — `send_message` + `download_media`.
2. `api/routes/whatsapp_webhook.py` — verification + inbound routing to the
   Citizen Shield pipeline.
3. Follow [`../whatsapp-bot/SETUP.md`](../whatsapp-bot/SETUP.md); test via
   `ngrok`.

### Phase D — Law-Enforcement Dashboard
Goal: a polished screen with a live hotspot map and reports.

1. `services/supabase_service.py` — `log_report`, `list_reports`, `get_stats`,
   `get_hotspots`.
2. `api/routes/reports.py` — expose the above.
3. `scripts/seed_reports.py` — populate realistic mock data.
4. Frontend: `StatCard`, `HotspotMap` (Mapbox), `ReportsTable`.

### Phase E — Fraud-Network Graph (technical flourish)
Goal: isolated reports cluster into a visible fraud ring.

1. `services/neo4j_service.py` (+ `core/graph_fallback.py`).
2. `api/routes/graph_intel.py` — ingest, clusters, ego network, intel package.
3. `scripts/seed_graph.py` — load a sample ring.
4. Frontend: `NetworkGraph` on the `network/` page.

### Phase F — Counterfeit Currency (breadth)
Goal: upload a note image → feature checklist + verdict.

1. `services/huggingface_service.py` — `classify_image`.
2. `api/routes/counterfeit.py` — wire it up.
3. Add a file-upload demo tile to the dashboard (or Streamlit "Live Demo" tab).

### Phase G — Deploy & Harden
1. Follow [`../infra/DEPLOYMENT.md`](../infra/DEPLOYMENT.md).
2. Add the shared-token guard from `core/security.py` to sensitive endpoints.
3. Run `scripts/check_env.py` against the deployed backend.

### Phase H — Rehearse the Pitch
1. Follow [`DEMO_SCRIPT.md`](DEMO_SCRIPT.md).
2. Time it. Freeze code ~1 hour before judging.

---

## 5. Testing Strategy (lightweight)

- Test the orchestrator verdict on known scam vs. legitimate fixtures.
- Test each service wrapper normalises provider responses.
- Test endpoints with FastAPI `TestClient`.
- Do **not** pre-write empty tests; add them as features land.

Run: `pytest` in `backend/`.

---

## 6. Security & Ethics (say this in the pitch)

- Sensitive endpoints (dashboard, graph, intel packages) **must** be
  authenticated. The demo uses a shared-token guard; production needs proper
  auth + RBAC. Call this out honestly.
- Verdicts are **advisory**, never automated enforcement.
- Intelligence packages are **auditable** (timestamped, source-attributed) for
  court admissibility.
- No real victim PII in any sample data.
- Fraud verdicts can have false positives — that's why citizen tools are tuned
  for low false-positive rates and always point to the official 1930 helpline.

---

## 7. Common Pitfalls

- **HF cold starts (503):** first call to an idle model is slow. Warm it up
  before the demo and add retry-with-backoff.
- **WhatsApp token expiry:** the test token expires in ~24h; generate a
  permanent system-user token for multi-day events.
- **Mapbox blank map:** almost always a missing/wrong `NEXT_PUBLIC_MAPBOX_TOKEN`.
- **CORS errors:** add the frontend origin to CORS in `main.py`.
- **Over-scoping:** if a feature isn't demoing by its phase deadline, cut it.

---

## 8. Definition of Done (for the demo)

- [ ] Live URL for backend + frontend.
- [ ] Voice note → scam verdict works on stage.
- [ ] WhatsApp reply works on stage (or recorded backup).
- [ ] Dashboard shows populated hotspots + reports.
- [ ] Graph shows at least one detected cluster.
- [ ] Counterfeit check returns a result.
- [ ] Pitch rehearsed and under time.
- [ ] Backup video recorded in case live wifi fails.

Now go build. Start at **Phase A**.
