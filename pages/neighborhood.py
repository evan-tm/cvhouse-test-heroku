# ------------------Neighborhood page------------------#
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import srcCode.toolbarDescs as tb
import srcCode.neighborhoodDescs as nd
import srcCode.dashFuncs as df
import srcCode.cvillepedia as cv
import srcCode.censusFuncs as cf
import srcCode.historyFuncs as hf

dash.register_page(__name__)

## Gets the correct description from the cvillepedia file (written by Erin)
## in: neighborhood
## out: html formatted text with neighborhood description
def getCvillepedia(n):
    if n is None:
        n = nd.default['DROPDOWN_NEIGHBORHOOD']
    nLen = len(cv.dictionary[n])
    if nLen == 1:
        return(cv.dictionary[n][0])
    else:
        retParas = []
        for paraIdx in range(nLen - 1):
            retParas.append(cv.dictionary[n][paraIdx])
            retParas.append(html.Br())
            retParas.append(html.Br())
        retParas.append(cv.dictionary[n][nLen - 1])
        return(html.P(retParas))

def layout(id=None):
    if id is not None:
        id = id.replace('_', ' ')
        if id in nd.opts['DROPDOWN_NEIGHBORHOOD']:
            return html.Div(
            [
                html.Div(
                    [
                        # Neighborhood dropdown
                        html.Div([
                            df.createDropdown(nd.text['DROPDOWN_NEIGHBORHOOD'], nd.opts['DROPDOWN_NEIGHBORHOOD'],
                                            id, dd_id="dropdown_neighborhood",
                                            dd_style={"display": "none"}, grid_width="1fr", clearable=False),
                        ], className="neighborhood_drop"),
                    ], className = "subcontainer"),
                # Population census charts
                html.Div([
                    df.createLeftAlignDropdown(nd.text['DROPDOWN_CENSUS'], nd.opts['DROPDOWN_CENSUS'],
                                    nd.default['DROPDOWN_CENSUS'], dd_id='dropdown_neighborhood_census',
                                    dd_style={'width': '175px'}, grid_class="grid_dd2",
                                    desc_id='dd_neighborhood_census_text',
                                    clearable=False, searchable=False),
                ], className = "subcontainer"),
                html.Div(
                    [
                        dcc.Graph(id='census_neighborhood_plot', 
                                figure=cf.plotIndustryByNeighborhood(id),
                                config={'displayModeBar': True,
                                    "displaylogo": False,
                                    'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                                'lasso2d', 'zoom2d',
                                                                'zoomIn2d', 'zoomOut2d',
                                                                'autoScale2d']},
                                style={'display': 'block'})
                    ], className="subcontainer"),
                html.Br(),
                html.Br(),
                # Household census charts
                html.Div([
                    df.createLeftAlignDropdown(nd.text['DROPDOWN_CENSUS_HH'], nd.opts['DROPDOWN_CENSUS_HH'],
                                    nd.default['DROPDOWN_CENSUS_HH'], dd_id='dropdown_neighborhood_census_hh',
                                    dd_style={'width': '175px'}, grid_class="grid_dd2",
                                    desc_id='dd_neighborhood_census_hh_text',
                                    clearable=False, searchable=False),
                ], className = "subcontainer"),
                html.Div(
                    [
                        dcc.Graph(id='census_hh_neighborhood_plot', 
                                figure=cf.plotIncomeNeighborhood(id),
                                config={'displayModeBar': True,
                                    "displaylogo": False,
                                    'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                                'lasso2d', 'zoom2d',
                                                                'zoomIn2d', 'zoomOut2d',
                                                                'autoScale2d']},
                                style={'display': 'block'})
                    ], className="subcontainer"),
                html.Br(),
                html.Br(),
                # History of price
                html.Div([
                    df.createLeftAlignDropdown(nd.text['HISTORY_TITLE'], nd.opts['DROPDOWN_HISTORY'],
                                    nd.default['DROPDOWN_HISTORY'], dd_id='dropdown_neighborhood_history',
                                    dd_style={'width': '150px'}, grid_class="grid_dd2",
                                    clearable=False, searchable=False),
                ], className = "subcontainer"),
                html.Div(
                    [
                        dcc.Graph(id='neighborhood_price_history_plot', 
                                figure=hf.plotNeighborhoodHistorySales(id, nd.default['DROPDOWN_HISTORY']),
                                style={"width": "100%"}, 
                                config={'displayModeBar': True,
                                    "displaylogo": False,
                                    'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                                'lasso2d', 'zoom2d',
                                                                'zoomIn2d', 'zoomOut2d',
                                                                'autoScale2d']}),
                        dcc.Graph(id='neighborhood_quant_history_plot', 
                                figure=hf.plotNeighborhoodHistorySales(id, nd.opts['DROPDOWN_HISTORY'][1]),
                                style={"width": "100%"}, 
                                config={'displayModeBar': True,
                                    "displaylogo": False,
                                    'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                                'lasso2d', 'zoom2d',
                                                                'zoomIn2d', 'zoomOut2d',
                                                                'autoScale2d']})
                    ], className="subcontainer"),
            ], className = "container background")
    return html.Div(
    [
        # Sidebar
        df.createTopBar(),
        #html.Br(),
        #html.H3(nd.text['MAIN_TITLE'], className = "center_text title"),
        html.Div(
            [
                # Neighborhood dropdown
                html.Div([
                    df.createDropdown(nd.text['DROPDOWN_NEIGHBORHOOD'], nd.opts['DROPDOWN_NEIGHBORHOOD'],
                                    nd.default['DROPDOWN_NEIGHBORHOOD'], dd_id="dropdown_neighborhood",
                                    dd_style={"width": "200px"}, grid_width="1fr", clearable=False),
                ], className="neighborhood_drop"),
                # Neighborhood CVillepedia description
                #html.Div(getCvillepedia(nd.default['DROPDOWN_NEIGHBORHOOD']), id="neighborhood_cvillepedia", className="left_text bodytext"),
            ], className = "subcontainer"),
        html.Br(),
        html.Br(),
        # Population census charts
        html.Div([
            df.createLeftAlignDropdown(nd.text['DROPDOWN_CENSUS'], nd.opts['DROPDOWN_CENSUS'],
                            nd.default['DROPDOWN_CENSUS'], dd_id='dropdown_neighborhood_census',
                            dd_style={'width': '175px'}, grid_class="grid_dd2",
                            desc_id='dd_neighborhood_census_text',
                            clearable=False, searchable=False),
        ], className = "subcontainer"),
        html.Div(
            [
                dcc.Graph(id='census_neighborhood_plot', 
                        figure=cf.plotIndustryByNeighborhood(nd.default['DROPDOWN_NEIGHBORHOOD']),
                        config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                        style={'display': 'block'})
            ], className="subcontainer"),
        html.Br(),
        html.Br(),
        # Household census charts
        html.Div([
            df.createLeftAlignDropdown(nd.text['DROPDOWN_CENSUS_HH'], nd.opts['DROPDOWN_CENSUS_HH'],
                            nd.default['DROPDOWN_CENSUS_HH'], dd_id='dropdown_neighborhood_census_hh',
                            dd_style={'width': '175px'}, grid_class="grid_dd2",
                            desc_id='dd_neighborhood_census_hh_text',
                            clearable=False, searchable=False),
        ], className = "subcontainer"),
        html.Div(
            [
                dcc.Graph(id='census_hh_neighborhood_plot', 
                        figure=cf.plotIncomeNeighborhood(nd.default['DROPDOWN_NEIGHBORHOOD']),
                        config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']},
                        style={'display': 'block'})
            ], className="subcontainer"),
        html.Br(),
        html.Br(),
        # History of price
        html.Div([
            df.createLeftAlignDropdown(nd.text['HISTORY_TITLE'], nd.opts['DROPDOWN_HISTORY'],
                            nd.default['DROPDOWN_HISTORY'], dd_id='dropdown_neighborhood_history',
                            dd_style={'width': '150px'}, grid_class="grid_dd2",
                            clearable=False, searchable=False),
        ], className = "subcontainer"),
        html.Div(
            [
                dcc.Graph(id='neighborhood_price_history_plot', 
                        figure=hf.plotNeighborhoodHistorySales(nd.default['DROPDOWN_NEIGHBORHOOD'], nd.default['DROPDOWN_HISTORY']),
                        style={"width": "100%"}, 
                        config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']}),
                dcc.Graph(id='neighborhood_quant_history_plot', 
                        figure=hf.plotNeighborhoodHistorySales(nd.default['DROPDOWN_NEIGHBORHOOD'], nd.opts['DROPDOWN_HISTORY'][1]),
                        style={"width": "100%"}, 
                        config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                        'lasso2d', 'zoom2d',
                                                        'zoomIn2d', 'zoomOut2d',
                                                        'autoScale2d']})
            ], className="subcontainer"),
        #dcc.Link('Take me back up', href='#', className = "subcontainer inline_sublinks"),
        html.Br(),
        html.Br(),
    ], className = "container background")

@callback(
    Output('neighborhood_cvillepedia', 'children'),
    Input('dropdown_neighborhood', 'value'))
def printCvillepedia(n):
    return getCvillepedia(n)

@callback(
    Output('dd_neighborhood_census_text', 'children'),
    Output('dd_neighborhood_census_hh_text', 'children'),
    Input('dropdown_neighborhood', 'value'))
def update_neighborhood_texts(n):
    if n == 'Jefferson Park Avenue':
        return nd.text['DROPDOWN_CENSUS'].format('Jefferson Park Ave'), \
            nd.text['DROPDOWN_CENSUS_HH'].format('Jefferson Park Ave')
    return nd.text['DROPDOWN_CENSUS'].format(n), \
        nd.text['DROPDOWN_CENSUS_HH'].format(n)

@callback(
    Output('census_neighborhood_plot', 'figure'),
    Input('dropdown_neighborhood_census', 'value'), 
    Input('dropdown_neighborhood', 'value'))
def update_census_neighborhood_plot(censusSelection, n):
    if n is None:
        return cf.plotIndustryByNeighborhood(nd.default['DROPDOWN_NEIGHBORHOOD'])
    if censusSelection == nd.opts['DROPDOWN_CENSUS'][0]:
        return cf.plotAgeNeighborhood(n)
    elif censusSelection == nd.opts['DROPDOWN_CENSUS'][1]:
        return cf.plotIndustryByNeighborhood(n)
    elif censusSelection == nd.opts['DROPDOWN_CENSUS'][2]:
        return cf.plotRaceNeighborhood(n)
    else:
        return cf.plotSizeNeighborhood(n)

@callback(
    Output('census_hh_neighborhood_plot', 'figure'),
    Input('dropdown_neighborhood_census_hh', 'value'), 
    Input('dropdown_neighborhood', 'value'))
def update_census_hh_neighborhood_plot(censusSelection, n):
    if n is None:
        return cf.plotIncomeNeighborhood(nd.default['DROPDOWN_NEIGHBORHOOD'])
    if censusSelection == nd.opts['DROPDOWN_CENSUS_HH'][0]:
        return cf.plotIncomeNeighborhood(n)
    elif censusSelection == nd.opts['DROPDOWN_CENSUS_HH'][1]:
        return cf.plotIncomeDistNeighborhood(n)
    elif censusSelection == nd.opts['DROPDOWN_CENSUS_HH'][2]:
        return cf.plotOccupancyNeighborhood(n)
    else:
        return cf.plotTenureNeighborhood(n)

@callback(Output("neighborhood_price_history_plot", "figure"),
          Output("neighborhood_quant_history_plot", "figure"),
          [Input("dropdown_neighborhood", "value")])
def history_neighborhood_sales(neighs):
    fig1 = hf.plotNeighborhoodHistorySales(neighs, nd.default['DROPDOWN_HISTORY'])
    fig2 = hf.plotNeighborhoodHistorySales(neighs, nd.opts['DROPDOWN_HISTORY'][1])
    return fig1, fig2

@callback(Output("neighborhood_price_history_plot", "style"),
          Output("neighborhood_quant_history_plot", "style"),
          Input("dropdown_neighborhood_history", "value"))
def show_hide_history_plot(historySelection):
    if historySelection == nd.opts['DROPDOWN_HISTORY'][0]:
        return ({'display': 'block', "width": "100%"}, 
                {'display': 'none'})
    else:
        return ({'display': 'none'}, 
                {'display': 'block', "width": "100%"})
