import numpy as np
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Input, Output, State, dcc, html, callback
import base64
import srcCode.affordFuncs as af
import srcCode.affordDescs as ad
import srcCode.toolbarDescs as tb
import srcCode.industryFuncs as indf
import srcCode.dashFuncs as df
import srcCode.cityDescs as cd

mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
# ----------------------------------------------------------------------------
# Data Files:
# Cleaned sales data file
sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
# Neighborhood data file
neighborhood_simple = gpd.read_file("neighborhood_simple.geojson")
# Census data file
census_simple = gpd.read_file("censusBlockDataFull.geojson")
# Sales data date cleaning
sales_clean_simple["SaleDate"] = pd.to_datetime(sales_clean_simple["SaleDate"])
# Loading rolling sales data
sales_year = pd.read_pickle("rolling/sales_year.pkl")
sales_year_single = pd.read_pickle("rolling/sales_year_single.pkl")
sales_year_two = pd.read_pickle("rolling/sales_year_two.pkl")
sales_year_multi = pd.read_pickle("rolling/sales_year_multi.pkl")
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

# History by zoning graph (number of sales)
def history_zoning_num():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["count"], 
                                    name="All Sales"))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["count"], 
                             name="Single Family"))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["count"], 
                             name="Two Family"))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["count"], 
                             name="Multi-family and Others"))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"])
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Number of Sales",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig

# History by zoning graph (median price)
def history_zoning_price():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["median"], 
                                    name="All Sales"))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["median"], 
                             name="Single Family"))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["median"], 
                             name="Two Family"))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["median"], 
                             name="Multi-family and Others"))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"])
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Median Sale Price [$, inflation adjusted]",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig

# ----------------------------------------------------------------------------
# All the texts
## History
history_title = "History of Real Estate Sales"
history_zoning_title = "By Zoning"
history_zoning_checklist_single = "Single family"
history_zoning_checklist_two = "Two family"
history_zoning_checklist_multi = "Multi family and others"
history_neighborhood_title = "By Neighborhood"

## Census
census_title = "Census Information"
## footnote
source = '''Data from Charlotteville Open Data Portal. Last update March 1, 2022.
Prices have been adjusted for inflation. Only sales with state code Residential 
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
# ----------------------------------------------------------------------------
# Building dash
year = np.arange(1945, 2021, 1, dtype=int)
neighborhood = ["Neighborhood Average", "Individual"]

layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            dbc.Button("☰", id='city_sidebar_button', className="background2 left_text title", 
                       style={"margin-left": "0"}),
            dbc.Collapse(
                [
                    dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['SECTOR'], href="#sector_plot", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['HIST'], href="#history_title", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['CENSUS'], href="#census_title", external_link=True, 
                                            className="background2 left_text subtitle")),
                ], id="city_sidebar", is_open=False, 
                style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = 'assets/title.png', style={'height':'50px'}), className="ml-5"),
                    ],
                    align="center",
                    className="g-0"
                )
            ),
        ], className="sidebar", color="#132C36", sticky="top"),
        html.H3(cd.text['MAIN_TITLE'], className = "center_text title"),
        # Level of detail dropdown
        df.createDropdown(ad.text['DD_LOD'], ad.opts['DD_LOD'],
                          ad.default['DD_LOD'], dd_id="afford_dropdown_lod", 
                          dd_style={"width": "200px"}, clearable=False, searchable = False),
        # Affordability
        html.Div(
            [
                html.Div([
                    dcc.Graph(id="afford_map", style={"width": "100%"}),
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 2fr) 1fr"}),
                html.Div([
                    html.Div([
                        dcc.Slider(min=1945, max=2021, step=1, value=2020, 
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   id="afford_slider_year")
                    ], style={"width": "100%"}),
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 4fr) 2fr 1fr"}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Sector/Industry chart
        html.Div(
            [
                dcc.Graph(id='sector_plot', figure=indf.plotIndustrySector(), style={'display': 'block'}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Neighborhood characteristics
        # History of price
        html.Div([
            html.Span(history_title, id="history_title", className="center_text title"),
            # By zoning
            html.Span(history_zoning_title, className="center_text subtitle"),
            dcc.Graph(id='history_zoning_num_plot', style={"width": "100%"},     
                      config={'displayModeBar': False}, figure=history_zoning_num()),
            dcc.Graph(id='history_zoning_price_plot', style={"width": "100%"},
                      config={'displayModeBar': False}, figure=history_zoning_price()),
        ], className="subcontainer"),
        # Census
        html.Div([
            html.Span(census_title, id="census_title", className="center_text title"),
            dcc.Graph(id='bar_plot', figure=plothhInc())
        ], className="subcontainer"),
        # Disclaimers
        html.Div([dcc.Markdown(children=source)], className="subcontainer left_text bodytext"),
        dcc.Link('Take me home', href='/home'),
    ], className="container background")

# Collapsable sidebar
@callback(Output("city_sidebar", "is_open"),
          [Input("city_sidebar_button", "n_clicks"), State("city_sidebar", "is_open")])
def sidebar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Update affordability graph
@callback(Output("afford_map", "figure"),
          [Input("afford_dropdown_lod", "value"), 
          Input("afford_slider_year", "value")])
def update_afford_map(lod, y):
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
