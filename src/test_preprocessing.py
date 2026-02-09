from src.data_loader import DataLoader
from src.preprocessing import Preprocessor


loader = DataLoader(
    csv_path="data/raw/india_unemployment.csv",
    country="India"
)

df = loader.load_clean_data()

preprocessor = Preprocessor(smoothing_window=3)
df_processed = preprocessor.preprocess(df)

print(df_processed.head())
print(df_processed.tail())
