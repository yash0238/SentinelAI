# ⏱️ SentinelAI — 24-Hour Execution Roadmap

An aggressive, realistic hour-by-hour plan for a 24-hour hackathon. Adjust
block sizes for your actual duration. Times assume a 1–3 person team; note the
solo variant where relevant.

> Map to build phases in [`GUIDELINE.md`](GUIDELINE.md).

---

## Hours 0–2 — Setup & Foundation (Phase A)
- [ ] Clone repo, read `GUIDELINE.md` + `HACKATHON_STRATEGY.md`.
- [ ] Create all accounts / API keys (`API_KEYS_SETUP.md`).
- [ ] Fill `.env`. Run `scripts/check_env.py` to confirm connectivity.
- [ ] Implement `config.py`, `main.py`, `/health`. Backend boots.
- [ ] Frontend shell renders (or Streamlit skeleton).
- **Milestone:** backend `/docs` loads; frontend shows a page.

## Hours 2–7 — Killer Feature (Phase B)
- [ ] `huggingface_service`: audio + zero-shot.
- [ ] `groq_service`: summarise + explain.
- [ ] `orchestrator` + `nodes`: scam pipeline.
- [ ] `scam_detection` + `citizen_shield` routes.
- [ ] Test with `ml/data/` fixtures; tune thresholds.
- **Milestone:** POST a voice note / text → explainable verdict. **This is the
  demo — protect this time.**

## Hours 7–8 — Deploy Early (Phase G, partial)
- [ ] Push to GitHub; deploy backend to Render.
- [ ] Verify deployed `/health` + a live scam call.
- **Milestone:** public backend URL works.

## Hours 8–12 — WhatsApp Interface (Phase C)
- [ ] `whatsapp_service` + webhook route.
- [ ] Meta app config + `ngrok`/deployed webhook.
- [ ] Forward a voice note on WhatsApp → get a reply.
- **Milestone:** the killer demo works over real WhatsApp.

## Hours 12–16 — Dashboard (Phase D)
- [ ] `supabase_service` + `reports` route.
- [ ] `scripts/seed_reports.py` — populate mock data.
- [ ] Frontend: StatCards + Mapbox HotspotMap + ReportsTable.
- [ ] Deploy frontend to Vercel.
- **Milestone:** polished, populated dashboard on a public URL.

## Hours 16–19 — Fraud-Network Graph (Phase E)
- [ ] `neo4j_service` (+ NetworkX fallback).
- [ ] `graph_intel` route; `scripts/seed_graph.py`.
- [ ] Frontend `NetworkGraph` on the network page.
- **Milestone:** a fraud-ring cluster is visible.

## Hours 19–21 — Counterfeit + Polish (Phase F)
- [ ] `classify_image` + `counterfeit` route.
- [ ] Upload demo tile / Streamlit "Live Demo" tab.
- [ ] Visual polish, empty-state handling, error messages.
- **Milestone:** all four features demo end-to-end.

## Hours 21–23 — Harden & Rehearse (Phases G–H)
- [ ] Token-guard sensitive endpoints.
- [ ] `scripts/demo_reset.py`; pre-warm models.
- [ ] Rehearse the `DEMO_SCRIPT.md`; time it.
- [ ] **Record a backup demo video.**
- **Milestone:** rehearsed pitch, backup ready.

## Hours 23–24 — Freeze & Submit
- [ ] **Freeze code.** No new features.
- [ ] Final smoke test on demo devices + hotspot.
- [ ] Submit repo + slides + video. Breathe.

---

## Solo-participant variant
- Skip the Next.js frontend → use **Streamlit** (`frontend-streamlit/`).
- Host both backend + Streamlit on **HuggingFace Spaces** to save deploy time.
- Consider cutting the graph feature (Phase E) to guarantee polish on the
  killer feature + dashboard.

## Danger signs (cut something)
- Killer feature not working by **hour 7** → stop everything else, fix it.
- Not deployed by **hour 12** → deploy now, features later.
- Not rehearsed by **hour 22** → cut the newest feature, rehearse.
