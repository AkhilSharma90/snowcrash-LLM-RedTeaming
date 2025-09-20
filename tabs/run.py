"""Run campaign tab renderer."""

import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from .common import mock_finding, title


def render(ss) -> None:
    st.subheader("Run Campaign")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Select scenarios & targets, then launch")
    scenarios = [scenario["name"] for scenario in ss.scenarios] or [
        "(create scenarios in Builder)"
    ]
    chosen = st.multiselect(
        "Scenarios", scenarios, default=(scenarios[:1] if scenarios else [])
    )
    runs = st.number_input("Parallel runs", 1, 256, 12)
    budget = st.number_input("Max steps per run", 1, 400, 40)
    safety = st.select_slider("Safety level", options=["Low", "Medium", "High"], value="Medium")
    c_go, c_dry = st.columns(2)
    launch = c_go.button("🚀 Launch Campaign")
    dry = c_dry.button("🧪 Dry-Run Plan")
    st.markdown("</div>", unsafe_allow_html=True)

    if dry:
        st.info(
            f"Plan: {len(chosen)} scenario(s) × {runs} parallel — safety={safety}, budget={budget}"
        )

    if launch:
        run_id = f"RUN-{len(ss.runs) + 1:04d}"
        ss.runs.append(
            {
                "run_id": run_id,
                "scenarios": chosen,
                "status": "Running",
                "launched_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                "parallel": runs,
                "budget": budget,
                "safety": safety,
            }
        )
        ss.log.append(
            f"[{run_id}] Launching {len(chosen)} scenario(s) × {runs} parallel — safety={safety}, budget={budget}"
        )
        st.success(f"Campaign launched: {run_id}")
        for idx in range(8):
            time.sleep(0.15)
            ss.log.append(f"[{run_id}] step {idx + 1}: probing tool-chain…")
            if random.random() < 0.55:
                ss.findings.append(mock_finding(run_id))

    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Active/Recent campaigns")
    if ss.runs:
        st.dataframe(pd.DataFrame(ss.runs), use_container_width=True, hide_index=True)
    else:
        st.info("No campaigns yet. Launch one above.")
    st.markdown("</div>", unsafe_allow_html=True)
