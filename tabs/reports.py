"""Reports tab renderer."""

import streamlit as st

from .common import title


def render(ss) -> None:  # pylint: disable=unused-argument
    st.subheader("Evidence & Reports")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Artifacts, traces, exportable reports")
    uploaded = st.file_uploader("Attach files", accept_multiple_files=True)
    if uploaded:
        st.success(
            f"Attached {len(uploaded)} file(s). (Placeholder — persist and link in backend)"
        )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Generate executive summary**")
        st.text_area("Notes", "Overall risk posture improved but 3 critical paths remain.")
        st.button("📄 Generate PDF (placeholder)")
    with c2:
        st.markdown("**Generate remediation plan**")
        st.text_area(
            "Notes", "Throttle tool-call permissions; add policy tests; rotate keys."
        )
        st.button("📝 Generate DOCX (placeholder)")
    st.markdown("</div>", unsafe_allow_html=True)
