from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.forecasting import ForecastingEngine
from src.shock_scenario import ShockScenario

# Load & preprocess
loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()
df = Preprocessor().preprocess(df)

# Baseline forecast
baseline = ForecastingEngine(forecast_horizon=6).forecast(df)

# Scenario A: Severe shock, slow recovery
severe = ShockScenario(
    shock_intensity=0.35,
    shock_duration=2,
    recovery_rate=0.20
).apply(baseline)

severe["Scenario"] = "Severe Shock"

# Scenario B: Mild shock, fast recovery
mild = ShockScenario(
    shock_intensity=0.15,
    shock_duration=1,
    recovery_rate=0.40
).apply(baseline)

mild["Scenario"] = "Mild Shock"

# Print comparison
print("\n=== BASELINE ===")
print(baseline[["Year", "Predicted_Unemployment"]])

print("\n=== SEVERE SHOCK SCENARIO ===")
print(severe[["Year", "Scenario_Unemployment"]])

print("\n=== MILD SHOCK SCENARIO ===")
print(mild[["Year", "Scenario_Unemployment"]])
