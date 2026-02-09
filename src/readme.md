🔍 Problem Statement

Traditional unemployment forecasting models usually provide a single predicted future, assuming stable economic conditions.
However, real economies experience shocks (recessions, pandemics, policy changes), and decision-makers need to answer:

What if a severe economic shock occurs?

How quickly does unemployment recover?

How effective are policy interventions?

This project addresses that gap by enabling scenario-based forecasting and comparison, rather than just point prediction.

🎯 Key Features

✅ Baseline unemployment forecasting using recent economic trends

⚠️ Economic shock simulation (severe, mild, policy-supported recovery)

📈 Side-by-side scenario comparison

📉 Quantified impact analysis (delta vs baseline)

🌐 Backend API (FastAPI)

🖥️ Interactive UI (Streamlit)

📊 Visual charts + tables

📂 Uses official World Bank unemployment data

🧠 System Architecture
World Bank Data
      ↓
Data Loader & Preprocessing
      ↓
Baseline Forecast Engine
      ↓
Shock & Recovery Simulation
      ↓
Scenario Metrics
      ↓
FastAPI Backend
      ↓
Streamlit Frontend


This separation ensures:

Clean logic

Reusability

Easy extension

🛠️ Tech Stack
Backend

Python

FastAPI

Pandas, NumPy

Frontend

Streamlit

Requests

Interactive charts

Data Source

World Bank Open Data

Indicator:
Unemployment, total (% of total labor force)
(SL.UEM.TOTL.ZS)

📂 Project Structure
Unemployment/
│
├── data/
│   └── raw/
│       └── india_unemployment.csv
│
├── src/
│   ├── api.py
│   ├── data_loader.py
│   ├── preprocessing.py
│   ├── forecasting.py
│   ├── shock_scenario.py
│   ├── scenario_metrics.py
│
├── app.py
├── requirements.txt
└── README.md

🚀 How to Run the Application
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Start Backend (FastAPI)
uvicorn src.api:app --reload


Backend runs at:

http://127.0.0.1:8000

3️⃣ Start Frontend (Streamlit)

Open a new terminal:

streamlit run app.py


Frontend runs at:

http://localhost:8501

🧪 How the App Works

User selects two economic scenarios

Adjusts:

Shock intensity

Shock duration

Recovery rate

Clicks Compare Scenarios

App displays:

Baseline forecast

Scenario A & B forecasts

Line chart comparison

All results are computed live via the backend.

📊 Example Scenarios
Scenario	Description
Severe Shock	High unemployment spike, slow recovery
Mild Shock	Smaller disruption, faster recovery
Policy Support	Government intervention accelerates recovery
⚠️ Assumptions & Limitations

Linear trend baseline (chosen for interpretability)

Shock and recovery modeled parametrically

Does not include causal variables (GDP, inflation)

Intended as a decision-support system, not a real-time predictor

🔮 Future Enhancements

Multi-country analysis

Probabilistic forecasting

Integration with GDP & inflation

Deployment on cloud (Streamlit Cloud / AWS)

Downloadable reports

👨‍💻 Author

Bhushan Nanavare
Full-Stack & Analytics Developer
Built as a real-world analytical application using best-fit technologies.