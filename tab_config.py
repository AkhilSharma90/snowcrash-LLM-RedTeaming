"""Target config tab renderer."""

import streamlit as st

from tab_common import title


def render(ss) -> None:  # pylint: disable=unused-argument
    st.subheader("Target Config")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Connect models, agents, and MCP tools")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.selectbox(
            "Model",
            [
                "OpenAI GPT-4/4.1",
                "Anthropic Claude",
                "Local vLLM",
                "Open Source (Llama, Mistral)",
            ],
        )
        st.slider("Temperature", 0.0, 1.5, 0.7, 0.05)
        st.slider("Top-p", 0.0, 1.0, 1.0, 0.05)
    with c2:
        st.selectbox(
            "Agent framework",
            ["LangChain", "LlamaIndex", "OpenAI Assistants", "Custom"],
        )
        st.multiselect(
            "MCP tools",
            ["filesystem", "browser", "slack", "github", "jira", "sql-db", "s3"],
            default=["filesystem", "github"],
        )
    with c3:
        st.selectbox(
            "Auth mode", ["Sandbox creds", "Customer sandbox", "Prod (read-only)"], index=0
        )
        st.number_input("Rate limit (req/min)", 1, 5000, 120)
    st.text_area(
        "Tooling config (YAML / JSON)",
        "mcp:\n  filesystem:\n    root: /tmp/sim\n  github:\n    repo: org/app\n",
        height=160,
    )
    st.success("Config ready (placeholder). Wire to backend runtime.")
    st.markdown("</div>", unsafe_allow_html=True)
