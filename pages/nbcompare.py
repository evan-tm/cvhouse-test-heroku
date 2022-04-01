# ------------------Neighborhood page------------------#
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.toolbarDescs as tb
import srcCode.nbcDescs as nbcd
import srcCode.dashFuncs as df
import srcCode.cvillepedia as cv
import srcCode.censusFuncs as cf
import srcCode.historyFuncs as hf
#------------------------------------------------------------------------------
# Neighborhood dropdown texts
checklist_nbc_opts = [{"value": each, "label": each} for each in nbcd.opts['DROPDOWN_NEIGHBORHOOD']]
max_selected_checklist = 2

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
                df.createDropdown(nbcd.text['DROPDOWN_HISTORY'], nbcd.opts['DROPDOWN_HISTORY'],
                                  nbcd.default['DROPDOWN_HISTORY'], dd_id="dropdown_nbc_history",
                                  dd_style={"width": "200px"}, clearable=False, searchable = False),
                dcc.Graph(id='nbc_history_plot', 
                          figure=hf.plotCompareHistorySales(0, nbcd.default['DROPDOWN_HISTORY'], ''),
                          style={"width": "100%"}, 
                          config={'displayModeBar': False}),
            ], className="subcontainer"),
        dcc.Link('Take me back up', href='#'),
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
def nbc_industry_plots(n, value):
    ind_plots = []
    if n:
        for each in value:
            ind_plots.append(dcc.Graph(figure=cf.plotIndustryByNeighborhood(each), 
                             config={'displayModeBar': False},
                             style={'display': 'block'}))
    return ind_plots


@callback(Output("nbc_age_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_age_plots(n, value):
    age_plots = []
    if n:
        for each in value:
            age_plots.append(dcc.Graph(figure=cf.plotAgeNeighborhood(each), 
                                       config={'displayModeBar': False},
                                       style={'display': 'block'}))
    return age_plots


@callback(Output("nbc_race_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_race_plots(n, value):
    race_plots = []
    if n:
        for each in value:
            race_plots.append(dcc.Graph(figure=cf.plotRaceNeighborhood(each), 
                              config={'displayModeBar': False},
                              style={'display': 'block'}))
    return race_plots


@callback(Output("nbc_income_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_income_plots(n, value):
    income_plots = []
    if n:
        for each in value:
            income_plots.append(dcc.Graph(figure=cf.plotIncomeNeighborhood(each), 
                                config={'displayModeBar': False},
                                style={'display': 'block'}))
    return income_plots


@callback(Output("nbc_history_plot", "figure"),
          [Input("compare_button", "n_clicks"), Input("dropdown_nbc_history", "value"), State("nbc_checklist", "value")])
def history_neighborhood_price(n, var, neighs):
    return hf.plotCompareHistorySales(n, var, neighs)