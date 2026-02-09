"""
preprocessing.py
"""

import pandas as pd


class Preprocessor:
    def __init__(self, smoothing_window: int = 3):
        self.smoothing_window = smoothing_window

    def handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["Unemployment_Rate"] = df["Unemployment_Rate"].ffill()
        df["Unemployment_Rate"] = df["Unemployment_Rate"].bfill()

        if df["Unemployment_Rate"].isna().any():
            raise ValueError("Missing values remain after fill.")

        return df

    def smooth_series(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["Unemployment_Smoothed"] = (
            df["Unemployment_Rate"]
            .rolling(window=self.smoothing_window, min_periods=1)
            .mean()
        )
        return df

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = self.handle_missing_values(df)
        df = self.smooth_series(df)
        return df
