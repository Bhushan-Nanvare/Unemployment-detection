"""
model_validator.py

Purpose:
    Provides comprehensive model validation metrics
    to assess forecast quality.
"""

import pandas as pd
import numpy as np


class ModelValidator:
    """
    Computes multiple validation metrics to assess forecast accuracy.
    """
    
    @staticmethod
    def mean_absolute_error(actual: np.ndarray, predicted: np.ndarray) -> float:
        """MAE: Average absolute difference"""
        return float(np.abs(actual - predicted).mean())
    
    @staticmethod
    def mean_absolute_percentage_error(actual: np.ndarray, predicted: np.ndarray) -> float:
        """MAPE: Average percentage error (handles 0 values)"""
        # Avoid division by zero
        mask = actual != 0
        if not mask.any():
            return 0.0
        
        mape = np.abs((actual[mask] - predicted[mask]) / actual[mask]) * 100
        return float(np.mean(mape))
    
    @staticmethod
    def root_mean_squared_error(actual: np.ndarray, predicted: np.ndarray) -> float:
        """RMSE: Square root of avg squared error (penalizes large errors)"""
        return float(np.sqrt(np.mean((actual - predicted) ** 2)))
    
    @staticmethod
    def directional_accuracy(actual: np.ndarray, predicted: np.ndarray) -> float:
        """
        Directional Accuracy: % of times model correctly predicted 
        whether unemployment would increase or decrease.
        """
        if len(actual) < 2:
            return 0.0
        
        actual_direction = np.diff(actual)
        predicted_direction = np.diff(predicted)
        
        correct = (np.sign(actual_direction) == np.sign(predicted_direction)).sum()
        accuracy = (correct / len(actual_direction)) * 100
        return float(accuracy)
    
    @staticmethod
    def compute_r_squared(actual: np.ndarray, predicted: np.ndarray) -> float:
        """
        R²: Coefficient of determination (0-1, higher is better)
        Explains how much variance the model captures.
        """
        ss_res = np.sum((actual - predicted) ** 2)
        ss_tot = np.sum((actual - np.mean(actual)) ** 2)
        
        if ss_tot == 0:
            return 0.0
        
        return float(1 - (ss_res / ss_tot))
    
    @staticmethod
    def forecast_bias(actual: np.ndarray, predicted: np.ndarray) -> float:
        """
        Forecast Bias: Average of (Predicted - Actual)
        Positive = overestimation, Negative = underestimation
        """
        return float(np.mean(predicted - actual))
    
    @staticmethod
    def get_validation_report(actual_df: pd.DataFrame, 
                              predicted_df: pd.DataFrame) -> dict:
        """
        Generates comprehensive validation report by merging
        actual historical data with predictions on overlapping years.
        """
        # Merge on Year
        merged = actual_df.merge(
            predicted_df[['Year', 'Predicted_Unemployment']], 
            on='Year', 
            how='inner'
        )
        
        if merged.empty:
            return {"error": "No overlapping years between actual and predicted"}
        
        """
        Implements rolling-origin (walk-forward) validation for unemployment forecasting.
        For each year t, fits the model using unemployment data from (t-10) to t,
        predicts unemployment for year (t+1), and compares prediction with actual (t+1).
        Computes MAE, MAPE, and R² over all rolling predictions.

        This evaluation matches real-world deployment because:
        - The model is always trained only on the most recent 10 years (no random splits).
        - Each prediction is made for the next unseen year, simulating real forecasting.
        - Prevents data leakage and fixes negative R² caused by unrealistic splits.
        """
        window = 10
        years = actual_df['Year'].values
        smoothed = actual_df['Unemployment_Smoothed'].values
        predictions = []
        actuals = []
        pred_years = []

        # Walk-forward: for each year t, fit on (t-10) to t, predict t+1
        for i in range(window, len(years)-1):
            train_years = years[i-window:i+1]
            train_values = smoothed[i-window:i+1]
            # Fit trend model (same as ForecastingEngine logic)
            x = np.arange(len(train_values))
            y = train_values
            coeffs = np.polyfit(x, y, deg=1)
            trend_model = np.poly1d(coeffs)
            # Predict for t+1
            pred_idx = len(train_values)
            pred = float(trend_model(pred_idx))
            predictions.append(pred)
            actuals.append(smoothed[i+1])
            pred_years.append(years[i+1])

        predictions = np.array(predictions)
        actuals = np.array(actuals)

        report = {
            "mae": round(ModelValidator.mean_absolute_error(actuals, predictions), 3),
            "mape": round(ModelValidator.mean_absolute_percentage_error(actuals, predictions), 2),
            "rmse": round(ModelValidator.root_mean_squared_error(actuals, predictions), 3),
            "r2_score": round(ModelValidator.compute_r_squared(actuals, predictions), 3),
            "directional_accuracy": round(ModelValidator.directional_accuracy(actuals, predictions), 1),
            "forecast_bias": round(ModelValidator.forecast_bias(actuals, predictions), 3),
            "accuracy_rating": _rate_accuracy(
                ModelValidator.mean_absolute_percentage_error(actuals, predictions)
            ),
            "years_tested": len(pred_years),
            "data": [
                {"Year": int(y), "Predicted_Unemployment": float(p), "Actual_Unemployment": float(a)}
                for y, p, a in zip(pred_years, predictions, actuals)
            ]
        }
        return report


def _rate_accuracy(mape: float) -> str:
    """Rate forecast quality based on MAPE."""
    if mape < 2:
        return "🟢 Excellent"
    elif mape < 5:
        return "🟢 Good"
    elif mape < 10:
        return "🟡 Acceptable"
    elif mape < 15:
        return "🟡 Poor"
    else:
        return "🔴 Very Poor"
