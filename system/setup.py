import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import shared utilities and libraries
from utils.common import log_message
from lib.functions.data.metrics.main import calculate_metrics
from common import sql3, pd, datetime, json, db_path, raw_path, processed_path

# Read CSV data
conn = sql3.connect(db_path)
asx_data = pd.read_csv(os.path.join(raw_path, "listed.csv"))
asx_data.to_sql('asx_all', conn, if_exists='replace')

current_date = datetime.now().strftime("%Y%m%d")
folder_path = os.path.join(processed_path, current_date)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

margin_loan_data = pd.read_csv(os.path.join(raw_path, "lvr.csv"))
merged_df = pd.merge(asx_data, margin_loan_data, on='code', how='inner')

log_message(f"Number of matched records: {len(merged_df)}")
log_message(f"Number of unmatched records: {len(asx_data) - len(merged_df)}")

# Initialize columns for metrics
for col in ['RSI14', 'SMA20', 'SMA50', 'SMA200', 'dividend_yield', 'ATH', 'ATL', 'current_price']:
    merged_df[col] = None

# Confirm action
user_input = input("Do you want to proceed with fetching stock metrics? This will create a database (Y/N): ")

if user_input.lower() in ['yes', 'y']:
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

    conn.close()

    # Log matched data
    matched_log_data = merged_df.to_dict(orient='records')
    with open(os.path.join(folder_path, f"matched_lvr_{current_date}.json"), 'w') as f:
        json.dump(matched_log_data, f)

    log_message("Stock metrics fetched and database updated.")