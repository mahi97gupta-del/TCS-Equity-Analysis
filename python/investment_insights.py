import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM master_analysis", conn)
conn.close()

print("\n===== INVESTMENT ANALYSIS =====\n")

# 1️⃣ Growth Trend
avg_growth = df["revenue_growth_pct"].mean()
print("Average Revenue Growth:", round(avg_growth,2), "%")

# 2️⃣ Profitability Strength
avg_roe = df["roe_pct"].mean()
print("Average ROE:", round(avg_roe,2), "%")

# 3️⃣ Margin Stability
margin_std = df["operating_margin_pct"].std()
print("Operating Margin Stability (lower is better):", round(margin_std,2))

# 4️⃣ Debt Risk
avg_de_ratio = df["debt_to_equity"].mean()
print("Average Debt to Equity:", round(avg_de_ratio,3))

# 5️⃣ Stock Performance
avg_return = df["stock_return_pct"].mean()
print("Average Stock Return:", round(avg_return,2), "%")

# 6️⃣ Correlation Insight
corr = df.corr()
rev_corr = corr.loc["revenue_growth_pct","stock_return_pct"]
roe_corr = corr.loc["roe_pct","stock_return_pct"]

print("\nCorrelation between Revenue Growth & Stock Return:", round(rev_corr,2))
print("Correlation between ROE & Stock Return:", round(roe_corr,2))

print("\n===== INTERPRETATION =====\n")

if avg_roe > 25:
    print("✔ Strong profitability business model.")
else:
    print("⚠ Moderate profitability.")

if avg_de_ratio < 0.5:
    print("✔ Low leverage risk.")
else:
    print("⚠ High leverage risk.")

if rev_corr > 0.3:
    print("✔ Revenue growth influences stock returns.")
else:
    print("⚠ Stock return weakly linked to revenue growth.")

print("\nFinal Conclusion: Review valuation before investing.")
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM master_analysis", conn)
conn.close()

print("\n===== INVESTMENT ANALYSIS =====\n")

# 1️⃣ Growth Trend
avg_growth = df["revenue_growth_pct"].mean()
print("Average Revenue Growth:", round(avg_growth,2), "%")

# 2️⃣ Profitability Strength
avg_roe = df["roe_pct"].mean()
print("Average ROE:", round(avg_roe,2), "%")

# 3️⃣ Margin Stability
margin_std = df["operating_margin_pct"].std()
print("Operating Margin Stability (lower is better):", round(margin_std,2))

# 4️⃣ Debt Risk
avg_de_ratio = df["debt_to_equity"].mean()
print("Average Debt to Equity:", round(avg_de_ratio,3))

# 5️⃣ Stock Performance
avg_return = df["stock_return_pct"].mean()
print("Average Stock Return:", round(avg_return,2), "%")

# 6️⃣ Correlation Insight
corr = df.corr()
rev_corr = corr.loc["revenue_growth_pct","stock_return_pct"]
roe_corr = corr.loc["roe_pct","stock_return_pct"]

print("\nCorrelation between Revenue Growth & Stock Return:", round(rev_corr,2))
print("Correlation between ROE & Stock Return:", round(roe_corr,2))

print("\n===== INTERPRETATION =====\n")

if avg_roe > 25:
    print("✔ Strong profitability business model.")
else:
    print("⚠ Moderate profitability.")

if avg_de_ratio < 0.5:
    print("✔ Low leverage risk.")
else:
    print("⚠ High leverage risk.")

if rev_corr > 0.3:
    print("✔ Revenue growth influences stock returns.")
else:
    print("⚠ Stock return weakly linked to revenue growth.")

print("\nFinal Conclusion: Review valuation before investing.")
import sqlite3
import pandas as pd

DB_PATH = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db"

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM master_analysis", conn)
conn.close()

print("\n===== INVESTMENT ANALYSIS =====\n")

# 1️⃣ Growth Trend
avg_growth = df["revenue_growth_pct"].mean()
print("Average Revenue Growth:", round(avg_growth,2), "%")

# 2️⃣ Profitability Strength
avg_roe = df["roe_pct"].mean()
print("Average ROE:", round(avg_roe,2), "%")

# 3️⃣ Margin Stability
margin_std = df["operating_margin_pct"].std()
print("Operating Margin Stability (lower is better):", round(margin_std,2))

# 4️⃣ Debt Risk
avg_de_ratio = df["debt_to_equity"].mean()
print("Average Debt to Equity:", round(avg_de_ratio,3))

# 5️⃣ Stock Performance
avg_return = df["stock_return_pct"].mean()
print("Average Stock Return:", round(avg_return,2), "%")

# 6️⃣ Correlation Insight
corr = df.corr()
rev_corr = corr.loc["revenue_growth_pct","stock_return_pct"]
roe_corr = corr.loc["roe_pct","stock_return_pct"]

print("\nCorrelation between Revenue Growth & Stock Return:", round(rev_corr,2))
print("Correlation between ROE & Stock Return:", round(roe_corr,2))

print("\n===== INTERPRETATION =====\n")

if avg_roe > 25:
    print("✔ Strong profitability business model.")
else:
    print("⚠ Moderate profitability.")

if avg_de_ratio < 0.5:
    print("✔ Low leverage risk.")
else:
    print("⚠ High leverage risk.")

if rev_corr > 0.3:
    print("✔ Revenue growth influences stock returns.")
else:
    print("⚠ Stock return weakly linked to revenue growth.")

print("\nFinal Conclusion: Review valuation before investing.")
