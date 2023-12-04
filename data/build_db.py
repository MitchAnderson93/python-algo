import pandas as pd
import json
from datetime import datetime
import os
import sqlite3

# metrics shared lib
from lib.metrics import calculate_metrics

# Check if SQLite database exists, and delete if so
db_path = './db.sqlite'
if os.path.exists(db_path):
    os.remove(db_path)

# Create a new SQLite database
conn = sqlite3.connect(db_path)

# Read the ASX listed companies data into a DataFrame
asx_data = pd.read_csv("./csv/listed.csv")

# Write the entire listed.csv file to the SQLite db in a table called 'all'
asx_data.to_sql('asx', conn, if_exists='replace')

# Get the current date in YYYYMMDD format
current_date = datetime.now().strftime("%Y%m%d")

# Create a folder path with the date
folder_path = f'./matched-lvr/{current_date}/'

# Create the folder if it doesn't exist
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Read the approved securities data into a DataFrame
margin_loan_data = pd.read_csv("./csv/lvr.csv")

# Merge the two DataFrames on the 'code' column
merged_df = pd.merge(asx_data, margin_loan_data, on='code', how='inner')

# Print the number of matched and unmatched records
print(f"Number of matched records: {len(merged_df)}")
print(f"Number of unmatched records: {len(asx_data) - len(merged_df)}")

# Ask user for confirmation
user_input = input("Do you want to proceed with fetching stock metrics? This will create a database (yes/no): ")

if user_input.lower() == 'yes':
    for idx, row in merged_df.iterrows():
        stock_code = row['code'] + '.AX'
        metrics = calculate_metrics(stock_code)
        merged_df.at[idx, 'RSI14'] = metrics['RSI14']
        merged_df.at[idx, 'SMA20'] = metrics['SMA20']
        merged_df.at[idx, 'SMA50'] = metrics['SMA50']
        merged_df.at[idx, 'SMA200'] = metrics['SMA200']
        merged_df.at[idx, 'dividend_yield'] = metrics['dividend_yield']
        merged_df.at[idx, 'ATH'] = metrics['ATH']
        merged_df.at[idx, 'ATL'] = metrics['ATL']
        merged_df.at[idx, 'current_price'] = metrics['current_price']

    # Write the matched DataFrame to the SQLite db in a table called 'LVR'
    merged_df.to_sql('LVR', conn, if_exists='replace')

    # Close the SQLite database connection
    conn.close()

    # Log the matched data into a JSON file
    matched_log_data = merged_df.to_dict(orient='records')
    with open(f'{folder_path}matched_lvr_{current_date}.json', 'w') as f:
        json.dump(matched_log_data, f)
