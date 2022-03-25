# ------------------General dash functions------------------#

# modules to import
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html, callback
import dash_bootstrap_components as dbc
import dash_daq as daq
import srcCode.toolbarDescs as tb


## Creates a Dash dropdown menu
def createDropdown(description, opts, default_value, 
                   dd_style={"width": "150px"}, dd_id=None, desc_id=None, 
                   grid_width="1fr 1fr", **kwargs):
    opts_dict = [{"label": each, "value": each} for each in opts]
    if desc_id:
        return html.Div([
            html.Span(description, id=desc_id, className="center_text bodytext"), 
            dcc.Dropdown(id=dd_id, options=opts_dict, value=default_value, className="subcontainer", 
            style=dd_style, **kwargs)
        ], className="grid_container", style={"grid-template-columns": grid_width})
    else:
        return html.Div([
            html.Span(description, className="center_text bodytext"),
            dcc.Dropdown(id=dd_id, options=opts_dict, value=default_value, className="subcontainer", 
            style=dd_style, **kwargs)
        ], className="grid_container", style={"grid-template-columns": grid_width})

## Creates a Dash input box
def createInput(description, opts, default_value, 
                ip_style={"width": "150px"}, ip_id=None, desc_id=None,
                grid_width="1fr 1fr", **kwargs):
    
    if desc_id:
        return html.Div([
            html.Span(description, id=desc_id, className="center_text bodytext"), 
            dcc.Input(id=ip_id, type=opts, placeholder=default_value, min=0, className="subcontainer", 
            style=ip_style, **kwargs)
            ], className="grid_container", style={"grid-template-columns": grid_width})
    else:
        return html.Div([
            html.Span(description, className="center_text bodytext"), 
            dcc.Input(id=ip_id, type=opts, placeholder=default_value, min=0, className="subcontainer", 
            style=ip_style, **kwargs)
            ], className="grid_container", style={"grid-template-columns": grid_width})

def createNumericInput(description, default_value, maximum, minimum=0, 
                       ip_style={"width": "150px"}, ip_id=None, desc_id=None, 
                       grid_width="1fr 1fr", size=150, **kwargs):
    
    if desc_id:
        return html.Div([
            html.Span(description, id=desc_id, className="center_text bodytext"), 
            daq.NumericInput(id=ip_id, value=default_value, min=minimum, 
                             max=maximum, className="subcontainer", style=ip_style, 
                             size=size, **kwargs)
            ], className="grid_container", style={"grid-template-columns": grid_width})
    else:
        return html.Div([
            html.Span(description, className="center_text bodytext"), 
            daq.NumericInput(id=ip_id, value=default_value, min=minimum, 
                             max=maximum, className="subcontainer", style=ip_style, 
                             size=size, **kwargs)
            ], className="grid_container", style={"grid-template-columns": grid_width})

    
def createTopBar():
    return html.A(dbc.Row(
        [
            dbc.Col(dbc.NavItem(dbc.NavLink(tb.opts['HOME'], href="/home", external_link=True, 
                                            className="background2 center_text subtitle", style={'height':'70px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink(tb.opts['CITY'], href="/city", external_link=True, 
                                            className="background2 center_text subtitle", style={'height':'70px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink(tb.opts['NEIGHBORHOOD'], href="/neighborhood", external_link=True, 
                                            className="background2 center_text subtitle", style={'height':'70px'}))),
            dbc.Col(dbc.NavItem(dbc.NavLink(tb.opts['NBCOMPARE'], href="/nbcompare", external_link=True, 
                                            className="background2 center_text subtitle", style={'height':'70px'}))),
            dbc.Col(html.Img(src = 'assets/title.png', style={'height':'70px'}), className="ml-5"),
        ], 
        align="center", className="g-0"))