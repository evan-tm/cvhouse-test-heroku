# ------------------QoL functions------------------#

# modules to import
import numpy as np
import shapely.geometry
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geopandas as gpd
#from dash import Input, Output, State, dcc, html, callback
#import dash_bootstrap_components as dbc

import srcCode.qolDescs as qd

# groceries
groceries = gpd.read_file('data/lifeQuality/groceries.geojson')
# fire stations
fire = gpd.read_file('data/lifeQuality/fire.geojson')
# electric vehicle charging stations
ev = gpd.read_file('data/lifeQuality/ev.geojson')
# train stations
train = gpd.read_file('data/lifeQuality/train.geojson')
# bike racks
bikeRacks = gpd.read_file('data/lifeQuality/bikeRacks.geojson')
# bus stops
busStops = gpd.read_file('data/lifeQuality/busStops.geojson')
# bike lanes
bikeLanes = gpd.read_file('data/lifeQuality/bikeLanes.geojson')
# food kitchens
kitchens = gpd.read_file('data/lifeQuality/kitchens.geojson')
# public libraries
libraries = gpd.read_file('data/lifeQuality/libraries.geojson')
# schools
eduPoints = gpd.read_file('data/lifeQuality/eduPoints.geojson')
# school zones (elementary only)
edu = gpd.read_file('data/lifeQuality/edu.geojson')
edu = edu.set_index('ElemSchool')
# tree coverage
treeDF = gpd.read_file('data/lifeQuality/trees.geojson')
treeDF = treeDF.set_index('NAME')

#mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
#mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
mapbox_token_public = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
mapbox_style = "mapbox://styles/evan-tm/cl1ik4lmv003z15ru0ip4isbz"
mapbox_token_public_hood = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
mapbox_style_hood = "mapbox://styles/evan-tm/cl1xthgjs000i14qv2eaz09w5"

lats = []
lons = []
details = []
widths = []

for feature, detail, width in zip(bikeLanes.geometry, bikeLanes['Lane Detail'], bikeLanes['TotalWidth']):
    if isinstance(feature, shapely.geometry.linestring.LineString):
        linestrings = [feature]
    elif isinstance(feature, shapely.geometry.multilinestring.MultiLineString):
        linestrings = feature.geoms
    else:
        continue
    for linestring in linestrings:
        x, y = linestring.xy
        lats = np.append(lats, y)
        lons = np.append(lons, x)
        details = np.append(details, [detail]*len(y))
        widths = np.append(widths, [width]*len(y))
        lats = np.append(lats, None)
        lons = np.append(lons, None)
        details = np.append(details, None)
        widths = np.append(widths, None)

## Plot the map of local resources
## out: figure
def plotResourcesMap():
    # groceries scatter
    fig1 = px.scatter_mapbox(groceries, lon = groceries.geometry.x, 
                            lat = groceries.geometry.y,
                            hover_name="name", hover_data={"addr:street": True},
                            center={"lat": 38.039, "lon": -78.47826}, 
                            color_discrete_sequence=['green'],
                            zoom=12)
    fig1.update_layout(mapbox_accesstoken=mapbox_token_public, 
                      mapbox_style=mapbox_style,
                      margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font={'size': 16, 'color': "rgb(255,255,255)"})
    fig1.update_traces(hovertemplate="<br>".join([
                                    "%{hovertext}",
                                    "",
                                    "Address: %{customdata[0]}"]),
                      marker={'size': 11})
    # food kitchens
    fig2 = px.scatter_mapbox(kitchens, lon = kitchens.geometry.x, 
                             lat = kitchens.geometry.y,
                             hover_name="name", hover_data={"address": True, 
                                                       "Desc": True},
                             center={"lat": 38.039, "lon": -78.47826}, 
                             color_discrete_sequence=['purple'],
                             zoom=12)
    fig2.update_layout(mapbox_accesstoken=mapbox_token_public, 
                       mapbox_style=mapbox_style,
                       margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                       plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)",
                       autosize=True,
                       font={'size': 16, 'color': "rgb(255,255,255)"})
    fig2.update_traces(hovertemplate="<br>".join([
                                     "%{hovertext}",
                                     "",
                                     "Address: %{customdata[0]}",
                                     "%{customdata[1]}"]),
                       marker={'size': 11})
    # libraries scatter
    fig3 = px.scatter_mapbox(libraries, lon = libraries.geometry.x, 
                             lat = libraries.geometry.y,
                             hover_name="name", hover_data={"address": True},
                             center={"lat": 38.039, "lon": -78.47826}, 
                             color_discrete_sequence=['teal'],
                             zoom=12)
    fig3.update_layout(mapbox_accesstoken=mapbox_token_public, 
                       mapbox_style=mapbox_style,
                       margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                       plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)",
                       autosize=True,
                       font={'size': 16, 'color': "rgb(255,255,255)"})
    fig3.update_traces(hovertemplate="<br>".join([
                                     "%{hovertext}",
                                     "",
                                     "Address: %{customdata[0]}"]), 
                       marker={'size': 11})
    # fire stations scatter
    fig4 = px.scatter_mapbox(fire, lon = fire.geometry.x, 
                             lat = fire.geometry.y,
                             hover_name="Station Name", 
                             hover_data={"Address": True},
                             center={"lat": 38.039, "lon": -78.47826}, 
                             color_discrete_sequence=['red'],
                             zoom=12)
    fig4.update_layout(mapbox_accesstoken=mapbox_token_public, 
                       mapbox_style=mapbox_style,
                       margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                       plot_bgcolor="rgba(0,0,0,0)",
                       paper_bgcolor="rgba(0,0,0,0)",
                       autosize=True,
                       font={'size': 16, 'color': "rgb(255,255,255)"})
    fig4.update_traces(hovertemplate="<br>".join([
                                     "%{hovertext}",
                                     "",
                                     "Address: %{customdata[0]}"]),
                       marker={'size': 11})
    # train station scatter
    fig5 = px.scatter_mapbox(train, lon = train.geometry.x, 
                             lat = train.geometry.y,
                             hover_name="Location", hover_data={"Address": True},
                             center={"lat": 38.039, "lon": -78.47826}, 
                            color_discrete_sequence=['orange'],
                            zoom=12)
    fig5.update_layout(mapbox_accesstoken=mapbox_token_public, 
                        mapbox_style=mapbox_style,
                        margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        autosize=True,
                        font={'size': 16, 'color': "rgb(255,255,255)"})
    fig5.update_traces(hovertemplate="<br>".join([
                                    "%{hovertext}",
                                    "",
                                    "Address: %{customdata[0]}"]), 
                    marker={'size': 11})
    # CAT bus stop scatter
    fig6 = px.scatter_mapbox(busStops, lon = busStops.geometry.x, 
                            lat = busStops.geometry.y,
                            hover_name="StopCode", hover_data={"StopName": True},
                            center={"lat": 38.039, "lon": -78.47826}, 
                            color_discrete_sequence=['steelblue'],
                            zoom=12)
    fig6.update_layout(mapbox_accesstoken=mapbox_token_public, 
                    mapbox_style=mapbox_style,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig6.update_traces(hovertemplate="<br>".join([
                                    "Name: %{customdata[0]}",
                                    "Code: %{hovertext}"]), 
                    marker={'size': 6})
    # bike rack scatter (need to include logic for na type and number values)
    fig7 = px.scatter_mapbox(bikeRacks, lon = bikeRacks.geometry.x, 
                            lat = bikeRacks.geometry.y,
                            hover_name="Type", hover_data={"Number": True},
                            center={"lat": 38.039, "lon": -78.47826}, 
                            color_discrete_sequence=['black'],
                            zoom=12)
    fig7.update_layout(mapbox_accesstoken=mapbox_token_public, 
                    mapbox_style=mapbox_style,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig7.update_traces(hovertemplate="<br>".join([
                                    "Type: %{hovertext}",
                                    "Capacity: %{customdata[0]}"]), 
                    marker={'size': 5})
    # Bike lane lines
    fig8 = px.line_mapbox(lon=lons, lat=lats, 
                        hover_name=details,
                        #hover_data=widths,
                        center={"lat": 38.039, "lon": -78.47826}, 
                        color_discrete_sequence=['darkgreen'], 
                        zoom=12)
    fig8.update_layout(mapbox_accesstoken=mapbox_token_public, 
                    mapbox_style=mapbox_style,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig8.update_traces(hovertemplate="<br>".join([
                                    "Type: %{hovertext}"]),
                    line={'width': 1.5})
    # ev charging scatter
    fig9 = px.scatter_mapbox(ev, lon = ev.geometry.x, 
                            lat = ev.geometry.y,
                            hover_name="Description", hover_data={"Location": True, 
                                                                "Address": True},
                            center={"lat": 38.039, "lon": -78.47826}, 
                            color_discrete_sequence=['blue'],
                            zoom=12)
    fig9.update_layout(mapbox_accesstoken=mapbox_token_public, 
                    mapbox_style=mapbox_style,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig9.update_traces(hovertemplate="<br>".join([
                                    "Type: %{hovertext}",
                                    "Location: %{customdata[0]}",
                                    "Address: %{customdata[1]}"]),
                    marker={'size': 11})

    fig = go.Figure(layout = fig1.layout)
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig2.data[0])
    fig.add_trace(fig3.data[0])
    fig.add_trace(fig4.data[0])
    fig.add_trace(fig5.data[0])
    fig.add_trace(fig6.data[0])
    fig.add_trace(fig7.data[0])
    fig.add_trace(fig8.data[0])
    fig.add_trace(fig9.data[0])
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

    for i in range(9):
        fig['data'][i]['showlegend']=True

    fig['data'][0]['name']='Grocery Stores'
    fig['data'][1]['name']='Food Kitchens'
    fig['data'][2]['name']='Public Libraries'
    fig['data'][3]['name']='Fire Stations'
    fig['data'][4]['name']='Train Stations'
    fig['data'][5]['name']='CAT Bus Stops'
    fig['data'][6]['name']='Bike Racks'
    fig['data'][7]['name']='Bike Lanes'
    fig['data'][8]['name']='EV Chargers'
    # deactivate the bus stops, bike racks, bike lanes, and ev chargers when plot first drawn
    items_to_hide = ["CAT Bus Stops", "Bike Racks", "Bike Lanes", "EV Chargers"]
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
                    if trace.name in items_to_hide else ())

    return fig

def plotSchoolMap():
    # school zones chloropleth
    fig = px.choropleth_mapbox(edu, geojson = edu.geometry, 
                            locations = edu.index,
                            hover_name = edu.index,
                            color = edu.index,
                            center={"lat": 38.039, "lon": -78.47826},
                            zoom=12, opacity = 0.5,
                            labels={'ElemSchool': 'Elementary School Zone'})
    fig.update_layout(mapbox_accesstoken=mapbox_token_public_hood, 
                    mapbox_style=mapbox_style_hood,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig.update_traces(hovertemplate=None, hoverinfo = 'skip')
    #fig.update_traces(hovertemplate="<br>".join([
    #                                "Elementary: %{hovertext}",
    #                                "Upper Elementary: Walker",
    #                                "Middle: Buford",
    #                                "High: Charlottesville"]))
    # school points scatter
    fig2 = px.scatter_mapbox(eduPoints, lon = eduPoints.geometry.x, 
                            lat = eduPoints.geometry.y,
                            hover_name="name", hover_data={"address": True},
                            color_discrete_sequence=['black'],
                            center={"lat": 38.039, "lon": -78.47826}, 
                            zoom = 12,
                            opacity = 1)
    fig2.update_layout(mapbox_accesstoken=mapbox_token_public_hood, 
                    mapbox_style=mapbox_style_hood,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig2.update_traces(hovertemplate="<br>".join([
                                    "%{hovertext}",
                                    "",
                                    "Address: %{customdata[0]}"]), 
                    marker={'size': 12})

    fig.add_trace(fig2.data[0])
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.data = fig.data[::-1]
    
    return fig


## Returns a plot of the tree coverage map
## in: data from tree coverage
## out: figure representing the data
def plotTreeMap():
    # tree coverage chloropleth
    fig = px.choropleth_mapbox(treeDF, geojson = treeDF.geometry, 
                            locations = treeDF.index,
                            color = treeDF.coverage,
                            center={"lat": 38.039, "lon": -78.47826},
                            zoom=12, opacity = 0.5, 
                            color_continuous_scale='Tropic_r',
                            labels={'coverage': 'Canopy Coverage (%)'})
    fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                    mapbox_style=mapbox_style,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    #fig.update_traces(hovertemplate=None, hoverinfo = 'skip')

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

