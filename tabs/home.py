"""Home tab renderer."""

import streamlit as st

from .common import title


def render(ss) -> None:
    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown("<div class='sc-card sc-hero'>", unsafe_allow_html=True)
        st.markdown(
            (
                "<h2 style='font-family:Space Grotesk, sans-serif; font-size:34px; margin-bottom:8px;'>"
                "snowcrash — Offensive LLM Security"
                "</h2>"
                "<p style='color:var(--text-secondary); font-size:16px; line-height:1.6;'>"
                "Purpose-built to stress-test LLM agents, MCP tools, and decision chains under real attacker pressure."
                "</p>"
            ),
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='chips'>"
            "<div class='chip'>Continuous assurance</div>"
            "<div class='chip chip-alt'>MCP tool abuse</div>"
            "<div class='chip'>Chain-of-thought red-teaming</div>"
            "<div class='chip'>Evidence & remediation insights</div>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
        st.markdown("**Today’s Activity**", unsafe_allow_html=True)
        k1, k2 = st.columns(2)
        k1.metric("Runs", "128", "+22")
        k2.metric("High/Crit", "7", "+3")
        st.line_chart(ss.spark, y="runs", height=90, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
    st.write(
        "Welcome. Use the navbar to jump into Builder, Config, Run, Console, Findings, Reports, or Settings."
    )
