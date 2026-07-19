# Backend tests

Run: `pytest` from the `backend/` directory.

Planned test files (add as features land — do not pre-write empty tests):

- `test_scam_pipeline.py`   — orchestrator produces expected verdict for
  known scam vs. legitimate fixtures.
- `test_services.py`        — service wrappers normalise provider responses.
- `test_routes.py`          — endpoint contracts via FastAPI TestClient.
- `test_graph.py`           — ingest + cluster detection on a seeded graph.

Keep fixtures (sample audio, images, transcripts) in `ml/data/` and reference
them from tests.
