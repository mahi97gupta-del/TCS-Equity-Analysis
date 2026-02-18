import pandas as pd
import sqlite3

# -----------------------------
# 1. FILE PATHS
# -----------------------------

income_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\data_raw\income_statement.csv"
db_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\sql\equity.db"

# -----------------------------
# 2. LOAD RAW FILE
# -----------------------------

df = pd.read_csv(income_path, skiprows=2)

# -----------------------------
# 3. KEEP ONLY REQUIRED ROWS
# -----------------------------

required_rows = ['Sales', 'Operating Profit', 'Net profit', 'EPS']
df = df[df['Narration'].isin(required_rows)]

# -----------------------------
# 4. KEEP ONLY REQUIRED YEARS
# -----------------------------

years_needed = ['Mar-19', 'Mar-20', 'Mar-21', 'Mar-22', 'Mar-23', 'Mar-24']
df = df[['Narration'] + years_needed]

# -----------------------------
# 5. TRANSPOSE (ROTATE TABLE)
# -----------------------------

df = df.set_index('Narration').T
df.reset_index(inplace=True)

# Rename columns
df.rename(columns={
    'index': 'year',
    'Sales': 'revenue',
    'Operating Profit': 'operating_profit',
    'Net profit': 'net_profit',
    'EPS': 'eps'
}, inplace=True)

# -----------------------------
# 6. CLEAN NUMBERS
# -----------------------------

for col in ['revenue', 'operating_profit', 'net_profit', 'eps']:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("'00", "", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Clean year column
df['year'] = df['year'].str.replace("Mar-", "", regex=False)

print("Cleaned Data:")
print(df)

# -----------------------------
# 7. INSERT INTO SQLITE
# -----------------------------

conn = sqlite3.connect(db_path)

df.to_sql("income_statement", conn, if_exists="replace", index=False)

conn.close()

print("\nIncome statement successfully imported into SQL!")

