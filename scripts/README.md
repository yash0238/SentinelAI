# Scripts

Helper scripts for setup, seeding, and demo prep. Create as needed:

- `seed_reports.py`   — insert realistic mock fraud reports into Supabase so
  the dashboard and hotspot map look populated for the demo.
- `seed_graph.py`     — load a sample fraud-ring into Neo4j so
  cluster-detection has something to find.
- `check_env.py`      — verify all required env vars + API connectivity
  (HuggingFace, Groq, Neo4j, Redis, Supabase) before you demo.
- `demo_reset.py`     — reset all mock data to a known-good demo state.

Keep scripts idempotent so you can re-run them safely right before judging.
