"""Findings tab renderer."""

from __future__ import annotations

import html
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from tab_common import sev_badge, title


def _terminal_summary_markup(df: pd.DataFrame) -> str:
    now = datetime.utcnow().replace(microsecond=0)
    lines: list[tuple[str, str]] = []
    total = len(df)
    lines.append(("ok", f"summary :: {total} finding(s) in view"))

    severity_order = ["Critical", "High", "Medium", "Low"]
    severity_counts = (
        df["severity"].str.title().value_counts().reindex(severity_order, fill_value=0)
    )
    for sev in severity_order:
        count = int(severity_counts.get(sev, 0))
        level = "crit" if sev == "Critical" else "warn" if sev == "High" else "ok"
        lines.append((level, f"sev::{sev.lower()} => {count}"))

    latest = df.sort_values("timestamp", ascending=False).head(5)
    for _, record in latest.iterrows():
        sev = (record.get("severity") or "").lower()
        if sev == "critical":
            level = "crit"
        elif sev == "high":
            level = "warn"
        else:
            level = "ok"
        ts = record.get("timestamp", "")
        run = record.get("run_id", "")
        cat = record.get("category", "")
        title_txt = record.get("title", "")
        text = (
            f"{ts} :: {run} :: {cat} :: {title_txt}"
        )
        lines.append((level, text))

    rendered = []
    for idx, (level, text) in enumerate(lines):
        cls = {
            "crit": "log-crit",
            "warn": "log-warn",
        }.get(level, "log-ok")
        ts_label = (now - timedelta(seconds=(len(lines) - idx - 1) * 11)).strftime(
            "%H:%M:%S"
        )
        rendered.append(
            "<div class='term-line {}'>".format(cls)
            + f"<span class='ts'>{ts_label}</span>"
            + "<span class='prompt'>λ</span>"
            + f"<span>{html.escape(text)}</span>"
            + "</div>"
        )

    body = "".join(rendered)
    return (
        "<div class='terminal-shell findings-terminal'>"
        "<div class='terminal-header'><span class='dot'></span> snowcrash::findings-summary</div>"
        f"<div class='terminal-body'>{body}</div>"
        "<div class='terminal-footer'>summary // filtered backlog snapshot</div>"
        "</div>"
    )


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

        st.markdown(_terminal_summary_markup(fdf), unsafe_allow_html=True)
        st.markdown("<div class='rule'></div>", unsafe_allow_html=True)

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
