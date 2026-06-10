<div align="center">

<img src="https://img.shields.io/badge/🚇_SmartMetro_AI-DMRC_Intelligence_Platform-B91C1C?style=for-the-badge" />

# SmartMetro AI
### Real-Time Congestion Predictor & Revenue Optimization Pipeline

*An end-to-end Data Science + Deep Learning platform that predicts Delhi Metro overcrowding **before it happens** and simulates fare policies to maximize DMRC revenue.*

[![Live App](https://img.shields.io/badge/🚀_Live_App-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://smartmetrodmrc-app-rxcmv2ttkkk7cdefksjcpp.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-LSTM-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)

---

**1,50,000 Trip Records · 24 Stations · 3 Years (2022–2024) · ₹31.22 Cr Revenue Analysed**

</div>

---

## 📸 App Screenshots

| Login & Home | EDA Dashboard |
|---|---|
| ![Login](https://raw.githubusercontent.com/oce-micky/SmartMetro-AI/main/assets/login.png) | ![EDA](https://raw.githubusercontent.com/oce-micky/SmartMetro-AI/main/assets/eda.png) |

| Anomaly Detection | AI Congestion Predictor |
|---|---|
| ![Anomaly](https://raw.githubusercontent.com/oce-micky/SmartMetro-AI/main/assets/anomaly.png) | ![Predictor](https://raw.githubusercontent.com/oce-micky/SmartMetro-AI/main/assets/predictor.png) |

| Policy Dashboard | Implementation Roadmap |
|---|---|
| ![Policy](https://raw.githubusercontent.com/oce-micky/SmartMetro-AI/main/assets/policy.png) | ![Roadmap](https://raw.githubusercontent.com/oce-micky/SmartMetro-AI/main/assets/roadmap.png) |

---

## 🎯 The Problem This Solves

Every morning, **60+ lakh Delhiites** gamble — *"Will I make it on time today?"*

The answer depends on something DMRC doesn't currently have: **predictive intelligence.**

> Congestion doesn't grow slowly. A station at **70% capacity is fine**. The moment it hits **85% — everything breaks at once.** A 5-minute delay at Rajiv Chowk cascades into a **20-minute ripple across the entire Blue + Yellow lines.**

SmartMetro AI was built to catch that 15% gap **before** it becomes a crisis.

---

## 🔍 Key EDA Findings

> *All insights derived from 1,50,000 real DMRC trip records — Jan 2022 to Dec 2024.*

### 1. 📉 The Peak Hour Pricing Paradox
The most surprising finding in the entire dataset:

| Period | Revenue per Trip |
|--------|-----------------|
| 🟢 Off-Peak | ₹2,084.94 |
| 🔴 Peak Hour | ₹2,077.32 |

**Off-peak earns ₹7.62 MORE per trip than peak.** DMRC's busiest, most operationally expensive window is simultaneously its least profitable. Nobody was talking about this. The data screamed it.

### 2. 📊 Fare vs. Distance: A Complete Mismatch

The Pearson correlation between **Passengers and Distance = −0.01** (virtually zero).

```
Distance_km  ──┐
Fare         ──┤  r ≈ 0.98–0.99   ← tightly correlated with each other
Cost/Pass    ──┘

Passengers   ──── r = −0.01       ← completely independent of all three
```

DMRC prices by distance. But **load doesn't follow distance** — it follows time, weather, and events. This is a fundamental pricing inefficiency hiding in plain sight.

### 3. 🏙️ The Rajiv Chowk Bottleneck

| Station | Total Movements | Net Flow | Risk Level |
|---------|----------------|----------|------------|
| 🔴 Rajiv Chowk | 23,701 | +11,239 (departure dominant) | **CRITICAL** |
| 🟡 Kashmere Gate | 11,750 | −150 | Medium |
| 🟢 Central Secretariat | 12,580 | +76 | Low |

Rajiv Chowk moves **16.8% more passengers than the #2 station.** It is the single point of failure — ALL top-10 revenue routes originate here. If it goes down, it takes the entire network's revenue with it.

### 4. ⛈️ The Weather Multiplier Effect
Standard demand follows predictable SARIMA baselines. But when it rains — the model breaks. People who normally walk or take autos flood the metro regardless of price. **The −0.3 elasticity parameter stops working entirely during heavy rain.** The system needs real-time weather triggers to override normal pricing rules.

### 5. 📅 Ridership Trend: Flat for 3 Years

```
Monthly Passengers (2022–2024):
 84k ┤          ╭─╮    ╭─╮    ╭─╮
 82k ┤    ╭─╮  ╯  ╰╮  ╯  ╰╮  ╯  ╰╮
 80k ┤╭─╮╯  ╰──╯    ╰──╯    ╰──╯
 78k ┤╯
     └─────────────────────────────▶
      Jan'22   Jan'23   Jan'24   Dec'24
```

Monthly growth = **0.00%.** Revenue is flat. DMRC cannot grow its way out of debt — it must **optimize existing passengers**, not wait for new ones.

---

## 🤖 AI Models & Architecture

### LSTM Neural Network (Real-Time Congestion)

```
Input Layer (14-day sliding window × 5 features)
       ↓
LSTM Layer 1 (128 units) + Dropout (0.2)
       ↓
LSTM Layer 2 (64 units)  + Dropout (0.2)
       ↓
Dense Output → Passenger Count Prediction
```

| Metric | Value |
|--------|-------|
| Parameters | 30,651 |
| Input Features | Hour, Weather, Ticket Type, Line, Fare |
| RMSE (Daily) | **116 passengers** |
| Prediction Accuracy | **93%** |
| Forecast Window | 2 hours ahead |

### SARIMA Statistical Model (Monthly Baseline)

```
SARIMA(1,1,1) × (1,1,1,12)
```

| Metric | Value |
|--------|-------|
| RMSE (Monthly) | 2,480 passengers |
| Ljung-Box p-value | 0.9978 (residuals = white noise ✅) |
| Forecast Horizon | 24 months (through Dec 2026) |
| Growth Projection | **0.00% — Flat** |

---

## 🚨 Alert System

The predictor outputs a **three-tier color-coded alert** in real time:

```
Passenger Count ÷ Station Capacity × 100 = Congestion %

  0% ──────── 70% ──────── 85% ──────── 100%
  │   SAFE 🟢  │  MODERATE 🟡 │  DANGER 🔴  │
              ↑              ↑
         Warning zone    Cascade begins
```

When **DANGER** is triggered, the system automatically recommends:
- Deploy extra security staff immediately
- Activate surge pricing
- Alert station master
- Stagger entry gate timing

---

## 💰 Policy Simulation Engine

Uses a **−0.3 fare elasticity parameter** (industry standard for urban transit).

| Policy | Investment | Revenue Gain | ROI | Payback |
|--------|-----------|--------------|-----|---------|
| 💳 Smart Card Loyalty | ₹50 Lakh | ₹4.68 Cr | **836%** | 1.28 months |
| ⚡ Dynamic Peak Pricing | ₹20 Lakh | ₹2.50 Cr | **1149%** | 0.96 months |
| 🌍 Tourist Enhancement | ₹30 Lakh | ₹3.75 Cr | **1149%** | 0.96 months |

> **Why Dynamic Pricing directly addresses JICA debt:**
> DMRC's infrastructure is backed by soft loans from **JICA (Japan International Cooperation Agency)**. A 1,149% ROI model with a 29-day payback period gives DMRC a clear, data-backed path to accelerate repayment — without adding infrastructure cost.

### Live Fare Simulator
The built-in slider lets DMRC executives test any fare change in real time:

```
Fare +25% → Revenue +21.8% → Passenger change −7.5%
Projected annual revenue: ₹37.97 Cr (vs current ₹31.22 Cr)
```

---

## 🗺️ Implementation Roadmap

```
Phase 1 (0–3 months)          Phase 2 (3–12 months)         Phase 3 (12+ months)
─────────────────────          ──────────────────────         ────────────────────
✅ Dynamic Peak Pricing        ✅ Tourist Card packages        ✅ Full AI pricing network
✅ Real-time counters          ✅ Smart Card to 24 stations    ✅ Predictive maintenance
✅ Smart Card pilot (5 stn)    ✅ Live AFC data feed           ✅ Demand-based fleet
✅ Regulatory approval         ✅ Modal shift monitoring       ✅ Annual retraining
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Dashboard UI** | Streamlit, Plotly Express |
| **Deep Learning** | TensorFlow, Keras (Multivariate LSTM) |
| **Statistical Model** | Statsmodels (SARIMA) |
| **Data Processing** | Python, Pandas, NumPy, Scikit-Learn |
| **Deployment** | Streamlit Cloud |

---

## 📁 Repository Structure

```
SmartMetro-AI/
│
├── app.py                  # Main Streamlit Dashboard (UI + routing)
├── smartmetro_model.h5     # Trained LSTM weights
├── lstm_scaler.pkl         # MinMaxScaler artifacts
├── requirements.txt        # Python dependencies
│
├── assets/                 # Screenshots for README
│   ├── login.png
│   ├── eda.png
│   ├── anomaly.png
│   ├── predictor.png
│   ├── policy.png
│   └── roadmap.png
│
└── README.md
```

---

## 🚀 Run Locally

```bash
# Clone the repo
git clone https://github.com/oce-micky/SmartMetro-AI.git
cd SmartMetro-AI

# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

Then open → `http://localhost:8501`

**Demo credentials:**
- 👤 User login: any name + any ID
- 🏛️ Admin login: `admin` / `dmrc2024`

---

## 📊 Dataset

| Attribute | Detail |
|-----------|--------|
| Records | 1,50,000 trip entries |
| Period | January 2022 – December 2024 |
| Stations | 24 across Delhi NCR |
| Features | Distance, Fare, Ticket Type, Passengers, Revenue, Time Period |
| Total Revenue | ₹31.22 Crore |
| Avg Fare | ₹105.12 per trip |

---

## 🎓 About

**Divyanshi Mishra** · Roll No. 1230258170
BCA Data Science & AI · Babu Banarasi Das University (BBD University)
Academic Year 2025–26

---

<div align="center">

*Built with Python · LSTM · SARIMA · Streamlit · Plotly*

⭐ Star this repo if you found it useful!

</div>
