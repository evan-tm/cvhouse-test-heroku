# ------------------History of sales functions------------------#
import plotly.graph_objects as go
import base64
import pandas as pd

# Loading rolling sales data
sales_year = pd.read_pickle("data/rolling/sales_year.pkl")
sales_year_single = pd.read_pickle("data/rolling/sales_year_single.pkl")
sales_year_two = pd.read_pickle("data/rolling/sales_year_two.pkl")
sales_year_multi = pd.read_pickle("data/rolling/sales_year_multi.pkl")

def plotNeighborhoodHistorySales(neighs, var):
    if var == "Sales Quantity":
        to_plot = "count"
        y_label = "<b>Number of Sales</b>"
        if len(neighs) == 2:
            title = "Sales Quantity by Year for " + neighs[0] + " and " + neighs[1]
        else:
            title = "Sales Quantity by Year for " + neighs
    else:
        to_plot = "median"
        y_label = "<b>Median Sale Price ($, inflation adjusted)</b>"
        if len(neighs) == 2:
            title = "Median Sale Price by Year for " + neighs[0] + " and " + neighs[1] + " ($, inflation adjusted)"
        else:
            title = "Median Sale Price by Year for " + neighs + " ($, inflation adjusted)"
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"][to_plot], 
                                    name="Charlottesville City", line=dict(color="#7c4375")))
    syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(neighs.encode('ascii')).decode('ascii') + ".pkl")
    fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"][to_plot], 
                             name=neighs, line=dict(color="#009192")))
    fig.update_layout(title=title,
                      xaxis_title="<b>Year</b>",
                      yaxis_title=y_label,
                      margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=17),
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      titlefont={'size': 19},
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E",
                      title_x=0.453)
    fig.update_xaxes(gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig['data'][0]['showlegend'] = True
    return fig


def plotCityHistoryPrice():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["median"], 
                                    name="All Sales", line=dict(color="#7c4375")))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["median"], 
                             name="Single Family", line=dict(color='#009192')))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["median"], 
                             name="Two Family", line=dict(color='#ed8851')))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["median"], 
                             name="Multi-family and Others", line=dict(color='#6b6d6f')))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"],
                     gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig.update_layout(title="Median Sale Price of Residential Property by Year in Charlottesville, Virginia ($, inflation adjusted)",
                      xaxis_title="<b>Year</b>",
                      yaxis_title="<b>Median Sale Price ($, inflation adjusted)</b>",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=17),
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      titlefont={'size': 19},
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E",
                      title_x=0.453)
    fig['data'][0]['showlegend'] = True
    return fig

def plotCityHistoryQuantity():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["count"], 
                                    name="All Sales", line=dict(color="#7c4375")))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["count"], 
                             name="Single Family", line=dict(color='#009192')))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["count"], 
                             name="Two Family", line=dict(color='#ed8851')))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["count"], 
                             name="Multi-family and Others", line=dict(color='#6b6d6f')))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"],
                     gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig.update_layout(title="Sales Quantity of Residential Property by Year in Charlottesville, Virginia",
                      xaxis_title="<b>Year</b>",
                      yaxis_title="<b>Number of Sales</b>",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=17),
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      titlefont={'size': 19},
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E",
                      title_x=0.453)
    fig['data'][0]['showlegend'] = True
    return fig\

def plotCompareHistorySales(n, var, neighs):
    if var == "Sales Quantity":
        to_plot = "count"
        y_label = "<b>Number of Sales</b>"
        title = "Sales Quantity of Residential Property by Year in Charlottesville, Virginia"
    else:
        to_plot = "median"
        y_label = "<b>Median Sale Price ($, inflation adjusted)</b>"
        title = "Median Sale Price of Residential Property by Year in Charlottesville, Virginia ($, inflation adjusted)"
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"][to_plot], 
                                    name="Charlottesville City", line=dict(color="#7c4375")))
    if n:
        i = 0
        colors = ['#009192', '#ed8851']
        for each in neighs:
            syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(each.encode('ascii')).decode('ascii') + ".pkl")
            fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"][to_plot], 
                                     name=each, line=dict(color=colors[i])))
            i = i + 1
    fig.update_layout(title = title,
                      xaxis_title="<b>Year</b>",
                      yaxis_title=y_label,
                      margin=go.layout.Margin(l=0, r=0, b=0, t=50, pad=15),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=17),
                      font_family="FranklinGothic",
                      font_color="#070D1E",
                      titlefont={'size': 19},
                      title_font_family="FranklinGothicPro",
                      title_font_color="#1C1D1E",
                      title_x=0.453)
    fig.update_xaxes(gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig['data'][0]['showlegend'] = True
    return fig