"""
scenario_engine.py

Purpose:
    Simulate alternative unemployment futures under explicit economic scenarios.
    This is counterfactual simulation, NOT prediction.

Shock model: initial magnitude + decay. Shocks do NOT permanently distort
the long-term baseline; they overlay and fade.
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
        - shock_intensity: initial magnitude (e.g. 0.3 = +30% spike in year 0)
        - shock_duration: legacy; decay is governed by recovery_rate
        - recovery_rate: speed of return to baseline; policy support increases this
        """
        self.shock_intensity = shock_intensity
        self.shock_duration = shock_duration
        self.recovery_rate = recovery_rate
        self._decay_rate = max(0.15, 1.0 - recovery_rate)

    def simulate(self, baseline_forecast: pd.DataFrame) -> pd.DataFrame:
        """
        Scenario = baseline + decaying shock overlay. Long-term → baseline.
        """
        df = baseline_forecast.copy()
        base_values = df["Predicted_Unemployment"].values
        initial_magnitude = float(base_values[0]) * self.shock_intensity

        scenario_values = []
        for i in range(len(df)):
            shock_effect = initial_magnitude * (self._decay_rate ** i)
            scenario_values.append(max(0.0, base_values[i] + shock_effect))
        df["Scenario_Unemployment"] = scenario_values
        return df
