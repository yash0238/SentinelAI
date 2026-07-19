# SentinelAI — ML Assets

We **do not train models from scratch**. We use pre-trained models via the
HuggingFace Inference API and Groq. This folder holds:

```
ml/
├── README.md              # you are here
├── MODEL_CARDS.md         # every model we use + why + limitations
├── notebooks/             # exploration & threshold-tuning notebooks
├── data/                  # sample/mock inputs for the demo (gitignored)
│   ├── audio/             # genuine + synthetic voice samples
│   ├── currency/          # genuine + fake note images
│   └── transcripts/       # scam vs. legitimate call transcripts
└── labels/                # candidate label sets for zero-shot classification
```

## Guiding principle

The AI heavy lifting is remote (HuggingFace/Groq), so your laptop needs **no
GPU**. Your local job is: prepare good sample data, tune the decision
thresholds, and wire the API calls in `backend/app/services/`.

## Getting sample data (legally)

- **Audio:** record your own voice; generate synthetic samples with a free TTS
  for the "fake voice" class. Do not use real victims' recordings.
- **Currency:** use RBI's published specimen images or clearly-labelled mock
  notes. Never photograph real high-value notes for redistribution — keep
  samples local and gitignored.
- **Transcripts:** write your own scam scripts based on public awareness
  advisories (1930 / cybercrime.gov.in). Do not use real victim PII.
