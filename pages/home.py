from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.homeDescs as hd
import srcCode.toolbarDescs as tb
import srcCode.affordFuncs as af
import srcCode.affordDescs as ad
import srcCode.dashFuncs as df

# Neighborhood dropdown texts
dropdown_neighborhood = ""
dropdown_neighborhood_lod_opts = ["Barracks Road", "Rose Hill", "Lewis Mountain", "Starr Hill",
                                  "Woolen Mills", "10th & Page", "The Meadows", "Martha Jefferson",
                                  "Johnson Village", "Greenbrier", "Barracks / Rugby", "North Downtown",
                                  "Locust Grove", "Jefferson Park Avenue", "Fifeville", "Fry's Spring",
                                  "Ridge Street", "Venable", "Belmont"]
dropdown_neighborhood_default = dropdown_neighborhood_lod_opts[11]

layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            dbc.Button("☰", id='home_sidebar_button', className="background2 left_text title", 
                       style={"margin-left": "0"}),
            dbc.Collapse(
                [
                    dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
                                            className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(tb.opts['CENSUS'], href="#census_title", external_link=True, 
                                            className="background2 left_text subtitle")),
                ], id="home_sidebar", is_open=False, 
                style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            df.createTopBar()
        ], className="sidebar", color="#132C36", sticky="top"),
    html.H3(hd.text['MAIN_TITLE'], className = "center_text title"),
    html.Div(
        [
            html.Div(hd.text['COPY'], id="copy_text", className="left_text bodytext"),
        ], className = "subcontainer"),
    html.Hr(className="center_text title"),
    html.Span(ad.text['DD_MAIN_TITLE'], className="center_text subtitle"),
    html.Div(
            [
                # Neighborhood dropdown for industry chart
                html.Div([
                    df.createDropdown(dropdown_neighborhood, dropdown_neighborhood_lod_opts,
                                      dropdown_neighborhood_default, dd_id="dropdown_neighborhood",
                                      dd_style={"width": "200px"}, grid_width="1fr", clearable=False),
                ], className="neighborhood_drop"),
            ], className = "subcontainer"),
    html.Div(
        [
            # Personal information
            df.createInput(ad.text['IN_INCOME'], "number", ad.default['IN_INCOME'], 
                           ip_id="afford_input_salary"),
            df.createDropdown(ad.text['DD_PAY'], ad.opts['DD_PAY'],
                                          ad.default['DD_PAY'], dd_id="afford_dropdown_pay",
                                          clearable=False),
            df.createDropdown(ad.text['DD_HOMESIZE'], ad.opts['DD_HOMESIZE'],
                                          ad.default['DD_HOMESIZE'], dd_id="afford_dropdown_homeSize",
                                          desc_id="afford_dropdown_homeSize_desc_id", clearable=False),
            df.createNumericInput(ad.text['IN_ADULTS'], ad.default['IN_ADULTS'],
                                  minimum=1, maximum=10, ip_id="afford_input_adults"),
            df.createNumericInput(ad.text['IN_KIDS'], ad.default['IN_KIDS'], 
                                  maximum=10, ip_id="afford_input_kids"),
            df.createNumericInput(ad.text['IN_CC'], ad.default['IN_CC'], 
                                  maximum=10, ip_id="afford_input_childcare",
                                  desc_id = "afford_input_cc_desc_id"),
            df.createNumericInput(ad.text['IN_AGE'], ad.default['IN_AGE'],
                                  maximum=130, ip_id="afford_input_age"),
            df.createDropdown(ad.text['DD_TRANSPORT'], ad.opts['DD_TRANSPORT'],
                              ad.default['DD_TRANSPORT'], dd_id="afford_dropdown_transport",
                              clearable=False),
            df.createDropdown(ad.text['DD_VEHICLE'], ad.opts['DD_VEHICLE'],
                              ad.default['DD_VEHICLE'], dd_id="afford_dropdown_vehicle",
                              desc_id="afford_dropdown_vehicle_desc_id", clearable=False),
            df.createInput(ad.text['IN_HCARE'], "number", ad.default['IN_HCARE'],
                           ip_id="afford_input_hcare"),
            df.createNumericInput(ad.text['IN_TECH'], ad.default['IN_TECH'],
                                  maximum=1000, ip_id="afford_input_tech"),
            dbc.Tooltip(ad.ttips['IN_TECH'], target="afford_input_tech", 
                        placement='bottom'),
            df.createDropdown(ad.text['DD_TAX'], ad.opts['DD_TAX'],
                              ad.default['DD_TAX'], dd_id="afford_dropdown_tax",
                              clearable=False),
            html.Button(ad.text['CALC_BUTTON'], id="afford_button", className="right_text subtitle",
                                style={"background-color": "#FFA858", "color": "#000000"}),
        ], className="subcontainer"),
    html.Div(ad.text['LOADING'], id="afford_result", className="center_text subtitle"),
    ], className = "container background")

# Collapsable sidebar
@callback(Output("home_sidebar", "is_open"),
          [Input("home_sidebar_button", "n_clicks"), State("home_sidebar", "is_open")])
def home_sidebar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open