from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.event_detection import EventDetector
from src.forecasting import ForecastingEngine

# Load data
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
engine = ForecastingEngine(forecast_horizon=5)
forecast_df = engine.forecast(df)

print("Future unemployment predictions:")
print(forecast_df)
