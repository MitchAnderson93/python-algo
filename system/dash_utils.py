from system.common import dash, dcc, html, dash_table, webbrowser, Timer

def create_dash_app(df, title):
    app = dash.Dash(__name__, assets_folder='assets')

    app.layout = html.Div([
        html.H1(title, className='dash-title'),
        dash_table.DataTable(
            id='table',
            columns=[{
                "name": i, 
                "id": i,
                "filter_options": {"case": "insensitive"},
                "type": "numeric" if df[i].dtype in ['int64', 'float64'] else "text"
            } for i in df.columns],
            data=df.to_dict('records'),
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            style_table={'overflowX': 'auto'},
            style_cell={
                'backgroundColor': '#2b2b2b',
                'color': '#f1edea',
                'textAlign': 'left'
            },
            style_header={
                'backgroundColor': '#1e1e1e',
                'color': '#f1edea',
                'fontWeight': 'bold'
            },
            style_filter={
                'backgroundColor': '#1e1e1e',
                'color': '#f1edea'
            }
        )
    ])

    return app

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def run_dash_app(app):
    Timer(1, open_browser).start()
    app.run_server(debug=True)