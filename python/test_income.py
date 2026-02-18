import pandas as pd

file_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\data_raw\income_statement.csv"

# Skip first 2 rows
df = pd.read_csv(file_path, skiprows=2)

print(df.head())
