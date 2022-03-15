# ------------------Industry functions------------------#

# modules to import
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, State, dcc, html, callback
import dash_bootstrap_components as dbc

# Industry by sector data file
indBySector = pd.read_csv("data/indBySectorHistFull.csv")
# Industry by neighborhood  data
indByNeighborhood = pd.read_csv("data/indByNeighborhoodHistFull.csv")

# texts (move to descs file in the future)
IND_SECTOR_TITLE = 'Industries and Sectors of Charlottesville Residents (% of Total Employed Age 16+ Civilians)'
HOVER_TEMPLATE_PCT = '<i>Sector</i>: %{data.name}' + \
                 '<br>%{value:.2f}% of Total Employed<br>' + \
                 'Industries: <b>%{customdata}</b>' + \
                 '<extra></extra>'
sector_legend = "Sector"

IND_NEIGHBORHOOD_TITLE = 'Industries of {hood} Residents (% of Total Employed Age 16+ Civilians)'
neighborhood_title = "Industries by Neighborhood"
neighborhood_legend = "Neighborhood"
HOVER_TEMPLATE_PCT_HOOD = '%{value:.2f}% of Total Employed<br>' + \
                 'Industries: <b>%{customdata}</b>' + \
                 '<extra></extra>'

## Adds annotations to plotIndustrySector figure
## in: figure, dataset, list of indices
## out: figure with annotations added
def addFigAnnotations(fig, data, num):
    
    for idx in num:
        fig.add_annotation(dict(font=dict(color = 'white', size = 10),
                               x = 1.004,
                               y = data['Industry'][idx],
                               showarrow=False,
                               text=data['ag'][idx],
                               textangle=0,
                               xanchor='right',
                               xref='paper',
                               yref='y'))
    return fig

## Adds annotations to plotIndustrySector figure frame layout
## in: frame, dataset, list of indices, index of frame in frame list
## out: frame with annotations added to layout
def addFrameAnnotations(frame, data, num, frameIndex):
    ## build list of annotations
    annotations = [
        go.layout.Annotation(
            dict(font=dict(color = 'white', size = 10), 
                 x = 1.004, 
                 y = data['Industry'][idx + frameIndex * len(num)], 
                 showarrow=False, 
                 text=data['ag'][idx + frameIndex * len(num)], 
                 textangle=0, 
                 xanchor='right',
                 xref='paper',
                 yref='y')
        ) for idx in num]
    ## Add annotations list to frame layout
    frame.layout = go.Layout(annotations = annotations)
    return frame

## Function for creating plot of industry employment populations by sector
## out: figure
def plotIndustrySector():
    fig = px.bar(indBySector, 
                y="Industry", 
                x=["Private For-Profit", "Self-Employed Incorporated", 
                    "Private Not-For-Profit", "Government", 
                    "Self-Employed Not Incorporated"], 
                animation_frame="Year",
                labels={'value':'Employed Population (%)', 
                        'Industry':'Industries'}, 
                orientation="h", custom_data=["Desc"],
                title = IND_SECTOR_TITLE)
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = HOVER_TEMPLATE_PCT)
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font=dict(size=13, color="rgb(255,255,255)"),
                    legend_title_text=sector_legend,
                    legend=dict(yanchor="bottom", 
                                x=0.83, 
                                y=0, 
                                xanchor="right",
                                bgcolor="DimGray"),
                    hoverlabel_align = 'left',
                    titlefont={'size': 14},
                    title_x = 0.52)
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, indBySector, [i for i in range(13)])
    ## Fixed x axis size for each frame
    fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", "25", "30", "35", "40"], 
                    tickvals = [i*5 for i in range(9)], 
                    range = [0, 49.5])
    #fig['layout']['updatemenus'][0]['pad']=dict(r= 0, t= 70)
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = HOVER_TEMPLATE_PCT
        f = addFrameAnnotations(f, indBySector, [i for i in range(13)], idx)
  
    return fig



## Function for creating plot of industry employment populations by neighborhood
## in: current neighborhood
## out: figure
@callback(
    Output('neighborhood_plot', 'figure'),
    Input('dropdown_neighborhood', 'value'))
def plotIndustryByNeighborhood(n):
    fig = px.bar(indByNeighborhood, 
                 x=[n],
                 y='Industry', 
                 labels={'value':'Employed Population (%)',
                         'Industry':'Industries'}, 
                 animation_frame = "Year",
                 orientation="h", custom_data = ["Desc"], 
                 title = IND_NEIGHBORHOOD_TITLE.format(hood=n))
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = HOVER_TEMPLATE_PCT_HOOD)
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15), 
                      plot_bgcolor="rgba(0,0,0,0)", 
                      paper_bgcolor="rgba(0,0,0,0)", 
                      autosize=True, 
                      font=dict(size=13, color="rgb(255,255,255)"), 
                      legend_title_text=neighborhood_legend,
                      legend=dict(yanchor="bottom", 
                                  x=0.85, 
                                  y=0, 
                                  xanchor="right", 
                                  bgcolor="DimGray"), 
                      hoverlabel_align = 'left', 
                      titlefont={'size': 14}, 
                      title_x = 0.55)
    ## get index of neighborhood selection
    hood_index = indByNeighborhood.columns.get_loc(n)
    ## update dataset with correct ticker for neighborhood selection
    indByNeighborhood['ag'] = [f'({indByNeighborhood.iloc[i, hood_index+19]:,} : {indByNeighborhood.iloc[i, hood_index]:.2f}%)' 
                               for i in range(indByNeighborhood.shape[0])]
    ## Adds (count : pct) ticker at far right of chart
    fig = addFigAnnotations(fig, indByNeighborhood, [i for i in range(13)])
    ## Fixed x axis size for each frame
    fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", "25", "30", "35", "40", "45", "50", "55", "60"], 
                    tickvals = [i*5 for i in range(13)], 
                    range = [0, 72])
    ## move slider's and buttons' positions slightly left
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = HOVER_TEMPLATE_PCT_HOOD
        f = addFrameAnnotations(f, indByNeighborhood, [i for i in range(13)], idx)

    return fig
