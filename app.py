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
external_stylesheets = ["https://dash.gallery/dash-spatial-clustering/assets/base.css"] 
# ----------------------------------------------------------------------------
# Helper functions
millnames = ['','k','M','B','T']

def millify(n):
    if not n:
        return "Not available"
    elif np.isnan(n):
        return "Not available"
    else:
        n = float(n)
        millidx = max(0, min(len(millnames) - 1, int(np.floor(0 if n == 0 else np.log10(abs(n))/3))))
        return '{:.2f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])

def nanformat(n, strcode):
    if not n:
        return "Not available"
    elif np.isnan(n):
        return "Not available"
    else:
        return strcode % n
# ----------------------------------------------------------------------------
# Cleaned data file
sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
# Neighborhood data file
neighborhood_simple = gpd.read_file("neighborhood_simple.geojson")
# ----------------------------------------------------------------------------
# All the texts
title = "Charlottesville Housing Affordability:  "
subtitle = "Building a Picture of Who Can Afford What"
header_text = '''Our goal is to bring attention to housing affordability issues
in the Charlottesville community. Below, you can explore what you can currently 
afford with our price prediction tool. Additionally, you can see where housing 
prices are headed and understand where they’ve been historically. '''
affordability_title = "What Can You Afford?"
salary_input_hint = "Salary: "
bedroom_dropdown_hint = "Bedrooms: "
bedroom_dropdown_options = [{"label": each, "value": each} for each in ["Studio", "1", "2", "3", "4+"]]
bedroom_dropdown_value = "2"
affordability_prediction_text = "Predicted price of potential home:"
affordability_prediction_idle = "$300,000"
affordability_prediction_algo = "Describe algorithm here. Some machine learning magic and stuff. Can include equations since it is a markdown cell."
imap_title = "Explore Charlottesville Housing Sales History"
source = '''Data from Charlotteville Open Data Portal. Last update Oct 28, 2021.
Price has been adjusted for inflation. Only sales with state code Residential 
(urban/suburban) and Multifamily are included.'''
# ----------------------------------------------------------------------------
# Building dash
year = np.arange(1945, 2021, 1, dtype=int)
neighborhood = ["Neighborhood Average", "Individual"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        # Header
        html.Div(
            [
                html.Span(title, className="left_text title"),
                html.Span(subtitle, className="left_text subtitle"),
                html.Span(header_text, className="left_text bodytext"),
            ], className="subcontainer"),
        # Affordability
        html.Div(
            [
                html.Span(affordability_title, className="center_text title"),
                html.Div(
                    [
                        # Salary
                        html.Div(
                            [
                                html.Span(salary_input_hint, className="left_text inline_title"),
                                dcc.Input(id="salary_input", type="number", placeholder="salary",
                                          className="subcontainer", style={"width": "200px"})
                            ], className="grid_container_1x2"),
                        # Bedrooms
                        html.Div(
                            [
                                html.Span(bedroom_dropdown_hint, className="left_text inline_title"),
                                dcc.Dropdown(id="bedroom_dropdown", 
                                             options=bedroom_dropdown_options, value=bedroom_dropdown_value,
                                             className="subcontainer", style={"width": "200px"})
                            ], className="grid_container_1x2"),
                    ], className="grid_container_1x2 background2"),
                # Predict
                html.Div(
                    [
                        html.Span(affordability_prediction_text, className="center_text inline_title"),
                        html.Span(affordability_prediction_idle, id="affordability_prediction",
                                  className="center_text inline_title", style={"color": "#DA6146"})
                    ], className="grid_container_1x2"),
                # Algorithm description
                html.Div([dcc.Markdown(affordability_prediction_algo)], className="left_text bodytext")
            ], className="subcontainer"),
        # Interactive map
        html.Div(
            [
                html.Span(imap_title, className="center_text title"),
                html.Div(
                [
                    html.Div([dcc.Graph(id="graph"),], className="subcontainer background"),
                    html.Div(
                        [
                            dcc.Dropdown(id='year', options=[{'label': i, 'value': i} for i in year], value=2019, 
                                         style={"width": "300px"}),
                            dcc.Dropdown(id='nb',
                                         options=[{'label': "Neighborhood Average", 'value': "nba"},
                                                  {'label': "Individual Sales", 'value': 'ind'}], 
                                         value="ind", style={"width": "300px"}),
                            dcc.Graph(id="table", className="background"),
                        ], className="subcontainer"),
                ], className="grid_container_1x2", style={"grid-template-columns:": "2fr 1fr"}),
            ], className="subcontainer"),
        # Disclaimers
        html.Div([dcc.Markdown(children=source)], className="subcontainer left_text bodytext"),
    ], className="container background")

@app.callback(Output(component_id="graph", component_property="figure"), 
              [Input(component_id='year', component_property="value"),
               Input(component_id='nb', component_property="value")])
def change_year(y, nb):
    mask = (sales_clean_simple["Year"] == y)
    sales_year = sales_clean_simple[mask].set_index("ParcelNumber")
    if nb == "ind":
        # Individual sales
        vmin, vmax = np.nanpercentile(sales_year["SaleAmountAdjusted"], (5, 95))
        fig = px.choropleth_mapbox(sales_year, 
                                   geojson=sales_year.geometry, 
                                   locations=sales_year.index, 
                                   color="SaleAmountAdjusted",
                                   range_color=[vmin, vmax],
                                   labels={"SaleAmountAdjusted": "Total Sale Price"},
                                   hover_name="Address", 
                                   hover_data={"SaleAmountStr": True, "AcreageStr": True, 
                                               "SaleDateStr": True, "Zone": True},
                                   center={"lat": 38.0293, "lon": -78.4767}, 
                                   zoom=15, 
                                   width=800,
                                   )
        fig.update_traces(hovertemplate="<br>".join([
            "%{hovertext}",
            "",
            "Total Sale Price: $%{customdata[0]}",
            "Acreage: %{customdata[1]}",
            "Last sale on %{customdata[2]}",
            "Zoning: %{customdata[3]}"]))
    else:
        # Neighborhood average
        sales_year_nba = sales_year.groupby("Neighborhood").agg({"SaleAmountAdjusted": ["size", "mean"]}).reset_index()
        sales_year_nba.columns = ["Neighborhood", "NumSales", "MeanSales"]
        sales_year_nba = neighborhood_simple.merge(sales_year_nba, how="inner", right_on="Neighborhood", left_on="NAME")
        sales_year_nba["MeanSalesStr"] = sales_year_nba["MeanSales"].apply(millify)
        vmin, vmax = np.nanpercentile(sales_year_nba["MeanSales"], (5, 95))
        fig = px.choropleth_mapbox(sales_year_nba, 
                                   geojson=sales_year_nba.geometry,
                                   locations=sales_year_nba.index, 
                                   color="MeanSales",
                                   range_color=[vmin, vmax],
                                   labels={"MeanSales": "Average Total Sale Price"},
                                   hover_name="Neighborhood", 
                                   hover_data={"MeanSalesStr": True, "NumSales": True},
                                   center={"lat": 38.0293, "lon": -78.4767}, 
                                   zoom=13, 
                                   width=800,
                                   )
        fig.update_traces(hovertemplate="<br>".join([
            "%{hovertext}",
            "",
            "Average Sale Price in Neighborhood: $%{customdata[0]}",
            "Number of Sales Recorded: %{customdata[1]}"]))
    fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                      mapbox_style=mapbox_style,
                      margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)")
    fig.update_coloraxes(colorbar_tickfont_color="rgb(255,255,255)", colorbar_tickfont_size=16)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

@app.callback(Output(component_id="table", component_property="figure"),
              [Input(component_id='graph',component_property="clickData"),])
def change_table(click):
    if click is None:
        fig = go.Figure(data=go.Table())
    else:
        addr = click['points'][0]['hovertext']
        data = click['points'][0]['customdata']
        if len(data) == 2:
            fig = go.Figure(data=go.Table(header=dict(values=["Neighborhood", addr]),
                                          cells=dict(values=[["Average Sale Price", "Number of Sales"],
                                                              data])))
        else:
            fig = go.Figure(data=go.Table(header=dict(values=["Address", addr]),
                                          cells=dict(values=[["Total Sale Price", "Acreage", "Last sale on", "Zoning"],
                                                              data])))
    fig.update_layout({"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"})
    fig.update_layout(margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(cells_font_size=15)
    return fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
