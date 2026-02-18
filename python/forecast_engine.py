import sqlite3
import pandas as pd
import numpy as np

DB_PATH = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT year, revenue FROM master_analysis", conn)
conn.close()

df = df.sort_values("year")

# Historical CAGR
start_revenue = df.iloc[0]["revenue"]
end_revenue = df.iloc[-1]["revenue"]
years = len(df) - 1

cagr = ((end_revenue / start_revenue) ** (1 / years) - 1)

print("Historical CAGR:", round(cagr * 100, 2), "%")

# Scenario assumptions
scenarios = {
    "Bear": 0.06,
    "Base": cagr,
    "Bull": 0.15
}

latest_revenue = df.iloc[-1]["revenue"]
latest_year = df.iloc[-1]["year"]

forecast_years = 3

forecast_data = []

for scenario, growth in scenarios.items():
    revenue = latest_revenue
    
    for i in range(1, forecast_years + 1):
        forecast_year = latest_year + i
        revenue = revenue * (1 + growth)
        
        forecast_data.append({
            "Scenario": scenario,
            "Year": forecast_year,
            "Forecast_Revenue": revenue
        })

forecast_df = pd.DataFrame(forecast_data)

print("\nRevenue Forecast (2025–2027):\n")
print(forecast_df)

forecast_df.to_csv("revenue_forecast.csv", index=False)

print("\nForecast file exported: revenue_forecast.csv")
