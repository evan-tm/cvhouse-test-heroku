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
        df.createTopBar(),
        html.Br(),
        html.H3(nbcd.text['MAIN_TITLE'], className = "center_text title"),
        # Neighborhood selector
        html.Div(
            [
                dcc.Checklist(options=checklist_nbc_opts, 
                              value=[], id="nbc_checklist", className="center_text bodytext", style={'width':'50%'},
                              inputStyle={"margin-left": "20px", "margin-right": "5px"}),
                html.Button(nbcd.text['COMPARE_BUTTON'], id="compare_button", className="center_text bodytext",
                            style={"background-color": "#e96a26", "color": "#FFFFFF"}),
                html.Span(id="compare_warning", className="center_text subtitle"),
            ], className="subcontainer"),
        html.Div(
            [
                html.Span(nbcd.text["COMPARE_DISCLAIMER"], className="center_text bodytext"),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
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
        # Size plot
        html.Div(className="grid_container", id="nbc_size_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Income plot
        html.Div(className="grid_container", id="nbc_income_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Occupancy plot
        html.Div(className="grid_container", id="nbc_occ_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Vacancy plot
        html.Div(className="grid_container", id="nbc_vac_plots",
                 style={"grid-template-columns": "minmax(600px, 1fr) minmax(600px, 1fr)"}),
        html.Hr(className="center_text title"),
        # Size plot
        html.Div(
            [
                dcc.Graph(id='nbc_size_plot', 
                          figure=cf.plotSizeCity(),
                          style={"width": "100%"}, 
                          config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # History of price
        html.Div([
            df.createLeftAlignDropdown(nbcd.text['HIST_NEIGHBORHOOD_TITLE'], nbcd.opts['DROPDOWN_HISTORY'],
                            nbcd.default['DROPDOWN_HISTORY'], dd_id='dropdown_nbc_history',
                            dd_style={'width': '150px'}, grid_class="grid_dd2",
                            clearable=False, searchable=False),
        ], className = "subcontainer"),
        html.Div(
            [
                dcc.Graph(id='nbc_history_plot', 
                          figure=hf.plotCompareHistorySales(0, nbcd.default['DROPDOWN_HISTORY'], ''),
                          style={"width": "100%"}, 
                          config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']}),
            ], className="subcontainer"),
        dcc.Link('Take me back up', href='#', className = "subcontainer inline_sublinks"),
        html.Br(),
        html.Br(),
    ], className = "container background")

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
        for ind, each in enumerate(value):
            ind_plots.append(dcc.Graph(id=('nbc_' + str(ind) + '_ind'),
                            figure=cf.plotIndustryByNeighborhood(each, True), 
                            config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                             style={'display': 'block'}))
    return ind_plots


@callback(Output("nbc_age_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_age_plots(n, value):
    age_plots = []
    if n:
        for ind, each in enumerate(value):
            age_plots.append(dcc.Graph(id=('nbc_' + str(ind) + '_age'),
                            figure=cf.plotAgeNeighborhood(each), 
                            config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                                       style={'display': 'block'}))
    return age_plots


@callback(Output("nbc_race_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_race_plots(n, value):
    race_plots = []
    if n:
        for ind, each in enumerate(value):
            race_plots.append(dcc.Graph(id=('nbc_' + str(ind) + '_race'),
                            figure=cf.plotRaceNeighborhood(each, True), 
                            config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                              style={'display': 'block'}))
    return race_plots


@callback(Output("nbc_income_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_income_plots(n, value):
    income_plots = []
    if n:
        for ind, each in enumerate(value):
            income_plots.append(dcc.Graph(id=('nbc_' + str(ind) + '_income'),
                                figure=cf.plotIncomeNeighborhood(each, True), 
                                config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                                style={'display': 'block'}))
    return income_plots


@callback(Output("nbc_occ_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_occ_plots(n, value):
    occ_plots = []
    if n:
        for ind, each in enumerate(value):
            occ_plots.append(dcc.Graph(id=('nbc_' + str(ind) + '_occ'),
                                figure=cf.plotOccupancyNeighborhood(each), 
                                config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                                style={'display': 'block'}))
    return occ_plots


@callback(Output("nbc_vac_plots", "children"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def nbc_vac_plots(n, value):
    vac_plots = []
    if n:
        for ind, each in enumerate(value):
            vac_plots.append(dcc.Graph(id=('nbc_' + str(ind) + '_vac'),
                                figure=cf.plotTenureNeighborhood(each), 
                                config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                                style={'display': 'block'}))
    return vac_plots


@callback(Output("nbc_size_plot", "figure"),
          [Input("compare_button", "n_clicks"), State("nbc_checklist", "value")])
def update_size_plot(n, neighs):
    if n:
        return cf.plotSizeNeighborhood(neighs)
    else:
        return cf.plotSizeCity()


@callback(Output("nbc_history_plot", "figure"),
          [Input("compare_button", "n_clicks"), Input("dropdown_nbc_history", "value"), State("nbc_checklist", "value")])
def history_neighborhood_price(n, var, neighs):
    return hf.plotCompareHistorySales(n, var, neighs)