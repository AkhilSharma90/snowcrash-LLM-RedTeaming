"""Home tab renderer."""

from __future__ import annotations

import math
import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from tab_common import title


def _init_home_state(ss) -> None:
    if "home_activity" in ss:
        return

    rng = random.Random(1337)
    base = datetime.utcnow() - timedelta(days=13)
    days = [base + timedelta(days=i) for i in range(14)]
    campaign_load = []
    finding_load = []
    mttr_hours = []
    for idx, _day in enumerate(days):
        campaign_load.append(58 + int(6 * math.sin(idx / 2.4)) + rng.randint(-3, 5))
        finding_load.append(14 + int(4 * math.cos(idx / 2.1)) + (idx % 5) - 1)
        mttr_raw = 6.4 - 0.28 * idx + 0.9 * math.sin(idx / 2.7)
        mttr_hours.append(max(1.8, round(mttr_raw, 2)))

    ss.home_activity = (
        pd.DataFrame(
            {
                "day": days,
                "Campaign load": campaign_load,
                "Findings": finding_load,
            }
        ).set_index("day")
    )

    ss.home_mttr = (
        pd.DataFrame({"day": days, "MTTR (hrs)": mttr_hours}).set_index("day")
    )

    ss.home_severity = (
        pd.DataFrame(
            {
                "Severity": ["Critical", "High", "Medium", "Low"],
                "Count": [11, 23, 36, 29],
            }
        ).set_index("Severity")
    )

    ss.home_environment = (
        pd.DataFrame(
            {
                "Environment": [
                    "Sandbox",
                    "Customer staging",
                    "Prod (read-only)",
                    "MCP sandboxes",
                ],
                "Runs": [192, 138, 84, 109],
            }
        ).set_index("Environment")
    )

    ss.home_snapshot = {
        "active_campaigns": 18,
        "active_campaigns_delta": "+3 vs yesterday",
        "critical_open": 11,
        "critical_open_delta": "+2",
        "mean_mttr": "5.2 h",
        "mean_mttr_delta": "-0.8h",
        "tools_in_scope": "42 tools",
        "tools_in_scope_delta": "+5 onboarded",
        "runs_24h": "312",
        "runs_delta": "+27",
        "crit_24h": "9",
        "crit_delta": "+3",
    }

    ss.home_coverage = [
        ("LLM agents", 0.82),
        ("MCP toolchain", 0.74),
        ("External connectors", 0.67),
        ("Decision routing", 0.58),
        ("Data loss guards", 0.71),
        ("Human hand-offs", 0.46),
    ]

    now = datetime.utcnow()
    ss.home_findings_table = pd.DataFrame(
        [
            {
                "Severity": "Critical",
                "Campaign": "RUN-0234",
                "Vector": "Tool abuse via MCP chain",
                "Detected": (now - timedelta(hours=1, minutes=18)).strftime(
                    "%Y-%m-%d %H:%MZ"
                ),
                "MTTR": "2.4 h",
                "Owner": "redteam@snowcrash",
            },
            {
                "Severity": "High",
                "Campaign": "RUN-0232",
                "Vector": "Prompt injection — policy override",
                "Detected": (now - timedelta(hours=3, minutes=5)).strftime(
                    "%Y-%m-%d %H:%MZ"
                ),
                "MTTR": "3.1 h",
                "Owner": "secops@client",
            },
            {
                "Severity": "High",
                "Campaign": "RUN-0229",
                "Vector": "Data exfil via retrieval",
                "Detected": (now - timedelta(hours=6, minutes=44)).strftime(
                    "%Y-%m-%d %H:%MZ"
                ),
                "MTTR": "4.6 h",
                "Owner": "redteam@snowcrash",
            },
            {
                "Severity": "Medium",
                "Campaign": "RUN-0227",
                "Vector": "Credential stuffing (simulated)",
                "Detected": (now - timedelta(hours=11, minutes=8)).strftime(
                    "%Y-%m-%d %H:%MZ"
                ),
                "MTTR": "5.1 h",
                "Owner": "eng@client",
            },
            {
                "Severity": "Medium",
                "Campaign": "RUN-0224",
                "Vector": "Hallucinated actions escalation",
                "Detected": (now - timedelta(hours=15, minutes=32)).strftime(
                    "%Y-%m-%d %H:%MZ"
                ),
                "MTTR": "6.8 h",
                "Owner": "secops@client",
            },
        ]
    )


def render(ss) -> None:
    _init_home_state(ss)

    snapshot = ss.home_snapshot

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("<div class='sc-card sc-hero'>", unsafe_allow_html=True)
        st.markdown(
            (
                "<h2 style='font-family:Space Grotesk, sans-serif; font-size:34px; margin-bottom:8px;'>"
                "Snowcrash Threat Operations Center"
                "</h2>"
                "<p style='color:var(--text-secondary); font-size:16px; line-height:1.6;'>"
                "Real-time adversarial telemetry across LLM agents, MCP tools, and downstream decision rails."
                "</p>"
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='chips'>"
            "<div class='chip'>Continuous assurance</div>"
            "<div class='chip chip-alt'>MCP tool abuse</div>"
            "<div class='chip'>Decision-chain tamper tests</div>"
            "<div class='chip'>Evidence-grade telemetry</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
        st.markdown("**Situational Snapshot (24h)**", unsafe_allow_html=True)
        k1, k2 = st.columns(2)
        k1.metric("Runs", snapshot["runs_24h"], snapshot["runs_delta"])
        k2.metric("Critical Hits", snapshot["crit_24h"], snapshot["crit_delta"])
        st.area_chart(
            ss.home_activity[["Campaign load"]],
            height=120,
            use_container_width=True,
        )
        st.caption("Campaign load trend (last 14 days)")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='rule'></div>", unsafe_allow_html=True)

    title("Live posture snapshot")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active campaigns", snapshot["active_campaigns"], snapshot["active_campaigns_delta"])
    m2.metric("Critical open", snapshot["critical_open"], snapshot["critical_open_delta"])
    m3.metric("Mean MTTR", snapshot["mean_mttr"], snapshot["mean_mttr_delta"])
    m4.metric("Tools in scope", snapshot["tools_in_scope"], snapshot["tools_in_scope_delta"])

    title("Adversarial activity — 14 day trend")
    c_trend, c_sev = st.columns([2, 1])
    with c_trend:
        st.area_chart(ss.home_activity, height=280, use_container_width=True)
        st.caption("Campaign pressure vs. confirmed findings")
    with c_sev:
        st.bar_chart(ss.home_severity, height=280, use_container_width=True)
        st.caption("Finding severity distribution (active backlog)")

    title("Remediation velocity & throughput")
    c_mttr, c_env = st.columns(2)
    with c_mttr:
        st.line_chart(ss.home_mttr, height=260, use_container_width=True)
        st.caption("MTTR trend — operational hours")
    with c_env:
        st.bar_chart(ss.home_environment, height=260, use_container_width=True)
        st.caption("Campaign throughput by deployment surface (7d)")

    title("Coverage readiness by surface")
    coverage = ss.home_coverage
    for row_idx in range(0, len(coverage), 2):
        cols = st.columns(2)
        for col_idx, col in enumerate(cols):
            idx = row_idx + col_idx
            if idx >= len(coverage):
                continue
            label, pct = coverage[idx]
            with col:
                st.markdown(f"**{label.upper()}** — {int(pct * 100)}%")
                st.progress(pct)

    title("Priority findings — last 24h")
    st.dataframe(
        ss.home_findings_table,
        use_container_width=True,
        hide_index=True,
    )
    st.caption("Escalated items ready for joint response.")
