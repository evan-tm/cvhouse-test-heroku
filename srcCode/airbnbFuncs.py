# ------------------QoL functions------------------#

# modules to import
# import numpy as np
# import shapely.geometry
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# import plotly.colors
# import geopandas as gpd
# from dash import Input, Output, State, dcc, html, callback, no_update
# import json
# from dash_iconify import DashIconify

# # airbnb property-level data
# propertiesDF = gpd.read_file('data/airbnb/airbnbProperties.geojson')
# ns = gpd.read_file('neighborhood_simple.geojson')

# mapbox_token_public = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
# mapbox_style = "mapbox://styles/evan-tm/cl1ik4lmv003z15ru0ip4isbz"
# mapbox_token_public_hood = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
# mapbox_style_hood = "mapbox://styles/evan-tm/cl1xthgjs000i14qv2eaz09w5"

# bluered_colors, _ = plotly.colors.convert_colors_to_same_type(px.colors.sequential.Bluered)
# colorscale = plotly.colors.make_colorscale(bluered_colors)


# ## Plot the map of local airbnb properties
# ## out: figure
# def plotPropertyMap():
#     # groceries scatter
#     fig = px.scatter_mapbox(propertiesDF, lon = propertiesDF.longitude, 
#                             lat = propertiesDF.latitude,
#                             center={"lat": 38.039, "lon": -78.47826}, 
#                             color="days_available",
#                             color_continuous_scale = px.colors.sequential.Bluered,
#                             custom_data = ("airbnb_property_id","homeaway_property_id",),
#                             labels={
#                                 "days_available": "Days Listed (Last 365 Days)"
#                             },
#                             zoom=12)
#     fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
#                       margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
#                       plot_bgcolor="rgba(0,0,0,0)",
#                       paper_bgcolor="rgba(0,0,0,0)",
#                       autosize=True,
#                       font={'size': 16, 'color': "rgb(7,13,30)"},
#                       mapbox={
#                         "style": "streets",
#                         "layers": [
#                             {
#                                 "source": json.loads(ns.geometry.to_json()),
#                                 "below": "traces",
#                                 "type": "line",
#                                 "color": "black",
#                                 "line": {"width": 1.5},
#                             }
#                         ],
#                       }
#                      )
#     texttrace = go.Scattermapbox(
#         lat=ns.geometry.centroid.y,
#         lon=ns.geometry.centroid.x,
#         text=ns["NAME"].astype(str),
#         textfont={"color":"black","size":23, 
#                   "family":"franklin-gothic-atf"},
#         mode="text",
#         name="NAME",
#         showlegend=False
#     )
#     fig.add_trace(texttrace)
#     fig.update_traces(hoverinfo="none", hovertemplate=None,
#                       marker={'size': 9})
#     fig.update_yaxes(scaleanchor="x", scaleratio=1)
#     fig['layout']['uirevision'] = 'hello'

#     return fig

# def get_continuous_color(colorscale, intermed):
#     """
#     Plotly continuous colorscales assign colors to the range [0, 1]. This function computes the intermediate
#     color for any value in that range.

#     Plotly doesn't make the colorscales directly accessible in a common format.
#     Some are ready to use:
    
#         colorscale = plotly.colors.PLOTLY_SCALES["Greens"]

#     Others are just swatches that need to be constructed into a colorscale:

#         viridis_colors, scale = plotly.colors.convert_colors_to_same_type(plotly.colors.sequential.Viridis)
#         colorscale = plotly.colors.make_colorscale(viridis_colors, scale=scale)

#     :param colorscale: A plotly continuous colorscale defined with RGB string colors.
#     :param intermed: value in the range [0, 1]
#     :return: color in rgb string format
#     :rtype: str
#     """
#     if len(colorscale) < 1:
#         raise ValueError("colorscale must have at least one color")

#     if intermed <= 0 or len(colorscale) == 1:
#         return colorscale[0][1]
#     if intermed >= 1:
#         return colorscale[-1][1]

#     for cutoff, color in colorscale:
#         if intermed > cutoff:
#             low_cutoff, low_color = cutoff, color
#         else:
#             high_cutoff, high_color = cutoff, color
#             break

#     # noinspection PyUnboundLocalVariable
#     return plotly.colors.find_intermediate_color(
#         lowcolor=low_color, highcolor=high_color,
#         intermed=((intermed - low_cutoff) / (high_cutoff - low_cutoff)),
#         colortype="rgb")

# def get_hover_header(img_src, room):
#     if img_src == "NAN2":
#         return html.Div([html.Br(),
#                          html.Span(f"{room}", 
#                                    className = "hover_window_statistics_timeframe"),])
#     else:
#         return html.Div([html.Span(f"{room}",
#                                    className = "hover_window_statistics_timeframe"),
#                          html.Img(src=img_src, style={"width": "100%"})])

# def get_property_desc(property, neighborhood):
#     if neighborhood is None:
#         return html.P(f"{property} outside of CVille")
#     else:
#         return html.P(f"{property} in {neighborhood}")

# @callback(
#     Output("airbnb_tooltip", "show"),
#     Output("airbnb_tooltip", "bbox"),
#     Output("airbnb_tooltip", "children"),
#     Input("airbnb_map", "hoverData"),
# )
# def display_hover(hoverData):
#     if hoverData is None:
#         return False, no_update, no_update
    
#     # demo only shows the first point, but other points may also be available
#     pt = hoverData["points"][0]
#     if 'marker.color' not in pt:
#         return False, no_update, no_update
#     bbox = pt["bbox"]
#     num = pt["pointNumber"]

#     df_row = propertiesDF.iloc[num]
#     img_src = df_row['img_links']
#     desc = df_row['title']
#     room = df_row['room_type']
#     property = df_row['property_type']
#     bedrooms = df_row['bedrooms']
#     bathrooms = df_row['bathrooms']
#     accommodates = df_row['accommodates']
#     neighborhood = df_row['NAME']
#     adr = df_row['adr']
#     days = df_row['days_available']
#     myColor = get_continuous_color(colorscale, 
#                                    intermed=pt['marker.color'] / 365)
#     if len(desc) > 50:
#         desc = desc[:50] + '...'

#     children = [
#         html.Div([
#             get_hover_header(img_src, room),
#             html.Span(f"{desc}", style={"color": myColor}),
#             html.Div([
#                 DashIconify(
#                     icon="fluent:bed-20-filled",
#                     width=15,
#                     height=15,
#                 ),
#                 html.Span(f"{bedrooms}"),
#                 DashIconify(
#                     icon="cil:bathroom",
#                     width=15,
#                     height=15,
#                 ),
#                 html.Span(f"{bathrooms}"),
#                 DashIconify(
#                     icon="bi:person-circle",
#                     width=15,
#                     height=15,
#                 ),
#                 html.Span(f"{accommodates}"),
#             ], className = "hover_property_row hover_property_row_flex \
#                             hover_property_row_space_between"),
#             get_property_desc(property, neighborhood),
#             html.Div([
#                 html.Div([
#                     html.Span("Last 365 Days")
#                 ], className = "hover_window_statistics_timeframe"),
#                 html.Div([
#                     html.P(f"{days}", style={"color": myColor}, 
#                            className = "hover_window_statistics_value"),
#                     html.P("Days Listed", className = "hover_window_statistics_title")
#                 ], className = "hover_window_statistics_item"),
#                 html.Div([
#                     html.P(f"${int(adr)}",  
#                            className = "hover_window_statistics_value"),
#                     html.P("Avg. Daily Rate", className = "hover_window_statistics_title")
#                 ], className = "hover_window_statistics_item"),
#             ], className = "hover_window_statistics"),
#         ], className = "hover_property_window", style={'width': '300px',
#                                                        'white-space': 'normal'})
#     ]

#     return True, bbox, children

# @callback(Output('rental_link', 'children'),
#           Output('rental_link', 'href'),
#           Output('rental_link_notif', 'children'),
#           [Input('airbnb_map', 'clickData')])
# def open_url(clickData):
#     if clickData is not None:
#         if clickData['points'][0]['customdata'][1] is None:
#             url = clickData['points'][0]['customdata'][0]
#             return "airbnb.com/rooms/" + str(url), \
#                     "https://www.airbnb.com/rooms/" + str(url), \
#                     ""
#         else:
#             url = clickData['points'][0]['customdata'][1]
#             return "vrbo.com/" + str(url), \
#                     "https://www.vrbo.com/" + str(url), \
#                     ""
#     else:
#         return no_update, no_update, no_update
