"""Console tab renderer."""

from __future__ import annotations

import html
from datetime import datetime, timedelta

import streamlit as st

from tab_common import title


def _format_terminal_lines(lines: list[str]) -> str:
    rendered = []
    start = max(len(lines) - 240, 0)
    window = lines[start:]
    base_time = datetime.utcnow()

    for idx, entry in enumerate(window):
        text = html.escape(entry)
        lowered = entry.lower()
        if any(word in lowered for word in ("fail", "critical", "blocked", "error")):
            level = "log-crit"
        elif any(word in lowered for word in ("warn", "retry", "suspicious")):
            level = "log-warn"
        else:
            level = "log-ok"

        ts = base_time.replace(microsecond=0) - (len(window) - idx - 1) * timedelta(seconds=9)
        ts_label = ts.strftime("%H:%M:%S")
        rendered.append(
            f"<div class='term-line {level}'>"
            f"<span class='ts'>{ts_label}</span>"
            f"<span class='prompt'>λ</span>"
            f"<span>{text}</span>"
            "</div>"
        )
    return "".join(rendered)


def render(ss) -> None:
    st.subheader("Live Console")
    st.markdown("<div class='sc-card'>", unsafe_allow_html=True)
    title("Streaming logs & step traces")

    if not ss.log:
        seed = [
            "boot >> wiring adversarial runner contexts…",
            "ok :: attached toolchain: filesystem, github, jira, sql-db",
            "info :: awaiting campaign launch signal (tab: run)",
            "hint :: run a campaign to stream live traces here",
        ]
        payload = _format_terminal_lines(seed)
    else:
        payload = _format_terminal_lines(ss.log)

    terminal_markup = (
        "<div class='terminal-shell'>"
        "<div class='terminal-header'><span class='dot'></span> snowcrash::live-console</div>"
        f"<div class='terminal-body'>{payload}</div>"
        "<div class='terminal-footer'>stream // ctrl+c to detach</div>"
        "</div>"
    )
    st.markdown(terminal_markup, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
