"""Console tab renderer."""

import streamlit as st

from .common import title


def render(ss) -> None:
    st.subheader("Live Console")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Streaming logs & step traces")
    if ss.log:
        st.text("\n".join(ss.log[-600:]))
    else:
        st.info("No logs yet. Launch a campaign to see live output.")
    st.markdown("</div>", unsafe_allow_html=True)
