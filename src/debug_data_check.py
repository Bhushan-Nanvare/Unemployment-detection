from src.data_loader import DataLoader
from src.preprocessing import Preprocessor

loader = DataLoader("data/raw/india_unemployment.csv", "India")
df = loader.load_clean_data()

print("RAW DATA (LAST 10 ROWS):")
print(df.tail(10))

df = Preprocessor().preprocess(df)

print("\nSMOOTHED DATA (LAST 10 ROWS):")
print(df[["Year", "Unemployment_Rate", "Unemployment_Smoothed"]].tail(10))

print("\nBASIC STATS:")
print(df[["Unemployment_Rate", "Unemployment_Smoothed"]].describe())
