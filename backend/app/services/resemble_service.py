"""
Service: Resemble AI wrapper (OPTIONAL — premium real-time voice-clone detect).

Used as the high-accuracy path for live "digital arrest" call audio when a
RESEMBLE_API_KEY is configured. Falls back to the HuggingFace audio classifier
otherwise, so the demo always works even without this key.

Functions (planned)
-------------------
- detect_voice_clone(audio_bytes) -> {is_synthetic: bool, confidence: float}

TODO
----
[ ] Implement only if RESEMBLE_API_KEY is present; otherwise no-op.
[ ] Keep the return shape identical to huggingface_service.classify_audio
    so the orchestrator can swap providers transparently.
"""
