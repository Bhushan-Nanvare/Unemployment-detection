"""
shock_scenario.py

Applies economic shock and recovery dynamics
to a baseline unemployment forecast.
"""


class ShockScenario:
    def __init__(self, shock_intensity, shock_duration, recovery_rate):
        self.shock_intensity = shock_intensity
        self.shock_duration = shock_duration
        self.recovery_rate = recovery_rate

    def apply(self, baseline_df):
        """
        Apply economic shock and recovery to baseline forecast.
        """
        df = baseline_df.copy()
        df["Scenario_Unemployment"] = df["Predicted_Unemployment"]

        for i in range(len(df)):
            # Year 0: no previous value
            if i == 0:
                df.loc[i, "Scenario_Unemployment"] = df.loc[
                    i, "Predicted_Unemployment"
                ]
                continue

            prev = df.loc[i - 1, "Scenario_Unemployment"]
            base = df.loc[i, "Predicted_Unemployment"]

            # Shock period
            if i < self.shock_duration:
                shock_effect = base * self.shock_intensity
                df.loc[i, "Scenario_Unemployment"] = base + shock_effect

            # Recovery period
            else:
                recovery_gap = prev - base
                df.loc[i, "Scenario_Unemployment"] = (
                    prev - self.recovery_rate * recovery_gap
                )

        return df
