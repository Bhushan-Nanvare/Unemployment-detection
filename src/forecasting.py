"""
forecasting.py

Purpose:
    Scenario-aware unemployment forecasting engine.
    Produces real numeric forecasts using historical trends.
    Supports multiple forecasting methods: Linear, Exponential, ARIMA-inspired.
"""

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


class ForecastingEngine:
    def __init__(self, forecast_horizon: int = 5, method: str = "exponential_smoothing"):
        """
        Parameters:
        - forecast_horizon: number of future years to predict
        - method: 'linear', 'exponential_smoothing', 'arima_inspired', or 'ensemble'
        """
        self.forecast_horizon = forecast_horizon
        self.method = method

    def _fit_trend(self, df: pd.DataFrame) -> np.poly1d:
        """
        Fits a linear trend using ONLY recent years
        to avoid unrealistic long-term extrapolation.
        """
        # Use last N years only (recent regime)
        window = 10
        recent_df = df.tail(window)

        x = np.arange(len(recent_df))
        y = recent_df["Unemployment_Smoothed"].values

        coeffs = np.polyfit(x, y, deg=1)
        trend_model = np.poly1d(coeffs)

        return trend_model

    def _exponential_smoothing(self, df: pd.DataFrame) -> list:
        """
        Simple exponential smoothing for more responsive forecasts.
        """
        series = df["Unemployment_Smoothed"].values
        alpha = 0.3  # smoothing factor (0.2-0.4 for year-to-year data)
        
        # Calculate smoothed values
        smoothed = [series[0]]
        for i in range(1, len(series)):
            smoothed.append(alpha * series[i] + (1 - alpha) * smoothed[i-1])
        
        # Forecast future values
        last_smoothed = smoothed[-1]
        trend = (smoothed[-1] - smoothed[-min(3, len(smoothed))]) / min(3, len(smoothed))
        
        predictions = []
        for i in range(self.forecast_horizon):
            predictions.append(last_smoothed + trend * (i + 1))
        
        return predictions

    def _arima_inspired(self, df: pd.DataFrame) -> list:
        """
        Simple ARIMA-inspired approach: trend + mean reversion.
        """
        series = df["Unemployment_Smoothed"].values
        
        # Trend component (recent change)
        trend = series[-1] - series[-min(5, len(series))]
        
        # Mean reversion component (pull towards historical mean)
        historical_mean = series.mean()
        last_value = series[-1]
        
        predictions = []
        value = last_value
        for i in range(self.forecast_horizon):
            # Mix trend with mean reversion
            reversion_factor = (i + 1) / (self.forecast_horizon + 3)
            value = value + trend * 0.3 - (value - historical_mean) * 0.1 * reversion_factor
            predictions.append(max(0, value))  # Prevent negative unemployment
        
        return predictions

    def _ensemble_forecast(self, df: pd.DataFrame) -> list:
        """
        Combines multiple methods for robust predictions.
        """
        linear_preds = self._forecast_linear(df)
        exp_preds = self._exponential_smoothing(df)
        arima_preds = self._arima_inspired(df)
        
        # Average the three methods
        ensemble = [
            (linear_preds[i] + exp_preds[i] + arima_preds[i]) / 3
            for i in range(self.forecast_horizon)
        ]
        
        return ensemble

    def _forecast_linear(self, df: pd.DataFrame) -> list:
        """Helper to get linear forecast as list."""
        trend_model = self._fit_trend(df)
        window = 10
        start_idx = window
        future_idx = np.arange(start_idx, start_idx + self.forecast_horizon)
        return trend_model(future_idx).tolist()

    def forecast(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates future unemployment forecasts using selected method.
        """
        df = df.copy()

        last_year = int(df["Year"].max())

        # Select forecasting method
        if self.method == "linear":
            predictions = self._forecast_linear(df)
        elif self.method == "exponential_smoothing":
            predictions = self._exponential_smoothing(df)
        elif self.method == "arima_inspired":
            predictions = self._arima_inspired(df)
        elif self.method == "ensemble":
            predictions = self._ensemble_forecast(df)
        else:
            # Default to ensemble (most robust)
            predictions = self._ensemble_forecast(df)

        future_years = np.arange(
            last_year + 1,
            last_year + 1 + self.forecast_horizon
        )

        forecast_df = pd.DataFrame({
            "Year": future_years,
            "Predicted_Unemployment": predictions
        })

        return forecast_df
