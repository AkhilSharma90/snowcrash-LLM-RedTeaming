"""Findings tab renderer."""

from datetime import datetime

import pandas as pd
import streamlit as st

from .common import sev_badge, title


def render(ss) -> None:
    st.subheader("Findings Dashboard")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Prioritized findings (severity × impact)")
    if ss.findings:
        df = pd.DataFrame(ss.findings)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            sev = st.multiselect("Severity", sorted(df["severity"].unique().tolist()))
        with c2:
            cat = st.multiselect("Category", sorted(df["category"].unique().tolist()))
        with c3:
            status = st.multiselect("Status", sorted(df["status"].unique().tolist()))
        with c4:
            owner = st.multiselect("Owner", sorted(df["owner"].unique().tolist()))
        fdf = df.copy()
        if sev:
            fdf = fdf[fdf["severity"].isin(sev)]
        if cat:
            fdf = fdf[fdf["category"].isin(cat)]
        if status:
            fdf = fdf[fdf["status"].isin(status)]
        if owner:
            fdf = fdf[fdf["owner"].isin(owner)]

        rows = []
        for _, record in fdf.sort_values("timestamp", ascending=False).iterrows():
            rows.append(
                "<tr>"
                f"<td>{record['timestamp']}</td>"
                f"<td>{record['run_id']}</td>"
                f"<td>{sev_badge(record['severity'])}</td>"
                f"<td>{record['category']}</td>"
                f"<td>{record['title']}</td>"
                f"<td>{record['status']}</td>"
                f"<td>{record['owner']}</td>"
                "</tr>"
            )
        html = (
            "<table style='width:100%;border-collapse:collapse'>"
            "<thead><tr><th style='text-align:left'>Time</th><th>Run</th><th>Severity</th>"
            "<th>Category</th><th>Title</th><th>Status</th><th>Owner</th></tr></thead>"
            "<tbody>" + "".join(rows) + "</tbody></table>"
        )
        st.markdown(html, unsafe_allow_html=True)

        st.download_button(
            "Download filtered CSV",
            data=fdf.to_csv(index=False).encode("utf-8"),
            file_name=f"snowcrash_findings_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )
    else:
        st.info("No findings yet. Run a campaign to generate evidence.")
    st.markdown("</div>", unsafe_allow_html=True)
