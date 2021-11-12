import numpy as np
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Input, Output, State


mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
external_stylesheets = [dbc.themes.BOOTSTRAP] 
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
sidebar_top = "Top"
sidebar_affordability = "Affordability"
sidebar_imap = "Exploring Housing History"
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
imap_sales_title = "Individual Sales"
imap_neigh_title = "Neighborhood Averages"
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
        # Sidebar
        dbc.Navbar([
            dbc.Button("☰", id='sidebar_button', className="background2 left_text title", 
                       style={"margin-left": "0"}),
            dbc.Collapse(
                [
                    dbc.NavItem(dbc.NavLink(sidebar_top, href="#", external_link=True, className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(sidebar_affordability, href="#affordability_title", external_link=True, className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(sidebar_imap, href="#imap_title", external_link=True, className="background2 left_text subtitle")),
                ], id="sidebar", is_open=False, style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
        ], className="sidebar", color="#132C36", sticky="top"),
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
                html.Span(affordability_title, className="center_text title", id="affordability_title"),
                html.Div(
                    [
                        # Salary
                        html.Div(
                            [
                                html.Span(salary_input_hint, className="left_text inline_title"),
                                dcc.Input(id="salary_input", type="number", placeholder="salary",
                                          className="subcontainer", style={"width": "200px"})
                            ], className="grid_container", style={"grid-template-columns": "1fr 1fr"}),
                        # Bedrooms
                        html.Div(
                            [
                                html.Span(bedroom_dropdown_hint, className="left_text inline_title"),
                                dcc.Dropdown(id="bedroom_dropdown", 
                                             options=bedroom_dropdown_options, value=bedroom_dropdown_value,
                                             className="subcontainer", style={"width": "200px"})
                            ], className="grid_container", style={"grid-template-columns": "1fr 1fr"}),
                    ], className="grid_container background2", style={"grid-template-columns": "1fr 1fr"}),
                # Predict
                html.Div(
                    [
                        html.Span(affordability_prediction_text, className="center_text inline_title"),
                        html.Span(affordability_prediction_idle, id="affordability_prediction",
                                  className="center_text inline_title", style={"color": "#DA6146"})
                    ], className="grid_container", style={"grid-template-columns": "1fr 1fr"}),
                # Algorithm description
                html.Div([dcc.Markdown(affordability_prediction_algo)], className="left_text bodytext")
            ], className="subcontainer"),
        # Interactive map
        html.Div(
            [
                html.Span(imap_title, className="center_text title", id="imap_title"),
                html.Div(
                [
                    # Sales map
                    html.Div(
                        [
                            html.Span(imap_sales_title, className="center_text subtitle"),
                            dcc.Graph(id="sales_graph"),
                        ], className="subcontainer background", style={"width": "100%"}),
                    # Year Dropdown
                    html.Div(
                        [
                            dcc.Dropdown(id='year', options=[{'label': i, 'value': i} for i in year], value=2019, 
                                         style={"width": "200px"}),
                            dcc.Graph(id="table", className="background"),
                        ], className="subcontainer background", style={"width": "100%"}),
                    # Average map
                    html.Div(
                        [
                            html.Span(imap_neigh_title, className="center_text subtitle"),
                            dcc.Graph(id="neigh_graph"),
                        ], className="subcontainer background", style={"width": "100%"}),
                ], className="grid_container", style={"grid-template-columns": "minmax(400px, 2fr) 1fr minmax(400px, 2fr)"}),
            ], className="subcontainer"),
        # Disclaimers
        html.Div([dcc.Markdown(children=source)], className="subcontainer left_text bodytext"),
    ], className="container background")

# Collapsable sidebar
@app.callback(Output("sidebar", "is_open"),
              [Input("sidebar_button", "n_clicks"), State("sidebar", "is_open")])
def sidebar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Individual sales year change
@app.callback(Output(component_id="sales_graph", component_property="figure"), 
              [Input(component_id='year', component_property="value")])
def change_year_sales(y):
    mask = (sales_clean_simple["Year"] == y)
    sales_year = sales_clean_simple[mask].set_index("ParcelNumber")
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
                               zoom=14,
                              )
    fig.update_traces(hovertemplate="<br>".join([
        "%{hovertext}",
        "",
        "Total Sale Price: $%{customdata[0]}",
        "Acreage: %{customdata[1]}",
        "Last sale on %{customdata[2]}",
        "Zoning: %{customdata[3]}"]))
    fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                      mapbox_style=mapbox_style,
                      margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,)
    fig.update_coloraxes(colorbar_tickfont_color="rgb(255,255,255)", colorbar_tickfont_size=16)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

# Neighborhood average year change
@app.callback(Output(component_id="neigh_graph", component_property="figure"), 
              [Input(component_id='year', component_property="value")])
def change_year_neigh(y):
    mask = (sales_clean_simple["Year"] == y)
    sales_year = sales_clean_simple[mask].set_index("ParcelNumber")
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
                               zoom=12, 
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
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,)
    fig.update_coloraxes(colorbar_tickfont_color="rgb(255,255,255)", colorbar_tickfont_size=16)
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

# Clicking on the interactive plots
@app.callback(Output(component_id="table", component_property="figure"),
              [Input(component_id='sales_graph',component_property="clickData"),
               Input(component_id='neigh_graph',component_property="clickData"),])
def change_table(click_s, click_n):
    if (click_s is None) and (click_n is None):
        fig = go.Figure(data=go.Table())
    else:
        ctx = dash.callback_context
        dropdown_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if dropdown_id == "sales_graph":
            # Individual sales
            addr = click_s['points'][0]['hovertext']
            data = click_s['points'][0]['customdata']
            fig = go.Figure(data=go.Table(header=dict(values=["Address", addr]),
                                          cells=dict(values=[["Total Sale Price", "Acreage", "Last sale on", "Zoning"],
                                                             data])))
        else:
            # Neighborhood average
            addr = click_n['points'][0]['hovertext']
            data = click_n['points'][0]['customdata']
            fig = go.Figure(data=go.Table(header=dict(values=["Neighborhood", addr]),
                                          cells=dict(values=[["Average Sale Price", "Number of Sales"],
                                                             data])))
    fig.update_layout(margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,)
    fig.update_traces(cells_font_size=15)
    return fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
