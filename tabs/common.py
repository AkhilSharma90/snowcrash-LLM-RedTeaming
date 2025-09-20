"""Shared helpers for Snowcrash tab renderers."""

import random
from datetime import datetime

import streamlit as st


def title(label: str) -> None:
    """Render a section title with the app's styled divider."""
    st.markdown(f"<div class='sec-title'>{label}</div>", unsafe_allow_html=True)


def sev_badge(sev: str) -> str:
    """Return a severity badge span with the proper CSS class."""
    severity = (sev or "").lower()
    if severity == "critical":
        cls = "badge-crit"
    elif severity == "high":
        cls = "badge-hi"
    else:
        cls = "badge"
    return f"<span class='{cls}'>{sev.title()}</span>"


def mock_finding(run_id: str) -> dict:
    """Create a pseudo finding payload for demo purposes."""
    sev = random.choices(
        ["Low", "Medium", "High", "Critical"], [0.25, 0.4, 0.25, 0.1]
    )[0]
    cat = random.choice(
        [
            "Prompt Injection",
            "Tool Abuse (MCP)",
            "Data Exfil",
            "PII Leakage",
            "Policy Bypass",
        ]
    )
    return {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "run_id": run_id,
        "severity": sev,
        "category": cat,
        "title": f"{cat} via multi-step chain",
        "repro": "prompt ▶ tool_call ▶ model_response (open evidence)",
        "status": "Open",
        "owner": random.choice(
            ["redteam@snowcrash", "secops@client", "eng@client"]
        ),
    }
