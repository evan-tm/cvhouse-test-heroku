# ------------------Contact page----------------------#
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.toolbarDescs as tb
import srcCode.contactDescs as cd
import srcCode.dashFuncs as df


layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            df.createTopBar()
        ], className="sidebar", color="#132C36"),
        html.Div(
        [
                html.H3(cd.text['MAIN_TITLE'], className = "center_text title"),
                html.Br(),
                html.Div([
                    html.A([
                        html.Img(src = 'assets/spencer.jpg', style={'height':'150px', 'width': '150px'}, 
                                 className="circular--square"),
                    ], href=cd.links['SPENCER'], target="_blank", className = "ctct_elem1"),
                    html.A([
                        html.Img(src = 'assets/xinlun.jpg', style={'height':'150px', 'width': '150px'}, 
                                 className="circular--square"),
                    ], href=cd.links['XINLUN'], target="_blank", className = "ctct_elem2"),
                    html.A([
                        html.Img(src = 'assets/malvika.jpg', style={'height':'150px', 'width': '150px'}, 
                                 className="circular--square"),
                    ], href=cd.links['MALVIKA'], target="_blank", className = "ctct_elem3"),
                    html.A([
                        html.Img(src = 'assets/evan.jpg', style={'height':'150px', 'width': '150px'}, 
                                 className="circular--square"),
                    ], href=cd.links['EVAN'], target="_blank", className = "ctct_elem4"),
                ], className = "grid_contact"),
                html.Div([
                    html.Span(cd.text['SPENCER'], className="ctct_elem1 center_text bodytext"),
                    html.Span(cd.text['XINLUN'], className="ctct_elem2 center_text bodytext"),
                    html.Span(cd.text['MALVIKA'], className="ctct_elem3 center_text bodytext"),
                    html.Span(cd.text['EVAN'], className="ctct_elem4 center_text bodytext"),
                ], className = "grid_contact"),
                html.Div([
                    html.Span(cd.text['STUDENT'], className="ctct_elem1 center_text bodytext"),
                    html.Span(cd.text['STUDENT'], className="ctct_elem2 center_text bodytext"),
                    html.Span(cd.text['STUDENT'], className="ctct_elem3 center_text bodytext"),
                    html.Span(cd.text['STUDENT'], className="ctct_elem4 center_text bodytext"),
                ], className = "grid_contact"),
                html.Br(),
                html.Br(),
                html.Div([
                    html.A([
                        html.Img(src = 'assets/kropko.jpg', style={'height':'150px', 'width': '150px'}, 
                                 className="circular--square"),
                    ], href=cd.links['KROPKO'], target="_blank", className = "ctct_elem2"),
                    html.A([
                        html.Img(src = 'assets/erin.jpg', style={'height':'150px', 'width': '150px'}, 
                                 className="circular--square"),
                    ], href=cd.links['ERIN'], target="_blank", className = "ctct_elem3"),
                ], className = "grid_contact"),
                html.Div([
                    html.Span(cd.text['KROPKO'], className="ctct_elem2 center_text bodytext"),
                    html.Span(cd.text['ERIN'], className="ctct_elem3 center_text bodytext"),
                ], className = "grid_contact"),
                html.Div([
                    html.Span(cd.text['ADVISOR'], className="ctct_elem2 center_text bodytext"),
                    html.Span(cd.text['SPONSOR'], className="ctct_elem3 center_text bodytext"),
                ], className = "grid_contact"),
                html.Br(),
                html.Span(cd.text['TEAM'], className="center_text subtitle"),
                html.Br(),
                html.Br(),
                html.H3(cd.text['SUPPORT'], className = "center_text title"),
                html.Br(),
                html.A(cd.text['ISSUES'], href=cd.links['ISSUES'], target="_blank",
                       className = "center_text links_text"),
                html.Br(),
                html.Br(),
                #dcc.Link('Take me back up', href='#', className = "left_text links_text"),
        ], className = "subcontainer")
    ], className = "container background")
