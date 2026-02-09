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
        
        actual_vals = merged['Unemployment_Smoothed'].values
        predicted_vals = merged['Predicted_Unemployment'].values
        
        report = {
            "mae": round(ModelValidator.mean_absolute_error(actual_vals, predicted_vals), 3),
            "mape": round(ModelValidator.mean_absolute_percentage_error(actual_vals, predicted_vals), 2),
            "rmse": round(ModelValidator.root_mean_squared_error(actual_vals, predicted_vals), 3),
            "r_squared": round(ModelValidator.compute_r_squared(actual_vals, predicted_vals), 3),
            "directional_accuracy": round(ModelValidator.directional_accuracy(actual_vals, predicted_vals), 1),
            "forecast_bias": round(ModelValidator.forecast_bias(actual_vals, predicted_vals), 3),
            "accuracy_rating": _rate_accuracy(
                ModelValidator.mean_absolute_percentage_error(actual_vals, predicted_vals)
            ),
            "years_tested": len(merged),
            "data": merged.to_dict(orient="records")
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
