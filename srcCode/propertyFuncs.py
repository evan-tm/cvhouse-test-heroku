# ------------------Property map functions------------------#
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import geopandas as gpd
import pandas as pd

# Cleaned sales data file
sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
# Sales data date cleaning
sales_clean_simple["SaleDate"] = pd.to_datetime(sales_clean_simple["SaleDate"])

# Neighborhood data file
neighborhood_simple = gpd.read_file("neighborhood_simple.geojson")

#mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
#mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
mapbox_token_public_ind = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
mapbox_style_ind = "mapbox://styles/evan-tm/cl1ik4lmv003z15ru0ip4isbz"
mapbox_token_public_hood = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
mapbox_style_hood = "mapbox://styles/evan-tm/cl1xthgjs000i14qv2eaz09w5"

millnames = ['','k','M','B','T']

def millify(n):
    if not n:
        return "Not available"
    elif np.isnan(n):
        return "Not available"
    else:
        n = float(n)
        millidx = max(0, min(len(millnames) - 1, int(np.floor(0 if n == 0 else np.log10(abs(n))/3))))
        return '{:.2f}{}'.format(n / 10 ** (3 * millidx), millnames[millidx])


def plotAffordMap(lod, y):
    mask = (sales_clean_simple["Year"] == y)
    sales_year = sales_clean_simple[mask].set_index("ParcelNumber")
    if lod == "Neighborhood":
        # Neighborhood map
        sales_year_nba = sales_year.groupby("Neighborhood").agg({"SaleAmountAdjusted": ["size", "mean"]}).reset_index()
        sales_year_nba.columns = ["Neighborhood", "NumSales", "MeanSales"]
        sales_year_nba = neighborhood_simple.merge(sales_year_nba, how="inner", 
                                                   right_on="Neighborhood", left_on="NAME")
        sales_year_nba["MeanSalesStr"] = sales_year_nba["MeanSales"].apply(millify)
        vmin, vmax = np.nanpercentile(sales_year_nba["MeanSales"], (5, 95))
        fig = px.choropleth_mapbox(sales_year_nba, 
                                   geojson=sales_year_nba.geometry,
                                   locations=sales_year_nba.index, 
                                   color="MeanSales",
                                   range_color=[vmin, vmax],
                                   labels={"MeanSales": "Average Total Sale Price"},
                                   hover_name="Neighborhood", 
                                   hover_data={"MeanSalesStr": True, "NumSales": True},
                                   center={"lat": 38.039, "lon": -78.47826}, 
                                   zoom=12, 
                                   )
        fig.update_traces(hovertemplate="<br>".join([
            "%{hovertext}",
            "",
            "Average Sale Price in Neighborhood: $%{customdata[0]}",
            "Number of Sales Recorded: %{customdata[1]}"]))
        fig.update_layout(mapbox_accesstoken=mapbox_token_public_hood, 
                        mapbox_style=mapbox_style_hood,
                        margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        autosize=True,
                        font=dict(size=16),
                        font_family="franklin-gothic-atf,Helvetica,sans-serif",
                        font_color="#070D1E",
                        title_font_family="franklin-gothic-condensed,Helvetica,sans-serif",
                        title_font_color="#1C1D1E")
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
    else:
        # Individual property map
        vmin, vmax = np.nanpercentile(sales_year["SaleAmountAdjusted"], (5, 95))
        fig = px.choropleth_mapbox(sales_year, 
                                   geojson=sales_year.geometry, 
                                   locations=sales_year.index, 
                                   color="SaleAmountAdjusted",
                                   range_color=[vmin, vmax],
                                   labels={"SaleAmountAdjusted": "Total Sale Price"},
                                   hover_name="Address", 
                                   hover_data={"SaleAmountStr": True, "AcreageStr": True, 
                                               "SaleDateStr": True, "Zone": True},
                                   center={"lat": 38.039, "lon": -78.47826}, 
                                   zoom=14,
                                  )
        fig.update_traces(hovertemplate="<br>".join([
            "%{hovertext}",
            "",
            "Total Sale Price: $%{customdata[0]}",
            "Acreage: %{customdata[1]}",
            "Last sale on %{customdata[2]}",
            "Zoning: %{customdata[3]}"]))
        fig.update_layout(mapbox_accesstoken=mapbox_token_public_ind, 
                        mapbox_style=mapbox_style_ind,
                        margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        autosize=True,
                        font=dict(size=16),
                        font_family="franklin-gothic-atf,Helvetica,sans-serif",
                        font_color="#070D1E",
                        title_font_family="franklin-gothic-condensed,Helvetica,sans-serif",
                        title_font_color="#1C1D1E")
        fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig['layout']['uirevision'] = 'something'
    return fig
