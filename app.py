from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import home, city, neighborhood, nbcompare, resources, contact

external_stylesheets = [dbc.themes.BOOTSTRAP]

app = Dash(__name__, external_stylesheets=external_stylesheets, 
           suppress_callback_exceptions=True, 
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, \
            initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}])
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/home':
        return home.layout
    elif pathname == '/city':
        return city.layout
    elif pathname == '/neighborhood':
        return neighborhood.layout
    elif pathname == '/nbcompare':
        return nbcompare.layout
    elif pathname == '/resources':
        return resources.layout
    elif pathname == '/contact':
        return contact.layout
    else:
        return home.layout

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
