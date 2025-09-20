"""Settings tab renderer."""

import streamlit as st

from tab_common import title


def render(ss) -> None:  # pylint: disable=unused-argument
    st.subheader("Settings")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Org, API keys, retention, access controls")
    st.text_input("Organization", "Snowcrash Security")
    st.text_input("Contact email", "security@snowcrash.example")
    st.selectbox(
        "Evidence retention", ["7 days", "30 days", "90 days", "1 year"], index=2
    )
    st.text_input("OpenAI API key", type="password")
    st.text_input("Anthropic API key", type="password")
    st.text_input("GitHub token", type="password")
    st.checkbox("Mask PII in logs", value=True)
    st.checkbox("Disable external network during tests", value=False)
    st.success("Settings saved (placeholder). Store securely in your backend.")
    st.markdown("</div>", unsafe_allow_html=True)
