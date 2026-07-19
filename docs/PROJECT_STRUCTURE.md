# 🗂️ SentinelAI — Annotated Project Structure

```
SentinelAI/
│
├── README.md                       # Project overview, features, quick start
├── LICENSE                         # MIT
├── .env.example                    # Env var template (copy to .env)
├── .gitignore                      # Ignores secrets, deps, media
│
├── docs/                           # 📚 All planning & guideline documents
│   ├── GUIDELINE.md                #   Complete start-to-finish build guide
│   ├── ARCHITECTURE.md             #   System design, data flow, diagrams
│   ├── HACKATHON_STRATEGY.md       #   "One Killer Feature" winning strategy
│   ├── ROADMAP_24H.md              #   Hour-by-hour execution plan
│   ├── API_KEYS_SETUP.md           #   How/where to get every API key
│   ├── DEMO_SCRIPT.md              #   Judge-facing pitch + live demo flow
│   ├── PROJECT_STRUCTURE.md        #   This file
│   └── CONTRIBUTING.md             #   Team workflow & conventions
│
├── backend/                        # ⚙️ FastAPI orchestrator (the brain)
│   ├── README.md
│   ├── requirements.txt            #   Pinned Python deps
│   ├── Dockerfile
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 #   App entry: routers, CORS, /health
│   │   ├── config.py               #   Typed settings from .env
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── routes/             #   Thin HTTP controllers
│   │   │       ├── __init__.py
│   │   │       ├── scam_detection.py     # Digital arrest scam alerting
│   │   │       ├── citizen_shield.py     # Conversational fraud shield
│   │   │       ├── counterfeit.py        # Currency verification
│   │   │       ├── graph_intel.py        # Fraud-network graph
│   │   │       ├── whatsapp_webhook.py   # WhatsApp inbound
│   │   │       └── reports.py            # Dashboard data
│   │   ├── agents/                 #   🧠 LangGraph orchestration
│   │   │   ├── __init__.py
│   │   │   ├── orchestrator.py     #     Pipeline definition & entry points
│   │   │   └── nodes.py            #     Individual graph node functions
│   │   ├── services/               #   External API / model wrappers
│   │   │   ├── __init__.py
│   │   │   ├── huggingface_service.py    # audio / zero-shot / vision
│   │   │   ├── groq_service.py           # Llama 3 conversational
│   │   │   ├── resemble_service.py       # optional premium voice detect
│   │   │   ├── neo4j_service.py          # graph DB
│   │   │   ├── whatsapp_service.py       # send + media download
│   │   │   ├── supabase_service.py       # report persistence
│   │   │   └── redis_service.py          # session state
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── schemas.py          #   Pydantic request/response contracts
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   └── citizen_shield_prompts.py # LLM prompt templates
│   │   └── core/                   #   Cross-cutting concerns
│   │       ├── __init__.py
│   │       ├── logging.py          #     App + audit logging
│   │       ├── security.py         #     Auth guards, webhook verify, PII
│   │       ├── constants.py        #     Labels, languages, thresholds
│   │       └── graph_fallback.py   #     NetworkX in-memory fallback
│   └── tests/
│       ├── __init__.py
│       └── README.md
│
├── frontend/                       # 🖥️ Next.js law-enforcement dashboard
│   ├── README.md
│   ├── package.json
│   ├── .env.local.example
│   ├── app/
│   │   ├── layout.jsx              #   App shell + nav
│   │   ├── page.jsx                #   Dashboard home (KPIs + hotspot map)
│   │   ├── network/page.jsx        #   Fraud-network graph explorer
│   │   └── reports/page.jsx        #   Reports table
│   ├── components/
│   │   └── README.md               #   Component build order
│   └── lib/
│       └── api.js                  #   Fetch helpers to the backend
│
├── frontend-streamlit/             # 🖥️ Streamlit dashboard (ALTERNATIVE)
│   ├── README.md                   #   Pick this OR frontend/, not both
│   ├── app.py
│   └── requirements.txt
│
├── whatsapp-bot/                   # 💬 Citizen interface (config + copy)
│   ├── README.md                   #   How the WhatsApp flow works
│   ├── SETUP.md                    #   Meta app + webhook setup
│   └── message-templates.md        #   Reply copy (multilingual)
│
├── ml/                             # 🤖 Model assets (no training from scratch)
│   ├── README.md
│   ├── MODEL_CARDS.md              #   Every model + why + limitations
│   ├── notebooks/
│   │   └── README.md
│   ├── labels/
│   │   └── scam_labels.md          #   Zero-shot candidate labels
│   └── data/
│       └── README.md               #   Sample data rules (gitignored media)
│
├── infra/                          # 🚀 Deployment
│   ├── README.md
│   ├── DEPLOYMENT.md               #   End-to-end deploy checklist
│   ├── render.yaml                 #   Render backend blueprint
│   ├── railway.md                  #   Railway alternative
│   └── vercel.md                   #   Frontend deploy notes
│
└── scripts/                        # 🛠️ Setup, seed & demo helpers
    └── README.md                   #   check_env, seed_reports, seed_graph...
```

## Conventions
- **Thin routes, fat orchestrator.** Business logic lives in `agents/`.
- **One service = one external system.** Wrappers normalise responses so the
  orchestrator stays provider-agnostic.
- **Docs first.** Every folder has a README explaining its purpose.
- **Pick one frontend.** Delete `frontend/` or `frontend-streamlit/` before the
  demo to avoid confusion.
