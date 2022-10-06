# ------------------Census functions------------------#

# modules to import
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import srcCode.censusDescs as cd

# City industry data
industryCity = pd.read_csv('data/census/industryCity.csv')
# Neighborhood industry data
industryNeighborhood = pd.read_csv('data/census/industryNeighborhood.csv')
# City age data
ageCity = pd.read_csv("data/census/ageCity.csv")
# Neighborhood age data
ageNeighborhood = pd.read_csv("data/census/ageNeighborhood.csv")
# City race data
raceCity = pd.read_csv('data/census/raceEthnicityCity.csv')
# Neighborhod race data
raceNeighborhood = pd.read_csv('data/census/raceEthnicityNeighborhood.csv')
# City median income data
incomeCity = pd.read_csv('data/census/incomeCity.csv')
# Neighborhood median income data
incomeNeighborhood = pd.read_csv('data/census/incomeNeighborhood.csv')
# City income distribution data
incomeCityDist = pd.read_csv('data/census/incomeCityDist.csv')
# Neighborhood income distribution data
incomeNeighborhoodDist = pd.read_csv('data/census/incomeNeighborhoodDist.csv')
# City occupancy data
occupancyCity = pd.read_csv('data/census/occupancyCity.csv')
# Neighborhood occupancy data
occupancyNeighborhood = pd.read_csv('data/census/occupancyNeighborhood.csv')
# City tenure data
tenureCity = pd.read_csv('data/census/tenureCity.csv')
# Neighborhood tenure data
tenureNeighborhood = pd.read_csv('data/census/tenureNeighborhood.csv')
# City population size data
popCity = pd.read_csv('data/census/populationCity.csv')
# Neighborhood population size data
popNeighborhood = pd.read_csv('data/census/populationNeighborhood.csv')

## Adds ticker annotations to figures
## in: figure, dataset, list of indices, column
## out: figure with annotations added
def addFigAnnotations(fig, data, num, column, compare = False):
    if compare:
        for idx in num:
            fig.add_annotation(dict(font=dict(color = "rgb(7,13,30)", size = 12),
                                x = 1.004,
                                y = data[column][idx],
                                showarrow=False,
                                text=data['ag'][idx],
                                textangle=0,
                                xanchor='right',
                                xref='paper',
                                yref='y'))
    else:
        for idx in num:
            fig.add_annotation(dict(font=dict(color = "rgb(7,13,30)", size = 14),
                                x = 1.004,
                                y = data[column][idx],
                                showarrow=False,
                                text=data['ag'][idx],
                                textangle=0,
                                xanchor='right',
                                xref='paper',
                                yref='y'))
    return fig

## Adds ticker annotations to figure frames
## in: frame, dataset, list of indices, index of frame in frame list, column
## out: frame with annotations added to layout
def addFrameAnnotations(frame, data, num, frameIndex, column, compare = False):
    if compare:
        ## build list of annotations
        annotations = [
            go.layout.Annotation(
                dict(font=dict(color = "rgb(7,13,30)", size = 12), 
                    x = 1.004, 
                    y = data[column][idx + frameIndex * len(num)], 
                    showarrow=False, 
                    text=data['ag'][idx + frameIndex * len(num)], 
                    textangle=0, 
                    xanchor='right',
                    xref='paper',
                    yref='y')
            ) for idx in num]
    else:
        ## build list of annotations
        annotations = [
            go.layout.Annotation(
                dict(font=dict(color = "rgb(7,13,30)", size = 14), 
                    x = 1.004, 
                    y = data[column][idx + frameIndex * len(num)], 
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
def plotIndustrySector(tickers = True):
    fig = px.bar(industryCity, 
                y="Industry", 
                x="Total", 
                animation_frame="Year",
                labels={'Total':cd.text['IND_X_TITLE'], 
                        'Industry':cd.text['IND_Y_TITLE']},
                orientation="h", custom_data=["Desc"],
                title = cd.text['IND_CITY_TITLE'])
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['IND_CITY_HOVER'],
                      marker_color='#ed8851', marker_line_color='#e96a26',
                      marker_line_width=1.5, opacity=0.8)
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    autosize=True,
                    font=dict(size=17, color="rgb(7,13,30)"),
                    hoverlabel_align = 'left',
                    titlefont={'size': 19},
                    title_x = 0.56,
                    font_family="FranklinGothic",
                    font_color="#070D1E",
                    title_font_family="FranklinGothicPro",
                    title_font_color="#1C1D1E")
    if tickers:
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, industryCity, [i for i in range(13)], 'Industry')
    ## Fixed x axis size for each frame
    fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                 "25", "30", "35", "40"], 
                    tickvals = [i*5 for i in range(9)], 
                    range = [0, 45],
                    gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['IND_CITY_HOVER']
            dat.marker = dict(color='#ed8851',
                              line=dict(color='#e96a26',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, industryCity, [i for i in range(13)], 
                                    idx, 'Industry')
  
    return fig

## Function for creating age plot for the city overall
## out: figure
def plotAgeCity(tickers = True):
    # begin building figure
    fig = px.bar(ageCity, 
                 y="Age", 
                 x="Total",
                 animation_frame='Year', 
                 barmode='group',
                 orientation="h",
                 title=cd.text['AGE_CITY_TITLE'], 
                 height = 550,
                 labels={'variable':cd.text['AGE_LEGEND_TITLE'], 
                         'Total':cd.text['AGE_X_TITLE'],
                         'Age':cd.text['AGE_Y_TITLE']},
                 custom_data=["Totalct"])
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['AGE_CITY_HOVER'],
                      marker_color='#7c4375', marker_line_color='#5b1453',
                      marker_line_width=1.5, opacity=0.8)
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 19},
                      title_x = 0.555,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, ageCity, [i for i in range(18)], 'Age')
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*2 for i in range(12)], 
                     range = [0, 24],
                     gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['AGE_CITY_HOVER']
            dat.marker = dict(color='#7c4375',
                              line=dict(color='#5b1453',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, ageCity, [i for i in range(18)], 
                                    idx, 'Age')
  
    return fig

## Function for creating race plot for the city overall
## out: figure
def plotRaceCity(tickers = True):
    # begin building figure
    fig = px.bar(raceCity, 
                 y="Race and Ethnicity", 
                 x="Pop",
                 animation_frame='Year',
                 orientation="h",
                 height = 500,
                 title=cd.text['RACE_CITY_TITLE'], 
                 labels={'Pop':cd.text['RACE_X_TITLE'],
                         'Race and Ethnicity':cd.text['RACE_Y_TITLE']})
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"), 
                      titlefont={'size': 19},
                      title_x = 0.585,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, raceCity, [i for i in range(8)], 
                                'Race and Ethnicity')
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*10 for i in range(8)], 
                     range = [0, 82],
                     gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.marker = dict(color='#33a7a8',
                              line=dict(color='#009192',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, raceCity, [i for i in range(8)], 
                                    idx, 'Race and Ethnicity')
    ## Set bar color
    fig.update_traces(marker_color='#33a7a8', marker_line_color='#009192',
                      marker_line_width=1.5, opacity=0.8)

    return fig

## Function for creating income plot for the city overall
## out: figure
def plotIncomeCity():
    fig = px.line(incomeCity, x="Year", y=cd.opts['CITY_LIST'],
                    title=cd.text['INCOME_CITY_TITLE'],
                    labels={'value': cd.text['INCOME_CITY_Y_TITLE'],
                            "Year": "<b>Year</b>",
                            'variable': '<b>City</b>'},
                    markers = True, height = 450,
                    color_discrete_sequence=["#ed8851", "#009192", "#7c4375", 
                                             "#dd5279", "#f7e144", "#6b6d6f"])
    fig.update_xaxes(tickvals = [2010 + 2*year for year in range(6)], 
                     range = [2008.5, 2020.5], gridcolor='Black')
    fig.update_yaxes(tickvals = [10000 * k for k in range(3, 8)],
                     gridcolor='Black')
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    autosize=True,
                    font=dict(size=17),
                    font_family="FranklinGothic",
                    font_color="#070D1E",
                    titlefont={'size': 19},
                    title_font_family="FranklinGothicPro",
                    title_font_color="#1C1D1E",
                    title_x=0.46)
    fig.update_traces(line_width=5, mode='lines')
                      
    return fig

## Function for creating income distribution plot for the city overall
## out: figure
def plotIncomeDistCity(tickers = True):
    # begin building figure
    fig = px.bar(incomeCityDist, 
                 y="Bracket", 
                 x="Income",
                 animation_frame='Year',
                 orientation="h",
                 title=cd.text['INCOME_DIST_CITY_TITLE'], 
                 height=550,
                 labels={'Income':cd.text['INCOME_X_TITLE'],
                         'Bracket':cd.text['INCOME_Y_TITLE']},
                 color_discrete_sequence=["#e96a26"])
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 19},
                      title_x = 0.55,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, incomeCityDist, [i for i in range(16)], 'Bracket')
    ## Fixed x axis size for each frame
    fig.update_xaxes(tickvals = [i*2 for i in range(9)], 
                     range = [0, 18],
                     gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.marker = dict(color='#ed8851',
                              line=dict(color='#e96a26',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, incomeCityDist, 
                                    [i for i in range(16)], 
                                    idx, 'Bracket')
    ## Update bar styling
    fig.update_traces(marker_color='#ed8851', marker_line_color='#e96a26',
                      marker_line_width=1.5, opacity=0.8)

    return fig

## Function for creating plot of occupancy status for the city overall
## out: figure
def plotOccupancyCity():
    occupancyCity['x'] = 0

    fig = px.bar(occupancyCity, x='Units', y='x',color='OccupancyStatus', 
                animation_frame = "Year",
                color_discrete_map={'Occupied': '#009192',
                                    'Vacant': '#e96a26'},
                orientation = 'h',
                custom_data=["Unitsct"],
                labels={"OccupancyStatus": "Occupancy Status",
                        "Units": ""},
                title = cd.text['OCC_CITY_TITLE'])
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['OCC_CITY_HOVER'],
                      texttemplate = cd.text['OCC_ANNOTATE'])
    fig.update_layout(margin=go.layout.Margin(l=50, r=10, b=0, t=30, pad=15),
                        autosize=True,
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(size=17, color="rgb(7,13,30)"),
                        titlefont={'size': 19},
                        title_x = 0.55,
                        font_family="FranklinGothic",
                        font_color="#070D1E",
                        title_font_family="FranklinGothicPro",
                        title_font_color="#1C1D1E")

    fig.update_xaxes(showticklabels=False, range=[0,100])
    fig.update_yaxes(showticklabels=False, title=None)
    fig['layout']['updatemenus'][0]['x']=0.1
    fig['layout']['sliders'][0]['x']=0.1
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['OCC_CITY_HOVER']

    return fig

## Function for creating plot of tenure for the city overall
## out: figure
def plotTenureCity():
    tenureCity['x'] = 0

    fig = px.bar(tenureCity, x='Units', y='x',color='Tenure', 
                animation_frame = "Year",
                color_discrete_map={'Owner occupied': '#009192',
                                    'Renter occupied': '#5b1453'},
                orientation = 'h',
                custom_data=["Unitsct"],
                labels={"Units": ""},
                title = cd.text['TENURE_CITY_TITLE'])
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['OCC_CITY_HOVER'], 
                      texttemplate=cd.text['OCC_ANNOTATE'])
    fig.update_layout(margin=go.layout.Margin(l=50, r=10, b=0, t=30, pad=15),
                        autosize=True,
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(size=17, color="rgb(7,13,30)"),
                        titlefont={'size': 19},
                        title_x = 0.55,
                        font_family="FranklinGothic",
                        font_color="#070D1E",
                        title_font_family="FranklinGothicPro",
                        title_font_color="#1C1D1E")

    fig.update_xaxes(showticklabels=False, range=[0,100])
    fig.update_yaxes(showticklabels=False, title=None)
    fig['layout']['updatemenus'][0]['x']=0.1
    fig['layout']['sliders'][0]['x']=0.1
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['OCC_CITY_HOVER']

    return fig

## Function for creating plot of population size by neighborhood
## out: figure
def plotSizeCity():
    fig = px.line(popCity, x="Year", y=cd.opts['CITY_LIST'],
                    labels={'Year':cd.text['SIZE_X_TITLE'],
                            'value':cd.text['SIZE_Y_TITLE'],
                            'variable': '<b>City</b>'}, 
                    title=cd.text['SIZE_CITY_TITLE'],
                    height = 450,
                    color_discrete_sequence=["#ed8851", "#009192", "#7c4375", 
                                             "#dd5279", "#f7e144", "#6b6d6f"])
    fig.update_xaxes(tickvals = [2010 + 2*year for year in range(6)], 
                     range = [2008.5, 2020.5], gridcolor='Black')
    fig.update_yaxes(tickvals = [25000 + 10000 * k for k in range(4)],
                     gridcolor='Black')
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(size=17),
                    font_family="FranklinGothic",
                    font_color="#070D1E",
                    titlefont={'size': 19},
                    title_font_family="FranklinGothicPro",
                    title_font_color="#1C1D1E",
                    title_x=0.46)
    fig.update_traces(line_width=5, mode='lines')

    return fig

## Function for creating plot of industry employment populations by neighborhood
## out: figure
def plotIndustryByNeighborhood(n, compare = False, 
                               article = False, tickers = True):
    fig = px.bar(industryNeighborhood, 
                 x=n,
                 y='Industry', 
                 labels={n:cd.text['IND_X_TITLE'],
                         'Industry':cd.text['IND_Y_TITLE']}, 
                 animation_frame = "Year",
                 orientation="h", custom_data = ["Desc"], 
                 title = cd.text['IND_NEIGHBORHOOD_TITLE'].format(hood=n))
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['IND_NEIGHBORHOOD_HOVER'],
                      marker_color='#ed8851', marker_line_color='#e96a26',
                      marker_line_width=1.5, opacity=0.8)
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15), 
                      plot_bgcolor="white", 
                      paper_bgcolor="white", 
                      autosize=True, 
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.85, 
                                  y=0, 
                                  xanchor="right", 
                                  bgcolor="DimGray"), 
                      hoverlabel_align = 'left', 
                      titlefont={'size': 19}, 
                      title_x = 0.55,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## get index of neighborhood selection
        hood_index = industryNeighborhood.columns.get_loc(n)
        ## update dataset with correct ticker for neighborhood selection
        industryNeighborhood['ag'] = [f'({industryNeighborhood.iloc[i, hood_index+19]:,}' + 
                                      f' : {industryNeighborhood.iloc[i, hood_index]:.2f}%)' 
                                      for i in range(industryNeighborhood.shape[0])]
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, industryNeighborhood, 
                                [i for i in range(13)], 'Industry',
                                compare)
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                    "25", "30", "35", "40", "45", 
                                    "50", "55", "60"], 
                        tickvals = [i*5 for i in range(13)], 
                        range = [0, 76],
                        gridcolor='Black')
        fig.update_layout(titlefont={'size': 16})
    elif article:
        ## Fixed x axis size for each frame
        fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                    "25", "30", "35", "40", "45", 
                                    "50", "55", "60"], 
                        tickvals = [i*5 for i in range(13)], 
                        range = [0, 74],
                        gridcolor='Black')
        fig.update_layout(titlefont={'size': 16})
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(ticktext = ["0", "5", "10", "15", "20", 
                                    "25", "30", "35", "40", "45", 
                                    "50", "55", "60"], 
                        tickvals = [i*5 for i in range(13)], 
                        range = [0, 68],
                        gridcolor='Black')
    ## move slider's and buttons' positions slightly left
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['IND_NEIGHBORHOOD_HOVER']
            dat.marker = dict(color='#ed8851',
                              line=dict(color='#e96a26',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, industryNeighborhood, 
                                    [i for i in range(13)], 
                                    idx, 'Industry', compare)

    return fig


## Function for creating plot of age by sex by neighborhood
## out: figure
def plotAgeNeighborhood(n, compare = False, 
                        article = False, tickers = True):
    # begin building figure
    fig = px.bar(ageNeighborhood, 
                 y="Age", 
                 x=n + "_T",
                 animation_frame='Year', 
                 barmode='group',
                 orientation="h",
                 height = 550,
                 title=cd.text['AGE_NEIGHBORHOOD_TITLE'].format(hood=n), 
                 labels={'variable':cd.text['AGE_LEGEND_TITLE'], 
                         n+"_T":cd.text['AGE_X_TITLE'],
                         'Age':cd.text['AGE_Y_TITLE']})
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 19},
                      title_x = 0.56,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## get index of neighborhood selection
        hood_index = ageNeighborhood.columns.get_loc(n + "_T")
        ## update dataset with correct ticker for neighborhood selection
        ageNeighborhood['ag'] = [f'({ageNeighborhood.iloc[i, hood_index+1]:,}' + 
                                 f' : {ageNeighborhood.iloc[i, hood_index]:.2f}%)' 
                                 for i in range(ageNeighborhood.shape[0])]
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, ageNeighborhood, 
                                [i for i in range(18)], 'Age',
                                compare)
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(11)], 
                        range = [0, 62],
                        gridcolor='Black')
    elif article:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(11)], 
                        range = [0, 61],
                        gridcolor='Black')
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(11)], 
                        range = [0, 56],
                        gridcolor='Black')
    # update legend and hovers for animated frames
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['AGE_NEIGHBORHOOD_HOVER']
            dat.marker = dict(color='#7c4375',
                              line=dict(color='#5b1453',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, ageNeighborhood, 
                                    [i for i in range(18)], 
                                    idx, 'Age', compare)
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['AGE_NEIGHBORHOOD_HOVER'],
                      marker_color='#7c4375', marker_line_color='#5b1453',
                      marker_line_width=1.5, opacity=0.8)

    return fig

## Function for creating race plot for the individual neighborhoods
## in: neighborhood, t/f whether the plot is for the comparison page
## out: figure
def plotRaceNeighborhood(n, compare = False, 
                         article = False, tickers = True):
    # begin building figure
    fig = px.bar(raceNeighborhood, 
                 y="Race and Ethnicity", 
                 x=n,
                 animation_frame='Year',
                 orientation="h",
                 height = 500,
                 title=cd.text['RACE_NEIGHBORHOOD_TITLE'].format(hood=n), 
                 labels={n:cd.text['RACE_X_TITLE'],
                         'Race and Ethnicity':cd.text['RACE_Y_TITLE']})
    ## Fix bar order
    fig.update_yaxes(categoryorder="total ascending")
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 19},
                      title_x = 0.59,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## get index of neighborhood selection
        hood_index = raceNeighborhood.columns.get_loc(n)
        ## update dataset with correct ticker for neighborhood selection
        raceNeighborhood['ag'] = [f'({raceNeighborhood.iloc[i, hood_index+19]:,} : {raceNeighborhood.iloc[i, hood_index]:.2f}%)' 
                                for i in range(raceNeighborhood.shape[0])]
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, raceNeighborhood, 
                                [i for i in range(8)], 'Race and Ethnicity',
                                compare)
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*10 for i in range(10)], 
                        range = [0, 122],
                        gridcolor='Black')
        fig.update_layout(titlefont={'size': 17})
    elif article:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*10 for i in range(10)], 
                        range = [0, 118],
                        gridcolor='Black')
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*10 for i in range(11)], 
                        range = [0, 114],
                        gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.marker = dict(color='#33a7a8',
                              line=dict(color='#009192',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, raceNeighborhood, 
                                    [i for i in range(8)], 
                                    idx, 'Race and Ethnicity', compare)
    ## Set bar color
    fig.update_traces(marker_color='#33a7a8', marker_line_color='#009192',
                      marker_line_width=1.5, opacity=0.8)

    return fig

## Function for creating plot of median income by neighborhood
## in: neighborhood (string or list if comparing)
## out: figure
def plotIncomeNeighborhood(n):
    if isinstance(n, list):
        n.append('Year')
        dfIncomeHood = incomeNeighborhood[n]
        fig = px.line(dfIncomeHood, x="Year", y=n, 
                        title="Median Household Income by Year for " + n[0] + \
                            " and " + n[1] + ' ($)',
                        labels={"variable": "Neighborhood",
                                "value": "<b>Median Household Income ($)</b>",
                                "Year": "<b>Year</b>"},
                        markers = True, height = 450,
                        color_discrete_sequence=["#7c4375", "#009192"])
        fig.update_layout(title_x=0.46)
    else:
        n = [n]
        n.append('Year')
        dfIncomeHood = incomeNeighborhood[n]
        fig = px.line(dfIncomeHood, x="Year", y=n[0],
                        title="Median Household Income by Year for " + n[0] + ' ($)',
                        labels={n[0]: "<b>Median Household Income ($)</b>",
                                "Year": "<b>Year</b>"},
                        markers = True, height = 450,
                        color_discrete_sequence=["#7c4375"])
        fig.update_layout(title_x=0.517)

    fig.update_xaxes(tickvals = [year for year in range(2013, 2021)], 
                     range = [2012.5, 2020.5], gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(size=17),
                    font_family="FranklinGothic",
                    font_color="#070D1E",
                    titlefont={'size': 19},
                    title_font_family="FranklinGothicPro",
                    title_font_color="#1C1D1E")
    fig.update_traces(line_width=5, mode='lines')
                      
    return fig

## Function for creating income distribution plot for the neighborhoods
## in: neighborhood, t/f whether the plot is for the comparison page
## out: figure
def plotIncomeDistNeighborhood(n, compare = False, 
                               article = False, tickers = True):
    # begin building figure
    fig = px.bar(incomeNeighborhoodDist, 
                 y="Bracket", 
                 x=n,
                 animation_frame='Year',
                 orientation="h",
                 title=cd.text['INCOME_NEIGHBORHOOD_TITLE'].format(hood=n), 
                 height=550,
                 labels={n:cd.text['INCOME_X_TITLE'],
                         'Bracket':cd.text['INCOME_Y_TITLE']})
    # update layout
    fig.update_layout(margin=go.layout.Margin(l=200, r=10, b=0, t=30, pad=15),
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(size=17, color="rgb(7,13,30)"),
                      legend=dict(yanchor="bottom", 
                                  x=0.90, 
                                  y=0.85, 
                                  xanchor="right",
                                  bgcolor="DimGray"),
                      titlefont={'size': 19},
                      title_x = 0.555,
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E")
    if tickers:
        ## get index of neighborhood selection
        hood_index = incomeNeighborhoodDist.columns.get_loc(n)
        ## update dataset with correct ticker for neighborhood selection
        incomeNeighborhoodDist['ag'] = [f'({incomeNeighborhoodDist.iloc[i, hood_index+19]:,}' + \
                                        f' : {incomeNeighborhoodDist.iloc[i, hood_index]:.2f}%)' 
                                        for i in range(incomeNeighborhoodDist.shape[0])]
        ## Adds (count : pct) ticker at far right of chart
        fig = addFigAnnotations(fig, incomeNeighborhoodDist, 
                                [i for i in range(16)], 'Bracket',
                                compare)
    if compare:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(8)], 
                        range = [0, 43],
                        gridcolor='Black')
    elif article:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(8)], 
                        range = [0, 42],
                        gridcolor='Black')
    else:
        ## Fixed x axis size for each frame
        fig.update_xaxes(tickvals = [i*5 for i in range(8)], 
                        range = [0, 40],
                        gridcolor='Black')
    fig['layout']['updatemenus'][0]['x']=-0.04
    fig['layout']['sliders'][0]['x']=-0.04
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.marker = dict(color='#ed8851',
                              line=dict(color='#e96a26',
                                        width=1.5))
        if tickers:
            f = addFrameAnnotations(f, incomeNeighborhoodDist, 
                                    [i for i in range(16)], 
                                    idx, 'Bracket', compare)
    fig.update_traces(marker_color='#ed8851', marker_line_color='#e96a26',
                      marker_line_width=1.5, opacity=0.8)
    
    return fig

## Function for creating plot of occupancy status by neighborhood
## out: figure
def plotOccupancyNeighborhood(n):
    occupancyNeighborhood['x'] = 0

    fig = px.bar(occupancyNeighborhood, x=n, y='x',
                color='OccupancyStatus', 
                animation_frame = "Year",
                color_discrete_map={'Occupied': '#009192',
                                    'Vacant': '#e96a26'},
                orientation = 'h',
                custom_data=[n + "ct"],
                labels={"OccupancyStatus": "Occupancy Status",
                        n: ""},
                height = 400,
                title = cd.text['OCC_NEIGHBORHOOD_TITLE'].format(hood=n))
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['OCC_NEIGHBORHOOD_HOVER'],
                      texttemplate = cd.text['OCC_ANNOTATE'])
    fig.update_layout(margin=go.layout.Margin(l=50, r=10, b=0, t=30, pad=15),
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(size=17, color="rgb(7,13,30)"),
                        titlefont={'size': 19},
                        title_x = 0.55,
                        font_family="FranklinGothic",
                        font_color="#070D1E",
                        title_font_family="FranklinGothicPro",
                        title_font_color="#1C1D1E")

    fig.update_xaxes(showticklabels=False, range=[0,100])
    fig.update_yaxes(showticklabels=False, title=None)
    fig['layout']['updatemenus'][0]['x']=0.08
    fig['layout']['sliders'][0]['x']=0.08
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['OCC_NEIGHBORHOOD_HOVER']

    return fig

## Function for creating plot of tenure by neighborhood
## out: figure
def plotTenureNeighborhood(n):
    tenureNeighborhood['x'] = 0

    fig = px.bar(tenureNeighborhood, x=n, y='x',
                color='Tenure', 
                animation_frame = "Year",
                color_discrete_map={'Owner occupied': '#009192',
                                    'Renter occupied': '#5b1453'},
                orientation = 'h',
                custom_data=[n + "ct"],
                labels={n: ""},
                height = 400,
                title = cd.text['TENURE_NEIGHBORHOOD_TITLE'].format(hood=n))
    ## Change text displayed when mouse hovering over bar
    fig.update_traces(hovertemplate = cd.text['OCC_NEIGHBORHOOD_HOVER'],
                      texttemplate = cd.text['OCC_ANNOTATE'])
    fig.update_layout(margin=go.layout.Margin(l=50, r=10, b=0, t=30, pad=15),
                        plot_bgcolor="white",
                        paper_bgcolor="white",
                        font=dict(size=17, color="rgb(7,13,30)"),
                        titlefont={'size': 19},
                        title_x = 0.55,
                        font_family="FranklinGothic",
                        font_color="#070D1E",
                        title_font_family="FranklinGothicPro",
                        title_font_color="#1C1D1E")

    fig.update_xaxes(showticklabels=False, range=[0,100])
    fig.update_yaxes(showticklabels=False, title=None)
    fig['layout']['updatemenus'][0]['x']=0.08
    fig['layout']['sliders'][0]['x']=0.08
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 500
    ## Loop through frames to edit hover and by-frame ticker annotations
    for idx, f in enumerate(fig.frames):
        for dat in f.data:
            dat.hovertemplate = cd.text['OCC_NEIGHBORHOOD_HOVER']

    return fig


## Function for creating plot of population size by neighborhood
## in: neighborhood (string or list if comparing)
## out: figure
def plotSizeNeighborhood(n):
    if isinstance(n, list):
        dfPopHood = popNeighborhood[popNeighborhood['NAME'].isin(n)]
        dfPopHood = dfPopHood.reset_index(drop=True)
        fig = px.line(dfPopHood, x="Year", y="Population", color='NAME',
                        title="Population by Year for " + dfPopHood['NAME'][0] + \
                            " and " + dfPopHood['NAME'][1],
                        labels={"NAME": "Neighborhood",
                                "Year": cd.text['SIZE_X_TITLE'],
                                "Population": cd.text['SIZE_Y_TITLE']},
                        markers = True, height = 500,
                        color_discrete_sequence=["#7c4375", "#009192"])
        fig.update_layout(title_x=0.46)
    else:
        dfPopHood = popNeighborhood[popNeighborhood['NAME'] == n]
        dfPopHood = dfPopHood.reset_index(drop=True)
        fig = px.line(dfPopHood, x="Year", y="Population",
                        title="Population by Year for " + dfPopHood['NAME'][0],
                        labels={"Year": cd.text['SIZE_X_TITLE'],
                                "Population": cd.text['SIZE_Y_TITLE']},
                        markers = True, height = 500,
                        color_discrete_sequence=["#7c4375"])
        fig.update_layout(title_x=0.517)

    fig.update_xaxes(tickvals = [year for year in range(2013, 2021)], 
                     range = [2012.5, 2020.5], gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(size=17),
                    font_family="FranklinGothic",
                    font_color="#070D1E",
                    titlefont={'size': 19},
                    title_font_family="FranklinGothicPro",
                    title_font_color="#1C1D1E")
    fig.update_traces(line_width=5, mode='lines')
                      
    return fig