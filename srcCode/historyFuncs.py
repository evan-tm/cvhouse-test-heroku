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
        y_label = "Yearly Number of Sales"
    else:
        to_plot = "median"
        y_label = "Yearly Median Sale Price [$, inflation adjusted]"
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"][to_plot], 
                                    name="Charlottesville City"))
    syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(neighs.encode('ascii')).decode('ascii') + ".pkl")
    fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"][to_plot], name=neighs))
    fig.update_layout(xaxis_title="Year",
                      yaxis_title=y_label,
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(7,13,30)"))
    fig.update_xaxes(gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig['data'][0]['showlegend'] = True
    return fig


def plotCityHistoryPrice():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["median"], 
                                    name="All Sales"))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["median"], 
                             name="Single Family"))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["median"], 
                             name="Two Family"))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["median"], 
                             name="Multi-family and Others"))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"],
                     gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Median Sale Price [$, inflation adjusted]",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(7,13,30)"))
    fig['data'][0]['showlegend'] = True
    return fig

def plotCityHistoryQuantity():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["count"], 
                                    name="All Sales"))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["count"], 
                             name="Single Family"))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["count"], 
                             name="Two Family"))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["count"], 
                             name="Multi-family and Others"))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"],
                     gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Number of Sales",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(7,13,30)"))
    fig['data'][0]['showlegend'] = True
    return fig\

def plotCompareHistorySales(n, var, neighs):
    if var == "Sales Quantity":
        to_plot = "count"
        y_label = "Yearly Number of Sales"
    else:
        to_plot = "median"
        y_label = "Yearly Median Sale Price [$, inflation adjusted]"
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"][to_plot], 
                                    name="Charlottesville City"))
    if n:
        for each in neighs:
            syn = pd.read_pickle("data/rolling/sales_year_nb_" + base64.b64encode(each.encode('ascii')).decode('ascii') + ".pkl")
            fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"][to_plot], name=each))
    fig.update_layout(xaxis_title="Year",
                      yaxis_title=y_label,
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=13, color="rgb(7,13,30)"))
    fig.update_xaxes(gridcolor='Black')
    fig.update_yaxes(gridcolor='Black')
    fig['data'][0]['showlegend'] = True
    return fig