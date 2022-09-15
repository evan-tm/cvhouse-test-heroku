import dash
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets, 
           suppress_callback_exceptions=True, 
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, \
            initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],
           use_pages = True)
server = app.server

app.layout = html.Div([
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
