import sqlite3

conn = sqlite3.connect(r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS income_statement (
    year TEXT,
    revenue REAL,
    operating_profit REAL,
    net_profit REAL,
    eps REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS balance_sheet (
    year TEXT,
    total_assets REAL,
    total_equity REAL,
    total_debt REAL,
    cash REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cash_flow (
    year TEXT,
    operating_cash_flow REAL,
    investing_cash_flow REAL,
    financing_cash_flow REAL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stock_price (
    date TEXT,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    adj_close REAL,
    volume REAL
);
""")

conn.commit()
conn.close()

print("Database created successfully!")
print("Test file working")

