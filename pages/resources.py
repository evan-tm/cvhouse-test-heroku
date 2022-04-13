# ------------------Neighborhood page------------------#
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.toolbarDescs as tb
import srcCode.resourcesDescs as rd
import srcCode.dashFuncs as df


layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            # dbc.Button("☰", id='rsrc_sidebar_button', className="background2 left_text title", 
            #            style={"margin-left": "0"}),
            # dbc.Collapse(
            #     [
            #         dbc.NavItem(dbc.NavLink(tb.opts['TOP'], href="#", external_link=True, 
            #                                 className="background2 left_text subtitle")),
            #     ], id="rsrc_sidebar", is_open=False, 
            #     style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            df.createTopBar()
        ], className="sidebar", color="#132C36"),
        html.H3(rd.text['MAIN_TITLE'], className = "center_text title"),
        html.Span(rd.text['SOURCES_HOOD'], className="left_text bodytext"), 
        html.Span(rd.text['THANKS'], className="left_text bodytext"), 
        html.A(rd.text['THANKSLINK'], href=rd.links['THANKS'], 
                target="_blank", className = "left_text links_text"),
        html.Span(rd.text["CVILLE_WEEKLY"], className="left_text bodytext"),
        html.A(rd.text['CVILLE_1'], href=rd.links['CVILLE_1'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['CVILLE_2'], href=rd.links['CVILLE_2'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['CVILLE_3'], href=rd.links['CVILLE_3'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['CVILLE_4'], href=rd.links['CVILLE_4'], 
                target="_blank", className = "left_text links_text"),
        html.Span(rd.text["CVILLEPEDIA"], className="left_text bodytext"),
        html.A(rd.text['CVP'], href=rd.links['CVP'], 
                target="_blank", className = "left_text links_text"),
        html.Span(rd.text["CVILLETOMORROW"], className="left_text bodytext"),
        html.A(rd.text['CVT_1'], href=rd.links['CVT_1'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['CVT_2'], href=rd.links['CVT_2'], 
                target="_blank", className = "left_text links_text"),
        html.Br(),
        html.Span(rd.text["AFFORD"], className="left_text bodytext"),
        html.A(rd.text['METHODS'], href=rd.links['METHODS'], 
                target="_blank", className = "left_text links_text"),
        html.Br(),
        html.Span(rd.text["CENSUS"], className="left_text bodytext"),
        html.A(rd.text['SEXBYAGE'], href=rd.links['SEXBYAGE'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['INCOME'], href=rd.links['INCOME'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['INDUSTRY'], href=rd.links['INDUSTRY'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['RACE'], href=rd.links['RACE'], 
                target="_blank", className = "left_text links_text"),
        html.Br(),
        html.Span(rd.text["SALES"], className="left_text bodytext"),
        html.A(rd.text['HISTORY'], href=rd.links['HISTORY'], 
                target="_blank", className = "left_text links_text"),
        html.Br(),
        html.Span(rd.text["QOL_MAP"], className="left_text bodytext"),
        html.A(rd.text['TRANSPORT'], href=rd.links['TRANSPORT'], 
                target="_blank", className = "left_text links_text"),
        html.A(rd.text['OPENST'], href=rd.links['OPENST'], 
                target="_blank", className = "left_text links_text"),
        html.Br(),
        #dcc.Link('Take me back up', href='#', className = "left_text links_text"),
    ], className = "container background")

# Collapsable sidebar
# @callback(Output("rsrc_sidebar", "is_open"),
#           [Input("rsrc_sidebar_button", "n_clicks"), State("rsrc_sidebar", "is_open")])
# def hood_sidebar_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open

