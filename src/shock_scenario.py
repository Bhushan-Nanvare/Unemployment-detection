"""
shock_scenario.py

Applies economic shock and recovery dynamics to a baseline unemployment forecast.
Shocks are temporary overlays that decay over time; they do NOT permanently
alter the long-term baseline path.

Economic rationale:
- Shocks (COVID, policy changes, recessions) have initial magnitude and fade.
- Labor markets and policy interventions eventually restore equilibrium.
- Policy support accelerates recovery (faster decay) but does not change the
  long-run baseline; it only modifies the transitional slope temporarily.
"""

import numpy as np


class ShockScenario:
    def __init__(self, shock_intensity, shock_duration, recovery_rate):
        """
        Parameters:
        - shock_intensity: initial magnitude (e.g. 0.3 = +30% spike in year 0)
        - shock_duration: legacy; used for compatibility. Decay is governed by
          recovery_rate (higher recovery → faster decay).
        - recovery_rate: speed of return to baseline (0.1–0.5). Policy support
          increases this → shock decays faster. Does NOT change long-run baseline.
        """
        self.shock_intensity = shock_intensity
        self.shock_duration = shock_duration
        self.recovery_rate = recovery_rate
        # Decay rate: fraction of shock effect remaining each year.
        # Higher recovery_rate → lower decay_rate → shock fades faster.
        # Policy support raises recovery_rate → temporary steeper path back.
        self._decay_rate = max(0.15, 1.0 - recovery_rate)

    def apply(self, baseline_df):
        """
        Apply shock as a decaying overlay on baseline. Scenario = baseline + shock_effect.
        Shock effect decays to zero over time → NO permanent distortion of long-term forecast.

        Distinction from baseline:
        - Baseline: structural forecast from trend + mean-reversion (no shock).
        - Scenario: baseline + temporary shock overlay that fades.
        """
        df = baseline_df.copy()
        base_values = df["Predicted_Unemployment"].values

        # Initial magnitude: shock adds (intensity * year-0 baseline) in year 0.
        # Economic: spike is proportional to pre-shock level (e.g. 30% of baseline).
        initial_magnitude = float(base_values[0]) * self.shock_intensity

        scenario_values = []
        for i in range(len(df)):
            base = base_values[i]
            # Shock effect decays exponentially: effect_year_i = initial * decay^i.
            # Year 0: full effect. Year 1: decay^1, etc. → long-term effect → 0.
            shock_effect = initial_magnitude * (self._decay_rate ** i)
            scenario = base + shock_effect
            scenario_values.append(max(0.0, scenario))

        df["Scenario_Unemployment"] = scenario_values
        return df
