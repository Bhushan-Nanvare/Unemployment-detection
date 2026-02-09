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

# Shock + recovery scenario
scenario = ShockScenario(
    shock_intensity=0.30,   # 30% shock
    shock_duration=2,       # lasts 2 years
    recovery_rate=0.25      # gradual recovery
)

result = scenario.apply(baseline)

print(result[[
    "Year",
    "Predicted_Unemployment",
    "Scenario_Unemployment"
]])
