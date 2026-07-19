# 🤝 Contributing & Team Workflow

Lightweight conventions to keep a fast-moving hackathon team unblocked.

## Branching
- `main` — always demoable. Never push broken code here.
- `feat/<short-name>` — one branch per feature (e.g. `feat/scam-pipeline`).
- Open a PR into `main`; a teammate skims it before merge when time allows.

## Ownership (suggested split for a 3-person team)
| Person | Owns |
|--------|------|
| **AI/Backend** | `services/`, `agents/`, scam + shield routes |
| **Platform** | dashboard (`frontend/`), reports + graph routes, deploy |
| **Integration/Pitch** | WhatsApp, seed scripts, demo script, slides |

Solo? Follow the phase order in `GUIDELINE.md` strictly and cut ruthlessly.

## Commits
- Small, frequent, present-tense: `add zero-shot scam classifier`.
- Never commit `.env` or anything under `ml/data/`.
- Flag any file that might contain secrets before committing.

## Code style
- **Python:** format with `ruff`/`black`; type-hint public functions.
- **JS/React:** `next lint`; keep components presentational.
- Keep routes thin; put logic in `agents/` and `services/`.

## Definition of "done" for a feature
- [ ] Wired end-to-end (route → orchestrator → service).
- [ ] Works against a fixture in `ml/data/`.
- [ ] Visible in the demo (or explicitly a backend-only capability).
- [ ] Doesn't break `main`.

## Communication
- Post blockers immediately — don't sit stuck for more than 20 minutes.
- Keep a shared "demo state" note: what's working, what's mocked, what's cut.

## Before every push to `main`
- [ ] Backend still boots (`uvicorn app.main:app --reload`).
- [ ] No secrets in the diff.
- [ ] The killer demo still works.
