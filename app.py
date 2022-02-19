import numpy as np
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html


mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
external_stylesheets = [dbc.themes.BOOTSTRAP] 
# ----------------------------------------------------------------------------
# Data Files:
# Cleaned sales data file
sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
# Neighborhood data file
neighborhood_simple = gpd.read_file("neighborhood_simple.geojson")
# Census data file
census_simple = gpd.read_file("censusBlockDataFull.geojson")
# Industry by sector data file
indBySector = pd.read_csv("indBySector.csv")
indBySector = indBySector.iloc[1: , :]
indBySector = indBySector.sort_values(by="Total", ascending = True)

# Industry by neighborhood  data
indByNeighborhood = pd.read_csv("indByNeighborhoodCleanedTest.csv")
indByNeighborhood = indByNeighborhood.iloc[1: , :]
dropdown_neighborhood = ""
dropdown_neighborhood_lod_opts = ["Barracks Road", "Rose Hill", "Lewis Mountain", "Starr Hill / Mall",
                                  "Woolen Mills", "10th & Page", "The Meadows", "Martha Jefferson",
                                  "Johnson Village", "Greenbrier", "Barracks / Rugby", "North Downtown",
                                  "Locust Grove", "Jefferson Park Ave", "Fifeville", "Fry's Spring",
                                  "Ridge Street", "Venable", "Belmont"]
dropdown_neighborhood_default = dropdown_neighborhood_lod_opts[0]
#indByNeighborhood = indByNeighborhood.sort_values(by="Total", ascending = True)

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
    
def plothhInc():
    # Function for creating plot of population size by hh income bracket
    fig = px.bar(hhIncPcts, x='bracket', y='hhInc', color='hhInc', 
                 labels={'bracket':'Income Bracket', 
                         'hhInc':'Households (% of total, n = 89829)'}, height=400)
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    return fig

def plotIndustrySector():
    # Function for creating plot of industry employment populations by sector
    fig = px.bar(indBySector, y="Industry", 
                 x=["Private For-Profit", "Self-Employed Incorporated", 
                    "Private Not-For-Profit", "Government", "Self-Employed Not Incorporated"], 
                 labels={'value':'Employed (count)'}, orientation="h")
    fig.update_layout(margin=go.layout.Margin(l=200, r=0, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(255,255,255)"),
                      legend_title_text=sector_legend,
                      legend=dict(yanchor="bottom", 
                                  x=1, 
                                  y=0, 
                                  xanchor="right",
                                  bgcolor="DimGray")
    )
    return fig
def createDropdown(description, opts, default_value, dd_style={"width": "150px"}, dd_id=None, grid_width="1fr 1fr",
                   **kwargs):
    opts_dict = [{"label": each, "value": each} for each in opts]
    return html.Div([
        html.Span(description, className="center_text bodytext"),
        dcc.Dropdown(id=dd_id, options=opts_dict, value=default_value, className="subcontainer", 
                     style=dd_style, **kwargs)
    ], className="grid_container", style={"grid-template-columns": grid_width})

def createInput(description, opts, default_value, ip_style={"width": "150px"}, ip_id=None, grid_width="1fr 1fr",
                **kwargs):
    return html.Div([
        html.Span(description, className="center_text bodytext"),
        dcc.Input(id=ip_id, type=opts, placeholder=default_value, min=0, className="subcontainer", 
                  style=ip_style, **kwargs)
    ], className="grid_container", style={"grid-template-columns": grid_width})

# ----------------------------------------------------------------------------
# All the texts
## Sidebar
sidebar_top = "Top"
sidebar_afford = "Affordability"
sidebar_imap = "Exploring Housing History"
sidebar_census = "Census Information"
## Header
title = "Charlottesville Housing Affordability:  "
subtitle = "Building a Picture of Who Can Afford What"
header_text = '''Our goal is to bring attention to housing affordability issues
in the Charlottesville community. Below, you can explore what you can currently 
afford with our price prediction tool. Additionally, you can see where housing 
prices are headed and understand where they’ve been historically. '''
## Affordability
afford_title = "What Can You Afford?"
afford_dropdown_title = "Learn more about our neighborhoods:"
afford_dropdown_industry_desc = "By Industry:"
afford_dropdown_industry_opts = ["Industry 1", "Industry 2", "Industry 3"]
afford_dropdown_industry_default = afford_dropdown_industry_opts[0]
afford_dropdown_person_info_title = "By Personal Situation:"
afford_input_salary_desc = "Household Income:"
afford_input_salary_default = "26000"
afford_dropdown_kids_desc = "Kids:"
afford_dropdown_kids_opts = ["0", "1", "2", "3", "4+"]
afford_dropdown_kids_default = afford_dropdown_kids_opts[0]
afford_input_age_desc = "Your Age:"
afford_input_age_default = "30"
afford_advanced_title = "Advanced Options"
afford_input_tech_desc = "Monthly Technology Budget:"
afford_input_tech_default = "40"
afford_input_tech_tip = "Cell phone plans, etc"
afford_input_saving_desc = "Monthly Allocated Savings:"
afford_input_saving_default = "500"
afford_button = "Calculate"
afford_dropdown_lod_desc = "Lever of Detail"
afford_dropdown_lod_opts = ["Neighborhood", "Individual Properties"]
afford_dropdown_lod_default = afford_dropdown_lod_opts[0]
afford_prediction_text = "You can afford 0% of houses in cville."
afford_prediction_algo = "Describe algorithm here. Some machine learning magic and stuff. Can include equations since it is a markdown cell."
## Neighborhood
## History
imap_title = "Explore Charlottesville Housing Sales History"
imap_sales_title = "Individual Sales"
imap_neigh_title = "Neighborhood Averages"
## Industry and Sector Counts of the civilian employed population aged 16 and 
##   older in Charlottesville
sector_title = "Charlottesville Industry and Sector Counts of the civilian \
    employed population aged 16 and older."
sector_legend = "Sector"

# Industry by Neighborhood
neighborhood_title = "Industries by Neighborhood"
neighborhood_legend = "Neighborhood"

## Census
census_title = "Census Information"
## footnote
source = '''Data from Charlotteville Open Data Portal. Last update Feb 7, 2022.
Price has been adjusted for inflation. Only sales with state code Residential 
(urban/suburban) and Multifamily are included.'''
# ----------------------------------------------------------------------------
# Data processing for census_plot
colsHHInc = ['GEOID', 'hhInc10E', 'hhInc10to15E', 'hhInc15to20E', 
             'hhInc20to25E', 'hhInc25to30E', 'hhInc30to35E', 
             'hhInc35to40E', 'hhInc40to45E', 'hhInc45to50E', 
             'hhInc50to60E', 'hhInc60to75E', 'hhInc75to100E', 
             'hhInc100to125E', 'hhInc125to150E', 'hhInc150to200E',
             'hhInc200E']
hhIncDF = census_simple[colsHHInc]
hhIncPivot = pd.wide_to_long(hhIncDF, stubnames="hhInc", i="GEOID", j="bracket", suffix='\\w+')
hhIncPivot = hhIncPivot.reset_index().reindex(["GEOID", "bracket", "hhInc"], axis=1)
hhIncPcts = hhIncPivot.groupby(hhIncPivot['bracket']).agg({'hhInc':'sum'}).reset_index()
n = sum(hhIncPcts['hhInc'])
hhIncPcts['hhInc'] = 100 * hhIncPcts['hhInc'] / sum(hhIncPcts['hhInc'])
hhIncPcts = hhIncPcts.reindex([1,2,5,7,8,9,10,11,12,13,14,15,0,3,4,6])
hhIncPcts['bracket'] = '$' + hhIncPcts['bracket'].str[:-1] + 'k'
hhIncPcts.at[1,'bracket'] = "< " + hhIncPcts['bracket'][1]
hhIncPcts.at[6,'bracket'] = hhIncPcts['bracket'][6] + "+"
# Data processing for sector_plot
indBySector = indBySector.iloc[1: , :]

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
                    dbc.NavItem(dbc.NavLink(sidebar_top, href="#", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(sidebar_afford, href="#afford_title", 
                                            external_link=True, className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(sidebar_imap, href="#imap_title", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(sidebar_census, href="#imap_title", external_link=True, 
                                            className="background2 left_text subtitle")),
                ], id="sidebar", is_open=False, 
                style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
        ], className="sidebar", color="#132C36", sticky="top"),
        # Header
        html.Div([
            html.Div(
            [
                html.Span(title, className="left_text title"),
                html.Span(subtitle, className="left_text subtitle"),
                html.Span(header_text, className="left_text bodytext"),
            ], className="subcontainer"),
            html.Img(src="https://via.placeholder.com/240", className="subcontainer")
        ], className="grid_container background", style={"grid-template-columns": "4fr 1fr"}),
        # Affordability
        html.Div(
            [
                html.Span(afford_title, className="center_text title", id="afford_title"),
                html.Div([
                    dcc.Graph(id="afford_map", style={"width": "100%"}),
                    html.Div([
                        html.Span(afford_dropdown_title, className="left_text subtitle"),
                        # Industry
                        createDropdown(afford_dropdown_industry_desc, afford_dropdown_industry_opts,
                                       afford_dropdown_industry_default, dd_id="afford_dropdown_industry",
                                       dd_style={"width": "200px"}),
                        # Personal information
                        html.Hr(className="center_text title"),
                        html.Span(afford_dropdown_person_info_title, className="left_text subtitle"),
                        createInput(afford_input_salary_desc, "number", afford_input_salary_default, 
                                    ip_id="afford_input_salary"),
                        createDropdown(afford_dropdown_kids_desc, afford_dropdown_kids_opts,
                                       afford_dropdown_kids_default, dd_id="afford_dropdown_kids"),
                        createInput(afford_input_age_desc, "number", afford_input_age_default,
                                    ip_id="afford_input_age"),
                        # Advnaced options
                        html.Span(afford_advanced_title, className="left_text bodytext"),
                        createInput(afford_input_tech_desc, "number", afford_input_tech_default,
                                    ip_id="afford_input_tech"),
                        dbc.Tooltip(afford_input_tech_tip, target="afford_input_tech"),
                        createInput(afford_input_saving_desc, "number", afford_input_saving_default,
                                    ip_id="afford_input_saving"),
                    ], className="subcontainer")
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 2fr) 1fr"}),
                html.Div([
                    html.Div([
                        dcc.Slider(min=1945, max=2021, step=1, value=2020, 
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   id="afford_slider_year")
                    ], style={"width": "100%"}),
                    createDropdown(afford_dropdown_lod_desc, afford_dropdown_lod_opts,
                                   afford_dropdown_lod_default, dd_id="afford_dropdown_lod", 
                                   dd_style={"width": "200px"}),
                    html.Button(afford_button, id="afford_button", className="right_text subtitle",
                                style={"background-color": "#FFA858", "color": "#000000"}),
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 4fr) 2fr 1fr"}),
                html.Span(afford_prediction_text, id="afford_prediction", className="center_text subtitle"),
                # Algorithm description
                html.Div([dcc.Markdown(afford_prediction_algo)], className="left_text bodytext")
            ], className="subcontainer"),
        # Sector and Industry chart
        html.Div(
            [
                html.Span(sector_title, id="sector_title", className="center_text title"),
                dcc.Graph(id='sector_plot', figure=plotIndustrySector(), style={'display': 'inline-block'}),
            ], className="subcontainer"),
        # Industry and Neighborhood chart
        html.Div(
            [
                html.Span(neighborhood_title, id="neighborhood_title", className="center_text title"),
                createDropdown(dropdown_neighborhood, dropdown_neighborhood_lod_opts,
                               dropdown_neighborhood_default, dd_id="dropdown_neighborhood",
                               dd_style={"width": "200px"}, grid_width="1fr"),
                dcc.Graph(id='neighborhood_plot'),
            ], className="subcontainer"),
        # Neighborhood characteristics
        # History of price
        # Census
        html.Div(
            [
                html.Span(census_title, id="census_title", className="center_text title"),
                dcc.Graph(id='census_plot', figure=plothhInc())
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

@app.callback(
    Output('neighborhood_plot', 'figure'),
    Input('dropdown_neighborhood', 'value'))
def plotIndustryByNeighborhood(n):
    # Function for creating plot of industry employment populations by neighborhood
    fig = px.bar(indByNeighborhood, y="Industry",
                 x=[n], labels={'value':'Employed (count)'}, orientation="h").update_yaxes(categoryorder="total ascending")
    fig.update_layout(margin=go.layout.Margin(l=200, r=0, b=0, t=30, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(255,255,255)"),
                      legend_title_text=neighborhood_legend,
                      legend=dict(yanchor="bottom",
                                  x=1,
                                  y=0,
                                  xanchor="right",
                                  bgcolor="DimGray")
    )
    return fig


# Update affordability graph
@app.callback(Output("afford_map", "figure"),
              [Input("afford_button", "n_clicks"), State("afford_slider_year", "value"),
               State("afford_dropdown_lod", "value")])
def update_afford_map(n, y, lod):
    mask = (sales_clean_simple["Year"] == y)
    sales_year = sales_clean_simple[mask].set_index("ParcelNumber")
    if lod == "Neighborhood":
        # Neighborhood map
        sales_year_nba = sales_year.groupby("Neighborhood").agg({"SaleAmountAdjusted": ["size", "mean"]}).reset_index()
        sales_year_nba.columns = ["Neighborhood", "NumSales", "MeanSales"]
        sales_year_nba = neighborhood_simple.merge(sales_year_nba, how="inner", 
                                                   right_on="Neighborhood", left_on="NAME")
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
    else:
        # Individual property map
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
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
