"""Tab renderer registry for the Snowcrash Streamlit app."""

import tab_builder
import tab_config
import tab_console
import tab_findings
import tab_home
import tab_reports
import tab_run
import tab_settings

TAB_RENDERERS = {
    "home": tab_home.render,
    "builder": tab_builder.render,
    "config": tab_config.render,
    "run": tab_run.render,
    "console": tab_console.render,
    "findings": tab_findings.render,
    "reports": tab_reports.render,
    "settings": tab_settings.render,
}

__all__ = ["TAB_RENDERERS"]
