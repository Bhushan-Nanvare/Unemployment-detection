from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.forecasting import ForecastingEngine
from src.shock_scenario import ShockScenario

# Load & preprocess
loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()
df = Preprocessor().preprocess(df)

# Baseline forecast
baseline = ForecastingEngine(forecast_horizon=5).forecast(df)

# Apply shock (25%)
shock = ShockScenario(shock_intensity=0.25)
shock_df = shock.apply(baseline)

print("BASELINE vs SHOCK")
print(shock_df[["Year", "Predicted_Unemployment", "Shock_Unemployment"]])
