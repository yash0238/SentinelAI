"""
SentinelAI — Streamlit dashboard (Python-only frontend).

Runs standalone with realistic mock data (Demo Mode) and automatically uses the
FastAPI backend when one is reachable and Demo Mode is turned off.

Run:  streamlit run app.py
Host: works as-is on HuggingFace Spaces (Streamlit SDK) or Streamlit Cloud.

Tabs:
  - Overview:  KPIs, hotspot map, trend + scam-type charts.
  - Live Demo: text / voice / currency analysis with explainable verdicts.
  - Network:   fraud-ring cluster graph + intelligence package.
  - Reports:   filterable table of logged fraud reports.
"""

from __future__ import annotations

import streamlit as st

from utils import api_client, theme, views

st.set_page_config(
    page_title="SentinelAI — Digital Public Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

theme.inject_css()

# --- Session defaults --------------------------------------------------------
st.session_state.setdefault("demo_mode", True)
st.session_state.setdefault("api_base_url", "http://localhost:8000")

# --- Sidebar: connection controls -------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Connection")
    st.session_state["demo_mode"] = st.toggle(
        "Demo Mode (offline mock data)",
        value=st.session_state["demo_mode"],
        help="On: use realistic mock data, no backend needed. "
             "Off: call the live FastAPI backend, falling back to mock on error.",
    )
    st.session_state["api_base_url"] = st.text_input(
        "Backend URL",
        value=st.session_state["api_base_url"],
        disabled=st.session_state["demo_mode"],
    )

    if st.session_state["demo_mode"]:
        st.info("🧪 Demo Mode — showing mock data.", icon="🧪")
    else:
        online = api_client.backend_online()
        if online:
            st.success("🟢 Backend connected.", icon="🟢")
        else:
            st.warning("🔴 Backend unreachable — falling back to mock data.", icon="🔴")

    st.markdown("---")
    st.markdown(
        "**Problem Statement 6**\n\nAI for Digital Public Safety — defeating "
        "counterfeiting, fraud & digital arrest scams."
    )
    st.caption(
        "Prototype for demonstration only. Verdicts are advisory. Not a "
        "certified law-enforcement or financial system."
    )

# --- Main --------------------------------------------------------------------
theme.header()

tab_overview, tab_demo, tab_network, tab_reports = st.tabs(
    ["📊 Overview", "🔬 Live Demo", "🕸️ Network", "📋 Reports"]
)

with tab_overview:
    views.render_overview()

with tab_demo:
    views.render_live_demo()

with tab_network:
    views.render_network()

with tab_reports:
    views.render_reports()
