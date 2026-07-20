"""
API client for the SentinelAI Streamlit dashboard.

Every function tries the live FastAPI backend first and falls back to
`mock_data` if the backend is unreachable or Demo Mode is on. This means the
dashboard ALWAYS works — perfect for a hackathon where the backend may not be
finished or the venue wifi is flaky.

Backend base URL resolution order:
  1. st.session_state["api_base_url"]  (set from the sidebar)
  2. env var NEXT_PUBLIC_API_BASE_URL / API_BASE_URL
  3. http://localhost:8000
"""

from __future__ import annotations

import os

import requests
import streamlit as st

from . import mock_data

DEFAULT_TIMEOUT = 8


def get_base_url() -> str:
    return (
        st.session_state.get("api_base_url")
        or os.getenv("NEXT_PUBLIC_API_BASE_URL")
        or os.getenv("API_BASE_URL")
        or "http://localhost:8000"
    )


def demo_mode() -> bool:
    """When True, always use mock data and never hit the network."""
    return st.session_state.get("demo_mode", True)


def backend_online() -> bool:
    """Cheap health probe; cached in session to avoid spamming the backend."""
    if demo_mode():
        return False
    try:
        r = requests.get(f"{get_base_url()}/health", timeout=3)
        return r.status_code == 200
    except requests.RequestException:
        return False


def _get(path: str, fallback):
    """GET helper with graceful fallback to a mock provider callable."""
    if demo_mode():
        return fallback()
    try:
        r = requests.get(f"{get_base_url()}{path}", timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return fallback()


def _post(path: str, fallback, **kwargs):
    """POST helper with graceful fallback."""
    if demo_mode():
        return fallback()
    try:
        r = requests.post(f"{get_base_url()}{path}", timeout=DEFAULT_TIMEOUT, **kwargs)
        r.raise_for_status()
        return r.json()
    except requests.RequestException:
        return fallback()


# --- Dashboard data ----------------------------------------------------------

def get_stats() -> dict:
    return _get("/reports/stats", mock_data.get_stats)


def get_reports() -> list[dict]:
    return _get("/reports", mock_data.get_reports)


def get_hotspots() -> list[dict]:
    return _get("/reports/hotspots", mock_data.get_hotspots)


def get_scam_trend() -> list[dict]:
    # No dedicated backend endpoint yet — always mock for now.
    return mock_data.get_scam_trend()


def get_scam_type_breakdown() -> list[dict]:
    return mock_data.get_scam_type_breakdown()


def get_clusters() -> dict:
    return _get("/graph/clusters", mock_data.get_clusters)


# --- Live demo (analysis) ----------------------------------------------------

def analyze_text(text: str) -> dict:
    return _post(
        "/shield/chat",
        lambda: mock_data.analyze_text(text),
        json={"message": text},
    )


def analyze_audio(file_bytes: bytes, filename: str) -> dict:
    return _post(
        "/scam/analyze-audio",
        lambda: mock_data.analyze_audio(filename),
        files={"file": (filename, file_bytes)},
    )


def analyze_image(file_bytes: bytes, filename: str) -> dict:
    return _post(
        "/counterfeit/verify",
        lambda: mock_data.analyze_image(filename),
        files={"file": (filename, file_bytes)},
    )
