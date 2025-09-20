"""Tab renderer modules for the Snowcrash Streamlit app."""

from . import home, builder, config, run, console, findings, reports, settings

TAB_RENDERERS = {
    "home": home.render,
    "builder": builder.render,
    "config": config.render,
    "run": run.render,
    "console": console.render,
    "findings": findings.render,
    "reports": reports.render,
    "settings": settings.render,
}

__all__ = ["TAB_RENDERERS"]
