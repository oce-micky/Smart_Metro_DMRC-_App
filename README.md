# SmartMetro AI — Real-Time Congestion Predictor & Revenue Optimization Pipeline

An end-to-end data science and deep learning pipeline designed to optimize scheduling, forecast ridership baselines, and mitigate station-level overcrowding across the Delhi Metro Rail Corporation (DMRC) network.

##  Live Deployment
**https://smartmetrodmrc-app-rxcmv2ttkkk7cdefksjcpp.streamlit.app/**

---

##  Tech Stack & Architecture
* **Frontend UI & Presentation:** Streamlit, Plotly Express
* **Deep Learning Engine (The Brain):** TensorFlow, Keras (Multivariate LSTM)
* **Statistical Forecasting:** Statsmodels (SARIMA)
* **Data Processing Backend:** Python, Pandas, NumPy, Scikit-Learn

---

##  Key Features

1. **Real-Time Congestion Inference (LSTM Backend)**
   * Utilizes a Multivariate Long Short-Term Memory (LSTM) neural network with dual stacked layers and a `0.2` Dropout mechanism.
   * Processes data through a 14-day sliding window to output high-accuracy passenger volume predictions based on temporal and environmental triggers.
   
2. **Color-Coded Operator Alert System**
   * Automatically standardizes raw predicted passenger counts against physical station engineering capacities (e.g., Rajiv Chowk capped at 500).
   * Generates instant live UI safety states: **Safe (Green < 70%)**, **Warning (Yellow 70%-85%)**, and **Critical (Red > 85%)**.

3. **24-Month Baseline Forecasting**
   * Implements a `SARIMA(1,1,1)x(1,1,1,12)` time-series model to project baseline commuter volume trends through December 2026.

4. **Dynamic Policy Simulation Framework**
   * Incorporates an econometric policy engine utilizing a `-0.3` price elasticity parameter.
   * Proves an actionable **1,149% ROI** for implementing Dynamic Peak Hour Surge Pricing protocols to curb crowding and increase non-fare yields.

---

##  Repository Structure
```text
├── app1.py                # Main Streamlit Dashboard Application (The Skin)
├── smartmetro_model.h5   # Trained LSTM Neural Network Weights (The Brain)
├── lstm_scaler.pkl       # Serialized MinMaxScaler artifacts
├── requirements.txt      # Active Python dependencies for deployment
└── README.md             # Project documentation
