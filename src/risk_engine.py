"""
risk_engine.py

Purpose:
    Scenario-aware forecasting adjustments and
    unemployment risk estimation.
"""

import pandas as pd
import numpy as np


class RiskEngine:
    def __init__(
        self,
        shock_dampening: float = 0.5,
        recovery_dampening: float = 0.75
    ):
        """
        Parameters:
        - shock_dampening: reduces trend influence during shock
        - recovery_dampening: partial trend during recovery
        """
        self.shock_dampening = shock_dampening
        self.recovery_dampening = recovery_dampening

    def adjust_forecast(
        self,
        historical_df: pd.DataFrame,
        forecast_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Adjusts forecast based on most recent economic regime.
        """
        last_regime = historical_df.iloc[-1]["Regime"]

        adjusted = forecast_df.copy()

        if last_regime == "Shock":
            adjusted["Predicted_Unemployment"] *= self.shock_dampening

        elif last_regime == "Recovery":
            adjusted["Predicted_Unemployment"] *= self.recovery_dampening

        # Stable → no change
        return adjusted

    def estimate_risk(
        self,
        historical_df: pd.DataFrame,
        forecast_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Estimates unemployment risk using volatility.
        """
        volatility = historical_df["YoY_Change"].std()

        forecast_df = forecast_df.copy()
        forecast_df["Uncertainty"] = volatility
        forecast_df["Lower_Bound"] = (
            forecast_df["Predicted_Unemployment"] - volatility
        )
        forecast_df["Upper_Bound"] = (
            forecast_df["Predicted_Unemployment"] + volatility
        )

        forecast_df["Risk_Level"] = np.where(
            volatility > historical_df["YoY_Change"].mean(),
            "High",
            "Moderate"
        )

        return forecast_df
