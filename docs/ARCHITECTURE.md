# 🏗️ SentinelAI — Architecture

## 1. System Overview

SentinelAI is a **converged intelligence layer**: multiple input channels feed
a single orchestration brain that fuses multi-modal AI signals into
explainable, auditable verdicts, then surfaces them to citizens and law
enforcement.

```
        CITIZENS                          LAW ENFORCEMENT / FI
   ┌───────────────┐                      ┌───────────────────┐
   │  WhatsApp /    │                      │  Dashboard        │
   │  IVR           │                      │  (Next.js /       │
   │                │                      │   Streamlit)      │
   └───────┬───────┘                      └─────────┬─────────┘
           │ voice/text/image                       │ queries
           ▼                                         ▼
   ┌──────────────────────────────────────────────────────────┐
   │                    FastAPI  (Orchestrator)                 │
   │                                                            │
   │   ┌──────────────── LangGraph pipeline ────────────────┐   │
   │   │ classify → [audio|text|image|number] → fuse →      │   │
   │   │            explain → log/alert                     │   │
   │   └────────────────────────────────────────────────────┘  │
   └───┬─────────┬──────────┬───────────┬──────────┬───────────┘
       │         │          │           │          │
       ▼         ▼          ▼           ▼          ▼
   HuggingFace  Groq     Neo4j       Redis     Supabase
   (audio/     (Llama3) (graph)    (session)  (reports)
    zero-shot/
    vision)
```

## 2. Components

### 2.1 Input Channels
- **WhatsApp Cloud API** — the primary citizen touchpoint (no frontend needed).
- **IVR** (future) — same pipeline, phone-based.
- **Dashboard** — law-enforcement analytics + graph exploration.

### 2.2 Orchestrator (FastAPI + LangGraph)
The brain. Routes are thin controllers; all decision logic lives in
`agents/orchestrator.py`. A single pipeline serves every channel, guaranteeing
consistent verdicts.

**Scam pipeline (example):**
```
classify_intent
   ├─ audio?  → run_audio_detection      (HF / Resemble)
   ├─ text?   → run_script_classification (HF zero-shot)
   └─ number? → lookup_number_reputation  (Neo4j)
fuse_signals            → weighted risk score → RiskLevel
generate_explanation    → Groq/Llama 3 human-readable verdict
log_and_alert           → Supabase log; MHA alert if CRITICAL
```

### 2.3 AI Services (swappable wrappers)
- `huggingface_service` — audio classification, zero-shot text, vision.
- `groq_service` — fast multilingual summarisation + explanations.
- `resemble_service` — optional premium real-time voice-clone detection
  (identical return shape, so it drops in transparently).

### 2.4 Data & State
- **Neo4j** — fraud-network graph (victims, suspects, phones, UPI, IPs,
  devices). NetworkX fallback for offline demos.
- **Redis** — ephemeral scam-call session state + chat memory (TTL'd).
- **Supabase (Postgres)** — persistent report log + dashboard aggregates.

## 3. Data Flow — "Digital Arrest" scenario

1. Victim receives a call from a fake "CBI officer" (AI-cloned voice).
2. Victim forwards the recorded voice note to the SentinelAI WhatsApp number.
3. Webhook downloads the media → orchestrator runs audio deepfake detection +
   scam-script classification.
4. Signals fuse to `CRITICAL`; Groq generates a calm, multilingual warning.
5. Citizen gets an instant "⚠️ HIGH RISK — disconnect, call 1930" reply.
6. The report is logged to Supabase and its entities ingested into Neo4j.
7. On the dashboard, the new report appears on the hotspot map; if it links to
   existing reports, a fraud-ring cluster grows.

## 4. Graph Data Model (Neo4j)

```
(:Victim)-[:FILED]->(:Report)-[:INVOLVES]->(:Phone|:UPI|:IP|:Device)
(:Phone)-[:LINKED_TO]->(:Device)
(:UPI)-[:TRANSFERRED_TO]->(:UPI)          // money-mule chains
```
Community detection over this graph surfaces coordinated fraud rings from
otherwise isolated victim reports.

## 5. Non-Functional Concerns

| Concern | Approach |
|---------|----------|
| **Latency** | Remote inference (Groq is sub-second); Redis caches session state. |
| **Availability** | Graceful fallbacks (NetworkX, in-memory) keep the demo alive. |
| **Auditability** | Every verdict/ingest emits a timestamped, source-attributed audit record. |
| **Security** | Token-guarded LE endpoints; webhook signature verification; PII redaction in logs. |
| **Scalability** | Stateless FastAPI (horizontal scale); managed DBs; serverless inference. |
| **Cost** | Free tiers throughout; no GPU. |

## 6. Deployment Topology

```
Vercel (frontend)  ─────▶  Render/Railway (FastAPI)  ─────▶  Groq / HuggingFace
                                   │
                    ┌──────────────┼───────────────┐
                    ▼              ▼               ▼
              Supabase        Neo4j Aura       Upstash Redis
```

See [`../infra/DEPLOYMENT.md`](../infra/DEPLOYMENT.md).

## 7. Future Extensions (mention in pitch, don't build)
- Real-time streaming audio analysis during a live call (not just voice notes).
- Fine-tuned counterfeit-currency model with microprint/security-thread heads.
- Geospatial patrol optimisation ML on hotspot clusters.
- Automated, verified MHA/NCRB alert integration.
