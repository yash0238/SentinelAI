"""
Mock data provider for the SentinelAI Streamlit dashboard.

Lets the dashboard demo fully WITHOUT a running backend. Every function here
mirrors the shape the real backend endpoints will return, so switching to the
live API (see api_client.py) is transparent.

All data is synthetic. No real victim PII.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

# Deterministic-ish randomness so the demo looks stable across reruns.
random.seed(42)

SCAM_TYPES = [
    "Digital Arrest (fake CBI/ED)",
    "Fake Courier / Customs",
    "KYC / Bank Update",
    "OTP / UPI Phishing",
    "Investment / Trading",
    "Loan App Extortion",
    "Electricity Disconnection",
    "Job / Work-from-home",
]

LANGUAGES = ["Hindi", "English", "Marathi", "Tamil", "Telugu", "Bengali", "Kannada"]

# (city, lat, lng) — major Indian cities used for hotspot placement.
CITIES = [
    ("Delhi", 28.6139, 77.2090),
    ("Mumbai", 19.0760, 72.8777),
    ("Bengaluru", 12.9716, 77.5946),
    ("Hyderabad", 17.3850, 78.4867),
    ("Chennai", 13.0827, 80.2707),
    ("Kolkata", 22.5726, 88.3639),
    ("Pune", 18.5204, 73.8567),
    ("Jaipur", 26.9124, 75.7873),
    ("Ahmedabad", 23.0225, 72.5714),
    ("Lucknow", 26.8467, 80.9462),
    ("Nagpur", 21.1458, 79.0882),
    ("Patna", 25.5941, 85.1376),
]

STATUSES = ["New", "Under Review", "Escalated", "Resolved"]


def get_stats() -> dict:
    """KPI figures for the overview header."""
    return {
        "active_sessions": 18,
        "high_risk_today": 47,
        "total_reports": 1284,
        "counterfeit_flags": 63,
        "amount_saved_cr": 12.4,          # ₹ crore of attempted fraud blocked
        "avg_detection_seconds": 3.2,
    }


def get_reports(n: int = 60) -> list[dict]:
    """A list of synthetic fraud reports for the reports table."""
    reports = []
    now = datetime.now()
    for i in range(n):
        city, lat, lng = random.choice(CITIES)
        risk = random.choices(
            ["CRITICAL", "HIGH", "MEDIUM", "LOW"], weights=[15, 35, 30, 20]
        )[0]
        reports.append(
            {
                "id": f"SA-{10000 + i}",
                "created_at": (now - timedelta(minutes=random.randint(1, 4320))).strftime(
                    "%Y-%m-%d %H:%M"
                ),
                "scam_type": random.choice(SCAM_TYPES),
                "risk_level": risk,
                "risk_score": {
                    "CRITICAL": random.randint(88, 99),
                    "HIGH": random.randint(70, 87),
                    "MEDIUM": random.randint(45, 69),
                    "LOW": random.randint(5, 44),
                }[risk],
                "language": random.choice(LANGUAGES),
                "source": random.choice(["WhatsApp", "IVR", "Dashboard"]),
                "city": city,
                "lat": lat + random.uniform(-0.05, 0.05),
                "lng": lng + random.uniform(-0.05, 0.05),
                "amount_involved": random.choice([0, 25000, 50000, 120000, 300000, 750000]),
                "status": random.choice(STATUSES),
            }
        )
    return reports


def get_hotspots() -> list[dict]:
    """Aggregated hotspot points for the map (city-level counts)."""
    hotspots = []
    for city, lat, lng in CITIES:
        count = random.randint(8, 120)
        hotspots.append(
            {
                "city": city,
                "lat": lat,
                "lng": lng,
                "count": count,
                "risk": "CRITICAL" if count > 90 else "HIGH" if count > 50 else "MEDIUM",
            }
        )
    return hotspots


def get_scam_trend(days: int = 14) -> list[dict]:
    """Daily report counts for the trend chart."""
    now = datetime.now()
    trend = []
    base = 40
    for d in range(days, 0, -1):
        base += random.randint(-6, 10)
        day = now - timedelta(days=d)
        trend.append({"date": day.strftime("%b %d"), "reports": max(10, base)})
    return trend


def get_scam_type_breakdown() -> list[dict]:
    """Counts per scam type for the breakdown chart."""
    return [
        {"scam_type": t, "count": random.randint(40, 260)} for t in SCAM_TYPES
    ]


def get_clusters() -> dict:
    """
    A fraud-network cluster: nodes + edges for the graph view.
    Node types: victim, suspect, phone, upi, device, ip.
    """
    nodes = [
        {"id": "V1", "label": "Victim A", "type": "victim"},
        {"id": "V2", "label": "Victim B", "type": "victim"},
        {"id": "V3", "label": "Victim C", "type": "victim"},
        {"id": "P1", "label": "+91 98••• 210", "type": "phone"},
        {"id": "P2", "label": "+91 90••• 774", "type": "phone"},
        {"id": "U1", "label": "mule1@upi", "type": "upi"},
        {"id": "U2", "label": "mule2@upi", "type": "upi"},
        {"id": "U3", "label": "collector@upi", "type": "upi"},
        {"id": "D1", "label": "Device 4F:A2", "type": "device"},
        {"id": "S1", "label": "Suspect X", "type": "suspect"},
    ]
    edges = [
        ("V1", "P1", "received call"),
        ("V2", "P1", "received call"),
        ("V3", "P2", "received call"),
        ("P1", "D1", "linked device"),
        ("P2", "D1", "linked device"),
        ("V1", "U1", "transferred"),
        ("V2", "U2", "transferred"),
        ("V3", "U2", "transferred"),
        ("U1", "U3", "funneled"),
        ("U2", "U3", "funneled"),
        ("D1", "S1", "operated by"),
        ("U3", "S1", "controlled by"),
    ]
    return {"nodes": nodes, "edges": edges, "cluster_id": "RING-007"}


# --- Live-demo verdict mocks -------------------------------------------------

def analyze_text(text: str) -> dict:
    """Heuristic mock scam classifier for the live demo (no backend needed)."""
    text_l = (text or "").lower()
    signals = {
        "arrest": ["arrest", "cbi", "ed ", "narcotics", "police case", "money laundering", "custody"],
        "courier": ["parcel", "courier", "customs", "fedex", "seized"],
        "kyc": ["kyc", "account block", "verify your account", "pan card"],
        "otp": ["otp", "upi pin", "share code", "cvv"],
        "urgency": ["urgent", "immediately", "arrest warrant", "do not disconnect", "within 1 hour"],
    }
    score = 0
    matched = []
    for label, kws in signals.items():
        for kw in kws:
            if kw in text_l:
                score += 18
                matched.append(label)
                break
    score = min(score, 99)
    scam_type = "Digital Arrest (fake CBI/ED)" if "arrest" in matched else (
        "Fake Courier / Customs" if "courier" in matched else (
            "OTP / UPI Phishing" if "otp" in matched else (
                "KYC / Bank Update" if "kyc" in matched else "Likely Legitimate")))
    risk = _score_to_risk(score)
    return {
        "risk_level": risk,
        "risk_score": score,
        "scam_type": scam_type,
        "matched_signals": sorted(set(matched)),
        "explanation": _explain(risk, scam_type),
        "source": "mock",
    }


def analyze_audio(filename: str) -> dict:
    """Mock deepfake-voice verdict. Uses filename hints for a stable demo."""
    fn = (filename or "").lower()
    synthetic = any(k in fn for k in ["synthetic", "fake", "clone", "ai"])
    prob = 0.94 if synthetic else 0.11
    score = int(prob * 100) if synthetic else 22
    risk = _score_to_risk(score if synthetic else 20)
    return {
        "risk_level": risk,
        "risk_score": score,
        "synthetic_voice_probability": prob,
        "scam_type": "Digital Arrest (fake CBI/ED)" if synthetic else "Likely Legitimate",
        "explanation": (
            "High probability of an AI-generated voice combined with a coercive "
            "script — consistent with a live digital-arrest scam."
            if synthetic
            else "Voice appears human and no coercive script detected."
        ),
        "source": "mock",
    }


def analyze_image(filename: str) -> dict:
    """Mock counterfeit-note verdict with a per-feature checklist."""
    fn = (filename or "").lower()
    fake = any(k in fn for k in ["fake", "counterfeit", "forged"])
    checklist = {
        "Microprint": not fake,
        "Security thread": not fake,
        "Serial-number pattern": not fake,
        "Intaglio print texture": not fake,
        "Watermark": True,  # often passes even on fakes
    }
    passed = sum(checklist.values())
    score = int((1 - passed / len(checklist)) * 100)
    return {
        "authentic": not fake,
        "risk_level": _score_to_risk(score),
        "risk_score": score,
        "feature_checklist": checklist,
        "explanation": (
            "Multiple security features failed verification — flag for manual "
            "inspection." if fake else "All key security features verified."
        ),
        "source": "mock",
    }


def _score_to_risk(score: int) -> str:
    if score >= 85:
        return "CRITICAL"
    if score >= 65:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def _explain(risk: str, scam_type: str) -> str:
    if risk in ("CRITICAL", "HIGH"):
        return (
            f"This matches a known **{scam_type}** pattern. Do not pay, share "
            "OTP/UPI PIN, or stay on the call. Disconnect and call 1930."
        )
    if risk == "MEDIUM":
        return "Some suspicious markers present. Stay cautious and verify independently."
    return "No strong scam markers detected. Remain alert and never share OTPs."
