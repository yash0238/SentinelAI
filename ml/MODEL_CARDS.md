# Model Cards

Every model SentinelAI relies on, why we chose it, and its limits. Being
honest about limitations scores points on Technical Excellence and shows
judges you understand real-world deployment.

---

## 1. Audio Deepfake / Synthetic Voice Detection

- **Model:** `facebook/wav2vec2-base-960h` (baseline) or a fine-tuned
  synthetic-voice detector from the HuggingFace Hub.
- **Task:** `audio-classification`.
- **Input:** short voice-note clip (wav/ogg).
- **Output:** probability the audio is AI-generated.
- **Why:** catches AI-cloned voices used in live digital-arrest calls.
- **Limitations:** accuracy drops on noisy phone audio and unseen TTS engines;
  treat as one signal, not a sole verdict. Consider Resemble AI for the
  premium real-time path.

## 2. Scam-Script Classification

- **Model:** `MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli`.
- **Task:** `zero-shot-classification`.
- **Input:** message / transcript text.
- **Output:** best-matching scam category + confidence.
- **Why:** zero training needed; classifies novel scripts against our label
  set (see `labels/`).
- **Limitations:** English-centric; pair with Groq translation for regional
  languages. Confidence is relative, not calibrated probability.

## 3. Counterfeit Currency Vision

- **Model:** `google/vit-base-patch16-224` (baseline ViT).
- **Task:** `image-classification`.
- **Input:** banknote photo.
- **Output:** authenticity signal / feature flags.
- **Why:** demonstrates the mobile/POS counterfeit-check flow.
- **Limitations:** a generic ViT is **not** a trained counterfeit detector; for
  the demo, present it honestly as a feature-checking prototype and describe
  the production path (fine-tune on genuine/fake datasets, add microprint &
  security-thread specialised checks).

## 4. Conversational / Summarisation LLM

- **Model:** `llama3-70b-8192` via **Groq**.
- **Why:** blazing inference speed for real-time multilingual replies and
  verdict explanations.
- **Limitations:** can hallucinate; constrain with tight prompts and never let
  it invent legal/financial advice.

---

> Update this file as you swap models or tune thresholds. Judges love a clear,
> honest model card.
