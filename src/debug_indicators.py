import pandas as pd

df = pd.read_csv("data/raw/india_unemployment.csv", skiprows=4)

print("UNIQUE INDICATOR CODES IN FILE:")
print(df["Indicator Code"].unique())

print("\nUNIQUE INDICATOR NAMES:")
print(df["Indicator Name"].unique())
