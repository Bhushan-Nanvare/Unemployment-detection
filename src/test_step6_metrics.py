from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.forecasting import ForecastingEngine
from src.shock_scenario import ShockScenario
from src.scenario_metrics import ScenarioMetrics

# Load & preprocess
loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()
df = Preprocessor().preprocess(df)

# Baseline
baseline = ForecastingEngine(forecast_horizon=6).forecast(df)

# Severe shock
severe = ShockScenario(
    shock_intensity=0.35,
    shock_duration=2,
    recovery_rate=0.20
).apply(baseline)

# Compute delta
metrics = ScenarioMetrics.compute_delta(baseline, severe)

print(metrics[["Year", "Predicted_Unemployment", "Scenario_Unemployment", "Delta"]])
