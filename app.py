# app.py — Snowcrash LLM Red-Teaming (Full Terminal Theme + Top Navbar)
import random
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

from tab_registry import TAB_RENDERERS

# ------------------------------------------------
# Page config
# ------------------------------------------------
st.set_page_config(
    page_title="snowcrash — LLM Red-Teaming",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",   # hide the old sidebar
)

# ------------------------------------------------
# Minimal state
# ------------------------------------------------
ss = st.session_state
ss.setdefault("scenarios", [])
ss.setdefault("runs", [])
ss.setdefault("findings", [])
ss.setdefault("log", [])
if "spark" not in ss:
    base = datetime.utcnow() - timedelta(hours=6)
    ss.spark = (
        pd.DataFrame(
            {
                "t": [base + timedelta(minutes=i * 10) for i in range(48)],
                "runs": [35 + int(6 * random.random()) for _ in range(48)],
            }
        ).set_index("t")
    )

# ------------------------------------------------
# Global terminal/CRT CSS (applies to entire app)
# ------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600&display=swap');

:root{
  --bg:#05070f; --bg-alt:#090c18; --card:rgba(15,18,28,0.82);
  --card-border:rgba(109,118,209,0.2); --divider:rgba(255,255,255,0.08);
  --text:#f5f7ff; --text-secondary:rgba(245,247,255,0.68);
  --accent:#6e63ff; --accent-soft:rgba(110,99,255,0.18); --accent-strong:#9087ff;
  --success:#4ade80; --warning:#fb7185;
  --chip-bg:rgba(110,99,255,0.14);
}

.stApp, .stApp *{
  font-family:'Inter', 'Segoe UI', system-ui, -apple-system, BlinkMacSystemFont, sans-serif!important;
  letter-spacing:0!important; -webkit-font-smoothing:antialiased!important;
}

.stApp{
  background:
    radial-gradient(circle at top, rgba(110,99,255,0.16), transparent 45%),
    radial-gradient(circle at 20% 120%, rgba(30,214,190,0.08), transparent 38%),
    var(--bg)!important;
  color:var(--text)!important;
}

.stApp [data-testid="stHeader"],
.stApp [data-testid="stToolbar"]{
  background:transparent!important; border:none!important;
  pointer-events:none; height:0; min-height:0;
}

.stApp .block-container{
  padding-top:6.5rem!important; padding-bottom:3rem!important;
  max-width:1180px!important;
}

.stApp [data-testid="stSidebar"]{
  background:var(--bg-alt)!important; color:var(--text);
  border-right:1px solid var(--divider)!important;
}

.stApp a, .stApp p, .stApp span, .stApp label, .stApp h1, .stApp h2, .stApp h3,
.stApp h4, .stApp h5, .stApp h6, .stApp li, .stApp td, .stApp th{
  color:inherit!important;
}

/* fixed top navbar */
.sc-nav{
  position:fixed; top:0; left:0; right:0; z-index:1000;
  display:flex; align-items:center; gap:28px; padding:18px 42px;
  background:rgba(6,8,14,0.82); backdrop-filter:blur(16px);
  border-bottom:1px solid var(--divider); box-shadow:0 20px 40px rgba(3,6,16,0.28);
}
.sc-logo{display:flex; align-items:center; gap:14px; font-weight:600; font-size:18px; color:var(--text);}
.sc-logo .badge{margin-left:4px;}
.sc-nav-links{display:flex; align-items:center; gap:8px; flex-wrap:wrap;}
.sc-nav a{
  color:var(--text-secondary)!important; text-decoration:none; padding:8px 16px;
  border-radius:999px; border:1px solid transparent; transition:.18s ease;
  font-size:14px; font-weight:500; background:transparent;
}
.sc-nav a:hover{border-color:var(--accent-soft); color:var(--text)!important; background:var(--accent-soft);}
.sc-nav a.active{color:var(--text)!important; background:var(--accent); border-color:transparent; box-shadow:0 10px 22px rgba(110,99,255,0.28);}

/* cards */
.sc-card{
  border:1px solid var(--card-border); border-radius:20px; padding:24px;
  background:linear-gradient(160deg, rgba(16,20,34,0.94), rgba(9,13,23,0.88));
  box-shadow:0 20px 50px rgba(5,10,25,0.35);
}
.sc-card h3{margin-top:0; font-weight:600; font-size:20px;}
.sc-hero{
  position:relative; overflow:hidden;
  background:linear-gradient(140deg, rgba(110,99,255,0.22), rgba(30,214,190,0.16));
}
.sc-hero:before{
  content:""; position:absolute; inset:-40px; background:linear-gradient(135deg, rgba(144,135,255,0.35), transparent 60%);
  filter:blur(0px); opacity:.7;
}
.sc-hero > *{position:relative; z-index:1;}

/* section title */
.sec-title{
  font-size:12px; text-transform:uppercase; letter-spacing:.22em;
  color:var(--text-secondary); padding-bottom:8px; border-bottom:1px solid var(--divider);
  margin:0 0 16px;
}

/* chips/badges */
.chips{display:flex; flex-wrap:wrap; gap:8px; margin:16px 0 0;}
.chip{padding:8px 14px; border-radius:999px; background:var(--chip-bg); color:var(--text); font-size:13px; border:1px solid transparent;}
.chip-alt{background:rgba(30,214,190,0.18); color:#c8fff6;}
.badge{display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:999px; border:1px solid var(--accent-soft); font-size:12px; color:var(--text-secondary); background:rgba(255,255,255,0.04);}
.badge-ok{background:rgba(74,222,128,0.16); color:#c2f9d8; border-color:rgba(74,222,128,0.28);}
.badge-hi{background:rgba(255,166,158,0.18); color:#ffd8d2; border-color:rgba(255,166,158,0.32);}
.badge-crit{background:rgba(251,113,133,0.24); color:#ffe5eb; border-color:rgba(251,113,133,0.4);}

/* inputs */
.stApp div[data-baseweb="input"]>div, .stApp textarea, .stApp select, .stApp label,
.stSelectbox, .stTextInput{ color:var(--text)!important; }
.stApp .stTextInput>div>div>input, .stApp textarea, .stApp select{
  background:rgba(10,14,24,0.92)!important; border:1px solid var(--card-border)!important; border-radius:14px!important;
}
.stApp .stSelectbox>div>div{border-radius:14px!important;}
.stApp input, .stApp textarea { caret-color:var(--accent)!important; }

/* buttons */
.stApp .stButton>button{
  color:var(--text)!important; background:var(--accent); border:none!important; border-radius:14px;
  padding:0.6rem 1.35rem; font-weight:600; transition:.18s ease; box-shadow:0 12px 30px rgba(110,99,255,0.35);
}
.stApp .stButton>button:hover{transform:translateY(-1px); box-shadow:0 18px 36px rgba(110,99,255,0.45);}
.stApp .stButton>button:focus-visible{outline:2px solid var(--accent-strong); outline-offset:2px;}

/* tables and dataframe */
.stApp table{ color:var(--text)!important; border-collapse:separate!important; border-spacing:0 6px;}
.stApp thead th { border-bottom:1px solid var(--divider)!important; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--text-secondary)!important;}
.stApp tbody td { border:none!important; background:rgba(15,18,30,0.72); padding:16px 12px!important; border-top:1px solid rgba(255,255,255,0.04)!important; border-bottom:1px solid rgba(255,255,255,0.04)!important;}
.stApp [data-testid="stStyledTableContainer"]{
  border:1px solid var(--card-border); border-radius:16px; background:rgba(9,12,22,0.55);
}

/* metrics */
.stApp [data-testid="stMetricValue"]{color:var(--text)!important; font-weight:600!important;}
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricDelta"]{color:var(--text-secondary)!important;}

/* alerts */
.stAlert{border-radius:14px!important; border:1px solid var(--card-border)!important; background:rgba(17,22,36,0.85)!important;}

/* divider */
.rule{height:1px; background:var(--divider); margin:28px 0 18px;}

/* charts */
.stApp .stPlotlyChart div, .stApp canvas{filter:saturate(1.15) contrast(1.05);}

</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ------------------------------------------------
# Top navbar (replaces sidebar)
# ------------------------------------------------
TABS = [
    ("Home", "home"), ("Builder", "builder"), ("Config", "config"),
    ("Run", "run"), ("Console", "console"), ("Findings", "findings"),
    ("Reports", "reports"), ("Settings", "settings")
]

# derive active from query param
def _get_query_params() -> dict:
    """Return current query params with legacy/new Streamlit support."""
    try:
        params_proxy = st.query_params  # type: ignore[attr-defined]
        # convert proxy to plain dict without mutating original
        return {k: v for k, v in params_proxy.items()}
    except Exception:
        return st.experimental_get_query_params()


def _set_query_params(**kwargs) -> None:
    """Update query params regardless of Streamlit version."""
    try:
        for key, value in kwargs.items():
            if isinstance(value, list):
                st.query_params[key] = value  # type: ignore[attr-defined]
            else:
                st.query_params[key] = value  # type: ignore[attr-defined]
    except Exception:
        st.experimental_set_query_params(**kwargs)


params = _get_query_params()
raw_tab = params.get("tab", "home")
if isinstance(raw_tab, list):
    raw_tab = raw_tab[0] if raw_tab else "home"
active = (raw_tab or "home").lower()
valid_tabs = {key for _, key in TABS}
if active not in valid_tabs:
    active = "home"
if params.get("tab") != active:
    _set_query_params(tab=active)
ss.active_tab = active

def nav_link(lbl, key):
    cls = "active" if key == active else ""
    return f'<a class="{cls}" href="?tab={key}" target="_self" rel="noopener">{lbl}</a>'

navbar = (
    '<div class="sc-nav">'
    '<div class="sc-logo">snowcrash <span class="badge badge-ok">LLM Red-Teaming</span></div>'
    '<div class="sc-nav-links">'
    + "".join(nav_link(lbl, key) for lbl, key in TABS) +
    '</div>'
    '</div>'
)
st.markdown(navbar, unsafe_allow_html=True)

renderer = TAB_RENDERERS.get(active)
if renderer is None:
    renderer = TAB_RENDERERS["home"]
renderer(ss)

# ------------------------------------------------
# Footer
# ------------------------------------------------
st.markdown("<div class='rule'></div>", unsafe_allow_html=True)
st.caption(f"© {datetime.utcnow().year} snowcrash — Offensive LLM Security • Modern dark interface preview")
