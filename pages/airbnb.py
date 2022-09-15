# ------------------AirBNB page----------------------#
import dash
from dash import dcc, html, Input, Output, State, callback, no_update
import dash_bootstrap_components as dbc
import srcCode.toolbarDescs as tb
import srcCode.contactDescs as cd
import srcCode.dashFuncs as df
import srcCode.airbnbFuncs as af

dash.register_page(__name__)

layout = html.Div(
    [
        # Sidebar
        df.createTopBar(),
        html.Br(),
        html.Div(
        [
            # Property map
            dcc.Graph(id='airbnb_map', 
                    figure=af.plotPropertyMap(), 
                    config={'displayModeBar': True,
                            "displaylogo": False,
                            'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d',
                                                        'toImage'],
                            'scrollZoom': False},
                    style={'width': '100%', 'height': '550px'},
                    clear_on_unhover=True),
            dcc.Tooltip(id="airbnb_tooltip"),
        ], className="subcontainer"),
        html.A("", href="",
               target="_blank", 
               id = "rental_link",
               className = "left_text inline_sublinks"),
        html.Span("Click any rental to view its weblink.", 
                  id='rental_link_notif',
                  className = "left_text bodytext"),
        html.Br(),
        html.Br()
    ], className = "container background")

