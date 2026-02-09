
import pandas as pd

class StoryGenerator:
    """
    Converts data into a year-by-year narrative (Story Mode).
    """

    @staticmethod
    def generate_story(scenario_df: pd.DataFrame, baseline_df: pd.DataFrame) -> list:
        """
        Returns a list of story events: {"year": 2025, "event": "..."}
        """
        story = []
        
        # Merge to compare
        merged = pd.merge(
            scenario_df[["Year", "Scenario_Unemployment"]],
            baseline_df[["Year", "Predicted_Unemployment"]],
            on="Year"
        )
        
        # Calculate Delta
        merged["Delta"] = merged["Scenario_Unemployment"] - merged["Predicted_Unemployment"]
        
        # Find key points
        peak_idx = merged["Scenario_Unemployment"].idxmax()
        peak_year = merged.loc[peak_idx, "Year"]
        peak_val = merged.loc[peak_idx, "Scenario_Unemployment"]
        
        # Iterate through years to build narrative
        for i, row in merged.iterrows():
            year = int(row["Year"])
            val = row["Scenario_Unemployment"]
            delta = row["Delta"]
            
            event_text = ""
            icon = "📅"
            
            if i == 0:
                event_text = f"Simulation begins. Unemployment starts at {round(val, 2)}%."
                icon = "🏁"
            elif year == peak_year:
                event_text = f"CRITICAL: Peak unemployment reached at {round(val, 2)}%. The labor market is under maximum stress."
                icon = "🔥"
            elif delta > 0.5:
                # Rising or high
                prev_val = merged.loc[i-1, "Scenario_Unemployment"]
                if val > prev_val:
                    event_text = "Unemployment continues to rise as shock effects deepen."
                    icon = "📈"
                else:
                    event_text = "Recovery is underway, but rates remain elevated above baseline."
                    icon = "📉"
            elif 0 < delta <= 0.5:
                event_text = "The market is stabilizing, approaching baseline levels."
                icon = "⛅"
            else:
                event_text = "Full recovery achieved. Unemployment tracks with baseline projections."
                icon = "✅"
                
            story.append({
                "year": year,
                "icon": icon,
                "description": event_text,
                "value": round(val, 2)
            })
            
        return story
