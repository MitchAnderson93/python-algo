import pandas as pd
import sqlite3
from lib.metrics import calculate_metrics 

# Connect to the SQLite database
conn = sqlite3.connect('./db.sqlite')

# Read the 'all' table into a DataFrame
asx_data_all = pd.read_sql('SELECT * FROM asx', conn)

# Loop through each row and update metrics
for idx, row in asx_data_all.iterrows():
    stock_code = row['code'] + '.AX'
    print(stock_code)
    metrics = calculate_metrics(stock_code)
    if not metrics:
        print(f"Skipping {stock_code} due to no data.")
        continue
    for metric, value in metrics.items():
        asx_data_all.at[idx, metric] = value

# Write the updated DataFrame back to the SQLite 'all' table
asx_data_all.to_sql('asx', conn, if_exists='replace', index=False)

# Close the SQLite database connection
conn.close()