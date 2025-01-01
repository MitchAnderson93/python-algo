import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from system.common import datetime, json, log_message, processed_path, sql3, db_path, pd

# Load securities from SQLite database
conn = sql3.connect(db_path)
securities_df = pd.read_sql_query("SELECT * FROM LVR", conn)
conn.close()

# Convert DataFrame to list of dictionaries
securities = securities_df.to_dict(orient='records')

# Filter based on metrics
filtered_securities = [
    s for s in securities
    if s["RSI14"] is not None and float(s["RSI14"]) < 30
    and s["current_price"] is not None and s["SMA200"] is not None and float(s["current_price"]) < float(s["SMA200"])
    and s["dividend_yield"] is not None and float(s["dividend_yield"]) > 5
    and s["portfolio_lvr"] is not None and float(s["portfolio_lvr"]) >= 60
]

# Sort by dividend yield and RSI14
filtered_securities = sorted(filtered_securities, key=lambda x: (-float(x["dividend_yield"]), float(x["RSI14"])))

# Create output directory based on today's date
current_date = datetime.now().strftime("%Y%m%d")
output_dir = os.path.join(processed_path, current_date)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Output
output_path = os.path.join(output_dir, "value-filter.json")
with open(output_path, "w") as f:
    json.dump(filtered_securities, f, indent=4)

log_message(f"Filtered securities saved to {output_path}")