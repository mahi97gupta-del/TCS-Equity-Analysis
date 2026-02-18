import pandas as pd
import sqlite3

# ==========================================================
# BASE PATHS
# ==========================================================

base_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project"

income_path = base_path + r"\data_raw\income_statement.csv"
balance_path = base_path + r"\data_raw\balance_sheet.csv"
cashflow_path = base_path + r"\data_raw\cash_flow.csv"
db_path = base_path + r"\sql\equity.db"

years_needed = ['Mar-19', 'Mar-20', 'Mar-21', 'Mar-22', 'Mar-23', 'Mar-24']


# ==========================================================
# GENERIC CLEANING FUNCTION
# ==========================================================

def clean_statement(file_path, required_rows, rename_map):

    # Load CSV and skip first 2 rows
    df = pd.read_csv(file_path, skiprows=2)

    # Keep only required financial rows
    df = df[df['Narration'].isin(required_rows)]

    # Keep only selected years
    df = df[['Narration'] + years_needed]

    # Transpose (rotate table)
    df = df.set_index('Narration').T
    df.reset_index(inplace=True)

    # Rename columns
    df.rename(columns=rename_map, inplace=True)

    # Clean numeric columns
    for col in df.columns:
        if col != 'year':
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("'00", "", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Clean year column
    df['year'] = df['year'].str.replace("Mar-", "", regex=False)

    return df


# ==========================================================
# INCOME STATEMENT
# ==========================================================

income_required = ['Sales', 'Operating Profit', 'Net profit', 'EPS']

income_rename = {
    'index': 'year',
    'Sales': 'revenue',
    'Operating Profit': 'operating_profit',
    'Net profit': 'net_profit',
    'EPS': 'eps'
}

income_df = clean_statement(income_path, income_required, income_rename)

print("Cleaned Income Statement:")
print(income_df)


# ==========================================================
# BALANCE SHEET
# ==========================================================

balance_required = [
    'Total Assets',
    'Total Equity',
    'Borrowings',
    'Cash Equivalents'
]

balance_rename = {
    'index': 'year',
    'Total Assets': 'total_assets',
    'Total Equity': 'total_equity',
    'Borrowings': 'total_debt',
    'Cash Equivalents': 'cash'
}

balance_df = clean_statement(balance_path, balance_required, balance_rename)

print("\nCleaned Balance Sheet:")
print(balance_df)


# ==========================================================
# CASH FLOW
# ==========================================================

cashflow_required = [
    'Cash from Operating Activity',
    'Cash from Investing Activity',
    'Cash from Financing Activity'
]

cashflow_rename = {
    'index': 'year',
    'Cash from Operating Activity': 'operating_cash_flow',
    'Cash from Investing Activity': 'investing_cash_flow',
    'Cash from Financing Activity': 'financing_cash_flow'
}

cashflow_df = clean_statement(cashflow_path, cashflow_required, cashflow_rename)

print("\nCleaned Cash Flow:")
print(cashflow_df)


# ==========================================================
# INSERT INTO SQLITE DATABASE
# ==========================================================

conn = sqlite3.connect(db_path)

income_df.to_sql("income_statement", conn, if_exists="replace", index=False)
balance_df.to_sql("balance_sheet", conn, if_exists="replace", index=False)
cashflow_df.to_sql("cash_flow", conn, if_exists="replace", index=False)

conn.close()

print("\nAll financial statements successfully imported into SQL!")
