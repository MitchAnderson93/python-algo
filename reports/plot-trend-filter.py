import os
import sys

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
sys.path.insert(0, project_root)

from system.common import processed_path, datetime, json, pd
from system.dash_utils import create_dash_app, run_dash_app

# Load filtered securities JSON
current_date = datetime.now().strftime("%Y%m%d")
output_path = os.path.join(processed_path, current_date, "trending-filter.json")
with open(output_path, "r") as f:
    filtered_securities = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(filtered_securities)

# Create and run Dash app 
app = create_dash_app(df, "Possible trending securities")

if __name__ == '__main__':
    run_dash_app(app)