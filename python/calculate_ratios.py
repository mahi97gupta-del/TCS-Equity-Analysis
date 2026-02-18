import pandas as pd
import sqlite3

# ==========================================================
# DATABASE PATH
# ==========================================================

db_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db"

conn = sqlite3.connect(db_path)

# ==========================================================
# LOAD TABLES
# ==========================================================

income = pd.read_sql_query("SELECT * FROM income_statement", conn)
balance_raw = pd.read_sql_query("SELECT * FROM balance_sheet", conn)
cashflow = pd.read_sql_query("SELECT * FROM cash_flow", conn)

conn.close()

# ==========================================================
# REBUILD BALANCE SHEET PROPERLY
# ==========================================================

# Load raw CSV directly to compute equity properly
balance_csv_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\data_raw\balance_sheet.csv"

balance_csv = pd.read_csv(balance_csv_path, skiprows=2)

years_needed = ['Mar-19', 'Mar-20', 'Mar-21', 'Mar-22', 'Mar-23', 'Mar-24']

balance_csv = balance_csv[['Narration'] + years_needed]

# Extract required rows
equity_capital = balance_csv[balance_csv['Narration'] == 'Equity Share Capital']
reserves = balance_csv[balance_csv['Narration'] == 'Reserves']
borrowings = balance_csv[balance_csv['Narration'] == 'Borrowings']

# Convert wide to long
equity_capital = equity_capital.set_index('Narration').T
reserves = reserves.set_index('Narration').T
borrowings = borrowings.set_index('Narration').T

# Clean numbers function
def clean_series(series):
    return (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("'00", "", regex=False)
        .astype(float)
    )

equity_capital = clean_series(equity_capital.iloc[:,0])
reserves = clean_series(reserves.iloc[:,0])
borrowings = clean_series(borrowings.iloc[:,0])

balance = pd.DataFrame({
    "year": equity_capital.index.str.replace("Mar-", ""),
    "total_equity": equity_capital.values + reserves.values,
    "total_debt": borrowings.values
})

# ==========================================================
# MERGE ALL TABLES
# ==========================================================

df = income.merge(balance, on="year").merge(cashflow, on="year")

df = df.sort_values("year")

# ==========================================================
# CALCULATE RATIOS
# ==========================================================

df["revenue_growth_pct"] = df["revenue"].pct_change() * 100
df["operating_margin_pct"] = (df["operating_profit"] / df["revenue"]) * 100
df["net_margin_pct"] = (df["net_profit"] / df["revenue"]) * 100
df["roe_pct"] = (df["net_profit"] / df["total_equity"]) * 100
df["debt_to_equity"] = df["total_debt"] / df["total_equity"]
df["free_cash_flow"] = df["operating_cash_flow"] - df["investing_cash_flow"]

final_df = df[[
    "year",
    "revenue",
    "revenue_growth_pct",
    "operating_margin_pct",
    "net_margin_pct",
    "roe_pct",
    "debt_to_equity",
    "free_cash_flow"
]]

print("\nFinancial Ratios:")
print(final_df)

# Save to SQL
conn = sqlite3.connect(db_path)
final_df.to_sql("financial_ratios", conn, if_exists="replace", index=False)
conn.close()

print("\nFinancial ratios successfully saved to SQL!")
