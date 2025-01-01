import os
import sys
import json
import pandas as pd
import dash
from dash import dcc, html
import dash_table
from dash.dependencies import Input, Output
import webbrowser
from threading import Timer

# Add the project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from system.common import processed_path, datetime

# Load filtered securities JSON
current_date = datetime.now().strftime("%Y%m%d")
output_path = os.path.join(processed_path, current_date, "value-filter.json")
with open(output_path, "r") as f:
    filtered_securities = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(filtered_securities)

# Initialize Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Filtered Securities", style={'textAlign': 'left', 'color': 'white'}),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
            'whiteSpace': 'normal',
            'backgroundColor': '#303030',
            'color': 'white',
            'textAlign': 'left'
        },
        style_header={
            'backgroundColor': '#1f1f1f',
            'fontWeight': 'bold',
            'color': 'white',
            'textAlign': 'left'
        },
    )
], style={'backgroundColor': '#000000'})  # Set the background color to black

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True)