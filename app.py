import numpy as np
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import dash
import dash_core_components as dcc
import dash_html_components as html


mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


source = '''Data from Charlotteville Open Data Portal. Last update Sept 24,
2021.'''

sales_2020 = gpd.read_file("sales_2020.geojson")
vmin, vmax = np.nanpercentile(sales_2020["SaleAmount"], [5, 95])
fig = px.choropleth_mapbox(sales_2020, geojson=sales_2020.geometry, 
                           locations=sales_2020.index, color="SaleAmount",
                           hover_name="Address", 
                           center={"lat": 38.0293, "lon": -78.4767}, zoom=11, 
                           width=700, height=700, range_color=[vmin, vmax], 
                           labels={"SaleAmount": "Total Price", 
                                   "PricePerSqft": "USD per Sqft", 
                                   "SaleDate": "Date"},
                           hover_data={"SaleAmount": True, "Acreage": True, 
                                       "PricePerSqft": ":.2f", 
                                       "SaleDate": True, "Zoning": True})
fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                  mapbox_style=mapbox_style)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        html.H1("Charlottesville Real Estate Sale in Year 2020"),
        dcc.Graph(figure=fig),
        dcc.Markdown(children=source)
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
