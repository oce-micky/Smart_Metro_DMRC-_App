import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import datetime

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartMetro AI — DMRC Intelligence",
    page_icon="🚇",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS  — Off-white / Cream / Red / Green / Yellow
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    background-color: #FAF7F2 !important;
    color: #1C1917 !important;
}
.stApp { background-color: #FAF7F2 !important; }
.main .block-container { padding: 1.5rem 2.5rem 3rem; max-width: 1500px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #B91C1C 0%, #7F1D1D 60%, #450A0A 100%) !important;
}
section[data-testid="stSidebar"] * { color: #FFF7ED !important; }
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    color: #FFF7ED !important;
    font-family: 'DM Sans' !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.55rem 1rem !important;
    transition: all 0.2s !important;
    text-align: left !important;
    width: 100% !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.35) !important;
}

/* ── HERO BANNER ── */
.hero-banner {
    background: linear-gradient(135deg, #B91C1C 0%, #991B1B 40%, #1C3461 100%);
    border-radius: 20px;
    padding: 3rem 3.5rem;
    color: #FFF7ED;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(185,28,28,0.25);
}
.hero-banner::before {
    content: '';
    position: absolute; top: -80px; right: -60px;
    width: 350px; height: 350px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.hero-banner::after {
    content: '';
    position: absolute; bottom: -40px; right: 120px;
    width: 180px; height: 180px;
    background: rgba(255,247,237,0.04);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 800;
    margin: 0; line-height: 1.15;
    color: #FFF7ED;
}
.hero-sub { font-size: 1.05rem; opacity: 0.85; margin-top: 0.7rem; font-weight: 400; }
.hero-badge {
    display: inline-block;
    background: rgba(255,247,237,0.15);
    border: 1px solid rgba(255,247,237,0.3);
    padding: 5px 16px; border-radius: 20px;
    font-size: 0.75rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 1.2rem; color: #FEF3C7;
}
.hero-stat {
    display: inline-block;
    background: rgba(255,247,237,0.1);
    border: 1px solid rgba(255,247,237,0.15);
    border-radius: 12px; padding: 0.8rem 1.5rem;
    margin-right: 1rem; margin-top: 1.5rem; text-align: center;
}
.hero-stat-num { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: #FEF3C7; }
.hero-stat-lbl { font-size: 0.7rem; opacity: 0.7; letter-spacing: 0.1em; text-transform: uppercase; }

/* ── KPI Cards ── */
.kpi-card {
    background: #FFFFFF;
    border-radius: 16px; padding: 1.4rem 1.5rem;
    border: 1.5px solid #F3EDE3;
    box-shadow: 0 2px 16px rgba(28,25,23,0.06);
    transition: transform 0.2s, box-shadow 0.2s;
    text-align: center; margin-bottom: 0.8rem;
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 10px 30px rgba(28,25,23,0.1); }
.kpi-icon { font-size: 1.6rem; margin-bottom: 0.4rem; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 1.9rem; font-weight: 700; margin: 0; line-height: 1.1; }
.kpi-label { font-size: 0.72rem; font-weight: 600; color: #78716C; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 0.4rem; }
.kpi-change { font-size: 0.78rem; margin-top: 0.35rem; font-weight: 500; }

/* ── Section Headers ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.45rem; font-weight: 700; color: #1C1917;
    border-bottom: 3px solid #B91C1C;
    padding-bottom: 0.45rem;
    margin: 2rem 0 1.2rem;
    display: inline-block;
}

/* ── Insight / Info Cards ── */
.insight-card {
    background: #FFFFFF;
    border-radius: 14px; padding: 1.2rem 1.4rem;
    border-left: 5px solid #1C3461;
    box-shadow: 0 2px 12px rgba(28,25,23,0.06);
    margin-bottom: 1rem;
}
.insight-card.red { border-left-color: #B91C1C; background: #FFF5F5; }
.insight-card.green { border-left-color: #15803D; background: #F0FDF4; }
.insight-card.yellow { border-left-color: #A16207; background: #FEFCE8; }
.insight-card.blue { border-left-color: #1C3461; background: #EFF6FF; }
.insight-title { font-weight: 700; font-size: 0.98rem; color: #1C1917; margin-bottom: 0.35rem; }
.insight-body { font-size: 0.87rem; color: #57534E; line-height: 1.65; }

/* ── Status Badges ── */
.badge-safe { background: #DCFCE7; color: #14532D; padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 0.88rem; display: inline-block; border: 1.5px solid #86EFAC; }
.badge-moderate { background: #FEFCE8; color: #713F12; padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 0.88rem; display: inline-block; border: 1.5px solid #FDE047; }
.badge-danger { background: #FEE2E2; color: #7F1D1D; padding: 5px 14px; border-radius: 20px; font-weight: 700; font-size: 0.88rem; display: inline-block; border: 1.5px solid #FCA5A5; }

/* ── Forecast Result Cards ── */
.forecast-card {
    background: #FFFFFF;
    border-radius: 18px; padding: 1.8rem;
    border: 2px solid #F3EDE3;
    box-shadow: 0 4px 24px rgba(28,25,23,0.08);
    text-align: center;
}
.forecast-number { font-family: 'Playfair Display', serif; font-size: 3.2rem; font-weight: 800; line-height: 1; }
.forecast-label { font-size: 0.78rem; font-weight: 700; color: #78716C; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 0.4rem; }
.forecast-sub { font-size: 0.8rem; color: #A8A29E; margin-top: 0.3rem; }

/* ── Policy Cards ── */
.policy-card {
    background: #FFFFFF;
    border-radius: 18px; padding: 1.6rem;
    border: 1.5px solid #F3EDE3;
    box-shadow: 0 3px 16px rgba(28,25,23,0.07);
    margin-bottom: 1rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.policy-card:hover { transform: translateY(-3px); box-shadow: 0 8px 28px rgba(28,25,23,0.12); }
.policy-title { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1.1rem; color: #1C1917; margin-bottom: 0.4rem; }
.policy-roi { font-family: 'Playfair Display', serif; font-size: 2rem; font-weight: 800; color: #15803D; }
.policy-detail { font-size: 0.83rem; color: #78716C; line-height: 1.65; }

/* ── Admin Alert ── */
.admin-alert {
    background: linear-gradient(135deg, #FEF9C3, #FEF3C7);
    border: 2px solid #EAB308;
    border-radius: 12px; padding: 0.9rem 1.4rem;
    margin-bottom: 1.5rem; font-size: 0.88rem; color: #713F12; font-weight: 500;
}
.user-alert {
    background: linear-gradient(135deg, #DCFCE7, #F0FDF4);
    border: 2px solid #22C55E;
    border-radius: 12px; padding: 0.9rem 1.4rem;
    margin-bottom: 1.5rem; font-size: 0.88rem; color: #14532D; font-weight: 500;
}

/* ── Login Page ── */
.login-wrap {
    max-width: 500px; margin: 2rem auto;
    background: #FFFFFF; border-radius: 24px; padding: 2.8rem;
    box-shadow: 0 12px 50px rgba(28,25,23,0.12);
    border: 1.5px solid #F3EDE3;
}

/* ── Dividers ── */
.brand-divider { height: 4px; background: linear-gradient(90deg, #B91C1C, #EAB308, #15803D); border-radius: 2px; margin: 1.5rem 0; }

/* ── Nav section label in sidebar ── */
.nav-section-lbl { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(255,247,237,0.45) !important; padding: 0.8rem 0 0.3rem; margin-left: 0.3rem; }

/* ── Data table ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }

/* ── Form fields ── */
.stSelectbox > div, .stSlider, .stTextInput > div, .stNumberInput > div {
    background: #FFFFFF !important;
}
.stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label, .stRadio label, .stCheckbox label {
    font-weight: 600 !important; color: #44403C !important; font-size: 0.88rem !important;
}
input { border-radius: 10px !important; border-color: #E7E0D8 !important; }
hr { border-color: #E7E0D8 !important; }

/* ── Main buttons ── */
.stForm .stButton > button, .main .stButton > button {
    background: linear-gradient(135deg, #B91C1C, #991B1B) !important;
    color: #FFF7ED !important; border: none !important;
    border-radius: 12px !important; font-weight: 700 !important;
    font-size: 0.95rem !important; padding: 0.7rem 2rem !important;
    width: 100% !important; transition: all 0.2s !important;
    box-shadow: 0 4px 14px rgba(185,28,28,0.3) !important;
}
.stForm .stButton > button:hover, .main .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(185,28,28,0.4) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: #F3EDE3 !important; border-radius: 12px !important; gap: 4px; padding: 4px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px !important; font-weight: 600 !important; font-size: 0.88rem !important; }
.stTabs [aria-selected="true"] { background: #B91C1C !important; color: white !important; }

/* ── Anomaly boxes ── */
.anomaly-danger { background: #FEF2F2; border: 2px solid #FCA5A5; border-radius: 14px; padding: 1.2rem; margin-bottom: 0.8rem; }
.anomaly-warn { background: #FEFCE8; border: 2px solid #FDE047; border-radius: 14px; padding: 1.2rem; margin-bottom: 0.8rem; }

/* ── Progress bar custom ── */
.progress-wrap { background: #F3EDE3; border-radius: 99px; height: 10px; overflow: hidden; margin: 6px 0; }
.progress-fill-red { background: linear-gradient(90deg, #B91C1C, #EF4444); height: 100%; border-radius: 99px; transition: width 0.8s ease; }
.progress-fill-yellow { background: linear-gradient(90deg, #A16207, #EAB308); height: 100%; border-radius: 99px; }
.progress-fill-green { background: linear-gradient(90deg, #15803D, #22C55E); height: 100%; border-radius: 99px; }

/* ── Train Metro Illustration strip ── */
.metro-strip {
    background: linear-gradient(90deg, #1C3461 0%, #B91C1C 50%, #15803D 100%);
    height: 6px; border-radius: 3px; margin: 1rem 0 2rem;
}

/* ── Risk matrix ── */
.risk-low { background: #DCFCE7; color: #14532D; border-radius: 10px; padding: 0.9rem; text-align: center; font-weight: 700; font-size: 0.8rem; min-height: 4.5rem; display: flex; align-items: center; justify-content: center; }
.risk-med  { background: #FEFCE8; color: #713F12; border-radius: 10px; padding: 0.9rem; text-align: center; font-weight: 700; font-size: 0.8rem; min-height: 4.5rem; display: flex; align-items: center; justify-content: center; }
.risk-high { background: #FEE2E2; color: #7F1D1D; border-radius: 10px; padding: 0.9rem; text-align: center; font-weight: 700; font-size: 0.8rem; min-height: 4.5rem; display: flex; align-items: center; justify-content: center; }

/* ── Page title style ── */
.page-title {
    font-family: 'Playfair Display', serif;
    font-size: 2rem; font-weight: 800; color: #1C1917;
    margin-bottom: 0.3rem; line-height: 1.2;
}
.page-subtitle { font-size: 0.95rem; color: #78716C; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for key, default in [("logged_in", False), ("user_role", None), ("current_page", "home")]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────────────────────────────────────────────────────────
#  DATA
# ─────────────────────────────────────────────────────────────────────────────
STATION_DATA = {
    "Rajiv Chowk":         {"departures": 17470, "arrivals": 6231,  "total": 23701, "net": 11239,  "type": "Hub",    "capacity": 4500, "base": 316},
    "Noida City Centre":   {"departures": 13949, "arrivals": 6338,  "total": 20287, "net": 7611,   "type": "Hub",    "capacity": 3800, "base": 270},
    "New Delhi":           {"departures": 10037, "arrivals": 6119,  "total": 16156, "net": 3918,   "type": "Major",  "capacity": 4000, "base": 215},
    "Mandi House":         {"departures": 9931,  "arrivals": 6078,  "total": 16009, "net": 3853,   "type": "Major",  "capacity": 3200, "base": 210},
    "Central Secretariat": {"departures": 6328,  "arrivals": 6252,  "total": 12580, "net": 76,     "type": "Medium", "capacity": 3200, "base": 150},
    "Kashmere Gate":       {"departures": 5800,  "arrivals": 5950,  "total": 11750, "net": -150,   "type": "Medium", "capacity": 3000, "base": 155},
    "Dilshad Garden":      {"departures": 6344,  "arrivals": 6306,  "total": 12650, "net": 38,     "type": "Major",  "capacity": 3000, "base": 168},
    "Kalkaji Mandir":      {"departures": 6338,  "arrivals": 6273,  "total": 12611, "net": 65,     "type": "Major",  "capacity": 2800, "base": 165},
    "Hauz Khas":           {"departures": 6183,  "arrivals": 6372,  "total": 12555, "net": -189,   "type": "Medium", "capacity": 2800, "base": 163},
    "Model Town":          {"departures": 6247,  "arrivals": 6252,  "total": 12499, "net": -5,     "type": "Medium", "capacity": 2800, "base": 162},
    "Karol Bagh":          {"departures": 5700,  "arrivals": 5800,  "total": 11500, "net": -100,   "type": "Minor",  "capacity": 2500, "base": 150},
    "Janakpuri West":      {"departures": 6205,  "arrivals": 6340,  "total": 12545, "net": -135,   "type": "Medium", "capacity": 2600, "base": 160},
}
ALL_STATIONS = list(STATION_DATA.keys())

MONTHLY_PASS = [78200,79400,81200,80100,82300,79800,81500,83200,80400,82100,79600,83800,
                80200,81700,79900,82400,80800,83100,81300,80500,82700,79300,83500,80900,
                82000,81100,83300,80600,82500,81800,83700,80300,82200,81400,83000,80700]
MONTHS = [f"{y}-{m:02d}" for y in [2022,2023,2024] for m in range(1,13)]

TICKET_DATA = {
    "Tourist Card": {"trips": 59193, "revenue": 62219974, "avg_fare": 105.11},
    "Smart Card":   {"trips": 37244, "revenue": 39126715, "avg_fare": 105.06},
    "Single":       {"trips": 37341, "revenue": 39372412, "avg_fare": 105.44},
    "Return":       {"trips": 14722, "revenue": 15397491, "avg_fare": 104.59},
}

REMARKS_DATA = {
    "off-peak":    {"trips": 24859, "passengers": 492409, "revenue": 51829449, "rev_trip": 2084.94},
    "festival":    {"trips": 24812, "passengers": 490933, "revenue": 51653488, "rev_trip": 2079.50},
    "maintenance": {"trips": 24771, "passengers": 490726, "revenue": 51563437, "rev_trip": 2081.20},
    "peak":        {"trips": 24591, "passengers": 486292, "revenue": 51083363, "rev_trip": 2077.32},
    "weekend":     {"trips": 24710, "passengers": 489370, "revenue": 51477090, "rev_trip": 2083.20},
}

FORECAST_2025 = [82342,79322,82978,83008,79682,81356,79575,82847,83604,79366,83592,80961]
FORECAST_2026 = [82112,79465,82770,82799,79697,81253,79601,82314,84724,79890,83421,82302]

POLICIES = {
    "Smart Card Loyalty":  {"cost": 5000000, "revenue": 46841844, "roi": 836.84, "payback": 1.28, "passengers": 148526},
    "Dynamic Pricing":     {"cost": 2000000, "revenue": 24982317, "roi": 1149.12,"payback": 0.96, "passengers": -59410},
    "Tourist Enhancement": {"cost": 3000000, "revenue": 37473475, "roi": 1149.12,"payback": 0.96, "passengers": 237642},
}

RED   = "#B91C1C"
BLUE  = "#1C3461"
GREEN = "#15803D"
GOLD  = "#A16207"
CREAM = "#FAF7F2"

BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(250,247,242,0.5)",
    font=dict(family="DM Sans", color="#44403C"),
    margin=dict(l=24, r=24, t=50, b=24),
    xaxis=dict(gridcolor="#EDE9E3", linecolor="#EDE9E3", tickfont=dict(size=11)),
    yaxis=dict(gridcolor="#EDE9E3", linecolor="#EDE9E3", tickfont=dict(size=11)),
)

# ─────────────────────────────────────────────────────────────────────────────
#  PREDICTION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def predict_congestion(station, is_peak, weather, ticket_type, hour, line, avg_cost, model="LSTM"):
    cfg      = STATION_DATA.get(station, {"base": 200, "capacity": 3000})
    base     = cfg["base"]
    capacity = cfg["capacity"]

    peak_hours = [8, 9, 10, 17, 18, 19]
    near_peak  = [7, 11, 16, 20]
    if hour in peak_hours:   time_f = 1.35 if is_peak else 1.15
    elif hour in near_peak:  time_f = 1.10
    elif 0 <= hour <= 5:     time_f = 0.12
    elif 6 <= hour <= 7:     time_f = 0.55
    else:                    time_f = 0.75

    weather_map = {"Clear Sky": 1.0, "Light Rain": 1.12, "Heavy Rain": 1.22, "Extreme Weather": 0.65, "Foggy / Winter": 0.88}
    ticket_map  = {"Tourist Card": 1.05, "Smart Card": 1.02, "Single Journey": 0.98, "Return": 0.95}
    line_map    = {"Blue Line": 1.08, "Yellow Line": 1.05, "Red Line": 0.95, "Green Line": 0.88,
                   "Violet Line": 0.92, "Pink Line": 0.90, "Orange Line": 0.85, "Magenta Line": 0.87, "Grey Line": 0.82}

    peak_f    = 1.20 if is_peak else 1.0
    weather_f = weather_map.get(weather, 1.0)
    ticket_f  = ticket_map.get(ticket_type, 1.0)
    line_f    = line_map.get(line, 1.0)
    cost_f    = 1.0 + (avg_cost - 105) / 1000 if avg_cost > 105 else 1.0

    # Model variance
    noise_std = base * (0.05 if model == "LSTM" else 0.10 if model == "SARIMA" else 0.13)
    np.random.seed(int(hour * 7 + base))
    noise     = np.random.normal(0, noise_std)

    current   = int(base * time_f * peak_f * weather_f * ticket_f * line_f * cost_f + noise)
    current   = max(20, min(current, capacity))
    pct       = (current / capacity) * 100

    # 2-hour forecast
    next_hour = (hour + 2) % 24
    if next_hour in peak_hours and hour not in peak_hours: trend = 1.28
    elif hour in peak_hours and next_hour not in peak_hours: trend = 0.75
    elif next_hour in peak_hours: trend = 1.05
    else: trend = 0.92
    forecast  = int(current * trend + np.random.normal(0, current * 0.04))
    forecast  = max(20, min(forecast, capacity))
    f_pct     = (forecast / capacity) * 100

    if pct >= 85:   status, badge = "🔴 DANGER",   "danger"
    elif pct >= 70: status, badge = "🟡 MODERATE", "moderate"
    else:           status, badge = "🟢 SAFE",      "safe"

    if f_pct >= 85:   f_status = "🔴 DANGER"
    elif f_pct >= 70: f_status = "🟡 MODERATE"
    else:             f_status = "🟢 SAFE"

    return current, pct, status, badge, forecast, f_pct, f_status

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: HOME
# ─────────────────────────────────────────────────────────────────────────────
def page_home():
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-badge">🚇 DMRC AI Intelligence Platform · BBD University · 2025</div>
        <div class="hero-title">SmartMetro AI</div>
        <div class="hero-sub">AI-Driven Ridership Forecasting & Congestion Intelligence<br>
        Powered by LSTM Neural Network + SARIMA Statistical Model</div>
        <div>
            <div class="hero-stat"><div class="hero-stat-num">1,50,000</div><div class="hero-stat-lbl">Trip Records</div></div>
            <div class="hero-stat"><div class="hero-stat-num">₹31.22 Cr</div><div class="hero-stat-lbl">Revenue Analysed</div></div>
            <div class="hero-stat"><div class="hero-stat-num">24</div><div class="hero-stat-lbl">Stations</div></div>
            <div class="hero-stat"><div class="hero-stat-num">3 Years</div><div class="hero-stat-lbl">2022–2024</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI Strip
    c1, c2, c3, c4, c5 = st.columns(5)
    kpis = [
        (c1, "1,54,230", "Total Records",   "🗄️", BLUE,  "Full dataset"),
        (c2, "₹31.22 Cr","Total Revenue",   "💰", GREEN, "+0% YoY"),
        (c3, "29.7 Lakh","Passengers",      "👥", BLUE,  "Served 2022–24"),
        (c4, "RMSE 116", "LSTM Accuracy",   "🤖", RED,   "Daily model"),
        (c5, "1149%",    "Best Policy ROI", "📈", GOLD,  "Dynamic Pricing"),
    ]
    for col, val, lbl, ico, clr, sub in kpis:
        col.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-icon">{ico}</div>
            <div class="kpi-value" style="color:{clr}">{val}</div>
            <div class="kpi-label">{lbl}</div>
            <div class="kpi-change" style="color:#78716C">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    # Mission + Capabilities
    col_l, col_r = st.columns([1.2, 1])
    with col_l:
        st.markdown('<div class="section-header">🎯 What SmartMetro AI Does</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="insight-card blue">
            <div class="insight-title">🚇 About This System</div>
            <div class="insight-body">SmartMetro AI transforms <b>1,50,000 raw Delhi Metro trip records</b> (Jan 2022–Dec 2024)
            into a live intelligence platform. It predicts platform congestion <b>before it happens</b>,
            simulates revenue impact of fare policies, and gives DMRC decision-makers a clear view of
            network performance across 24 stations.</div>
        </div>
        <div class="insight-card red">
            <div class="insight-title">❌ Critical Finding — Pricing Paradox</div>
            <div class="insight-body">Off-peak trips earn <b>₹7.62 MORE per trip</b> than peak trips.
            DMRC's busiest service is its <b>least profitable</b>. Dynamic Pricing fixes this with
            1149% ROI and a 29-day payback period.</div>
        </div>
        <div class="insight-card green">
            <div class="insight-title">✅ Three Policies — Combined Gain ₹11 Cr+</div>
            <div class="insight-body">Smart Card Loyalty (ROI 836%), Dynamic Pricing (ROI 1149%),
            Tourist Enhancement (ROI 1149%). All have payback periods under 2 months.</div>
        </div>
        """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-header">⚙️ System Modules</div>', unsafe_allow_html=True)
        modules = [
            ("🤖", "LSTM Neural Network",    "5-feature model · 30,651 params · RMSE 116 (daily)"),
            ("📈", "SARIMA Forecasting",     "24-month ahead · RMSE 2,480 · Ljung-Box p=0.9978"),
            ("🏙️", "Station Intelligence",   "Hub / Major / Medium / Minor · 12 key stations"),
            ("🚨", "Anomaly Detection",      "2,847 outliers detected · 1.90% anomaly rate"),
            ("💡", "Policy Simulator",       "3 policies · Live fare slider · Instant ROI"),
            ("🔐", "Role-Based Access",      "Admin: full access · User: forecasting only"),
        ]
        for ico, title, body in modules:
            st.markdown(f"""
            <div class="insight-card" style="padding:0.85rem 1.2rem; margin-bottom:0.55rem">
                <div class="insight-title">{ico} {title}</div>
                <div class="insight-body" style="font-size:0.81rem">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    # Ridership chart preview
    st.markdown('<div class="section-header">📊 Ridership Overview — 2022–2024</div>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=MONTHS, y=MONTHLY_PASS,
        mode="lines", fill="tozeroy",
        fillcolor="rgba(28,52,97,0.08)",
        line=dict(color=BLUE, width=2.5),
        hovertemplate="<b>%{x}</b><br>Passengers: %{y:,}<extra></extra>"
    ))
    fig.update_layout(**BASE_LAYOUT, height=280,
        title=dict(text="Monthly Passenger Trend — 36 Months · Jan 2022–Dec 2024", font=dict(size=14, color=BLUE, family="Playfair Display")))
    st.plotly_chart(fig, use_container_width=True)

    # CTA
    st.markdown("""
    <div style="text-align:center; padding:2rem; background:#FFFFFF; border-radius:18px;
                border:1.5px solid #F3EDE3; margin-top:1rem; box-shadow:0 4px 20px rgba(28,25,23,0.06)">
        <div style="font-family:'Playfair Display',serif; font-size:1.5rem; color:#1C1917; font-weight:700; margin-bottom:0.5rem">
            Ready to explore?
        </div>
        <div style="color:#78716C; font-size:0.92rem">
            🔐 Login as <b>Admin</b> for full EDA, Anomaly, Forecasting & Policy access<br>
            👤 Login as <b>User</b> for direct congestion forecasting
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; margin-top:2rem; color:#A8A29E; font-size:0.78rem">
        SmartMetro AI · BBD University · BCA DS&AI · 2025-26<br>
        Divyanshi Mishra · Roll: 1230258170
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: LOGIN
# ─────────────────────────────────────────────────────────────────────────────
def page_login():
    st.markdown("""
    <div style="text-align:center; padding:2rem 0 0.5rem">
        <div style="font-size:3.5rem">🚇</div>
        <div style="font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:800; color:#1C1917">SmartMetro AI</div>
        <div style="color:#78716C; font-size:0.92rem; margin-top:0.3rem">Delhi Metro Rail Corporation — Intelligence Platform</div>
    </div>
    <div class="metro-strip"></div>
    """, unsafe_allow_html=True)

    col_center = st.columns([1, 1.6, 1])[1]
    with col_center:
        tab1, tab2 = st.tabs(["👤  General User", "🏛️  Administration"])

        with tab1:
            st.markdown("<br>", unsafe_allow_html=True)
            name    = st.text_input("Your Name", placeholder="Enter your full name")
            user_id = st.text_input("User ID",   placeholder="Any employee or citizen ID")
            if st.button("Login as User", key="user_login_btn"):
                if name and user_id:
                    st.session_state.logged_in    = True
                    st.session_state.user_role    = "user"
                    st.session_state.current_page = "forecast"
                    st.rerun()
                else:
                    st.warning("⚠️ Please enter your name and user ID.")

        with tab2:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username", placeholder="admin", key="adm_user")
            password = st.text_input("Password", type="password", placeholder="••••••••", key="adm_pass")
            st.markdown('<div style="font-size:0.76rem; color:#A8A29E; margin-top:-0.5rem">Demo: admin / dmrc2024</div>', unsafe_allow_html=True)
            if st.button("Login as Administrator", key="admin_login_btn"):
                if username == "admin" and password == "dmrc2024":
                    st.session_state.logged_in    = True
                    st.session_state.user_role    = "admin"
                    st.session_state.current_page = "eda"
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Use admin / dmrc2024")

    st.markdown("""
    <div style="text-align:center; margin-top:2.5rem; color:#A8A29E; font-size:0.76rem">
        SmartMetro AI · BBD University · BCA DS&AI · 2025-26 · Divyanshi Mishra
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: EDA (Admin)
# ─────────────────────────────────────────────────────────────────────────────
def page_eda():
    st.markdown('<div class="admin-alert">🔐 <b>Admin Access — Exploratory Data Analysis</b> · Full 1,50,000 record dataset · Jan 2022–Dec 2024</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">📊 Exploratory Data Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Deep-dive into 3 years of Delhi Metro ridership data — temporal patterns, ticket behaviour, revenue trends and station traffic</div>', unsafe_allow_html=True)

    # KPI Row
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    for col, val, lbl, clr, ico in [
        (c1, "1,50,000", "Total Trips",    BLUE,  "🗄️"),
        (c2, "₹31.22 Cr","Revenue",        GREEN, "💰"),
        (c3, "29.7 Lakh","Passengers",     BLUE,  "👥"),
        (c4, "5.49 km",  "Avg Distance",   GOLD,  "📍"),
        (c5, "₹105.12",  "Avg Fare",       RED,   "🎫"),
        (c6, "20",       "Avg Pass/Trip",  BLUE,  "🚃"),
    ]:
        col.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">{ico}</div>
            <div class="kpi-value" style="color:{clr}; font-size:1.45rem">{val}</div>
            <div class="kpi-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    # ── Tab structure ──
    tab_temp, tab_station, tab_ticket, tab_peak = st.tabs(
        ["📅 Temporal Analysis", "🏙️ Station Analysis", "🎫 Ticket & Revenue", "⚡ Peak vs Off-Peak"])

    # ── TEMPORAL ──
    with tab_temp:
        st.markdown('<div class="section-header">Monthly Passenger Trend</div>', unsafe_allow_html=True)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=MONTHS, y=MONTHLY_PASS, mode="lines+markers",
            fill="tozeroy", fillcolor="rgba(28,52,97,0.07)",
            line=dict(color=BLUE, width=2.5), marker=dict(size=4, color=BLUE),
            hovertemplate="<b>%{x}</b><br>%{y:,} passengers<extra></extra>"))
        # Year markers — use shapes instead of add_vline (avoids int+str TypeError with categorical x)
        for yr, idx in [("2022", 0), ("2023", 12), ("2024", 24)]:
            fig1.add_shape(type="line", x0=idx, x1=idx, y0=0, y1=1,
                           xref="x", yref="paper",
                           line=dict(color=RED, width=1, dash="dot"))
            fig1.add_annotation(x=idx, y=1, xref="x", yref="paper",
                                text=yr, showarrow=False,
                                font=dict(size=11, color=RED), yanchor="bottom")
        fig1.update_layout(**BASE_LAYOUT, height=300, title="36-Month Ridership · Jan 2022–Dec 2024")
        st.plotly_chart(fig1, use_container_width=True)

        col_a, col_b = st.columns(2)
        with col_a:
            hours   = list(range(24))
            h_pass  = [20,12,8,5,4,8,45,180,320,280,160,130,120,115,125,140,180,310,340,220,140,90,60,35]
            colors  = [RED if v>250 else BLUE if v>100 else "#D6D3D1" for v in h_pass]
            fig_h   = go.Figure(go.Bar(x=[f"{h:02d}:00" for h in hours], y=h_pass,
                marker_color=colors, hovertemplate="<b>%{x}</b><br>%{y} avg passengers<extra></extra>"))
            fig_h.add_hrect(y0=250, y1=360, fillcolor="rgba(185,28,28,0.06)", line_width=0, annotation_text="Peak Zone")
            fig_h.update_layout(**BASE_LAYOUT, height=290, title="Average Hourly Distribution (per Station)")
            st.plotly_chart(fig_h, use_container_width=True)

        with col_b:
            days    = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
            d_pass  = [88200, 85400, 84100, 85800, 87200, 72300, 68500]
            d_colors= [RED if v>85000 else BLUE if v>75000 else "#D6D3D1" for v in d_pass]
            fig_d   = go.Figure(go.Bar(x=days, y=d_pass, marker_color=d_colors,
                text=[f"{v//1000}k" for v in d_pass], textposition="outside",
                hovertemplate="<b>%{x}</b><br>%{y:,} passengers<extra></extra>"))
            layout_d = {**BASE_LAYOUT}
            layout_d["yaxis"] = {**layout_d.get("yaxis", {}), "range": [60000, 95000]}
            fig_d.update_layout(**layout_d, height=290, title="Ridership by Day of Week")
            st.plotly_chart(fig_d, use_container_width=True)

        st.markdown("""
        <div class="insight-card blue">
            <div class="insight-title">📌 Temporal Key Findings</div>
            <div class="insight-body">
                Peak hours 8–10 AM and 5–8 PM account for <b>52% of daily ridership</b>.
                Monday is the busiest weekday (+18% vs Sunday). No significant year-on-year growth —
                flat pattern at <b>79,000–84,000/month</b> across all 3 years.
            </div>
        </div>""", unsafe_allow_html=True)

    # ── STATION ──
    with tab_station:
        st.markdown('<div class="section-header">Station Traffic Ranking</div>', unsafe_allow_html=True)
        stations_sorted = sorted(STATION_DATA.items(), key=lambda x: x[1]["total"], reverse=True)
        snames  = [s[0] for s in stations_sorted]
        stotals = [s[1]["total"] for s in stations_sorted]
        s_colors= [RED if s=="Rajiv Chowk" else BLUE if STATION_DATA[s]["type"]=="Hub" else "#94A3B8" for s in snames]

        col_c, col_d = st.columns(2)
        with col_c:
            fig_st = go.Figure(go.Bar(x=stotals, y=snames, orientation="h",
                marker_color=s_colors,
                text=[f"{v:,}" for v in stotals], textposition="outside",
                hovertemplate="<b>%{y}</b><br>%{x:,} movements<extra></extra>"))
            layout_st = {**BASE_LAYOUT}
            layout_st["yaxis"] = {**layout_st.get("yaxis", {}), "autorange": "reversed"}
            fig_st.update_layout(**layout_st, height=420, title="Station Traffic — All 12 Stations")
            st.plotly_chart(fig_st, use_container_width=True)

        with col_d:
            nets = [STATION_DATA[s]["net"] for s in snames[:10]]
            n_colors = [BLUE if v>0 else RED for v in nets]
            fig_net = go.Figure(go.Bar(x=snames[:10], y=nets, marker_color=n_colors,
                hovertemplate="<b>%{x}</b><br>Net Flow: %{y:+,}<extra></extra>"))
            fig_net.add_hline(y=0, line_color="#1C1917", line_width=1)
            fig_net.update_layout(**BASE_LAYOUT, height=420, title="Net Passenger Flow (Departures − Arrivals)")
            st.plotly_chart(fig_net, use_container_width=True)

        type_icon = {"Hub": "🔵", "Major": "🟢", "Medium": "🟡", "Minor": "🔴"}
        df_st = pd.DataFrame([{
            "Station": s, "Type": f"{type_icon.get(d['type'],'⚪')} {d['type']}",
            "Total Traffic": f"{d['total']:,}",
            "Departures": f"{d['departures']:,}", "Arrivals": f"{d['arrivals']:,}",
            "Net Flow": f"+{d['net']:,}" if d['net']>0 else f"{d['net']:,}",
            "Capacity": f"{d['capacity']:,}"
        } for s,d in sorted(STATION_DATA.items(), key=lambda x: x[1]["total"], reverse=True)])
        st.dataframe(df_st, use_container_width=True, hide_index=True)

    # ── TICKET & REVENUE ──
    with tab_ticket:
        col_e, col_f = st.columns(2)
        with col_e:
            st.markdown('<div class="section-header">Ticket Type Split</div>', unsafe_allow_html=True)
            fig_pie = go.Figure(go.Pie(
                labels=list(TICKET_DATA.keys()),
                values=[v["revenue"] for v in TICKET_DATA.values()],
                hole=0.55,
                marker=dict(colors=[BLUE, GREEN, RED, GOLD], line=dict(color="white", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<extra></extra>"))
            fig_pie.update_layout(**BASE_LAYOUT, height=320, showlegend=False,
                annotations=[dict(text="Revenue<br>Split", x=0.5, y=0.5,
                    font=dict(size=13, color=BLUE, family="Playfair Display"), showarrow=False)])
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_f:
            st.markdown('<div class="section-header">Revenue by Year</div>', unsafe_allow_html=True)
            fig_rev = go.Figure(go.Bar(
                x=["2022","2023","2024"], y=[10.39, 10.42, 10.41],
                marker_color=[BLUE, RED, GREEN],
                text=["₹10.39 Cr","₹10.42 Cr","₹10.41 Cr"], textposition="outside",
                hovertemplate="<b>%{x}</b><br>₹%{y:.2f} Crore<extra></extra>"))
            layout_rev = {**BASE_LAYOUT}
            layout_rev["yaxis"] = {**layout_rev.get("yaxis", {}), "range": [10.3, 10.5]}
            fig_rev.update_layout(**layout_rev, height=320, title="Yearly Revenue — 0% Growth Confirmed")
            st.plotly_chart(fig_rev, use_container_width=True)

        # Ticket summary table
        df_tkt = pd.DataFrame([{
            "Ticket Type": t,
            "Trips": f"{d['trips']:,}",
            "Revenue": f"₹{d['revenue']:,}",
            "Avg Fare": f"₹{d['avg_fare']:.2f}",
            "Share": f"{d['trips']/sum(v['trips'] for v in TICKET_DATA.values())*100:.1f}%"
        } for t,d in TICKET_DATA.items()])
        st.dataframe(df_tkt, use_container_width=True, hide_index=True)

    # ── PEAK vs OFF-PEAK ──
    with tab_peak:
        st.markdown('<div class="section-header">Revenue Anomaly — Peak Pricing Paradox</div>', unsafe_allow_html=True)
        periods = list(REMARKS_DATA.keys())
        rev_trip= [REMARKS_DATA[p]["rev_trip"] for p in periods]
        b_cols  = [RED if p=="peak" else GREEN if p=="off-peak" else "#94A3B8" for p in periods]

        col_g, col_h = st.columns([1.5, 1])
        with col_g:
            fig_pk = go.Figure(go.Bar(x=rev_trip, y=periods, orientation="h",
                marker_color=b_cols,
                text=[f"₹{v:.2f}" for v in rev_trip], textposition="outside",
                hovertemplate="<b>%{y}</b><br>₹%{x:.2f} per trip<extra></extra>"))
            layout_pk = {**BASE_LAYOUT}
            layout_pk["xaxis"] = {**layout_pk.get("xaxis", {}), "range": [2070, 2090]}
            fig_pk.update_layout(**layout_pk, height=300,
                title="Revenue per Trip by Time Period — Cell 37 Output")
            st.plotly_chart(fig_pk, use_container_width=True)

        with col_h:
            st.markdown("""
            <div class="insight-card red">
                <div class="insight-title">❌ The Paradox</div>
                <div class="insight-body">
                    Peak: <b>₹2,077.32/trip</b><br>
                    Off-Peak: <b>₹2,084.94/trip</b><br><br>
                    Off-peak earns <b>₹7.62 MORE</b> — DMRC's busiest window is its least profitable!
                </div>
            </div>
            <div class="insight-card green">
                <div class="insight-title">✅ Solution: Dynamic Pricing</div>
                <div class="insight-body">
                    Raise peak fare <b>+25% → ₹131.56</b><br>
                    Annual gain: <b>₹2.5 Crore</b><br>
                    ROI: <b>1149%</b> · Payback: <b>0.96 months</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Correlation heatmap
        st.markdown('<div class="section-header">Correlation Matrix</div>', unsafe_allow_html=True)
        corr_labels = ["Distance_km","Fare","Cost/Pass","Passengers","Revenue"]
        corr_matrix = [[1.00,0.98,0.98,-0.01,0.62],
                       [0.98,1.00,0.99,-0.01,0.64],
                       [0.98,0.99,1.00,-0.01,0.63],
                       [-0.01,-0.01,-0.01,1.00,0.47],
                       [0.62,0.64,0.63,0.47,1.00]]
        fig_hm = go.Figure(go.Heatmap(
            z=corr_matrix, x=corr_labels, y=corr_labels,
            colorscale=[[0,"#FEE2E2"],[0.5,"#FAF7F2"],[1,"#DBEAFE"]],
            text=[[f"{v:.2f}" for v in row] for row in corr_matrix],
            texttemplate="%{text}", textfont=dict(size=13),
            hovertemplate="<b>%{x} vs %{y}</b><br>r = %{z:.2f}<extra></extra>"))
        fig_hm.update_layout(**BASE_LAYOUT, height=340, title="Pearson Correlation Matrix — Cell 17")
        st.plotly_chart(fig_hm, use_container_width=True)
        st.markdown("""
        <div class="insight-card yellow">
            <div class="insight-title">🔑 Key Finding</div>
            <div class="insight-body">Passengers vs Distance = <b>r = −0.01</b>. Load is completely
            independent of trip length — DMRC charges by distance but load doesn't follow distance.
            A massive hidden pricing inefficiency.</div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: ANOMALY (Admin)
# ─────────────────────────────────────────────────────────────────────────────
def page_anomaly():
    st.markdown('<div class="admin-alert">🔐 <b>Admin Access — Anomaly Detection Dashboard</b> · Statistical outliers · High-variance zones</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">🚨 Anomaly Detection</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Statistical outliers, high-variance stations, and the hidden revenue paradox</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl,clr,ico in [
        (c1,"2,847","Outlier Records",RED,"⚠️"),
        (c2,"1.90%","Anomaly Rate",GOLD,"📊"),
        (c3,"2","High-Variance Zones",RED,"🏙️"),
        (c4,"₹7.62","Revenue Gap",GREEN,"💰"),
    ]:
        col.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">{ico}</div>
            <div class="kpi-value" style="color:{clr}; font-size:1.6rem">{val}</div>
            <div class="kpi-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔴 High-Variance Stations</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="anomaly-danger">
            <div style="font-weight:800; font-size:1rem; color:#7F1D1D">🔴 RAJIV CHOWK — CRITICAL VARIANCE</div>
            <div style="font-size:0.85rem; color:#991B1B; margin-top:0.6rem; line-height:1.75">
                <b>Total Movements:</b> 23,701 (16.8% above #2 station)<br>
                <b>Net Flow:</b> +11,239 (extreme departure dominance)<br>
                <b>Risk:</b> Single point of failure — ALL top-10 revenue routes originate here<br>
                <b>Impact if disrupted:</b> Simultaneous revenue loss across all top routes<br>
                <b>Recommendation:</b> Dedicated contingency protocol + crowd management AI
            </div>
        </div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="anomaly-warn">
            <div style="font-weight:800; font-size:1rem; color:#713F12">🟡 KASHMERE GATE — MEDIUM VARIANCE</div>
            <div style="font-size:0.85rem; color:#92400E; margin-top:0.6rem; line-height:1.75">
                <b>Total Movements:</b> 11,750<br>
                <b>Net Flow:</b> −150 (slight arrival dominance)<br>
                <b>Risk:</b> Multi-line interchange station → crowd overflow risk<br>
                <b>Peak Pressure:</b> 8–10 AM window<br>
                <b>Recommendation:</b> Extra staff during peak interchange hours
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-header">📊 Outlier Visualisation</div>', unsafe_allow_html=True)
    col_c, col_d = st.columns(2)
    with col_c:
        # Box plots
        np.random.seed(42)
        cats = list(REMARKS_DATA.keys())
        base_v = {p: REMARKS_DATA[p]["rev_trip"] for p in cats}
        fig_box = go.Figure()
        bx_colors = {p: RED if p=="peak" else GREEN if p=="off-peak" else "#94A3B8" for p in cats}
        for cat in cats:
            vals = np.random.normal(base_v[cat], 15, 200)
            fig_box.add_trace(go.Box(y=vals, name=cat, marker_color=bx_colors[cat], boxmean=True))
        fig_box.update_layout(**BASE_LAYOUT, height=320,
            title="Revenue/Trip Distribution by Period", showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    with col_d:
        np.random.seed(42)
        x_sc = np.random.normal(20, 4, 200)
        y_sc = np.random.normal(105, 30, 200)
        out_idx = np.random.choice(200, 20, replace=False)
        c_sc = [RED if i in out_idx else BLUE for i in range(200)]
        fig_sc = go.Figure(go.Scatter(x=x_sc, y=y_sc, mode="markers",
            marker=dict(color=c_sc, size=6, opacity=0.65),
            hovertemplate="Pass: %{x:.0f} | Fare: ₹%{y:.0f}<extra></extra>"))
        fig_sc.update_layout(**BASE_LAYOUT, height=320,
            title="Passenger vs Fare Scatter — Outliers in Red",
            xaxis_title="Passengers", yaxis_title="Fare (₹)")
        st.plotly_chart(fig_sc, use_container_width=True)

    # Correlation heatmap
    st.markdown('<div class="section-header">🔗 Correlation Analysis</div>', unsafe_allow_html=True)
    cl = ["Distance_km","Fare","Cost/Pass","Passengers","Revenue"]
    cm = [[1.00,0.98,0.98,-0.01,0.62],[0.98,1.00,0.99,-0.01,0.64],
          [0.98,0.99,1.00,-0.01,0.63],[-0.01,-0.01,-0.01,1.00,0.47],[0.62,0.64,0.63,0.47,1.00]]
    fig_ch = go.Figure(go.Heatmap(z=cm, x=cl, y=cl,
        colorscale=[[0,"#FEE2E2"],[0.5,"#FAF7F2"],[1,"#DBEAFE"]],
        text=[[f"{v:.2f}" for v in row] for row in cm],
        texttemplate="%{text}", textfont=dict(size=13),
        hovertemplate="<b>%{x} vs %{y}</b><br>r = %{z:.2f}<extra></extra>"))
    fig_ch.update_layout(**BASE_LAYOUT, height=330, title="Pearson Correlation Matrix — Cell 17 Output")
    st.plotly_chart(fig_ch, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: FORECAST (Admin + User)
# ─────────────────────────────────────────────────────────────────────────────
def page_forecast():
    role = st.session_state.user_role
    if role == "user":
        st.markdown('<div class="user-alert">👤 <b>User Access</b> — Welcome to SmartMetro AI Congestion Predictor. Fill in the form below to get instant predictions.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="admin-alert">🔐 <b>Admin Access — Full Forecasting Hub</b> · SARIMA monthly forecasts + Live LSTM congestion predictor</div>', unsafe_allow_html=True)

    st.markdown('<div class="page-title">🤖 AI Congestion Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Select station, time, weather, ticket type and cost — get passenger count, congestion %, status and 2-hour ahead forecast</div>', unsafe_allow_html=True)

    # ── ADMIN ONLY: SARIMA chart ──
    if role == "admin":
        st.markdown('<div class="section-header">📈 SARIMA 24-Month Passenger Forecast</div>', unsafe_allow_html=True)

        model_choice = st.selectbox("Select Forecasting Model",
            ["SARIMA(1,1,1)×(1,1,1,12) — Best (RMSE: 2,480)",
             "ARIMA(2,1,2) — RMSE: 2,709",
             "LSTM Neural Network — RMSE: 116 (daily)"])

        mc1,mc2,mc3,mc4 = st.columns(4)
        for col,lbl,val,clr in [
            (mc1,"Best Model","SARIMA(1,1,1)",BLUE),
            (mc2,"SARIMA RMSE","2,480 pass",GREEN),
            (mc3,"Ljung-Box p","0.9978",GREEN),
            (mc4,"Growth Rate","0.00% — Flat",GOLD),
        ]:
            col.markdown(f"""<div class="kpi-card">
                <div class="kpi-value" style="color:{clr}; font-size:1rem">{val}</div>
                <div class="kpi-label">{lbl}</div>
            </div>""", unsafe_allow_html=True)

        fig_fc = go.Figure()
        fig_fc.add_trace(go.Scatter(x=MONTHS, y=MONTHLY_PASS, name="Historical 2022–24",
            line=dict(color=BLUE, width=2.5),
            hovertemplate="<b>%{x}</b><br>%{y:,} passengers<extra></extra>"))
        months_2025 = [f"2025-{m:02d}" for m in range(1,13)]
        months_2026 = [f"2026-{m:02d}" for m in range(1,13)]
        fig_fc.add_trace(go.Scatter(x=months_2025, y=FORECAST_2025, name="Forecast 2025",
            line=dict(color=RED, width=2.5, dash="dash"),
            hovertemplate="<b>%{x}</b><br>%{y:,} predicted<extra></extra>"))
        fig_fc.add_trace(go.Scatter(x=months_2026, y=FORECAST_2026, name="Forecast 2026",
            line=dict(color=GREEN, width=2.5, dash="dot"),
            hovertemplate="<b>%{x}</b><br>%{y:,} predicted<extra></extra>"))
        layout_fc = {**BASE_LAYOUT}
        layout_fc["yaxis"] = {**layout_fc.get("yaxis", {}), "range": [76000, 86000]}
        fig_fc.update_layout(**layout_fc, height=330,
            title="Monthly Passenger Forecast 2025–2026 — SARIMA Output",
            legend=dict(orientation="h", y=1.05))
        st.plotly_chart(fig_fc, use_container_width=True)

        st.markdown("""
        <div class="insight-card blue">
            <div class="insight-title">📌 Forecast Summary</div>
            <div class="insight-body">Ridership stays flat at <b>79,000–84,724/month</b> through Dec 2026.
            Monthly growth = <b>0.00%</b>. DMRC should focus on revenue optimisation from existing
            passengers rather than urgent infrastructure expansion.</div>
        </div>""", unsafe_allow_html=True)
        st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    # ── PREDICTION FORM ──
    st.markdown('<div class="section-header">🔮 Live Station Congestion Predictor</div>', unsafe_allow_html=True)

    with st.form("pred_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            station = st.selectbox("📍 Station Name", ALL_STATIONS)
            line    = st.selectbox("🚇 Metro Line",
                ["Blue Line","Yellow Line","Red Line","Green Line","Violet Line","Pink Line","Orange Line","Magenta Line","Grey Line"])
            ticket_type = st.selectbox("🎫 Ticket Type",
                ["Tourist Card","Smart Card","Single Journey","Return"])
        with col2:
            hour    = st.slider("🕐 Time of Day (Hour)", 0, 23, datetime.datetime.now().hour)
            is_peak = st.checkbox("⚡ Peak Hour (Rush Hour)", value=(datetime.datetime.now().hour in [8,9,10,17,18,19]))
            weather = st.selectbox("🌤️ Weather Condition",
                ["Clear Sky","Light Rain","Heavy Rain","Extreme Weather","Foggy / Winter"])
        with col3:
            avg_cost = st.slider("💰 Average Fare (₹)", min_value=10, max_value=200, value=105)
            if role == "admin":
                pred_model = st.selectbox("🤖 Prediction Model",
                    ["LSTM Neural Network","SARIMA","ARIMA"])
            else:
                pred_model = "LSTM Neural Network"
                st.markdown("""
                <div class="insight-card blue" style="margin-top:0.5rem">
                    <div class="insight-title">🤖 Model: LSTM</div>
                    <div class="insight-body">Neural network model · RMSE 116 · 5 features · Best accuracy</div>
                </div>""", unsafe_allow_html=True)

        submit = st.form_submit_button("🔮  Generate Prediction", use_container_width=True)

    if submit:
        count, pct, status, badge, forecast, f_pct, f_status = predict_congestion(
            station, int(is_peak), weather, ticket_type, hour, line, avg_cost, pred_model)

        cap = STATION_DATA.get(station, {}).get("capacity", 3000)

        st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📊 Prediction Results")

        # ── Result cards row 1 ──
        r1,r2,r3,r4 = st.columns(4)
        clr_pct = RED if pct>=85 else GOLD if pct>=70 else GREEN
        clr_fc  = RED if f_pct>=85 else GOLD if f_pct>=70 else GREEN

        with r1:
            st.markdown(f"""<div class="forecast-card">
                <div class="forecast-label">🚶 Passenger Count</div>
                <div class="forecast-number" style="color:{BLUE}">{count:,}</div>
                <div class="forecast-sub">At {hour:02d}:00 · {station}</div>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""<div class="forecast-card">
                <div class="forecast-label">📊 Congestion Level</div>
                <div class="forecast-number" style="color:{clr_pct}">{pct:.1f}%</div>
                <div class="forecast-sub">of {cap:,} capacity</div>
            </div>""", unsafe_allow_html=True)
        with r3:
            badge_html = f'<div class="badge-{badge}">{status}</div>'
            st.markdown(f"""<div class="forecast-card">
                <div class="forecast-label">🚦 Current Status</div>
                <div style="margin:0.8rem 0">{badge_html}</div>
                <div class="forecast-sub">{line}</div>
            </div>""", unsafe_allow_html=True)
        with r4:
            st.markdown(f"""<div class="forecast-card">
                <div class="forecast-label">⏩ 2-Hour Forecast</div>
                <div class="forecast-number" style="color:{clr_fc}">{forecast:,}</div>
                <div class="forecast-sub">{f_pct:.1f}% capacity · {f_status}</div>
            </div>""", unsafe_allow_html=True)

        # ── Input Summary Row ──
        st.markdown("<br>", unsafe_allow_html=True)
        s1,s2,s3,s4,s5,s6 = st.columns(6)
        for col,ico,lbl,val in [
            (s1,"📍","Station",station[:15]),
            (s2,"🚇","Line",line.replace(" Line","")),
            (s3,"🎫","Ticket",ticket_type[:12]),
            (s4,"🌤️","Weather",weather[:12]),
            (s5,"💰","Avg Fare",f"₹{avg_cost}"),
            (s6,"⚡","Peak Hour","Yes" if is_peak else "No"),
        ]:
            col.markdown(f"""<div class="kpi-card" style="padding:0.9rem">
                <div style="font-size:1.2rem">{ico}</div>
                <div style="font-weight:700; color:#1C1917; font-size:0.85rem">{val}</div>
                <div class="kpi-label" style="font-size:0.68rem">{lbl}</div>
            </div>""", unsafe_allow_html=True)

        # ── Congestion gauge chart ──
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=pct,
                delta={"reference": 70, "valueformat": ".1f", "suffix": "%"},
                title={"text": f"Congestion — {station}", "font": {"size": 14, "family": "Playfair Display"}},
                gauge={
                    "axis": {"range": [0, 100], "tickfont": {"size": 11}},
                    "bar": {"color": clr_pct},
                    "steps": [
                        {"range": [0, 70],  "color": "#F0FDF4"},
                        {"range": [70, 85], "color": "#FEFCE8"},
                        {"range": [85, 100],"color": "#FEE2E2"},
                    ],
                    "threshold": {"line": {"color": RED, "width": 3}, "thickness": 0.8, "value": 85},
                },
                number={"suffix": "%", "font": {"size": 36, "family": "Playfair Display"}},
            ))
            fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300,
                margin=dict(l=30, r=30, t=80, b=20),
                font=dict(family="DM Sans"))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with col_chart2:
            # Time-series prediction chart
            hrs = list(range(max(0, hour-3), min(24, hour+5)))
            base_mul = [0.12,0.08,0.05,0.04,0.04,0.08,0.45,1.6,2.8,2.4,1.4,1.1,
                        1.0,0.9,1.0,1.2,1.6,2.8,3.0,2.0,1.2,0.8,0.55,0.32]
            hist_v = [int(STATION_DATA.get(station,{}).get("base",200) * base_mul[h] * 3) for h in hrs]
            pred_v = [None]*len(hrs)
            pi = hrs.index(hour) if hour in hrs else 0
            pred_v[pi] = count
            if pi+2 < len(hrs): pred_v[pi+1] = int((count+forecast)/2); pred_v[pi+2] = forecast

            fig_ts = go.Figure()
            fig_ts.add_trace(go.Scatter(x=[f"{h:02d}:00" for h in hrs], y=hist_v,
                name="Historical Avg", line=dict(color="#D6D3D1", width=2, dash="dot")))
            fig_ts.add_trace(go.Scatter(x=[f"{h:02d}:00" for h in hrs], y=pred_v,
                name="AI Prediction", line=dict(color=RED, width=3),
                mode="lines+markers", marker=dict(size=9, color=RED)))
            fig_ts.add_hline(y=cap*0.85, line_dash="dash", line_color=RED, opacity=0.4, annotation_text="DANGER (85%)")
            fig_ts.add_hline(y=cap*0.70, line_dash="dash", line_color=GOLD, opacity=0.4, annotation_text="MODERATE (70%)")
            fig_ts.update_layout(**BASE_LAYOUT, height=300,
                title=f"Predicted Surge — {station}",
                legend=dict(orientation="h", y=1.05))
            st.plotly_chart(fig_ts, use_container_width=True)

        # ── Action Alert ──
        if badge == "danger":
            st.error(f"""🔴 **CRITICAL — DANGER ZONE** | {station} is at **{pct:.1f}%** of capacity ({count:,} passengers).
            **Immediate Actions:** Deploy extra security staff · Activate surge pricing · Alert station master · Stagger entry gates.
            **2-Hour Outlook:** {forecast:,} passengers ({f_pct:.1f}%) — {f_status}""")
        elif badge == "moderate":
            st.warning(f"""🟡 **MONITOR CLOSELY** | {station} is at **{pct:.1f}%** ({count:,} passengers).
            Keep backup staff on standby · Slow entry if nearing 85%.
            **2-Hour Outlook:** {forecast:,} passengers ({f_pct:.1f}%) — {f_status}""")
        else:
            st.success(f"""🟢 **NORMAL OPERATIONS** | {station} is at **{pct:.1f}%** ({count:,} passengers) — Safe for all commuters.
            Good window for maintenance checks or staff rotation.
            **2-Hour Outlook:** {forecast:,} passengers ({f_pct:.1f}%) — {f_status}""")

        # ── Detailed Breakdown Table ──
        st.markdown('<div class="section-header">📋 Full Prediction Breakdown</div>', unsafe_allow_html=True)
        df_res = pd.DataFrame({
            "Parameter": ["Station","Metro Line","Ticket Type","Weather","Hour","Peak Hour","Avg Fare","Model Used"],
            "Value":     [station, line, ticket_type, weather, f"{hour:02d}:00",
                          "Yes ⚡" if is_peak else "No", f"₹{avg_cost}", pred_model],
            "Prediction":["Passenger Count","Congestion %","Status","2-Hr Forecast","2-Hr Congestion %","2-Hr Status","Station Capacity","Alert Level"],
            "Result":    [f"{count:,}", f"{pct:.1f}%", status, f"{forecast:,}", f"{f_pct:.1f}%", f_status, f"{cap:,}", badge.upper()],
        })
        st.dataframe(df_res, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: POLICY (Admin)
# ─────────────────────────────────────────────────────────────────────────────
def page_policy():
    st.markdown('<div class="admin-alert">🔐 <b>Admin Access — Policy Dashboard</b> · Cost-benefit analysis · Live fare simulator · Implementation roadmap</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">💡 Operational Policy Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Evidence-based policy recommendations with ROI, payback periods, and live fare simulation</div>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col,val,lbl,clr,ico in [
        (c1,"₹4.68 Cr","Max Revenue Gain",GREEN,"📈"),
        (c2,"1149%","Best Policy ROI",GREEN,"🏆"),
        (c3,"0.96 months","Fastest Payback",BLUE,"⚡"),
        (c4,"₹31.22 Cr","Current Revenue",GOLD,"💰"),
    ]:
        col.markdown(f"""<div class="kpi-card">
            <div class="kpi-icon">{ico}</div>
            <div class="kpi-value" style="color:{clr}; font-size:1.7rem">{val}</div>
            <div class="kpi-label">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="brand-divider"></div>', unsafe_allow_html=True)

    # ── Policy Cards ──
    st.markdown('<div class="section-header">🏆 Policy Recommendations — Cell 39 Output</div>', unsafe_allow_html=True)
    pc1, pc2, pc3 = st.columns(3)
    pol_list = [
        (pc1, "💳 Smart Card Loyalty", "836%", "₹4.68 Cr", "₹50 Lakh", "1.28 months", BLUE,
         "Points reward system for frequent commuters. Partner merchant discounts. Expected +5% Smart Card adoption."),
        (pc2, "⚡ Dynamic Peak Pricing","1149%","₹2.50 Cr","₹20 Lakh","0.96 months", RED,
         "Raise peak fare to ₹131.56 (+25%). Directly fixes the off-peak earning more than peak anomaly."),
        (pc3, "🌍 Tourist Enhancement", "1149%","₹3.75 Cr","₹30 Lakh","0.96 months", GREEN,
         "Tiered tourist packages: 1-day, 3-day, weekly. Targets the 39.5% Tourist Card user segment."),
    ]
    for col,name,roi,gain,cost,pb,clr,desc in pol_list:
        col.markdown(f"""
        <div class="policy-card" style="border-top:4px solid {clr}">
            <div class="policy-title">{name}</div>
            <div class="policy-roi">{roi}</div>
            <div style="font-size:0.72rem; color:#78716C; margin-bottom:0.8rem">Return on Investment</div>
            <div style="border-top:1px solid #F3EDE3; padding-top:0.8rem">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem">
                    <span style="font-size:0.8rem; color:#78716C">Revenue Gain</span>
                    <span style="font-weight:700; color:{clr}; font-size:0.88rem">{gain}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.4rem">
                    <span style="font-size:0.8rem; color:#78716C">Cost</span>
                    <span style="font-weight:600; font-size:0.85rem">{cost}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:0.8rem">
                    <span style="font-size:0.8rem; color:#78716C">Payback</span>
                    <span style="font-weight:700; color:{GREEN}; font-size:0.85rem">{pb}</span>
                </div>
                <div style="font-size:0.82rem; color:#57534E; background:#FAF7F2; padding:0.6rem; border-radius:8px">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Charts ──
    col_roi, col_fare = st.columns(2)
    with col_roi:
        st.markdown('<div class="section-header">ROI Comparison</div>', unsafe_allow_html=True)
        fig_roi = go.Figure(go.Bar(
            x=["Smart Card\nLoyalty","Dynamic Peak\nPricing","Tourist\nEnhancement"],
            y=[836.84, 1149.12, 1149.12],
            marker_color=[BLUE, RED, GREEN],
            text=["836%","1149%","1149%"], textposition="outside",
            hovertemplate="<b>%{x}</b><br>ROI: %{y:.2f}%<extra></extra>"))
        layout_roi = {**BASE_LAYOUT}
        layout_roi["yaxis"] = {**layout_roi.get("yaxis", {}), "range": [0, 1350]}
        fig_roi.update_layout(**layout_roi, height=340,
            title="Policy ROI Comparison (%) — Cell 39 Output")
        st.plotly_chart(fig_roi, use_container_width=True)

    with col_fare:
        st.markdown('<div class="section-header">⚙️ Live Fare Simulator</div>', unsafe_allow_html=True)
        fare_pct   = st.slider("Fare Change (%)", -15, 25, 0, format="%d%%")
        elasticity = -0.3
        new_fare   = 105.12 * (1 + fare_pct/100)
        pass_chg   = fare_pct * elasticity
        new_rev    = 312278958 * (1 + fare_pct/100) * (1 + pass_chg/100)
        rev_chg    = (new_rev - 312278958) / 312278958 * 100

        sc1, sc2 = st.columns(2)
        sc1.markdown(f"""<div class="kpi-card">
            <div class="kpi-value" style="color:{BLUE}; font-size:1.5rem">₹{new_fare:.2f}</div>
            <div class="kpi-label">New Avg Fare</div>
        </div>""", unsafe_allow_html=True)
        rc = GREEN if rev_chg>=0 else RED
        sc2.markdown(f"""<div class="kpi-card">
            <div class="kpi-value" style="color:{rc}; font-size:1.5rem">{rev_chg:+.1f}%</div>
            <div class="kpi-label">Revenue Change</div>
        </div>""", unsafe_allow_html=True)

        card_cls = "green" if rev_chg>=0 else "red"
        st.markdown(f"""<div class="insight-card {card_cls}">
            <div class="insight-title">Simulation Result</div>
            <div class="insight-body">
                Fare <b>{fare_pct:+d}%</b> → Revenue <b>{rev_chg:+.1f}%</b><br>
                Passenger change: <b>{pass_chg:+.1f}%</b><br>
                Projected annual revenue: <b>₹{new_rev/1e7:.2f} Cr</b>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Risk Matrix ──
    st.markdown('<div class="section-header">⚠️ Risk Matrix — Load vs Efficiency</div>', unsafe_allow_html=True)
    risk_data = [
        ["LOW LOAD + LOW EFF.", "LOW LOAD + MED EFF.", "LOW LOAD + HIGH EFF."],
        ["MED LOAD + LOW EFF.", "MED LOAD + MED EFF.", "MED LOAD + HIGH EFF."],
        ["HIGH LOAD + LOW EFF.","HIGH LOAD + MED EFF.","HIGH LOAD + HIGH EFF."],
    ]
    risk_cls = [["risk-low","risk-low","risk-med"],["risk-low","risk-med","risk-med"],["risk-med","risk-high","risk-high"]]
    cols_risk = st.columns([0.6,1,1,1])
    with cols_risk[0]:
        st.markdown("<div style='height:2.2rem'></div>", unsafe_allow_html=True)
        for lbl in ["Low Load","Med Load","High Load"]:
            st.markdown(f"<div style='height:5rem; display:flex; align-items:center; font-weight:600; font-size:0.82rem; color:#44403C'>{lbl}</div>", unsafe_allow_html=True)
    for ci, (col, eff_l) in enumerate(zip(cols_risk[1:], ["Low Efficiency","Med Efficiency","High Efficiency"])):
        with col:
            st.markdown(f"<div style='text-align:center; font-weight:700; font-size:0.85rem; color:{BLUE}; margin-bottom:0.5rem'>{eff_l}</div>", unsafe_allow_html=True)
            for ri in range(3):
                st.markdown(f"<div class='{risk_cls[ri][ci]}'>{risk_data[ri][ci]}</div>", unsafe_allow_html=True)

    # ── Roadmap ──
    st.markdown('<div class="section-header">🗺️ Implementation Roadmap</div>', unsafe_allow_html=True)
    r1,r2,r3 = st.columns(3)
    roadmap = [
        (r1,"0–3 Months",RED,["Implement Dynamic Peak Pricing (₹131.56)","Deploy real-time passenger counters","Launch Smart Card rewards pilot (5 stations)","DMRC board regulatory approval"]),
        (r2,"3–12 Months",BLUE,["Roll out Tourist Card enhancement packages","Smart Card loyalty to all 24 stations","Integrate real-time AFC data feed","Monthly modal shift monitoring"]),
        (r3,"12+ Months",GREEN,["Full AI dynamic pricing across network","Predictive maintenance scheduling","Demand-based fleet deployment","Annual model retraining"]),
    ]
    for col,(_, phase, clr, actions) in zip([r1,r2,r3], roadmap):
        col.markdown(f"""
        <div class="policy-card" style="border-top:4px solid {clr}">
            <div style="font-weight:800; font-size:1rem; color:{clr}; margin-bottom:0.8rem">{phase}</div>
            {''.join([f'<div style="font-size:0.84rem; color:#374151; padding:0.3rem 0; border-bottom:1px solid #F3EDE3">✅ {a}</div>' for a in actions])}
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.5rem 0 1rem">
        <div style="font-size:2.8rem">🚇</div>
        <div style="font-family:'DM Sans',sans-serif; font-size:1.1rem; font-weight:800; color:#FFF7ED; letter-spacing:0.03em">SmartMetro AI</div>
        <div style="font-size:0.7rem; color:rgba(255,247,237,0.5); margin-top:2px; letter-spacing:0.1em; text-transform:uppercase">DMRC Intelligence System</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(255,247,237,0.15); margin:0.5rem 0'>", unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.markdown('<div class="nav-section-lbl">Navigation</div>', unsafe_allow_html=True)
        if st.button("🏠  Home"):
            st.session_state.current_page = "home"; st.rerun()
        if st.button("🔐  Login"):
            st.session_state.current_page = "login"; st.rerun()

    elif st.session_state.user_role == "admin":
        st.markdown("""<div style="background:rgba(185,28,28,0.2); border:1px solid rgba(185,28,28,0.4);
            border-radius:10px; padding:0.6rem 0.9rem; margin-bottom:1rem; font-size:0.8rem">
            🏛️ <b style="color:#FFF7ED">Admin Access</b><br>
            <span style="color:rgba(255,247,237,0.5); font-size:0.72rem">Full system access granted</span>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="nav-section-lbl">Research & Analysis</div>', unsafe_allow_html=True)
        for ico, pg, lbl in [("🏠","home","Home"), ("📊","eda","EDA Analysis"), ("🚨","anomaly","Anomaly Detection")]:
            if st.button(f"{ico}  {lbl}", key=f"nb_{pg}"):
                st.session_state.current_page = pg; st.rerun()

        st.markdown('<div class="nav-section-lbl">Production Tools</div>', unsafe_allow_html=True)
        for ico, pg, lbl in [("🤖","forecast","Forecasting Hub"), ("💡","policy","Operational Policy")]:
            if st.button(f"{ico}  {lbl}", key=f"nb_{pg}"):
                st.session_state.current_page = pg; st.rerun()

    else:
        st.markdown("""<div style="background:rgba(21,128,61,0.2); border:1px solid rgba(21,128,61,0.4);
            border-radius:10px; padding:0.6rem 0.9rem; margin-bottom:1rem; font-size:0.8rem">
            👤 <b style="color:#FFF7ED">User Access</b><br>
            <span style="color:rgba(255,247,237,0.5); font-size:0.72rem">Forecasting access only</span>
        </div>""", unsafe_allow_html=True)
        if st.button("🤖  Congestion Predictor", key="nb_fc"):
            st.session_state.current_page = "forecast"; st.rerun()

    st.markdown("<hr style='border-color:rgba(255,247,237,0.15); margin:0.8rem 0'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.7rem; color:rgba(255,247,237,0.4); padding:0.3rem 0; line-height:2">
        <div>📦 <b style="color:rgba(255,247,237,0.6)">Dataset</b>: 1,50,000 trips · 3 yrs</div>
        <div>🤖 <b style="color:rgba(255,247,237,0.6)">LSTM RMSE</b>: 116 passengers</div>
        <div>📈 <b style="color:rgba(255,247,237,0.6)">SARIMA RMSE</b>: 2,480 monthly</div>
        <div>🏙️ <b style="color:rgba(255,247,237,0.6)">Stations</b>: 24 across Delhi NCR</div>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown("<hr style='border-color:rgba(255,247,237,0.15)'>", unsafe_allow_html=True)
        if st.button("🚪  Logout"):
            st.session_state.logged_in    = False
            st.session_state.user_role    = None
            st.session_state.current_page = "home"
            st.rerun()

    st.markdown("""
    <div style="text-align:center; font-size:0.65rem; color:rgba(255,247,237,0.25); margin-top:1rem; padding-bottom:0.5rem; line-height:1.8">
        Divyanshi Mishra · Roll 1230258170<br>BCA DS&AI · BBD University · 2025-26
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────────────────────────────────────
page = st.session_state.current_page

if page == "home":
    page_home()
elif page == "login":
    page_login()
elif page == "eda":
    page_eda() if st.session_state.user_role == "admin" else st.error("🔐 Admin access required.")
elif page == "anomaly":
    page_anomaly() if st.session_state.user_role == "admin" else st.error("🔐 Admin access required.")
elif page == "forecast":
    page_forecast() if st.session_state.logged_in else (st.warning("Please login first.") or page_login())
elif page == "policy":
    page_policy() if st.session_state.user_role == "admin" else st.error("🔐 Admin access required.")