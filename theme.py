"""Shared visual theme. Styling only: no data or analysis logic lives here."""
import streamlit as st
 
PALETTE = ["#2DD4BF", "#F5C451", "#818CF8", "#F472B6", "#60A5FA",
           "#FB923C", "#A3E635", "#C084FC", "#34D399", "#F87171"]
TEAL = "#2DD4BF"
GOLD = "#F5C451"
GREEN = "#34D399"
RED = "#F87171"
GRAY = "#94A3B8"
 
DIRECTION_COLORS = {"Positive": GREEN, "Negative": RED, "Zero": GRAY}
 
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
 
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}
 
/* Background with soft glow */
.stApp {
    background:
        radial-gradient(900px 500px at 8% -5%, rgba(45,212,191,0.13), transparent 60%),
        radial-gradient(800px 500px at 95% 0%, rgba(129,140,248,0.12), transparent 55%),
        #0B1020;
}
 
/* Hide default footer / menu only (keep sidebar toggle) */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
 
.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1300px;
}
 
/* Title with gradient text */
h1 {
    font-weight: 800 !important;
    letter-spacing: -0.02em;
    color: #FFFFFF;
    padding-bottom: 0.35rem;
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(90deg, #2DD4BF, #818CF8, transparent) 1;
    text-shadow: 0 0 28px rgba(45,212,191,0.25);
}
h2, h3 {
    font-weight: 700 !important;
    letter-spacing: -0.01em;
    color: #F1F5F9;
}
h3::before, h2::before {
    content: "";
    display: inline-block;
    width: 4px;
    height: 0.95em;
    margin-right: 10px;
    border-radius: 4px;
    vertical-align: -0.1em;
    background: linear-gradient(180deg, #2DD4BF, #818CF8);
}
 
/* Metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.30);
    backdrop-filter: blur(6px);
    transition: transform .2s ease, border-color .2s ease, box-shadow .2s ease;
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: rgba(45,212,191,0.55);
    box-shadow: 0 16px 38px rgba(45,212,191,0.15);
}
div[data-testid="stMetricLabel"] p {
    color: #94A3B8 !important;
    font-size: 0.82rem !important;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
}
div[data-testid="stMetricValue"] {
    font-weight: 800;
    color: #FFFFFF;
}
 
/* Chart cards */
div[data-testid="stPlotlyChart"] {
    background: linear-gradient(145deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 10px 10px 2px 10px;
    box-shadow: 0 12px 34px rgba(0,0,0,0.28);
    margin-bottom: 0.6rem;
}
 
/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10172B 0%, #0B1020 100%);
    border-right: 1px solid rgba(255,255,255,0.07);
}
 
/* Inputs */
div[data-baseweb="select"] > div,
div[data-testid="stDateInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 12px !important;
}
div[data-baseweb="select"] > div:hover { border-color: #2DD4BF !important; }
 
/* Expander & dataframe */
div[data-testid="stExpander"] {
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    background: rgba(255,255,255,0.03);
}
div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
 
/* Captions, dividers, alerts */
div[data-testid="stCaptionContainer"] {
    color: #94A3B8;
    border-left: 3px solid rgba(245,196,81,0.7);
    padding-left: 12px;
}
hr { border-color: rgba(255,255,255,0.09) !important; }
div[data-testid="stAlert"] { border-radius: 14px; }
 
/* Scrollbar */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: #26304D; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #2DD4BF; }
</style>
"""
 
 
def apply_theme() -> None:
    """Inject the shared CSS. Call right after st.set_page_config()."""
    st.markdown(_CSS, unsafe_allow_html=True)
 
 
def style_fig(fig, height: int = 420):
    """Apply one consistent look to a Plotly figure (colors, grid, hover)."""
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#CBD5E1", size=13),
        title=dict(font=dict(size=17, color="#F8FAFC"), x=0.01, xanchor="left"),
        colorway=PALETTE,
        margin=dict(l=20, r=20, t=60, b=20),
        hovermode="x unified" if fig.data and getattr(fig.data[0], "type", "") == "scatter"
        and getattr(fig.data[0], "mode", None) in (None, "lines", "lines+markers") else "closest",
        hoverlabel=dict(bgcolor="#131A2E", bordercolor=TEAL,
                        font=dict(family="Inter, sans-serif", color="#F8FAFC")),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False,
                     linecolor="rgba(255,255,255,0.12)", title_font=dict(color=GRAY))
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.06)", zeroline=False,
                     linecolor="rgba(255,255,255,0.12)", title_font=dict(color=GRAY))
    return fig
 
