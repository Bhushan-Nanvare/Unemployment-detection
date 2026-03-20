
import pandas as pd
import numpy as np

class SectorAnalysis:
    """
    Computes sector-specific impacts based on macroeconomic shock scenarios.
    This is a rule-based intelligence layer, not a black-box prediction model.
    """

    # Sector Sensitivity Weights (Rule-based)
    # Higher weight = Higher vulnerability to economic shocks
    SECTOR_SENSITIVITY = {
        "Healthcare": 0.6,      # Essential, resilient
        "IT": 0.9,             # Remote-capable but investment-dependent
        "Services": 1.2,       # High human interaction, discretionary
        "Manufacturing": 1.3,  # Supply chain dependent, demand sensitive
        "Construction": 1.5    # Highly cyclical, capital intensive
    }

    # Sector Essentiality Scores (0-10)
    # Higher score = More essential, faster recovery, less volatile
    SECTOR_ESSENTIALITY = {
        "Healthcare": 9.0,
        "IT": 7.0,
        "Services": 4.0,
        "Manufacturing": 5.0,
        "Construction": 3.0
    }

    @staticmethod
    def analyze_sectors(scenario_df: pd.DataFrame, shock_intensity: float, recovery_rate: float) -> pd.DataFrame:
        """
        Computes both Relative Sector Stress Index (RSSI) and Resilience Scores.
        
        Returns:
            DataFrame with sector metrics.
        """
        
        # 1. Get Scenario Peak Unemployment
        scenario_peak = scenario_df["Scenario_Unemployment"].max()
        
        results = []
        
        # Scaling factor for RSSI (Normalized to 0-100)
        SCALING_FACTOR = 15.0 
        
        for sector, sensitivity in SectorAnalysis.SECTOR_SENSITIVITY.items():
            # --- RSSI Calculation ---
            effective_shock = max(shock_intensity, 0.05)
            stress_score = (scenario_peak * effective_shock * sensitivity * SCALING_FACTOR)
            
            # --- Resilience Calculation ---
            # Resilience = (Essentiality * 4) + (Recovery_Rate * 50) - (Shock_Intensity * 20)
            # Base resilience comes from essentiality.
            # Recovery rate boosts resilience.
            # Shock intensity lowers resilience.
            
            essentiality = SectorAnalysis.SECTOR_ESSENTIALITY.get(sector, 5.0)
            
            resilience_score = (essentiality * 6.0) + (recovery_rate * 40.0) - (shock_intensity * 30.0)
            
            # Normalize to 0-100 range (approximate clamping)
            resilience_score = max(0, min(100, resilience_score))
            
            # Badge
            if resilience_score >= 70:
                resilience_badge = "High"
            elif resilience_score >= 40:
                resilience_badge = "Medium"
            else:
                resilience_badge = "Low"

            results.append({
                "Sector": sector,
                "Sensitivity": sensitivity,
                "Essentiality": essentiality,
                "Stress_Score": round(stress_score, 2),
                "Resilience_Score": round(resilience_score, 1),
                "Resilience_Badge": resilience_badge,
                "Scenario_Peak": round(scenario_peak, 2)
            })
            
        return pd.DataFrame(results).sort_values(by="Stress_Score", ascending=False)

    # Legacy method wrapper if needed, but we will update API to use analyze_sectors
    @staticmethod
    def compute_rssi(scenario_df: pd.DataFrame, shock_intensity: float) -> pd.DataFrame:
        return SectorAnalysis.analyze_sectors(scenario_df, shock_intensity, 0.2)
