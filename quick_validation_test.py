#!/usr/bin/env python
"""
quick_validation_test.py

Run this to validate your unemployment forecasting model!
Usage: python quick_validation_test.py
"""

import requests
import json
import pandas as pd
from src.data_loader import DataLoader
from src.preprocessing import Preprocessor
from src.forecasting import ForecastingEngine
from src.model_validator import ModelValidator


def main():
    print("=" * 60)
    print("🔬 UNEMPLOYMENT FORECASTING MODEL VALIDATION")
    print("=" * 60)
    
    # ===== LOCAL VALIDATION =====
    print("\n📊 Loading India unemployment data...")
    loader = DataLoader("data/raw/india_unemployment.csv", "India")
    df = loader.load_clean_data()
    df = Preprocessor().preprocess(df)
    
    print(f"✅ Data loaded: {len(df)} years available")
    print(f"   Year range: {df['Year'].min():.0f} - {df['Year'].max():.0f}")
    print(f"   Current unemployment rate: {df['Unemployment_Smoothed'].iloc[-1]:.2f}%")
    
    # ===== TEST DIFFERENT FORECASTING METHODS =====
    print("\n" + "=" * 60)
    print("📈 COMPARING FORECASTING METHODS")
    print("=" * 60)
    
    methods = ["linear", "exponential_smoothing", "arima_inspired", "ensemble"]
    results_summary = []
    
    # Split: 40% train, 60% test
    split_idx = int(len(df) * 0.4)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    print(f"\nTrain period: {train_df['Year'].min():.0f} - {train_df['Year'].max():.0f}")
    print(f"Test period:  {test_df['Year'].min():.0f} - {test_df['Year'].max():.0f}")
    
    for method in methods:
        print(f"\n🔹 Testing {method.upper()}...")
        
        try:
            engine = ForecastingEngine(
                forecast_horizon=len(test_df),
                method=method
            )
            forecast_df = engine.forecast(train_df)
            
            # Validate
            report = ModelValidator.get_validation_report(test_df, forecast_df)
            
            if "error" in report:
                print(f"   ❌ Error: {report['error']}")
                continue
            
            # Print results
            print(f"   ✅ MAE:  {report['mae']:.3f}%")
            print(f"   ✅ MAPE: {report['mape']:.2f}%")
            print(f"   ✅ RMSE: {report['rmse']:.3f}%")
            print(f"   ✅ R²:   {report['r_squared']:.3f}")
            print(f"   ✅ Dir. Accuracy: {report['directional_accuracy']:.1f}%")
            print(f"   ✅ Bias: {report['forecast_bias']:+.3f}%")
            print(f"   💡 Rating: {report['accuracy_rating']}")
            
            results_summary.append({
                "Method": method,
                "MAPE": report['mape'],
                "R²": report['r_squared'],
                "Rating": report['accuracy_rating']
            })
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    # ===== SUMMARY TABLE =====
    print("\n" + "=" * 60)
    print("📊 SUMMARY COMPARISON")
    print("=" * 60)
    
    if results_summary:
        summary_df = pd.DataFrame(results_summary)
        summary_df = summary_df.sort_values('MAPE')
        print("\n" + summary_df.to_string(index=False))
        
        best_method = summary_df.iloc[0]
        print(f"\n🏆 BEST METHOD: {best_method['Method'].upper()}")
        print(f"   MAPE: {best_method['MAPE']:.2f}%")
    
    # ===== API VALIDATION =====
    print("\n" + "=" * 60)
    print("🌐 TESTING VALIDATION API ENDPOINT")
    print("=" * 60)
    
    try:
        print("\nCalling GET http://localhost:8000/validate")
        response = requests.get("http://localhost:8000/validate", timeout=10)
        
        if response.status_code == 200:
            api_report = response.json()
            print("✅ API Response received!")
            print(f"   MAE:  {api_report.get('mae')}%")
            print(f"   MAPE: {api_report.get('mape')}%")
            print(f"   R²:   {api_report.get('r_squared')}")
            print(f"   Rating: {api_report.get('accuracy_rating')}")
        else:
            print(f"❌ API Error: {response.status_code}")
    
    except requests.ConnectionError:
        print("❌ Could not connect to API. Is it running?")
        print("   Start it with: python -m uvicorn src.api:app --host 127.0.0.1 --port 8000")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    
    # ===== RECOMMENDATIONS =====
    print("\n" + "=" * 60)
    print("💡 RECOMMENDATIONS")
    print("=" * 60)
    
    if results_summary:
        best = summary_df.iloc[0]
        
        if best['MAPE'] < 5:
            print(f"""
✅ Your forecasting is performing WELL!
   - {best['Method'].upper()} method achieves {best['MAPE']:.2f}% MAPE
   - This is within acceptable range for economic forecasting
   - Consider using this method for production forecasts
""")
        else:
            print(f"""
⚠️  Your forecasting has room for improvement:
   - Current best MAPE: {best['MAPE']:.2f}%
   - Ensemble method provides more stable predictions
   - Consider adding external variables (GDP, inflation, etc.)
   - More training data could improve accuracy
""")
    
    print("\n" + "=" * 60)
    print("✨ Validation complete! See IMPROVEMENTS.md for next steps.")
    print("=" * 60)


if __name__ == "__main__":
    main()
