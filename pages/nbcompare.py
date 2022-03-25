# ------------------Neighborhood page------------------#
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import base64
import pandas as pd
import srcCode.toolbarDescs as tb
import srcCode.neighborhoodDescs as nd
import srcCode.nbcDescs as nbcd
import srcCode.dashFuncs as df
import srcCode.affordDescs as ad
import srcCode.cvillepedia as cv
import srcCode.censusFuncs as cf

# Loading rolling sales data
sales_year = pd.read_pickle("data/rolling/sales_year.pkl")

# Neighborhood dropdown texts
dropdown_neighborhood = ""
checklist_neighborhood_lod_opts = ["Barracks Road", "Rose Hill", "Lewis Mountain", "Starr Hill",
                                   "Woolen Mills", "10th & Page", "The Meadows", "Martha Jefferson",
                                   "Johnson Village", "Greenbrier", "Barracks / Rugby", "North Downtown",
                                   "Locust Grove", "Jefferson Park Avenue", "Fifeville", "Fry's Spring",
                                   "Ridge Street", "Venable", "Belmont"]
HIST_NEIGHBORHOOD_TITLE = 'History of Residential Sales:'

layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            dbc.Button("☰", id='nbc_sidebar_button', className="background2 left_text title", 
                       style={"margin-left": "0"}),
            dbc.Collapse(
                [
                    dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['SECTOR'], href="#hood_cvillepedia", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['HIST'], href="#ind_neighborhood_plot", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['CENSUS'], 
                                            href="#history_neighborhood_price_plot", 
                                            external_link=True, 
                                            className="background2 left_text subtitle")),
                ], id="nbc_sidebar", is_open=False, 
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
        html.H3(nbcd.text['MAIN_TITLE'], className = "center_text title"),
        # Neighborhood selector
        html.Div(
            [
                dcc.Checklist(options=checklist_neighborhood_lod_opts, 
                              value=checklist_neighborhood_lod_opts[0],
                              id="nbc_checklist")
            ], className="subcontainer"),
        # Industry chart
        html.Div(
            [
                dcc.Graph(id='ind_neighborhood_plot', style={'display': 'block'}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Age chart
        html.Div(
            [
                dcc.Graph(id='age_neighborhood_plot', style={'display': 'block'}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Race plot
        html.Div(
            [
                dcc.Graph(id='race_neighborhood_plot', style={'display': 'block'}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Income plot
        html.Div(
            [
                dcc.Graph(id='income_neighborhood_plot', style={'display': 'block'}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # History of price
        html.Div(
            [
                html.Span(HIST_NEIGHBORHOOD_TITLE, className="center_text subtitle"),
                dcc.Graph(id='history_neighborhood_num_plot', style={"width": "100%"},     
                          config={'displayModeBar': False}),
                dcc.Graph(id='history_neighborhood_price_plot', style={"width": "100%"},
                          config={'displayModeBar': False}),
            ], className="subcontainer"),
        dcc.Link('Take me home', href='/home'),
    ], className = "container background")


# Collapsable sidebar
@callback(Output("nbc_sidebar", "is_open"),
          [Input("nbc_sidebar_button", "n_clicks"), State("nbc_sidebar", "is_open")])
def hood_sidebar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

#@callback(
#    Output('hood_cvillepedia', 'children'),
#    Input('dropdown_neighborhood', 'value'))
#def printCvillepedia(hood):
#    i = 0
#    hoodLen = len(cv.dictionary[hood])
#    if hoodLen == 1:
#        return(cv.dictionary[hood][0])
#    else:
#        retParas = []
#        for paraIdx in range(hoodLen - 1):
#            retParas.append(cv.dictionary[hood][paraIdx])
#            retParas.append(html.Br())
#            retParas.append(html.Br())
#        retParas.append(cv.dictionary[hood][hoodLen - 1])
#        return(html.P(retParas))

#@callback(
#    Output('dropdown_neighborhood', 'value'),
#    Input('afford_map', 'clickData'))
#def printNeighborhood(clickData):
#    if clickData is None:
#        return dropdown_neighborhood_lod_opts[11]
#    return(str(clickData['points'][len(clickData['points']) - 1]['hovertext']))

#@callback(Output("history_neighborhood_num_plot", "figure"),
#          [Input("dropdown_neighborhood", "value"),])
#def history_neighborhood_num(neighs):
#    fig = go.Figure()
#    syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(neigh.encode('ascii')).decode('ascii') + ".pkl")
#    fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"]["count"] * 0.5, name=neigh))
#    fig.update_layout(xaxis_title="Year",
#                      yaxis_title="Yearly Number of Sales",
#                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
#                      plot_bgcolor="rgba(0,0,0,0)",
#                      paper_bgcolor="rgba(0,0,0,0)",
#                      autosize=True,
#                      font=dict(size=13, color="rgb(255,255,255)"))
#    fig['data'][0]['showlegend'] = True
#    return fig

#@callback(Output("history_neighborhood_price_plot", "figure"),
#          [Input("dropdown_neighborhood", "value"),])
#def history_neighborhood_price(neighs):
#    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["median"], 
#                                    name="All Sales"))
#    syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(neigh.encode('ascii')).decode('ascii') + ".pkl")
#    fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"]["median"], name=neigh))
#    fig.update_layout(xaxis_title="Year",
#                      yaxis_title="Yearly Median Sale Price [$, inflation adjusted]",
#                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
#                      plot_bgcolor="rgba(0,0,0,0)",
#                      paper_bgcolor="rgba(0,0,0,0)",
#                      autosize=True,
#                      font=dict(size=13, color="rgb(255,255,255)"))
#    fig['data'][0]['showlegend'] = True
#    return fig