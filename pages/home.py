import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.homeDescs as hd
import srcCode.toolbarDescs as tb
import srcCode.affordFuncs as af
import srcCode.affordDescs as ad
import srcCode.dashFuncs as df
import srcCode.qolFuncs as qf
import srcCode.qolDescs as qd

dash.register_page(__name__, path='/')

# Neighborhood dropdown texts

layout = html.Div(
    [
    # Sidebar
    df.createTopBar(),
    #html.Br(),
    #html.Div(
    #    [
    #        html.Span([html.B(hd.text['MOBILE_DISCLAIMER']), 
    #                   html.Br(), hd.text['COPY']], 
    #                  id="copy_text", className="left_text bodytext"),
    #    ], className = "subcontainer"),
    #html.Hr(className="center_text title"),
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
                              'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                         'lasso2d', 'toImage'],
                              'scrollZoom': False},
                      style={"width": "100%", "height": "550px"}),
            # Affordability map
            dcc.Graph(id='results_map', 
                      config={'displayModeBar': True,
                              "displaylogo": False,
                              'modeBarButtonsToRemove': ['pan2d', 'select2d', 
                                                         'lasso2d', 'toImage'],
                              'scrollZoom': False},
                      style={'display': 'none', "width": "100%", "height": "550px"})
        ], className = "subcontainer"),
    # divider
    html.Hr(className="center_text title"),
    # Affordability calc title
    html.Span(ad.text['DD_MAIN_TITLE'], className="center_text title"),
    # Affordability calc subtitle
    df.createInlineLink(ad.text['DD_SUB_TITLE'], ad.text['DD_LINK'],
                        ad.links['METHOD']),
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
                              dd_style={"width": "150px", "height": "100px", 
                                        "display": "inline-block"},
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
            # type of childcare
            df.createDropdown(ad.text['DD_CC'], ad.opts['DD_CC'],
                              ad.default['DD_CC'], dd_id="afford_dropdown_childcare",
                              desc_id="afford_dropdown_cc_desc_id",
                              clearable=False, searchable=False),
            # transportation costs
            df.createDropdown(ad.text['DD_TRANSPORT'], ad.opts['DD_TRANSPORT'],
                              ad.default['DD_TRANSPORT'], dd_id="afford_dropdown_transport",
                              clearable=False, searchable=False),
            # vehicle type
            df.createDropdown(ad.text['DD_VEHICLE'], ad.opts['DD_VEHICLE'],
                              ad.default['DD_VEHICLE'], dd_id="afford_dropdown_vehicle",
                              desc_id="afford_dropdown_vehicle_desc_id", clearable=False,
                              searchable=False),
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
                              clearable=False, searchable=False),
            html.Button(ad.text['CALC_BUTTON'], id="afford_button", className="center_text subtitle",
                                style={"background-color": "#e96a26", "color": "#FFFFFF",
                                       'border': '0', 'width': '150px'}),
        ], className="subcontainer"),
    html.Div(
        [
            html.Div(ad.text['LOADING'], id="afford_result", 
                     className="center_text subtitle"),
        ], className = "subcontainer"),
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
    elif currentMap == optsMap[2]:
        return qf.plotTreeMap()
    else:
        return currentResultsFig
