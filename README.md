# 🛡️ SentinelAI

**Proactive Intelligence for Digital Public Safety & Fraud Neutralisation**

> Shifting law enforcement from reactive case investigation to predictive threat neutralisation.

[![Problem Statement](https://img.shields.io/badge/Track-AI%20for%20Digital%20Public%20Safety-blue)]()
[![Status](https://img.shields.io/badge/Status-Hackathon%20MVP-orange)]()
[![Backend](https://img.shields.io/badge/Backend-FastAPI-green)]()
[![AI](https://img.shields.io/badge/AI-HuggingFace%20%7C%20Groq%20%7C%20Neo4j-yellow)]()

---

## 🚨 The Crisis We Are Solving

The digital safety landscape in India faces an unprecedented, industrialised threat:

- India registered **1.14 million** cybercrime complaints in 2023 — a **60% increase** over 2022.
- In the first nine months of 2024, **digital arrest scams** defrauded citizens of over **₹1,776 crore**.
- Fraudsters use spoofed numbers, AI-generated voices, and fake government portals to create multi-day psychological hostage situations.
- The **RBI Annual Report 2025** flagged record seizures of **Fake Indian Currency Notes (FICN)**, with ₹500 notes now sophisticated enough to defeat manual detection.

**The Gap:** Law enforcement lacks reliable tools to detect threats *at the point of contact*, leaving them with evidence only *after* mass victimisation has occurred.

---

## 💡 Our Solution

**SentinelAI** is an AI-powered Digital Public Safety Intelligence platform. It equips law enforcement, financial institutions, and citizens with a converged intelligence layer to detect, disrupt, and respond to digital fraud networks and counterfeit operations in real time.

### Core Features (The "Happy Path" Demo)

| Feature | Description |
|---------|-------------|
| 🎙️ **Digital Arrest Scam Alerting** | Real-time AI classifier analysing call-flow sequences, spoofing signatures, and voice authenticity to flag active scam sessions before money is transferred. |
| 💬 **Citizen Fraud Shield** | Conversational AI over WhatsApp and IVR providing instant fraud risk assessments and guided reporting to NCRB portals. |
| 🌐 **Multilingual Support** | Citizen advisory in 12 regional languages. |
| 🕸️ **Fraud Network Graph Intelligence** | Graph AI clustering victim reports, device fingerprints, and money-mule networks into court-admissible intelligence packages. |
| 💵 **Counterfeit Identifier** | Mobile / POS computer vision verifying microprints, security threads, and serial-number patterns to flag fake notes. |

---

## ⚙️ Technical Architecture (High Level)

| Technology Domain | Implementation |
|-------------------|----------------|
| **Speech AI** | Detection of voice spoofing and AI-generated voices |
| **NLP / LLMs** | Classification of scam scripts and psychological patterns |
| **Computer Vision** | Deepfake detection and counterfeit currency identification |
| **Graph AI & Network Analysis** | Mapping coordinated fraud rings and campaigns |
| **Geospatial Intelligence** | Cybercrime hotspot mapping and patrol optimisation |
| **Agentic AI** | Fusion of multi-source intelligence to trigger automated MHA alerts |

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full system design and data flow.

---

## 🧠 The AI Stack

| Capability | Primary Tool | Backup / Alternative |
|------------|--------------|----------------------|
| Audio Deepfake Detection | HuggingFace audio-classification pipeline | Resemble AI API / Modulate |
| Scam Script Classification | Zero-Shot (DeBERTa-v3 MNLI) | Llama 3 via Groq |
| Conversational Citizen Shield | Llama 3 via Groq | OpenAI |
| Counterfeit Currency Vision | ViT (google/vit-base-patch16-224) | Custom fine-tune |
| Graph Intelligence | Neo4j | NetworkX (local fallback) |
| Agent Orchestration | LangGraph | LangChain |
| Geospatial Mapping | MapTiler / MapLibre GL JS | CARTO Dark Matter (local fallback) |

---

## 📊 Evaluation & Impact Metrics

- **Precision & Recall** — extremely low false-positive rates for citizen-facing tools to preserve digital trust.
- **Speed to Detection** — maximise fraud-network detection lead time before mass victimisation.
- **Admissibility** — full auditability of intelligence packages for legal admissibility.

**Hackathon Weighting Alignment:** Innovation 25% · Business Impact 25% · Technical Excellence 20% · Scalability 15% · User Experience 15%

---

## 📁 Repository Structure

```
SentinelAI/
├── README.md                       # Project overview, features, quick start
├── LICENSE                         # MIT License
├── .env.example                    # Env var template
├── .gitignore                      # Git ignore file
│
├── docs/                           # 📚 Documentation & System Design
│   ├── ARCHITECTURE.md             #   System architecture, data flow & repository tree
│   ├── API_KEYS_SETUP.md           #   Complete API credential setup guide
│   └── DEMO_SCRIPT.md              #   Live pitch & judge demo flow guide
│
├── backend/                        # ⚙️ FastAPI Orchestrator (Python)
│   ├── app/                        #   FastAPI app, LangGraph agents, external services
│   ├── scripts/                    #   Database seed tools (seed_reports.py, seed_graph.py)
│   ├── requirements.txt            #   Backend Python dependencies
│   └── Dockerfile                  #   Container setup
│
├── frontend/                       # 🖥️ Law-Enforcement Dashboard (Next.js 14)
│   ├── app/                        #   App Router (Hotspots, Network Graph, Reports)
│   ├── components/                 #   HotspotMap (MapLibre GL), StatCards, Charts
│   └── package.json                #   Frontend dependencies
│
├── frontend-streamlit/             # 🖥️ Streamlit Dashboard (Alternative UI)
├── whatsapp-bot/                   # 💬 WhatsApp Cloud API setup & templates
├── ml/                             # 🤖 Model cards & sample datasets
├── infra/                          # 🚀 Deployment configurations (Render/Vercel)
└── scripts/                        # 🛠️ Maintenance & verification scripts
```

---

## 🚀 How to Run Locally (Demo)

> Full step-by-step in [`docs/API_KEYS_SETUP.md`](docs/API_KEYS_SETUP.md).

```bash
# 1. Clone
git clone https://github.com/your-team/SentinelAI.git
cd SentinelAI

# 2. Backend
cd backend
pip install -r requirements.txt
cp ../.env.example .env         # add your API keys

# 3. Run backend
uvicorn app.main:app --reload

# 4. Frontend (in a new terminal)
cd frontend
npm install
npm run dev

# 5. Open the dashboard
# http://localhost:3000
```

---

## 📚 Documentation Index

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture, data flow, component diagrams & repository tree |
| [API_KEYS_SETUP.md](docs/API_KEYS_SETUP.md) | Complete step-by-step API key setup guide (Groq, HF, MapTiler, Neo4j, Supabase) |
| [DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md) | The judge-facing pitch & live demo walkthrough |

---

## ⚖️ Disclaimer

SentinelAI is a hackathon prototype for demonstration purposes. It is **not** a certified law-enforcement or financial-fraud detection system. All fraud verdicts are advisory. Do not use in production without legal review, model validation, and compliance sign-off.

---

## 📄 License

See [LICENSE](LICENSE).
