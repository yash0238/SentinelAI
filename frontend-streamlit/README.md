# SentinelAI — Streamlit Dashboard

A complete, Python-only dashboard for SentinelAI. It runs **standalone with
realistic mock data** and automatically switches to the live FastAPI backend
when one is available — so it always demos, even offline or on flaky wifi.

## Features

- **📊 Overview** — KPI cards, a live "Active Digital-Arrest Hotspots" map
  (pydeck over India), a 14-day trend chart, and a scam-type breakdown.
- **🔬 Live Demo** — the killer feature. Submit:
  - a **text / transcript** → scam-script classification,
  - a **voice note** → deepfake-voice detection,
  - a **currency image** → counterfeit feature checklist.
  Each returns an explainable, colour-coded risk verdict.
- **🕸️ Network** — a fraud-ring cluster graph (Graphviz) linking victims,
  phones, UPI IDs, devices, and suspects, plus a court-admissible
  "intelligence package" action.
- **📋 Reports** — a filterable, sortable table of logged fraud reports.

## Run locally

```bash
cd frontend-streamlit
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

By default it starts in **Demo Mode** (mock data, no backend). To use the real
backend, toggle Demo Mode off in the sidebar and set the Backend URL.

## Demo Mode tips

Offline verdicts are keyword/filename driven so you get a stable, predictable
demo:

- **Text:** the pre-filled example triggers a CRITICAL "Digital Arrest" verdict.
  Words like `arrest`, `CBI`, `parcel`, `OTP`, `KYC` raise the score.
- **Voice note:** upload a file whose name contains `synthetic`, `fake`, or
  `clone` to trigger the high-risk (AI voice) path.
- **Currency image:** a filename containing `fake` or `counterfeit` triggers a
  flagged result.

## Connecting the backend

The dashboard calls these endpoints when Demo Mode is off (falling back to mock
on any error):

| Dashboard data | Endpoint |
|----------------|----------|
| Stats | `GET /reports/stats` |
| Reports | `GET /reports` |
| Hotspots | `GET /reports/hotspots` |
| Clusters | `GET /graph/clusters` |
| Text analysis | `POST /shield/chat` |
| Audio analysis | `POST /scam/analyze-audio` |
| Image analysis | `POST /counterfeit/verify` |

Response shapes match `utils/mock_data.py`, so the backend just needs to return
the same JSON.

## Deploy free on HuggingFace Spaces

1. Create a new **Space** → SDK **Streamlit**.
2. Push this folder's contents (or point the Space at your repo subdir).
3. Add `NEXT_PUBLIC_API_BASE_URL` as a Space secret if using a live backend.

## Layout

```
frontend-streamlit/
├── app.py                 # entry point: sidebar + tabs
├── requirements.txt
├── .streamlit/
│   └── config.toml        # dark theme
└── utils/
    ├── api_client.py      # backend calls with mock fallback
    ├── mock_data.py       # realistic synthetic data + verdict heuristics
    ├── theme.py           # CSS, colours, UI helpers
    └── views.py           # the four tab renderers
```

> Pick **either** this or the Next.js `frontend/` and delete the other before
> the demo (see `docs/HACKATHON_STRATEGY.md`).
