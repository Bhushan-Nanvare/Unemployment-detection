"""
ui_helpers.py — Shared dark glassmorphism design system
"""

API_BASE_URL = "http://127.0.0.1:8000"

PALETTE = {
    "bg": "#0a0e1a",
    "surface": "rgba(255,255,255,0.04)",
    "surface_hover": "rgba(255,255,255,0.08)",
    "border": "rgba(255,255,255,0.08)",
    "primary": "#6366f1",
    "primary_end": "#8b5cf6",
    "accent": "#06b6d4",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "text": "#e2e8f0",
    "muted": "#64748b",
}

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ─── App Background ─────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse at 20% 50%, #0d1b2a 0%, #0a0e1a 60%, #06020f 100%) !important;
    min-height: 100vh;
}

/* ─── Sidebar ────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: rgba(10,14,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
    backdrop-filter: blur(20px);
}
section[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] label { color: #94a3b8 !important; font-weight: 500 !important; }

/* ─── Global Text ─────────────────────────────────────── */
h1, h2, h3, h4, h5, h6 { color: #f1f5f9 !important; font-weight: 700 !important; }
p, div, span, li { color: #cbd5e1; }
label { color: #94a3b8 !important; font-weight: 500 !important; }
.stMarkdown p { color: #cbd5e1 !important; }

/* ─── Glass Card ──────────────────────────────────────── */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    transition: transform 0.25s ease, box-shadow 0.25s ease, background 0.25s ease;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
}
.glass-card:hover {
    background: rgba(255,255,255,0.07);
    transform: translateY(-3px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4), 0 0 0 1px rgba(99,102,241,0.2);
}

/* ─── KPI Card ────────────────────────────────────────── */
.kpi-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1.5rem;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.kpi-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #06b6d4);
    border-radius: 0 0 20px 20px;
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 24px 64px rgba(0,0,0,0.5), 0 0 0 1px rgba(99,102,241,0.3);
}
.kpi-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: block;
}
.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #64748b !important;
    margin-bottom: 0.25rem;
}
.kpi-value {
    font-size: 2.4rem;
    font-weight: 800;
    color: #f1f5f9 !important;
    line-height: 1;
    margin: 0.5rem 0;
    background: linear-gradient(135deg, #e2e8f0, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.kpi-delta {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.82rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
}
.kpi-delta.up   { background: rgba(239,68,68,0.15); color: #f87171 !important; }
.kpi-delta.down { background: rgba(16,185,129,0.15); color: #34d399 !important; }
.kpi-delta.neutral { background: rgba(100,116,139,0.2); color: #94a3b8 !important; }

/* ─── Page Header ─────────────────────────────────────── */
.page-hero {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(139,92,246,0.1) 100%);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.page-hero::before {
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.2) 0%, transparent 70%);
    top: -100px; right: -50px;
    border-radius: 50%;
}
.hero-title {
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    background: linear-gradient(135deg, #e2e8f0 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.hero-subtitle {
    color: #94a3b8 !important;
    font-size: 1.05rem;
    margin-top: 0.5rem;
    font-weight: 400;
}

/* ─── Status Badges ───────────────────────────────────── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.3px;
}
.badge-success  { background: rgba(16,185,129,0.15); color: #10b981 !important; border: 1px solid rgba(16,185,129,0.3); }
.badge-warning  { background: rgba(245,158,11,0.15); color: #f59e0b !important; border: 1px solid rgba(245,158,11,0.3); }
.badge-danger   { background: rgba(239,68,68,0.15);  color: #ef4444 !important; border: 1px solid rgba(239,68,68,0.3); }
.badge-info     { background: rgba(6,182,212,0.15);  color: #06b6d4 !important; border: 1px solid rgba(6,182,212,0.3); }
.badge-primary  { background: rgba(99,102,241,0.15); color: #818cf8 !important; border: 1px solid rgba(99,102,241,0.3); }

/* ─── Section Title ───────────────────────────────────── */
.section-title {
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1.2rem;
    padding-bottom: 0.75rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

/* ─── Skill Badge ─────────────────────────────────────── */
.skill-chip {
    display: inline-block;
    padding: 0.3rem 0.9rem;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #818cf8 !important;
    margin: 0.2rem;
}

/* ─── Timeline Item ───────────────────────────────────── */
.timeline-item {
    display: flex;
    gap: 1rem;
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.timeline-year {
    font-weight: 800;
    font-size: 1rem;
    color: #818cf8 !important;
    min-width: 50px;
}
.timeline-content { flex: 1; }
.timeline-value {
    font-size: 0.9rem;
    font-weight: 700;
    color: #f1f5f9 !important;
}
.timeline-desc {
    font-size: 0.85rem;
    color: #94a3b8 !important;
    margin-top: 0.2rem;
    line-height: 1.5;
}

/* ─── Buttons ─────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}

/* ─── Inputs / Sliders ────────────────────────────────── */
.stSlider > div > div { background: rgba(99,102,241,0.15) !important; }
.stSlider > div > div > div { background: linear-gradient(90deg, #6366f1, #8b5cf6) !important; }
.stSelectbox > div > div { 
    background: rgba(255,255,255,0.05) !important; 
    border: 1px solid rgba(255,255,255,0.1) !important;
    color: #e2e8f0 !important;
    border-radius: 10px !important;
}

/* ─── Tabs ────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03);
    border-radius: 14px;
    padding: 0.4rem;
    gap: 0.25rem;
    border: 1px solid rgba(255,255,255,0.07);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    color: #94a3b8 !important;
    font-weight: 600;
    background: transparent;
    border: none;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4);
}

/* ─── Tables / Dataframes ─────────────────────────────── */
.stDataFrame { border-radius: 12px; overflow: hidden; }
.stDataFrame th {
    background: rgba(99,102,241,0.2) !important;
    color: #c7d2fe !important;
    font-weight: 700 !important;
    border: none !important;
}
.stDataFrame td { 
    background: rgba(255,255,255,0.02) !important; 
    color: #cbd5e1 !important; 
    border-color: rgba(255,255,255,0.05) !important; 
}

/* ─── Info / Error / Success boxes ───────────────────── */
.stInfo { background: rgba(6,182,212,0.1) !important; border-left: 3px solid #06b6d4 !important; border-radius: 10px; }
.stSuccess { background: rgba(16,185,129,0.1) !important; border-left: 3px solid #10b981 !important; border-radius: 10px; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-left: 3px solid #f59e0b !important; border-radius: 10px; }
.stError { background: rgba(239,68,68,0.1) !important; border-left: 3px solid #ef4444 !important; border-radius: 10px; }
.stInfo p, .stSuccess p, .stWarning p, .stError p { color: #e2e8f0 !important; }

/* ─── Spinner ─────────────────────────────────────────── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ─── Metrics ─────────────────────────────────────────── */
[data-testid="stMetricValue"] { color: #f1f5f9 !important; font-weight: 800 !important; }
[data-testid="stMetricLabel"] { color: #94a3b8 !important; }
[data-testid="stMetricDelta"] svg { display: none; }

/* Custom scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.02); }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.4); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.6); }
</style>
"""


def render_kpi_card(icon: str, label: str, value: str, delta: str = "", delta_type: str = "neutral") -> str:
    """Return HTML for a KPI card."""
    delta_html = f'<div class="kpi-delta {delta_type}">{delta}</div>' if delta else ""
    return f"""
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


def render_badge(text: str, kind: str = "primary") -> str:
    """Return HTML for a status badge."""
    return f'<span class="badge badge-{kind}">{text}</span>'


def render_section_title(icon: str, title: str) -> str:
    return f'<div class="section-title">{icon} {title}</div>'


def plotly_dark_layout(**kwargs) -> dict:
    """Return a base Plotly layout dict using the dark theme.
    NOTE: xaxis/yaxis are intentionally excluded so callers can pass them
    freely via update_layout() without a 'multiple values for keyword argument' error.
    Use fig.update_xaxes() / fig.update_yaxes() for axis styling.
    """
    base = dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(family="Inter", color="#94a3b8"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.04)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(color="#cbd5e1"),
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode="x unified",
    )
    base.update(kwargs)
    return base


def apply_dark_axes(fig):
    """Apply dark axis styling to all axes in a figure."""
    axis_style = dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(color="#64748b"),
        title_font=dict(color="#94a3b8"),
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)
    return fig
