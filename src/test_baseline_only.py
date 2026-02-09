from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.forecasting import ForecastingEngine

# Load data
loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()

# Preprocess
df = Preprocessor().preprocess(df)

# Baseline forecast
engine = ForecastingEngine(forecast_horizon=5)
baseline = engine.forecast(df)

print("BASELINE FORECAST (NO SCENARIOS):")
print(baseline)
