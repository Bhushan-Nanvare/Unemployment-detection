from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.forecasting import ForecastingEngine
from src.shock_scenario import ShockScenario

# Load & preprocess
loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()
df = Preprocessor().preprocess(df)

# Baseline
baseline = ForecastingEngine(forecast_horizon=6).forecast(df)

# Severe shock (no policy)
no_policy = ShockScenario(
    shock_intensity=0.35,
    shock_duration=2,
    recovery_rate=0.20
).apply(baseline)

# Policy support scenario (faster recovery)
policy_support = ShockScenario(
    shock_intensity=0.35,
    shock_duration=2,
    recovery_rate=0.45   # faster recovery
).apply(baseline)

print("\nNO POLICY SUPPORT")
print(no_policy[["Year", "Scenario_Unemployment"]])

print("\nWITH POLICY SUPPORT")
print(policy_support[["Year", "Scenario_Unemployment"]])
