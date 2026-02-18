import pandas as pd

file_path = r"C:\Users\mg220\OneDrive\Documents\TCS_Equity_Project\data_raw\income_statement.csv"

# Load file properly
df = pd.read_csv(file_path, skiprows=2)

# Keep only required financial rows
required = ['Sales', 'Operating Profit', 'Net profit', 'EPS']
df_filtered = df[df['Narration'].isin(required)]

print(df_filtered)
