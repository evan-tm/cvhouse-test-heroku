import numpy as np
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


source = '''Data from Charlotteville Open Data Portal. Last update Oct 1, 2021.
Price has been adjusted for inflation.'''

sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
year = np.arange(1945, 2021, 1, dtype=int)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        html.H1("Charlottesville Real Estate Sale"),
        html.Div([
            dcc.Dropdown(id='year', options=[{'label': i, 'value': i} for i in year], value=2019),
        ], style={"width": "49%", "float": "right"}),
        html.Div([
            dcc.Graph(id="graph"),
        ], style={"width": "49%", "float": "left"}),
        html.Div([
            dcc.Graph(id="table"),
        ], style={"width": "49%", "float": "right"}),
        html.Div([
            dcc.Markdown(children=source),
        ], style={"width": "100%", "float": "left"}),
    ]
)
@app.callback(Output(component_id="graph",component_property="figure"), 
              [Input(component_id='year',component_property="value"),])
def change_year(y):
    mask = (sales_clean_simple["Year"] == y)
    sales_year = sales_clean_simple[mask]
    vmin, vmax = np.nanpercentile(sales_year["SaleAmountAdjusted"], (5, 95))
    fig = px.choropleth_mapbox(sales_year, 
                               geojson=sales_year.geometry, 
                               locations=sales_year.index, 
                               color="SaleAmountAdjusted",
                               range_color=[vmin, vmax],
                               labels={"SaleAmountAdjusted": "Total Sale Price"},
                               hover_name="Address", 
                               hover_data={"SaleAmountAdjusted": True, 
                                           "Acreage": True, 
                                           "PricePerSqftAdjusted": ":.2f", 
                                           "SaleDateStr": True, 
                                           "Zone": True},
                               center={"lat": 38.0293, "lon": -78.4767}, 
                               zoom=11, 
                               )
    fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                      mapbox_style=mapbox_style)
    fig.update_traces(hovertemplate="<br>".join([
        "Total Sale Price: $%{customdata[0]:,}",
            "Acreage: %{customdata[1]:.3f}",
            "Price per Sqft: $%{customdata[2]:.2f}",
            "Last sale on %{customdata[3]}",
            "Zoning: %{customdata[4]}"]))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

@app.callback(Output(component_id="table", component_property="figure"),
              [Input(component_id='graph',component_property="clickData"),])
def change_table(click):
    if click is None:
        return go.Figure()
    addr = click['points'][0]['hovertext']
    data = click['points'][0]['customdata']
    fig = go.Figure(data=go.Table(header=dict(values=["Address", addr]),
                                  cells=dict(values=[["Total Sale Price",
                                                      "Acreage",
                                                      "Pricer per Sqft",
                                                      "Last sale",
                                                      "Zoning"],
                                                      data])))
    return fig

if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
