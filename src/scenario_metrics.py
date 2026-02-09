"""
scenario_metrics.py

Purpose:
    Quantify scenario impact relative to baseline.
"""

import pandas as pd


class ScenarioMetrics:
    @staticmethod
    def compute_delta(
        baseline_df: pd.DataFrame,
        scenario_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Computes difference between scenario and baseline,
        on a year-by-year basis.
        """
        df = baseline_df.copy()

        df["Scenario_Unemployment"] = scenario_df["Scenario_Unemployment"]
        df["Delta"] = (
            df["Scenario_Unemployment"] - df["Predicted_Unemployment"]
        )

        return df

    @staticmethod
    def compute_indices(
        baseline_df: pd.DataFrame,
        scenario_df: pd.DataFrame,
        policy_name: str | None = None,
        policy_cost_label: str | None = None,
    ) -> dict:
        """
        Computes high-level summary indices for a scenario, intended
        for narrative reporting in the UI.

        The indices are intentionally simple and transparent:

        - Unemployment Stress Index (USI):
          Combines the peak deviation from baseline and the duration
          of years where unemployment is above baseline.

        - Policy Cushion Score (PCS):
          Measures by how many percentage points the policy scenario
          reduces (or amplifies) the peak unemployment relative to
          a no-policy baseline. Positive values indicate cushioning.

        - Cost Effectiveness Rating:
          Qualitative rating combining PCS with the self-declared
          relative fiscal cost of the policy.
        """
        merged = baseline_df.copy()
        merged["Scenario_Unemployment"] = scenario_df["Scenario_Unemployment"]

        merged["Delta"] = (
            merged["Scenario_Unemployment"] - merged["Predicted_Unemployment"]
        )

        peak_delta = float(merged["Delta"].max())
        years_above = int((merged["Delta"] > 0).sum())

        unemployment_stress_index = round(
            abs(peak_delta) * 10.0 + years_above, 2
        )

        peak_baseline = float(merged["Predicted_Unemployment"].max())
        peak_scenario = float(merged["Scenario_Unemployment"].max())
        policy_cushion_score = round(peak_baseline - peak_scenario, 2)

        # Qualitative cost-effectiveness tag
        cost = (policy_cost_label or "None").lower()
        if cost == "none":
            cost_effectiveness = "Not applicable"
        elif policy_cushion_score <= 0:
            cost_effectiveness = "Low"
        elif cost == "low":
            cost_effectiveness = "High"
        elif cost == "medium":
            cost_effectiveness = "Moderate"
        else:
            cost_effectiveness = "Moderate to Low"

        return {
            "policy_name": policy_name or "None",
            "policy_cost": policy_cost_label or "None",
            "unemployment_stress_index": unemployment_stress_index,
            "policy_cushion_score": policy_cushion_score,
            "peak_delta": round(peak_delta, 2),
            "years_above_baseline": years_above,
            "cost_effectiveness": cost_effectiveness,
        }

    @staticmethod
    def compute_rqi(scenario_df: pd.DataFrame, recovery_rate: float) -> dict:
        """
        Computes Recovery Quality Index (RQI).
        
        Classifies recovery as:
        - Fast & Stable
        - Fast but Fragile
        - Slow but Stable
        - Poor Recovery
        """
        # Calculate Volatility (Standard Deviation of year-over-year change)
        series = scenario_df["Scenario_Unemployment"]
        # Use simple standard deviation of the series itself or its changes?
        # "Smoothness (volatility)" usually implies volatility of changes.
        volatility = series.diff().std()
        if pd.isna(volatility):
            volatility = 0.0
            
        # Classification Thresholds
        # Recovery Rate: > 0.35 considered Fast (range is 0.1 to 0.6)
        # Volatility: < 0.5 considered Stable (heuristic)
        
        is_fast = recovery_rate >= 0.35
        is_stable = volatility < 0.5
        
        if is_fast and is_stable:
            label = "Fast & Stable"
        elif is_fast and not is_stable:
            label = "Fast but Fragile"
        elif not is_fast and is_stable:
            label = "Slow but Stable"
        else:
            label = "Poor Recovery"
            
        return {
            "rqi_label": label,
            "volatility": round(volatility, 3),
            "recovery_speed_rating": "Fast" if is_fast else "Slow"
        }
