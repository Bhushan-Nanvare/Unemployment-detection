from pathlib import Path
from data_loader import DataLoader

PROJECT_ROOT = Path(__file__).resolve().parent.parent

loader = DataLoader(
    csv_path=PROJECT_ROOT / "data" / "raw" / "india_unemployment.csv",
    country="India"
)

df = loader.load_clean_data()

print(df.head())
print(df.tail())
print("Rows:", len(df))
