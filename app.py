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
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
  --bg:#020b05; --bg-alt:#04140c; --card:rgba(6,28,20,0.94);
  --card-border:rgba(0,255,154,0.28); --divider:rgba(0,255,154,0.16);
  --text:#eafff4; --text-secondary:rgba(158,255,212,0.78);
  --accent:#00ff9a; --accent-soft:rgba(0,255,154,0.14); --accent-strong:#12ffa7;
  --success:#55f48f; --warning:#ff9a66;
  --chip-bg:rgba(0,255,154,0.14);
}

.stApp, .stApp *{
  font-family:'IBM Plex Mono','Segoe UI',monospace!important;
  letter-spacing:0!important; -webkit-font-smoothing:antialiased!important;
}

.stApp{
  background:
    radial-gradient(circle at top, rgba(0,255,154,0.12), transparent 45%),
    radial-gradient(circle at 20% 120%, rgba(0,187,255,0.08), transparent 40%),
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
  background:rgba(6,18,12,0.9); border-bottom:1px solid var(--divider);
  box-shadow:0 20px 48px rgba(2,12,8,0.55);
}
.sc-logo{display:flex; align-items:center; gap:14px; font-weight:600; font-size:18px; color:var(--accent);}
.sc-logo .badge{margin-left:4px;}
.sc-nav-links{display:flex; align-items:center; gap:10px; flex-wrap:wrap;}
.sc-nav a{
  color:var(--text-secondary)!important; text-decoration:none; padding:8px 16px;
  border-radius:999px; border:1px solid transparent; transition:.18s ease;
  font-size:13px; font-weight:500; background:transparent;
}
.sc-nav a:hover{border-color:var(--accent-soft); color:var(--accent)!important; background:var(--accent-soft); box-shadow:0 0 14px rgba(0,255,154,0.3);}
.sc-nav a.active{color:#03150b!important; background:var(--accent); border-color:transparent; box-shadow:0 10px 24px rgba(0,255,154,0.36);}

/* cards */
.sc-card{
  border:1px solid var(--card-border); border-radius:20px; padding:24px;
  background:linear-gradient(160deg, rgba(7,28,18,0.95), rgba(5,18,14,0.9));
  box-shadow:0 20px 50px rgba(2,10,6,0.45);
}
.sc-card h3{margin-top:0; font-weight:600; font-size:20px; color:var(--accent);}

.sc-hero{
  position:relative; overflow:hidden;
  background:linear-gradient(140deg, rgba(0,255,154,0.2), rgba(0,187,255,0.16));
}
.sc-hero:before{
  content:""; position:absolute; inset:-40px; background:linear-gradient(135deg, rgba(0,255,154,0.3), transparent 60%);
  opacity:.6;
}
.sc-hero > *{position:relative; z-index:1;}

/* section title */
.sec-title{
  font-size:12px; text-transform:uppercase; letter-spacing:.22em;
  color:var(--accent); padding-bottom:8px; border-bottom:1px solid var(--divider);
  margin:0 0 16px;
}

/* chips/badges */
.chips{display:flex; flex-wrap:wrap; gap:8px; margin:16px 0 0;}
.chip{padding:8px 14px; border-radius:999px; background:var(--chip-bg); color:var(--text); font-size:13px; border:1px solid transparent;}
.chip-alt{background:rgba(0,187,255,0.2); color:#c8fff6;}
.badge{display:inline-flex; align-items:center; gap:6px; padding:4px 10px; border-radius:999px; border:1px solid var(--accent-soft); font-size:12px; color:var(--text-secondary); background:rgba(0,255,154,0.12);}
.badge-ok{background:rgba(0,255,154,0.18); color:#d1ffe9; border-color:rgba(0,255,154,0.28);}
.badge-hi{background:rgba(255,166,158,0.18); color:#ffd8d2; border-color:rgba(255,166,158,0.32);}
.badge-crit{background:rgba(251,113,133,0.24); color:#ffe5eb; border-color:rgba(251,113,133,0.4);}

/* inputs */
.stApp div[data-baseweb="input"]>div, .stApp textarea, .stApp select, .stApp label,
.stSelectbox, .stTextInput{ color:var(--text)!important; }
.stApp .stTextInput>div>div>input, .stApp textarea, .stApp select{
  background:rgba(5,24,16,0.92)!important; border:1px solid var(--card-border)!important; border-radius:14px!important;
}
.stApp .stSelectbox>div>div{border-radius:14px!important;}
.stApp input, .stApp textarea { caret-color:var(--accent)!important; }

/* buttons */
.stApp .stButton>button{
  color:#03150b!important; background:var(--accent); border:none!important; border-radius:14px;
  padding:0.6rem 1.35rem; font-weight:600; transition:.18s ease; box-shadow:0 12px 30px rgba(0,255,154,0.35);
}
.stApp .stButton>button:hover{transform:translateY(-1px); box-shadow:0 18px 36px rgba(0,255,154,0.45);}
.stApp .stButton>button:focus-visible{outline:2px solid var(--accent-strong); outline-offset:2px;}

/* tables and dataframe */
.stApp table{ color:var(--text)!important; border-collapse:separate!important; border-spacing:0 6px;}
.stApp thead th { border-bottom:1px solid var(--divider)!important; font-size:12px; text-transform:uppercase; letter-spacing:.08em; color:var(--accent)!important;}
.stApp tbody td { border:none!important; background:rgba(6,24,16,0.78); padding:16px 12px!important; border-top:1px solid rgba(0,255,154,0.1)!important; border-bottom:1px solid rgba(0,255,154,0.1)!important;}
.stApp [data-testid="stStyledTableContainer"]{
  border:1px solid var(--card-border); border-radius:16px; background:rgba(4,18,12,0.65);
}

/* metrics */
.stApp [data-testid="stMetricValue"]{color:var(--accent)!important; font-weight:600!important;}
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricDelta"]{color:var(--text-secondary)!important;}

/* alerts */
.stAlert{border-radius:14px!important; border:1px solid var(--card-border)!important; background:rgba(8,30,18,0.85)!important;}

/* divider */
.rule{height:1px; background:var(--divider); margin:28px 0 18px; box-shadow:0 0 12px rgba(0,255,154,0.22);}

/* charts */
.stApp .stPlotlyChart div, .stApp canvas{filter:saturate(1.12) contrast(1.05);}

code{color:var(--accent); background:rgba(0,255,154,0.08); padding:2px 6px; border-radius:6px;}

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
