from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.event_detection import EventDetector
from src.forecasting import ForecastingEngine
from src.risk_engine import RiskEngine
from src.insights import InsightsEngine

# Load data
loader = DataLoader(
    csv_path="data/raw/india_unemployment.csv",
    country="India"
)
df = loader.load_clean_data()

# Preprocess
preprocessor = Preprocessor()
df = preprocessor.preprocess(df)

# Event detection
detector = EventDetector()
df = detector.apply(df)

# Forecast
forecast_engine = ForecastingEngine(forecast_horizon=5)
forecast_df = forecast_engine.forecast(df)

# Risk
risk_engine = RiskEngine()
forecast_df = risk_engine.adjust_forecast(df, forecast_df)
forecast_df = risk_engine.estimate_risk(df, forecast_df)

# Insights
insights_engine = InsightsEngine()
insights = insights_engine.generate_insights(df, forecast_df)

print("---- INSIGHTS ----")
for i, insight in enumerate(insights, 1):
    print(f"{i}. {insight}")
