"""
scenario_engine.py

Purpose:
    Simulate alternative unemployment futures under
    explicit economic scenarios.

This is NOT prediction.
This is counterfactual simulation.
"""

import pandas as pd
import numpy as np


class ScenarioEngine:
    def __init__(
        self,
        shock_intensity: float,
        shock_duration: int,
        recovery_rate: float
    ):
        """
        Parameters:
        - shock_intensity: % increase during shock (e.g. 0.3 = +30%)
        - shock_duration: number of years shock lasts
        - recovery_rate: speed of recovery (0.1–0.5 realistic)
        """
        self.shock_intensity = shock_intensity
        self.shock_duration = shock_duration
        self.recovery_rate = recovery_rate

    def simulate(
        self,
        baseline_forecast: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Simulates scenario-based unemployment path.
        """
        df = baseline_forecast.copy()
        df["Scenario_Unemployment"] = df["Predicted_Unemployment"]

        # Apply shock
        for i in range(min(self.shock_duration, len(df))):
            df.loc[i, "Scenario_Unemployment"] *= (1 + self.shock_intensity)

        # Recovery phase
        for i in range(self.shock_duration, len(df)):
            prev = df.loc[i - 1, "Scenario_Unemployment"]
            baseline = df.loc[i, "Predicted_Unemployment"]

            df.loc[i, "Scenario_Unemployment"] = (
                prev - self.recovery_rate * (prev - baseline)
            )

        return df
