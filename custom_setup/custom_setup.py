'''
This is an example of a custom_setup.py set of tasks and a sub /job for context specific use. 
In this example we setup the local data source specifically for securities, and use a sub job (metrics) to calculate price metrics in each row.
'''

from system.common import pd, os, sql3, db_path, raw_path, processed_path, datetime, tqdm, json
from system.utils.common import log_message
from custom_setup.jobs.metrics.main import calculate_metrics

# Connect to the database
conn = sql3.connect(db_path)

# Read CSV data
asx_data = pd.read_csv(os.path.join(raw_path, "listed.csv"))
asx_data.to_sql('asx_all', conn, if_exists='replace')

# Create the processed folder if it doesn't exist
current_date = datetime.now().strftime("%Y%m%d")
folder_path = os.path.join(processed_path, current_date)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Read margin loan data and merge with ASX data
margin_loan_data = pd.read_csv(os.path.join(raw_path, "lvr.csv"))
merged_df = pd.merge(asx_data, margin_loan_data, on='code', how='inner')

# logging if enabled
log_message(f"Number of matched records: {len(merged_df)}")
log_message(f"Number of unmatched records: {len(asx_data) - len(merged_df)}")

# Initialize columns for metrics
for col in ['RSI14', 'SMA20', 'SMA50', 'SMA200', 'dividend_yield', 'ATH', 'ATL', 'current_price']:
    merged_df[col] = None

# Confirm action
user_input = input("Do you want to proceed with calculating metrics for all securities in the local data source? This may take several minutes to complete (Y/N): ")

if user_input.lower() in ['yes', 'y']:
    with tqdm(total=len(merged_df), desc="Calculating metrics and writing to the local data source", unit="stock") as pbar:
        for idx, row in merged_df.iterrows():
            stock_code = row['code'] + '.AX'
            metrics = calculate_metrics(stock_code)
            
            # Ensure all keys are present in the DataFrame
            for key in ['RSI14', 'SMA20', 'SMA50', 'SMA200', 'dividend_yield', 'ATH', 'ATL', 'current_price']:
                value = metrics.get(key, None)
                if isinstance(value, pd.Series):
                    value = value.iloc[-1] if not value.empty else None
                merged_df.at[idx, key] = value
            
            # Save progress incrementally
            merged_df.iloc[[idx]].to_sql('lvr_filter', conn, if_exists='append', index=False)
            log_message(f"Updated metrics for {stock_code}")
            
            # Update the progress bar
            pbar.update(1)

    conn.close()

    # Log matched data
    matched_log_data = merged_df.to_dict(orient='records')
    with open(os.path.join(folder_path, f"matched_lvr_{current_date}.json"), 'w') as f:
        json.dump(matched_log_data, f)

# logging if enabled
log_message("Custom script: Custom setup completed (custom_setup/custom_setup.py)")