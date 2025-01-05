from system.common import dash, dcc, html, dash_table, webbrowser, Timer

def create_dash_app(df, title):
    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            html.H1(title, style={'textAlign': 'left'}),
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'},
                style_cell={
                    'height': 'auto',
                    'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                    'whiteSpace': 'normal',
                    'textAlign': 'left'
                },
                style_header={
                    'fontWeight': 'bold',
                    'textAlign': 'left'
                },
            )
        ]
    )

    return app

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050/")

def run_dash_app(app):
    Timer(1, open_browser).start()
    app.run_server(debug=True)