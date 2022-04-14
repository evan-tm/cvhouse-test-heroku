from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.homeDescs as hd
import srcCode.toolbarDescs as tb
import srcCode.affordFuncs as af
import srcCode.affordDescs as ad
import srcCode.dashFuncs as df
import srcCode.qolFuncs as qf
import srcCode.qolDescs as qd

# Neighborhood dropdown texts

layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            #dbc.Button("☰", id='home_sidebar_button', className="background2 left_text title", 
            #           style={"margin-left": "0"}),
            # dbc.Collapse(
            #     [
            #         dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
            #                                className="background2 left_text subtitle")),
            #         dbc.NavItem(dbc.NavLink(tb.opts['CENSUS'], href="#census_title", external_link=True, 
            #                                 className="background2 left_text subtitle")),
            #     ], id="home_sidebar", is_open=False, 
            #     style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            df.createTopBar()
        ], className="sidebar", color="#132C36"),
    #html.H3(hd.text['MAIN_TITLE'], className = "center_text title"),
    html.Div(
        [
            html.Div(hd.text['COPY'], id="copy_text", className="left_text bodytext"),
        ], className = "subcontainer"),
    html.Hr(className="center_text title"),
    html.Div([
        df.createLeftAlignDropdown(qd.text['DD_QOL'], qd.opts['DD_QOL'],
                          qd.default['DD_QOL'], dd_id='qol_dropdown',
                          dd_style={'width': '150px'}, 
                          clearable=False, searchable=False),
    ], className = "subcontainer"),
    # quality of life map
    html.Div(
        [
            # QoL map
            dcc.Graph(id='qol_map', 
                      figure=qf.plotResourcesMap(), 
                      config={'displayModeBar': True,
                              "displaylogo": False,
                              'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d']},
                      style={"width": "100%", "height": "550px"}),
            # School map
            # dcc.Graph(id='school_map', 
            #           figure=qf.plotSchoolMap(), 
            #           config={'displayModeBar': True,
            #                   "displaylogo": False,
            #                   'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d']},
            #           style={'diplay': 'block', "width": "100%", "height": "550px"}),
            # Affordability map
            dcc.Graph(id='results_map', 
                      config={'displayModeBar': True,
                              "displaylogo": False,
                              'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d']},
                      style={'display': 'none', "width": "100%", "height": "550px"})
        ], className = "subcontainer"),
    html.Hr(className="center_text title"),
    html.Span(ad.text['DD_MAIN_TITLE'], className="center_text title"),
    # html.Div(
    #         [
    #             # Neighborhood dropdown
    #             html.Div([
    #                 df.createDropdown(hd.text['DROPDOWN_NEIGHBORHOOD'], hd.opts['DROPDOWN_NEIGHBORHOOD'],
    #                                   hd.default['DROPDOWN_NEIGHBORHOOD'], dd_id="dropdown_neighborhood",
    #                                   dd_style={"width": "200px"}, grid_width="1fr", clearable=False),
    #             ], className="neighborhood_drop"),
    #         ], className = "subcontainer"),
    html.Div(
        [
            # Personal information
            # income
            df.createInput(ad.text['IN_INCOME'], "number", ad.default['IN_INCOME'], 
                           ip_id="afford_input_salary"),
            dbc.Tooltip(ad.ttips['IN_INCOME'], target="afford_input_salary", 
                        placement='bottom'),
            # ages of home residents
            df.createTagInput(ad.text['IN_AGE'], ad.default['IN_AGE'],
                              maximum=130, ip_id="afford_input_age",
                              button_desc="Add Person", button_id="age_button"),
            # Your household
            df.createDropdown(ad.text['DD_PEOPLE'], ad.opts['DD_PEOPLE'],
                              ad.default['DD_PEOPLE'], dd_id="afford_dropdown_people",
                              desc_id="afford_dropdown_people_desc_id", 
                              searchable = False, multi = True, clearable = False),
            # rent/buy
            df.createDropdown(ad.text['DD_PAY'], ad.opts['DD_PAY'],
                                          ad.default['DD_PAY'], dd_id="afford_dropdown_pay",
                                          clearable=False, searchable = False),
            # rental size
            df.createDropdown(ad.text['DD_HOMESIZE'], ad.opts['DD_HOMESIZE'],
                                          ad.default['DD_HOMESIZE'], dd_id="afford_dropdown_homeSize",
                                          desc_id="afford_dropdown_homeSize_desc_id", 
                                          clearable=False, searchable = False),
            # number of kids in childcare
            df.createNumericInput(ad.text['IN_CC'], ad.default['IN_CC'], 
                                  maximum=10, ip_id="afford_input_childcare",
                                  desc_id = "afford_input_cc_desc_id"),
            # transportation costs
            df.createDropdown(ad.text['DD_TRANSPORT'], ad.opts['DD_TRANSPORT'],
                              ad.default['DD_TRANSPORT'], dd_id="afford_dropdown_transport",
                              clearable=False),
            # vehicle type
            df.createDropdown(ad.text['DD_VEHICLE'], ad.opts['DD_VEHICLE'],
                              ad.default['DD_VEHICLE'], dd_id="afford_dropdown_vehicle",
                              desc_id="afford_dropdown_vehicle_desc_id", clearable=False),
            # healthcare costs
            df.createInput(ad.text['IN_HCARE'], "number", ad.default['IN_HCARE'],
                           ip_id="afford_input_hcare"),
            dbc.Tooltip(ad.ttips['IN_HCARE'], target="afford_input_hcare", 
                        placement='bottom'),
            # technology costs
            df.createNumericInput(ad.text['IN_TECH'], ad.default['IN_TECH'],
                                  maximum=1000, ip_id="afford_input_tech"),
            dbc.Tooltip(ad.ttips['IN_TECH'], target="afford_input_tech", 
                        placement='bottom'),
            # tax info
            df.createDropdown(ad.text['DD_TAX'], ad.opts['DD_TAX'],
                              ad.default['DD_TAX'], dd_id="afford_dropdown_tax",
                              clearable=False),
            html.Button(ad.text['CALC_BUTTON'], id="afford_button", className="right_text subtitle",
                                style={"background-color": "#FFE133", "color": "#000000"}),
        ], className="subcontainer"),
    html.Div(ad.text['LOADING'], id="afford_result", className="center_text subtitle"),
    html.Br(),
    ], className = "container background")

@callback(
   Output(component_id='qol_map', component_property='figure'),
   [Input(component_id='qol_dropdown', component_property='value'),
    Input('results_map', 'figure'),
    Input('afford_button', 'n_clicks')])
def show_hide_qol_map(currentMap, currentResultsFig, n):

    optsMap = qd.opts['DD_QOL']
    if currentMap == optsMap[0]:
        return qf.plotResourcesMap()
    elif currentMap == optsMap[1]:
        return qf.plotSchoolMap()
    else:
        return currentResultsFig

# Collapsable sidebar
# @callback(Output("home_sidebar", "is_open"),
#           [Input("home_sidebar_button", "n_clicks"), State("home_sidebar", "is_open")])
# def home_sidebar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

#@callback(
#    Output('dropdown_neighborhood', 'value'),
#    Input('qol_map', 'clickData'))
#def printNeighborhood(clickData):
#    if clickData is None:
#        return hd.default['DROPDOWN_NEIGHBORHOOD']
#    return(str(clickData['points'][len(clickData['points']) - 1]['hovertext']))
