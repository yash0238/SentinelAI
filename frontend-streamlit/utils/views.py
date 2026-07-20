"""
Tab render functions for the SentinelAI dashboard.

Each function renders one tab. app.py wires them into st.tabs(). Keeping them
here keeps app.py small and readable.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st

from . import api_client, theme


# =============================================================================
# TAB 1 — Overview
# =============================================================================
def render_overview() -> None:
    stats = api_client.get_stats()

    st.subheader("Command Overview")

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    cards = [
        (c1, stats["active_sessions"], "Active sessions", "#ff7f0e"),
        (c2, stats["high_risk_today"], "High-risk today", "#ff2e63"),
        (c3, f'{stats["total_reports"]:,}', "Total reports", "#4da6ff"),
        (c4, stats["counterfeit_flags"], "Counterfeit flags", "#a66bff"),
        (c5, f'₹{stats["amount_saved_cr"]} Cr', "Fraud blocked", "#2ecc71"),
        (c6, f'{stats["avg_detection_seconds"]}s', "Avg. detection", "#00d0d0"),
    ]
    for col, value, label, accent in cards:
        col.markdown(theme.kpi_card(value, label, accent), unsafe_allow_html=True)

    st.markdown("###  ")
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("#### 🗺️ Active Digital-Arrest Hotspots")
        _render_hotspot_map()

    with right:
        st.markdown("#### 📈 Reports — last 14 days")
        trend = pd.DataFrame(api_client.get_scam_trend())
        fig = px.area(trend, x="date", y="reports", markers=True)
        fig.update_traces(line_color="#4da6ff", fillcolor="rgba(77,166,255,0.15)")
        fig.update_layout(
            height=250, margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### 🧬 Scam-type breakdown")
    breakdown = pd.DataFrame(api_client.get_scam_type_breakdown()).sort_values(
        "count", ascending=True
    )
    fig2 = px.bar(breakdown, x="count", y="scam_type", orientation="h",
                  color="count", color_continuous_scale="Sunsetdark")
    fig2.update_layout(
        height=320, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        coloraxis_showscale=False, yaxis_title="", xaxis_title="",
    )
    st.plotly_chart(fig2, use_container_width=True)


def _render_hotspot_map() -> None:
    hotspots = pd.DataFrame(api_client.get_hotspots())
    hotspots["color"] = hotspots["risk"].map(theme.RISK_RGB)
    hotspots["radius"] = hotspots["count"] * 900

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=hotspots,
        get_position=["lng", "lat"],
        get_fill_color="color",
        get_radius="radius",
        pickable=True,
        opacity=0.55,
    )
    view = pdk.ViewState(latitude=22.0, longitude=79.0, zoom=3.6, pitch=25)
    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view,
            map_style="mapbox://styles/mapbox/dark-v10",
            tooltip={"text": "{city}\nReports: {count}\nRisk: {risk}"},
        )
    )


# =============================================================================
# TAB 2 — Live Demo (the killer feature)
# =============================================================================
def render_live_demo() -> None:
    st.subheader("🔬 Live Threat Analysis")
    st.caption(
        "Submit a suspicious message, a voice note, or a currency-note image. "
        "SentinelAI returns an explainable, multi-modal verdict."
    )

    mode = st.radio(
        "Choose input type",
        ["💬 Text / Transcript", "🎙️ Voice Note", "💵 Currency Note"],
        horizontal=True,
    )

    if mode == "💬 Text / Transcript":
        _render_text_demo()
    elif mode == "🎙️ Voice Note":
        _render_audio_demo()
    else:
        _render_image_demo()


def _render_text_demo() -> None:
    example = (
        "Sir, this is Inspector Sharma from CBI. Your Aadhaar is linked to a "
        "money laundering case. You are under digital arrest. Do not disconnect "
        "this call or share it with anyone. Transfer the amount for verification "
        "immediately or a warrant will be issued."
    )
    text = st.text_area("Paste a suspicious message or call transcript", value=example, height=160)
    if st.button("Analyze message", type="primary"):
        with st.spinner("Running scam-script classification..."):
            result = api_client.analyze_text(text)
        _render_verdict(result)


def _render_audio_demo() -> None:
    st.info(
        "Tip: filenames containing 'synthetic', 'fake', or 'clone' demo the "
        "high-risk path in offline Demo Mode.",
        icon="💡",
    )
    audio = st.file_uploader("Upload a voice note", type=["wav", "mp3", "ogg", "m4a"])
    if audio is not None:
        st.audio(audio)
        if st.button("Analyze voice note", type="primary"):
            with st.spinner("Running deepfake-voice detection..."):
                result = api_client.analyze_audio(audio.getvalue(), audio.name)
            _render_verdict(result, extra_key="synthetic_voice_probability",
                            extra_label="Synthetic-voice probability", is_pct=True)


def _render_image_demo() -> None:
    st.info(
        "Tip: filenames containing 'fake' or 'counterfeit' demo the flagged "
        "path in offline Demo Mode.",
        icon="💡",
    )
    img = st.file_uploader("Upload a banknote image", type=["jpg", "jpeg", "png"])
    if img is not None:
        st.image(img, width=320)
        if st.button("Verify currency", type="primary"):
            with st.spinner("Running counterfeit vision checks..."):
                result = api_client.analyze_image(img.getvalue(), img.name)
            _render_verdict(result)
            checklist = result.get("feature_checklist")
            if checklist:
                st.markdown("##### Security-feature checklist")
                for feature, ok in checklist.items():
                    st.markdown(f"- {'✅' if ok else '❌'} {feature}")


def _render_verdict(result: dict, extra_key: str | None = None,
                    extra_label: str = "", is_pct: bool = False) -> None:
    risk = result.get("risk_level", "LOW")
    score = result.get("risk_score", 0)
    color = theme.RISK_COLORS.get(risk, "#888")

    st.markdown(
        f"""
        <div class="sa-verdict" style="background:linear-gradient(160deg,{color}22,#0e131f);
             border-color:{color}66;">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <div style="font-size:1.4rem;font-weight:800;color:{color};">
                    {risk} RISK
                </div>
                <div style="font-size:1.1rem;color:#c7d0e0;">Risk score: <b>{score}</b>/100</div>
            </div>
            <div style="margin-top:6px;color:#c7d0e0;">
                <b>Type:</b> {result.get('scam_type', result.get('authentic') and 'Authentic' or 'N/A')}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.progress(min(int(score), 100) / 100)

    if extra_key and extra_key in result:
        val = result[extra_key]
        st.metric(extra_label, f"{val*100:.0f}%" if is_pct else val)

    matched = result.get("matched_signals")
    if matched:
        st.write("**Detected signals:** " + ", ".join(matched))

    st.markdown(f"**Verdict explanation:** {result.get('explanation', '')}")

    if risk in ("CRITICAL", "HIGH"):
        st.error(
            "⚠️ Recommended action: Disconnect immediately. Do NOT pay or share "
            "OTP/UPI PIN. Call the Cyber Crime Helpline **1930** and report at "
            "cybercrime.gov.in.",
            icon="🚨",
        )

    if result.get("source") == "mock":
        st.caption("🧪 Result generated in offline Demo Mode (no backend connected).")


# =============================================================================
# TAB 3 — Fraud Network
# =============================================================================
def render_network() -> None:
    st.subheader("🕸️ Fraud Network Intelligence")
    cluster = api_client.get_clusters()
    st.caption(
        f"Detected cluster **{cluster.get('cluster_id', 'N/A')}** — isolated "
        "victim reports linked into a single money-mule network."
    )

    dot = _build_graphviz(cluster)
    st.graphviz_chart(dot, use_container_width=True)

    with st.expander("Legend"):
        for ntype, color in theme.NODE_COLORS.items():
            st.markdown(
                f'<span style="color:{color};font-weight:700;">●</span> {ntype.title()}',
                unsafe_allow_html=True,
            )

    st.markdown("#### 📦 Intelligence Package")
    st.write(
        "Generate a court-admissible, timestamped, source-attributed package "
        "for this cluster."
    )
    if st.button("Generate intelligence package"):
        st.success(
            f"Package for cluster {cluster.get('cluster_id')} generated: "
            f"{len(cluster['nodes'])} entities, {len(cluster['edges'])} links, "
            "with full provenance and audit trail.",
            icon="📦",
        )


def _build_graphviz(cluster: dict) -> str:
    lines = [
        "digraph G {",
        'rankdir=LR; bgcolor="transparent";',
        'node [style=filled, fontcolor="#0b0f1a", fontname="Helvetica", shape=box, penwidth=0];',
        'edge [color="#8a94a6", fontcolor="#8a94a6", fontsize=9];',
    ]
    for node in cluster["nodes"]:
        color = theme.NODE_COLORS.get(node["type"], "#cccccc")
        shape = "ellipse" if node["type"] in ("victim", "suspect") else "box"
        lines.append(
            f'"{node["id"]}" [label="{node["label"]}", fillcolor="{color}", shape={shape}];'
        )
    for src, dst, label in cluster["edges"]:
        lines.append(f'"{src}" -> "{dst}" [label="{label}"];')
    lines.append("}")
    return "\n".join(lines)


# =============================================================================
# TAB 4 — Reports
# =============================================================================
def render_reports() -> None:
    st.subheader("📋 Fraud Reports")
    reports = pd.DataFrame(api_client.get_reports())

    f1, f2, f3 = st.columns(3)
    with f1:
        risk_filter = st.multiselect(
            "Risk level", ["CRITICAL", "HIGH", "MEDIUM", "LOW"], default=[]
        )
    with f2:
        type_filter = st.multiselect(
            "Scam type", sorted(reports["scam_type"].unique().tolist()), default=[]
        )
    with f3:
        source_filter = st.multiselect(
            "Source", sorted(reports["source"].unique().tolist()), default=[]
        )

    filtered = reports.copy()
    if risk_filter:
        filtered = filtered[filtered["risk_level"].isin(risk_filter)]
    if type_filter:
        filtered = filtered[filtered["scam_type"].isin(type_filter)]
    if source_filter:
        filtered = filtered[filtered["source"].isin(source_filter)]

    st.caption(f"Showing {len(filtered)} of {len(reports)} reports")

    display = filtered[
        ["id", "created_at", "scam_type", "risk_level", "risk_score",
         "language", "source", "city", "amount_involved", "status"]
    ].rename(
        columns={
            "id": "ID", "created_at": "Time", "scam_type": "Scam Type",
            "risk_level": "Risk", "risk_score": "Score", "language": "Lang",
            "source": "Source", "city": "City",
            "amount_involved": "Amount (₹)", "status": "Status",
        }
    )
    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=100, format="%d"
            ),
            "Amount (₹)": st.column_config.NumberColumn(format="₹%d"),
        },
    )
