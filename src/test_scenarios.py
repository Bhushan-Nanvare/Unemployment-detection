from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.event_detection import EventDetector
from src.forecasting import ForecastingEngine
from src.scenario_engine import ScenarioEngine

# Load and prepare data
loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()

df = Preprocessor().preprocess(df)
df = EventDetector().apply(df)

baseline = ForecastingEngine(forecast_horizon=6).forecast(df)

# Scenario 1: Baseline (no shock)
baseline["Scenario"] = "Baseline"
baseline["Scenario_Unemployment"] = baseline["Predicted_Unemployment"]

# Scenario 2: Economic Shock
shock = ScenarioEngine(
    shock_intensity=0.35,
    shock_duration=2,
    recovery_rate=0.25
).simulate(baseline)

shock["Scenario"] = "Shock"

print("\nBASELINE SCENARIO")
print(baseline[["Year", "Scenario_Unemployment"]])

print("\nSHOCK SCENARIO")
print(shock[["Year", "Scenario_Unemployment"]])
