# ------------------General dash functions------------------#

# modules to import
from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_daq as daq
import srcCode.toolbarDescs as tb

# -*- coding: utf-8 -*-

## Creates a Dash dropdown menu
def createDropdown(description, opts, default_value, 
                   dd_style={"width": "150px"}, dd_id=None, desc_id=None, 
                   grid_width="1fr 1fr", **kwargs):
    if opts is not None:
        opts_dict = [{"label": each, "value": each} for each in opts]
    else:
        opts_dict = None
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

def createTagInput(description, default_value, maximum, minimum=0, 
                   ip_style={"width": "150px"}, ip_id=None, desc_id=None, 
                   button_desc=None,
                   button_id=None, grid_width="1fr 1fr 1fr 1fr", size=150, **kwargs):
    
    if desc_id:
        return html.Div([
            html.Span(description, id=desc_id, className="elem1 center_text bodytext"), 
            daq.NumericInput(id=ip_id, value=default_value, min=minimum, 
                             max=maximum, className="elem2", style=ip_style, 
                             size=size, **kwargs),
            html.Button(button_desc, id=button_id, className="elem3 center_text subtitle",
                        style={"background-color": "#009192", "color": "#FFFFFF", 
                               'width': '150px', 'border': '0'}),
            ], className="grid_ages")
    else:
        return html.Div([
            html.Span(description, className="elem1 center_text bodytext"), 
            daq.NumericInput(id=ip_id, value=default_value, min=minimum, 
                             max=maximum, className="elem2", style=ip_style, 
                             size=size, **kwargs),
            html.Button(button_desc, id=button_id, className="elem3 center_text subtitle",
                        style={"background-color": "#009192", "color": "#FFFFFF", 
                               'width': '150px', 'border': '0'}),
            ], className="grid_ages")

    
def createTopBar():
    return dbc.NavbarSimple(children=[
                dbc.NavItem(dbc.NavLink(tb.opts['HOME'], href="/",
                                        className="header_links_text")),
                dbc.NavItem(dbc.NavLink(tb.opts['CITY_SELECT'], href="/city",
                                        className="header_links_text")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("Neighborhood data pages", header=True,
                                             className="header_links_text"),
                        dbc.DropdownMenuItem(tb.opts['NEIGHBORHOOD'], href="/neighborhood",
                                             className="header_links_text"),
                        dbc.DropdownMenuItem(tb.opts['NBCOMPARE'], href="/nbcompare",
                                             className="header_links_text"),
                    ],
                    nav=True,
                    in_navbar=True,
                    label=tb.opts['NEIGHBORHOOD_SELECT'],
                ),
                dbc.NavItem(dbc.NavLink(tb.opts['RESOURCES'], href="/resources",
                                        className="header_links_text")),
                dbc.NavItem(dbc.NavLink(tb.opts['CONTACT'], href="/contact",
                                        className="header_links_text")),
                dbc.DropdownMenu(
                    children=[
                        dbc.DropdownMenuItem("App settings", header=True,
                                             className="header_links_text"),
                        dcc.Checklist(
                            options=[{"value": "Show tickers", "label": "Show tickers"},
                                     {"value": "Smpl age", 
                                     "label": "Smpl age"},
                                     {"value": "Smpl income", 
                                     "label": "Smpl income"}],
                            value=["Smpl age", "Smpl income"], id="settings_checklist", className="header_links_text", 
                            persistence=True, inputStyle={"margin-left": "15px", "margin-right": "5px"}
                        ),
                    ],
                    nav=True,
                    in_navbar=True,
                    label='⚙',
                    align_end=True
                ),
            ],
            brand="Changing Charlottesville",
            brand_href="#",
            color="#5B1453",
            dark=True,
            class_name = "header_links_text"
        )

def createLeftAlignDropdown(description, opts, default_value, 
                   dd_style={"width": "150px"}, dd_id=None, desc_id=None,
                   grid_class="grid_dd", 
                   **kwargs):
    if opts is not None:
        opts_dict = [{"label": each, "value": each} for each in opts]
    else:
        opts_dict = None
    if desc_id:
        return html.Div([
            html.B(description, id=desc_id, 
                      className="dd_elem1 right_text bodytext"), 
            dcc.Dropdown(id=dd_id, options=opts_dict, value=default_value, 
                         className="dd_elem2 subcontainer", 
                         style=dd_style, **kwargs)
        ], className=grid_class)
    else:
        return html.Div([
            html.B(description, 
                      className="dd_elem1 right_text bodytext"),
            dcc.Dropdown(id=dd_id, options=opts_dict, value=default_value, 
                         className="dd_elem2 subcontainer", 
                         style=dd_style, **kwargs)
        ], className=grid_class)

def createArrowLink(link_text, link):
    return html.Div([
        html.Span('→ ', className = "left_text inline_bodytext"),
        html.A(link_text, href=link, 
                target="_blank", className = "left_text inline_links"),
    ])

def createInlineLink(text, link_text, link):
    return html.Div([
        html.A(link_text, href=link,
                target="_blank", className = "center_text inline_sublinks"),
        html.Span(text, className = "center_text inline_subtitle"),
    ], className = "center_div")
