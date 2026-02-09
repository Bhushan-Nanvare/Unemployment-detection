from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.event_detection import EventDetector
from src.forecasting import ForecastingEngine
from src.risk_engine import RiskEngine

# Load
loader = DataLoader(
    csv_path="data/raw/india_unemployment.csv",
    country="India"
)
df = loader.load_clean_data()

# Preprocess
preprocessor = Preprocessor()
df = preprocessor.preprocess(df)

# Detect events
detector = EventDetector()
df = detector.apply(df)

# Forecast
forecast_engine = ForecastingEngine(forecast_horizon=5)
forecast_df = forecast_engine.forecast(df)

# Scenario-aware risk adjustment
risk_engine = RiskEngine()
adjusted_forecast = risk_engine.adjust_forecast(df, forecast_df)
final_forecast = risk_engine.estimate_risk(df, adjusted_forecast)

print(final_forecast)
