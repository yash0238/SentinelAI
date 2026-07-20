"""
Theme, styling, and shared UI helpers for the SentinelAI dashboard.
"""

from __future__ import annotations

import streamlit as st

RISK_COLORS = {
    "CRITICAL": "#ff2e63",
    "HIGH": "#ff7f0e",
    "MEDIUM": "#f4c430",
    "LOW": "#2ecc71",
}

# RGB variants for pydeck (which needs [r,g,b,a] lists).
RISK_RGB = {
    "CRITICAL": [255, 46, 99],
    "HIGH": [255, 127, 14],
    "MEDIUM": [244, 196, 48],
    "LOW": [46, 204, 113],
}

NODE_COLORS = {
    "victim": "#4da6ff",
    "suspect": "#ff2e63",
    "phone": "#f4c430",
    "upi": "#a66bff",
    "device": "#2ecc71",
    "ip": "#00d0d0",
}


def inject_css() -> None:
    """Global CSS for a darker, more 'command-centre' feel."""
    st.markdown(
        """
        <style>
        .block-container {padding-top: 1.5rem;}
        .sa-header {
            display:flex; align-items:center; gap:14px; margin-bottom:0.25rem;
        }
        .sa-title {font-size:1.9rem; font-weight:800; margin:0; letter-spacing:-0.5px;}
        .sa-sub {color:#8a94a6; margin-top:-4px; font-size:0.95rem;}
        .sa-badge {
            display:inline-block; padding:3px 10px; border-radius:999px;
            font-size:0.78rem; font-weight:700; color:#0b0f1a;
        }
        .sa-kpi {
            background:linear-gradient(160deg,#141a2b,#0e131f);
            border:1px solid #232c42; border-radius:14px; padding:16px 18px;
        }
        .sa-kpi h3 {margin:0; font-size:1.7rem; font-weight:800;}
        .sa-kpi p {margin:2px 0 0; color:#8a94a6; font-size:0.82rem;}
        .sa-verdict {
            border-radius:16px; padding:20px 22px; border:1px solid #232c42;
            margin-top:8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def header() -> None:
    st.markdown(
        """
        <div class="sa-header">
            <span style="font-size:2rem;">🛡️</span>
            <div>
                <p class="sa-title">SentinelAI</p>
                <p class="sa-sub">Proactive Intelligence for Digital Public Safety &amp; Fraud Neutralisation</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(risk: str) -> str:
    color = RISK_COLORS.get(risk, "#888")
    return f'<span class="sa-badge" style="background:{color}">{risk}</span>'


def kpi_card(value, label: str, accent: str = "#4da6ff") -> str:
    return (
        f'<div class="sa-kpi"><h3 style="color:{accent}">{value}</h3>'
        f'<p>{label}</p></div>'
    )
