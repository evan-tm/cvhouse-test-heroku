# ------------------Neighborhood page------------------#
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import pandas as pd
import srcCode.toolbarDescs as tb
import srcCode.neighborhoodDescs as nd
import srcCode.dashFuncs as df
import srcCode.cvillepedia as cv
import srcCode.censusFuncs as cf
import srcCode.historyFuncs as hf

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

layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            # dbc.Button("☰", id='hood_sidebar_button', className="background2 left_text title", 
            #            style={"margin-left": "0"}),
            # dbc.Collapse(
            #     [
            #         dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
            #                                 className="background2 left_text subtitle")),
            #         dbc.NavItem(dbc.NavLink(tb.opts['CENSUS'], href="#dropdown_neighborhood_census", external_link=True, 
            #                                 className="background2 left_text subtitle")),
            #         dbc.NavItem(dbc.NavLink(tb.opts['HIST'], href="#dropdown_neighborhood_history", external_link=True, 
            #                                 className="background2 left_text subtitle")),
            #     ], id="hood_sidebar", is_open=False, 
            #     style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            df.createTopBar()
        ], className="sidebar", color="#132C36"),
        html.H3(nd.text['MAIN_TITLE'], className = "center_text title"),
        html.Div(
            [
                # Neighborhood dropdown
                html.Div([
                    df.createDropdown(nd.text['DROPDOWN_NEIGHBORHOOD'], nd.opts['DROPDOWN_NEIGHBORHOOD'],
                                      nd.default['DROPDOWN_NEIGHBORHOOD'], dd_id="dropdown_neighborhood",
                                      dd_style={"width": "200px"}, grid_width="1fr", clearable=False),
                ], className="neighborhood_drop"),
                # Neighborhood CVillepedia description
                html.Div(getCvillepedia(nd.default['DROPDOWN_NEIGHBORHOOD']), id="neighborhood_cvillepedia", className="left_text bodytext"),
            ], className = "subcontainer"),
        # Census charts
        html.Div(
            [
                # dropdown for census selection
                df.createDropdown(nd.text['DROPDOWN_CENSUS'], nd.opts['DROPDOWN_CENSUS'],
                                  nd.default['DROPDOWN_CENSUS'], dd_id="dropdown_neighborhood_census",
                                  dd_style={"width": "200px"}, clearable=False, searchable = False),
                dcc.Graph(id='census_neighborhood_plot', 
                          figure=cf.plotIndustryByNeighborhood(nd.default['DROPDOWN_NEIGHBORHOOD']),
                          config={'displayModeBar': False},
                          style={'display': 'block'})
            ], className="subcontainer"),
        html.Br(),
        # History of price
        html.Div(
            [
                html.Span(nd.text['HISTORY_TITLE'], className="center_text subtitle"),
                df.createDropdown(nd.text['DROPDOWN_HISTORY'], nd.opts['DROPDOWN_HISTORY'],
                                  nd.default['DROPDOWN_HISTORY'], dd_id="dropdown_neighborhood_history",
                                  dd_style={"width": "200px"}, clearable=False),
                dcc.Graph(id='neighborhood_history_plot', 
                          figure=hf.plotNeighborhoodHistorySales(nd.default['DROPDOWN_NEIGHBORHOOD'], nd.default['DROPDOWN_HISTORY']),
                          style={"width": "100%"}, 
                          config={'displayModeBar': False}),
            ], className="subcontainer"),
        dcc.Link('Take me back up', href='#'),
    ], className = "container background")

# Collapsable sidebar
# @callback(Output("hood_sidebar", "is_open"),
#           [Input("hood_sidebar_button", "n_clicks"), State("hood_sidebar", "is_open")])
# def hood_sidebar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

@callback(
    Output('neighborhood_cvillepedia', 'children'),
    Input('dropdown_neighborhood', 'value'))
def printCvillepedia(n):
    return getCvillepedia(n)

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
        return cf.plotIncomeNeighborhood(n)
    elif censusSelection == nd.opts['DROPDOWN_CENSUS'][2]:
        return cf.plotIndustryByNeighborhood(n)
    else:
        return cf.plotRaceNeighborhood(n)

#@callback(
#    Output('dropdown_neighborhood', 'value'),
#    Input('afford_map', 'clickData'))
#def printNeighborhood(clickData):
#    if clickData is None:
#        return dropdown_neighborhood_lod_opts[11]
#    return(str(clickData['points'][len(clickData['points']) - 1]['hovertext']))

@callback(Output("neighborhood_history_plot", "figure"),
          [Input("dropdown_neighborhood", "value"), Input("dropdown_neighborhood_history", "value")])
def history_neighborhood_sales(neighs, var):
    return hf.plotNeighborhoodHistorySales(neighs, var)
