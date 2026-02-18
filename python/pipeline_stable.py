import pandas as pd
import sqlite3
import os

BASE_PATH = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project"
RAW_PATH = BASE_PATH + r"\data_raw"
DB_PATH = BASE_PATH + r"\sql\equity.db"

# ==================================================
# CLEAN NUMERIC SERIES SAFELY
# ==================================================

def clean_series(series):
    series = series.astype(str)
    series = series.str.replace(",", "", regex=False)
    series = series.str.replace("'", "", regex=False)
    return series.astype(float)

# ==================================================
# PROCESS FINANCIAL FILE
# ==================================================

def process_financial(file_name, required_rows, rename_map):

    df = pd.read_csv(os.path.join(RAW_PATH, file_name), skiprows=2)

    df = df[df["Narration"].isin(required_rows)]

    df = df.set_index("Narration")

    # Keep only columns that start with "Mar-"
    valid_cols = [col for col in df.columns if col.startswith("Mar-")]
    df = df[valid_cols]

    df = df.T

    df.index.name = "year"
    df.reset_index(inplace=True)

    # Extract year safely
    df["year"] = df["year"].str.replace("Mar-", "", regex=False)
    df["year"] = df["year"].astype(int) + 2000

    # Remove duplicate column names safely
    df = df.loc[:, ~df.columns.duplicated()]

    # Clean numeric columns safely
    for col in df.columns:
        if col != "year":
            df[col] = clean_series(df[col])

    df.rename(columns=rename_map, inplace=True)

    return df

# ==================================================
# LOAD ALL FINANCIALS
# ==================================================

income = process_financial(
    "income_statement.csv",
    ["Sales", "Operating Profit", "Net profit", "EPS"],
    {
        "Sales": "revenue",
        "Operating Profit": "operating_profit",
        "Net profit": "net_profit",
        "EPS": "eps"
    }
)

balance = process_financial(
    "balance_sheet.csv",
    ["Total", "Borrowings"],
    {
        "Total": "total_assets",
        "Borrowings": "total_debt"
    }
)

cash = process_financial(
    "cash_flow.csv",
    ["Cash from Operating Activity", "Cash from Investing Activity"],
    {
        "Cash from Operating Activity": "operating_cash_flow",
        "Cash from Investing Activity": "investing_cash_flow"
    }
)

financial = income.merge(balance, on="year").merge(cash, on="year")

financial = financial[(financial["year"] >= 2020) & (financial["year"] <= 2024)]
financial = financial.sort_values("year")

# ==================================================
# CALCULATE RATIOS
# ==================================================

financial["revenue_growth_pct"] = financial["revenue"].pct_change() * 100
financial["operating_margin_pct"] = (financial["operating_profit"] / financial["revenue"]) * 100
financial["net_margin_pct"] = (financial["net_profit"] / financial["revenue"]) * 100
financial["free_cash_flow"] = financial["operating_cash_flow"] - financial["investing_cash_flow"]
financial["debt_to_equity"] = financial["total_debt"] / financial["total_assets"]
financial["roe_pct"] = (financial["net_profit"] / financial["total_assets"]) * 100

# ==================================================
# LOAD MARKET DATA
# ==================================================

price_files = [f for f in os.listdir(RAW_PATH) if f.startswith("tcs_") and f.endswith(".csv")]

price_list = []
for file in price_files:
    df = pd.read_csv(os.path.join(RAW_PATH, file))
    price_list.append(df)

price = pd.concat(price_list, ignore_index=True)

price["DATE"] = pd.to_datetime(price["DATE"], format="%d-%b-%Y")
price["year"] = price["DATE"].dt.year

price = price[(price["year"] >= 2020) & (price["year"] <= 2024)]

price = price.sort_values("DATE")
yearly_price = price.groupby("year").tail(1).copy()

yearly_price["year_end_price"] = clean_series(yearly_price["CLOSE"])

yearly_price = yearly_price[["year", "year_end_price"]]
yearly_price = yearly_price.sort_values("year")
yearly_price["stock_return_pct"] = yearly_price["year_end_price"].pct_change() * 100

# ==================================================
# FINAL MERGE
# ==================================================

master = financial.merge(yearly_price, on="year", how="inner")

print("\n===== MASTER DATASET =====\n")
print(master)

# SAVE TO SQLITE
conn = sqlite3.connect(DB_PATH)
master.to_sql("master_analysis", conn, if_exists="replace", index=False)
conn.close()

print("\nPipeline completed successfully.")
