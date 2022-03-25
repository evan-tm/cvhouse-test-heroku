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
neighborhood_list = ["Barracks Road", "Rose Hill", "Lewis Mountain", "Starr Hill",
                     "Woolen Mills", "10th & Page", "The Meadows", "Martha Jefferson",
                     "Johnson Village", "Greenbrier", "Barracks / Rugby", "North Downtown",
                     "Locust Grove", "Jefferson Park Avenue", "Fifeville", "Fry's Spring",
                     "Ridge Street", "Venable", "Belmont"]
checklist_nbc_opts = [{"value": each, "label": each} for each in neighborhood_list]
max_selected_checklist = 2
dropdown_nbc_history_opts = ["Number of Sales", "Median Price"]

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
            df.createTopBar()
        ], className="sidebar", color="#132C36", sticky="top"),
        html.H3(nbcd.text['MAIN_TITLE'], className = "center_text title"),
        # Neighborhood selector
        html.Div(
            [
                dcc.Checklist(options=checklist_nbc_opts, 
                              value=[], id="nbc_checklist", className="center_text bodytext", style={'width':'50%'},
                              inputStyle={"margin-left": "20px", "margin-right": "5px"}),
                html.Button(nbcd.text['COMPARE_BUTTON'], id="compare_button", className="center_text bodytext",
                            style={"background-color": "#FFA858", "color": "#000000"}),
                html.Span(id="compare_warning", className="center_text subtitle"),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        html.Div(
            [
                html.Span(nbcd.text["COMPARE_DISCLAIMER"], className="left_text bodytext"),
            ], className="subcontainer"),
        # Neighborhood name
        html.Div(className="grid_container", id="nbc_names",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Industry chart
        html.Div(className="grid_container", id="nbc_ind_plots", 
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Age chart
        html.Div(className="grid_container", id="nbc_age_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Race plot
        html.Div(className="grid_container", id="nbc_race_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Income plot
        html.Div(className="grid_container", id="nbc_income_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # History of price
        html.Div(
            [
                html.Span(nbcd.text["HIST_NEIGHBORHOOD_TITLE"], className="center_text subtitle"),
                df.createDropdown("", dropdown_nbc_history_opts,
                                  dropdown_nbc_history_opts[0], dd_id="dropdown_nbc_history",
                                  dd_style={"width": "200px"}, clearable=False),
                dcc.Graph(id='nbc_history_plot', style={"width": "100%"}, config={'displayModeBar': False}),
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

# Limit comparison
@callback(Output("nbc_checklist", "options"),
          Input("nbc_checklist", "value"))
def update_multi_options(value):
    options = checklist_nbc_opts
    if len(value) >= max_selected_checklist:
        options = [
            {
                "label": option["label"],
                "value": option["value"],
                "disabled": option["value"] not in value,
            }
            for option in options
        ]
    return options

# Warning when only one is chosen
#@callback(Output("compare_warning", "children"),
#          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
#def check_num_selected(n, value):
#    if n and (len(value) < 2):
#        return "Please select at least 2 neighborhoods to compare."
#    else:
#        return ""
    

@callback(Output("nbc_names", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_names(n, value):
    ind_plots = []
    if n:
        if len(value) == 0:
            ind_plots.append(html.Span(nbcd.text["NoSelectionWarning"], className="center_text subtitle"))
        for each in value:
            ind_plots.append(html.Span(each, className="center_text subtitle"))
    else:
        ind_plots.append(html.Span(nbcd.text["NoSelectionWarning"], className="center_text subtitle"))
    return ind_plots


@callback(Output("nbc_ind_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_ind_plots(n, value):
    ind_plots = []
    if n:
        for each in value:
            ind_plots.append(dcc.Graph(figure=cf.plotIndustryByNeighborhood(each), style={'display': 'block'}))
    return ind_plots


@callback(Output("nbc_age_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_age_plots(n, value):
    ind_plots = []
    if n:
        for each in value:
            ind_plots.append(dcc.Graph(figure=cf.plotAgeNeighborhood(each), style={'display': 'block'}))
    return ind_plots


@callback(Output("nbc_race_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_race_plots(n, value):
    ind_plots = []
    if n:
        for each in value:
            ind_plots.append(dcc.Graph(figure=cf.plotRaceNeighborhood(each), style={'display': 'block'}))
    return ind_plots


@callback(Output("nbc_income_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_race_plots(n, value):
    ind_plots = []
    if n:
        for each in value:
            ind_plots.append(dcc.Graph(figure=cf.plotIncomeNeighborhood(each), style={'display': 'block'}))
    return ind_plots


@callback(Output("nbc_history_plot", "figure"),
          [Input("compare_button", "n_clicks"), Input("dropdown_nbc_history", "value"), State("nbc_checklist", "value")])
def history_neighborhood_price(n, var, neighs):
    if var == "Number of Sales":
        to_plot = "count"
        y_label = "Yearly Number of Sales"
    else:
        to_plot = "median"
        y_label = "Yearly Median Sale Price [$, inflation adjusted]"
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"][to_plot], 
                                    name="Charlottesville City"))
    if n:
        for each in neighs:
            syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(each.encode('ascii')).decode('ascii') + ".pkl")
            fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"][to_plot], name=each))
    fig.update_layout(xaxis_title="Year",
                      yaxis_title=y_label,
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig