# SentinelAI — Backend

FastAPI orchestrator that fuses multi-modal AI signals (audio deepfake,
scam-script NLP, counterfeit vision, graph intelligence) into explainable,
auditable fraud verdicts.

## Quick start

```bash
cd backend
python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env      # fill in keys (see docs/API_KEYS_SETUP.md)
uvicorn app.main:app --reload
```

Interactive API docs: http://localhost:8000/docs

## Layout

```
app/
├── main.py              # app entry, router mounting, lifespan
├── config.py            # typed settings from .env
├── api/routes/          # HTTP endpoints (thin controllers)
├── agents/              # LangGraph orchestration (the "brain")
├── services/            # external API / model wrappers
├── models/              # pydantic schemas (API contracts)
├── prompts/             # LLM prompt templates
└── core/                # logging, security, constants, fallbacks
```

## Design principles

- **Routes are thin.** All decision logic lives in `agents/orchestrator.py`
  so REST, WhatsApp, and IVR reuse the same pipeline.
- **Providers are swappable.** HuggingFace is the default; Resemble AI is an
  optional premium path with an identical return shape.
- **Everything is auditable.** Verdicts and ingests emit audit records for
  court admissibility (see `core/logging.py`).
- **Degrade gracefully.** NetworkX and in-memory fallbacks keep the demo alive
  without Neo4j / Supabase.

See [`../docs/GUIDELINE.md`](../docs/GUIDELINE.md) for the full build order.
