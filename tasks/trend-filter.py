import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from system.common import datetime, json, log_message, processed_path, sql3, db_path, pd

# Load securities from SQLite database
conn = sql3.connect(db_path)
securities_df = pd.read_sql_query("SELECT * FROM lvr_filter", conn)
conn.close()

# Convert DataFrame to list of dictionaries
securities = securities_df.to_dict(orient='records')

# Filter trending stocks based on RSI and price momentum
trending_stocks = []
for s in securities:
    if (
        s["RSI14"] is not None
        and s["SMA50"] is not None
        and s["SMA200"] is not None
        and s["current_price"] is not None
    ):
        # Ensure RSI is in the healthy range (30 < RSI14 < 70)
        rsi_condition = 30 < float(s["RSI14"]) < 70

        # Ensure current price shows positive momentum (above SMA50 and SMA200)
        price_condition = (
            float(s["current_price"]) > float(s["SMA50"])
            and float(s["current_price"]) > float(s["SMA200"])
        )

        # If both conditions are met, add the stock to the trending list
        if rsi_condition and price_condition:
            trending_stocks.append(s)

# Sort by RSI (ascending) and price difference from SMA200 (descending)
trending_stocks = sorted(
    trending_stocks,
    key=lambda x: (
        float(x["RSI14"]),  # Sort by RSI (closer to 70 is better, but not overbought)
        -(float(x["current_price"]) - float(x["SMA200"])),  # Sort by price deviation from SMA200
    ),
)

# Create output directory based on today's date
current_date = datetime.now().strftime("%Y%m%d")
output_dir = os.path.join(processed_path, current_date)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Output
output_path = os.path.join(output_dir, "trending-filter.json")
with open(output_path, "w") as f:
    json.dump(trending_stocks, f, indent=4)

log_message(f"Trending stocks saved to {output_path}")
