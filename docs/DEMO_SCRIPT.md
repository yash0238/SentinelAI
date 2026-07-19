# 🎤 SentinelAI — Demo Script & Pitch

A tight 3–4 minute live demo. Rehearse until it's muscle memory. Record a
backup video in case venue wifi fails.

---

## Setup before you present
- [ ] Backend + frontend deployed and open in tabs.
- [ ] WhatsApp open on a phone (screen-mirrored if possible).
- [ ] Models pre-warmed (send one throwaway request).
- [ ] Mock data seeded (`scripts/seed_reports.py`, `scripts/seed_graph.py`).
- [ ] Sample voice note + fake-note image ready to send.
- [ ] Backup video queued.

---

## The script (≈ 3.5 min)

### [0:00–0:30] Hook — the human cost
> "Imagine a retired teacher gets a video call. On screen: a man in a police
> uniform, official seal behind him. He says she's under 'digital arrest' for
> money laundering. For six hours he keeps her on the call until she transfers
> her life savings. Last year, Indians lost **₹1,776 crore** to exactly this
> scam."

Pause. Let it land.

### [0:30–1:00] The gap
> "Cybercrime complaints jumped **60%** to over a million. But police get the
> case *after* the money is gone. There's no tool that detects the threat at
> the **point of contact**. That's the gap SentinelAI closes."

### [1:00–2:00] Killer demo — Citizen Fraud Shield (LIVE)
1. On the phone: forward the suspicious **voice note** to the SentinelAI
   WhatsApp number.
2. Narrate while it processes:
   > "SentinelAI runs deepfake voice detection and classifies the scam script —
   > right now, over WhatsApp, no app to install."
3. Show the reply: **⚠️ HIGH RISK — fake CBI officer scam. Disconnect. Call
   1930.**
   > "In seconds, in the citizen's own language, before a rupee is lost."

### [2:00–2:45] The platform — Law-enforcement dashboard
1. Switch to the dashboard. Point at the **hotspot map**.
   > "Every report becomes intelligence. Here are active digital-arrest
   > hotspots in real time."
2. Open the **fraud-network graph**.
   > "SentinelAI links phone numbers, UPI IDs and devices across victims —
   > turning isolated complaints into a single money-mule network, packaged for
   > court."

### [2:45–3:05] Breadth — Counterfeit check
1. Upload the **fake-note image**.
   > "The same platform verifies currency at the point of sale — closing the
   > loop on counterfeiting, the other half of this problem statement."

### [3:05–3:30] Impact + honest close
> "SentinelAI shifts public safety from reactive to proactive. It runs on
> serverless AI — no GPU, scales instantly, costs almost nothing per check.
> It's a prototype: the counterfeit model needs fine-tuning and the LE
> endpoints need production auth — and we've documented exactly how we'd get
> there. But the core — stopping a scam mid-call — works today."

---

## Judge Q&A — prepared answers

**"How is this different from existing fraud tools?"**
> Existing tools are reactive and single-modal. SentinelAI is proactive
> (point-of-contact) and converged — voice, text, image, and graph in one
> pipeline, delivered where citizens already are: WhatsApp.

**"What about false positives?"**
> Citizen tools are tuned for low false-positive rates and always point to the
> official 1930 helpline rather than making enforcement decisions. Verdicts are
> advisory.

**"Is the counterfeit detection real?"**
> It's a working Vision Transformer prototype. A production version needs a
> fine-tuned model with dedicated microprint/security-thread heads — that's in
> our model card and roadmap.

**"How does it scale / what does it cost?"**
> Stateless FastAPI, managed databases, and serverless inference (Groq +
> HuggingFace). No GPU. Cost scales per request, near-zero at rest.

**"Is it secure / privacy-safe?"**
> Sensitive LE endpoints are token-guarded (production needs full RBAC — we
> flag this honestly), verdicts are auditable for court admissibility, and we
> use no real victim PII.

**"What's the business model / who buys this?"**
> State police cybercrime units and MHA (intelligence + dashboard), and banks /
> payment providers (fraud shield + counterfeit at POS).

---

## Failure recovery
- Wifi dies → switch to the **backup video** immediately, keep narrating.
- HF cold-start lag → have a **pre-computed result** screenshot ready.
- WhatsApp hiccup → fall back to the **dashboard live-demo tile** with the same
  sample.
