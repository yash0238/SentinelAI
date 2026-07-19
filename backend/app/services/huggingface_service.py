"""
Service: HuggingFace Inference API wrapper.

Central client for all HuggingFace-hosted models so we never run heavy models
locally. One thin function per capability.

Capabilities
------------
- classify_audio(audio_bytes)   -> synthetic vs. human voice score
                                   (HF_AUDIO_MODEL, audio-classification).
- zero_shot_classify(text, labels) -> scam-script category + confidence
                                   (HF_ZEROSHOT_MODEL).
- classify_image(image_bytes)   -> banknote authenticity signal
                                   (HF_VISION_MODEL, image-classification).

Design notes
------------
- Use httpx.AsyncClient with retry (tenacity) for resilience.
- Read HF_API_TOKEN and model ids from app.config.settings.
- Normalise all responses to a small internal result dataclass.

TODO
----
[ ] Implement the three functions above.
[ ] Handle model cold-start (503) by retrying with backoff.
"""
