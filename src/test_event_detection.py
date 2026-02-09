from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.event_detection import EventDetector

loader = DataLoader(
    csv_path="data/raw/india_unemployment.csv",
    country="India"
)

df = loader.load_clean_data()

preprocessor = Preprocessor()
df = preprocessor.preprocess(df)

detector = EventDetector(z_threshold=2.0)
df_events = detector.apply(df)

print(df_events[["Year", "Unemployment_Rate", "YoY_Change", "Regime"]].tail(10))
