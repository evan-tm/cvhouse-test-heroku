import numpy as np
import os
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import Input, Output, State, dcc, html
from hampel import hampel


mapbox_token_public = "pk.eyJ1IjoieGlubHVuY2hlbmciLCJhIjoiY2t0c3g2eHRrMWp3MTJ3cDMwdDAyYnA2OSJ9.tCcD-LyXD1OK-T6uDd8CYA"
mapbox_style = "mapbox://styles/xinluncheng/cktsxjvd923p618mw4fut9gav"
external_stylesheets = [dbc.themes.BOOTSTRAP] 
# ----------------------------------------------------------------------------
# Data Files:
# Cleaned sales data file
sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
# Neighborhood data file
neighborhood_simple = gpd.read_file("neighborhood_simple.geojson")
# Census data file
census_simple = gpd.read_file("censusBlockDataFull.geojson")
# Industry by sector data file
indBySector = pd.read_csv("data/indBySectorHistFull.csv")
# Industry by neighborhood  data
indByNeighborhood = pd.read_csv("data/indByNeighborhoodHistFull.csv")
dropdown_neighborhood = ""
dropdown_neighborhood_lod_opts = ["Barracks Road", "Rose Hill", "Lewis Mountain", "Starr Hill",
                                  "Woolen Mills", "10th & Page", "The Meadows", "Martha Jefferson",
                                  "Johnson Village", "Greenbrier", "Barracks / Rugby", "North Downtown",
                                  "Locust Grove", "Jefferson Park Ave", "Fifeville", "Fry's Spring",
                                  "Ridge Street", "Venable", "Belmont"]
dropdown_neighborhood_default = dropdown_neighborhood_lod_opts[0]
# Rental affordability data
rentData = pd.read_csv('data/acsRent2019.csv')
# Childcare affordability data
ccareData = pd.read_csv('data/childcareCosts.csv')
# Food affordability data
foodData = pd.read_csv('data/foodCosts.csv')
# Transportation affordability data
transportData = pd.read_csv('data/transportCosts.csv')
# Health care out-of-pocket affordability data
oopHealthcareData = pd.read_csv('data/oopHealthcareAnnual.csv')
# Heatlh care premium affordability data
premiumHealthcareData = pd.read_csv('data/premiumHealthcare.csv')
# ----------------------------------------------------------------------------
# Helper functions
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

def nanformat(n, strcode):
    if not n:
        return "Not available"
    elif np.isnan(n):
        return "Not available"
    else:
        return strcode % n

## Calculates affordable rent cost for a two-bedroom apt based on median gross rent
## in: median gross rent (Charlottesville overall or neighborhood-specific)
## out: affordable rent cost for the geographic area described by the input
def hudCalc(acsRent):
    return acsRent * 1.05437 * 1.02916 * 1.04530

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
    
def plothhInc():
    # Function for creating plot of population size by hh income bracket
    fig = px.bar(hhIncPcts, x='bracket', y='hhInc', color='hhInc', 
                 labels={'bracket':'Income Bracket', 
                         'hhInc':'Households (% of total, n = 89829)'}, height=400)
    fig.update_layout(margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    return fig

## Function for creating plot of industry employment populations by sector
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

## logic for getting correct index to pull from oopHealthcareData
## in: age to find group for
## out: index for age_group row
def getAgeIdx(age):
    if age < 25:
        return 3
    elif age >= 25 and age < 35:
        return 7
    elif age >= 35 and age < 45:
        return 11
    elif age >= 45 and age < 55:
        return 15
    elif age >= 55 and age < 65:
        return 19
    else:
        return 23

## Approximates monthly tax payment for a given income
## in: status, income, adultCount, kidCount
## out: monthly tax
def getTax(status, income, adultCount, kidCount):
    
    optsTax = afford_dropdown_tax_opts
    eitc = 0
    povc = 0

    numPeople = adultCount + kidCount
    povertyLine = 8870 + 4720 * numPeople
    # check for VA low income tax credit qualification
    if (income < povertyLine):
        povc = 300 * numPeople
    # switch for tax filing status
    if status == optsTax[0]:
        income = income - 12950 # single filing status deduction for 2022
        # fed tax switch
        if income < 10276:
            fedTax = income * 0.1
        elif income >= 10276 and income < 41776:
            fedTax = 1027.50 + (income - 10275) * 0.12
        elif income >= 41776 and income < 89076:
            fedTax = 4807.50 + (income - 41775) * 0.22
        elif income >= 89076 and income < 170051:
            fedTax = 15213.5 + (income - 89075) * 0.24
        elif income >= 170051 and income < 215951:
            fedTax = 34647.5 + (income - 170050) * 0.32
        elif income >= 215951 and income < 539901:
            fedTax = 49335.5 + (income - 215950) * 0.35
        else:
            fedTax = 162718.0 + (income - 539900) * 0.37
        
        # earned income tax credit switch
        if income < 21431 and kidCount == 0:
            eitc = 1502.0
        elif income < 42159 and kidCount == 1:
            eitc = 3618.0
        elif income < 47916 and kidCount == 2:
            eitc = 5980.0
        elif income < 51465 and kidCount >= 3:
            eitc = 6728.0
    elif status == optsTax[1]:
        income = income - 25900 # married filing status deduction for 2022
        if income < 20551:
            fedTax = income * 0.1
        elif income >= 20551 and income < 83551:
            fedTax = 2055.0 + (income - 20550) * 0.12
        elif income >= 83551 and income < 178151:
            fedTax = 9615.0 + (income - 83550) * 0.22
        elif income >= 178151 and income < 340101:
            fedTax = 30427.0 + (income - 178150) * 0.24
        elif income >= 340101 and income < 431901:
            fedTax = 69295.0 + (income - 340100) * 0.32
        elif income >= 431901 and income < 647851:
            fedTax = 98671.0 + (income - 431900) * 0.35
        else:
            fedTax = 174253.5 + (income - 647850) * 0.37

        # earned income tax credit switch
        if income < 27381 and kidCount == 0:
            eitc = 1502.0
        elif income < 48109 and kidCount == 1:
            eitc = 3618.0
        elif income < 53866 and kidCount == 2:
            eitc = 5980.0
        elif income < 57415 and kidCount >= 3:
            eitc = 6728.0
    else:
        income = income - 19400 # head of household filing status deduction for 2022
        if income < 14651:
            fedTax = income * 0.1
        elif income >= 14651 and income < 55901:
            fedTax = 1465.0 + (income - 14650) * 0.12
        elif income >= 55901 and income < 89051:
            fedTax = 6415.0 + (income - 55900) * 0.22
        elif income >= 89051 and income < 170051:
            fedTax = 13708.0 + (income - 89050) * 0.24
        elif income >= 170051 and income < 215951:
            fedTax = 33148.0 + (income - 170050) * 0.32
        elif income >= 215951 and income < 539901:
            fedTax = 47836.0 + (income - 215950) * 0.35
        else:
            fedTax = 161218.5 + (income - 539900) * 0.37

        # earned income tax credit switch
        if income < 21431 and kidCount == 0:
            eitc = 1502.0
        elif income < 42159 and kidCount == 1:
            eitc = 3618.0
        elif income < 47916 and kidCount == 2:
            eitc = 5980.0
        elif income < 51465 and kidCount >= 3:
            eitc = 6728.0
    
    # if income less than standard deduction
    if income < 0:
        return 0.0
    
    ficaTax = income * 0.0765

    # state tax switch
    if income < 3001:
        stateTax = income * 0.02
    elif income >= 3001 and income < 5001:
        stateTax = 60.0 + (income - 3000) * 0.03
    elif income >= 5001 and income < 17001:
        stateTax = 120.0 + (income - 5000) * 0.05
    else:
        stateTax = 720.0 + (income - 17000) * 0.0575
    
    return (fedTax + stateTax + ficaTax - eitc - povc) / 12.0




# History by zoning graph
def history_zoning_num():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["count"], 
                                    name="All Sales"))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["count"], 
                             name="Single Family"))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["count"], 
                             name="Two Family"))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["count"], 
                             name="Multi-family and Others"))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"])
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Number of Sales",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig

def history_zoning_price():
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["median"], 
                                    name="All Sales"))
    fig.add_trace(go.Scatter(x=sales_year_single["SaleDate"], y=sales_year_single["SaleAmountAdjusted"]["median"], 
                             name="Single Family"))
    fig.add_trace(go.Scatter(x=sales_year_two["SaleDate"], y=sales_year_two["SaleAmountAdjusted"]["median"], 
                             name="Two Family"))
    fig.add_trace(go.Scatter(x=sales_year_multi["SaleDate"], y=sales_year_multi["SaleAmountAdjusted"]["median"], 
                             name="Multi-family and Others"))
    fig.update_xaxes(range=["1945-01-01T00:00:00Z", "2022-12-31T23:59:59Z"])
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Median Sale Price [$, inflation adjusted]",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig


# ----------------------------------------------------------------------------
# Cleaned data file
sales_clean_simple = gpd.read_file("real_estate_sales_simple.geojson")
sales_clean_simple["SaleDate"] = pd.to_datetime(sales_clean_simple["SaleDate"])
sales_year = pd.read_pickle("rolling/sales_year.pkl")
sales_year_single = pd.read_pickle("rolling/sales_year_single.pkl")
sales_year_two = pd.read_pickle("rolling/sales_year_two.pkl")
sales_year_multi = pd.read_pickle("rolling/sales_year_multi.pkl")
# Neighborhood data file
neighborhood_simple = gpd.read_file("neighborhood_simple.geojson")
# Census data file
census_simple = gpd.read_file("censusBlockDataFull.geojson")
# Rental affordability data calculations
twoBR = rentData
twoBR['Median_Gross_Rent'] = hudCalc(twoBR['Median_Gross_Rent'])
oneBR = twoBR
oneBR['Median_Gross_Rent'] = twoBR['Median_Gross_Rent'] * 0.841
studio = twoBR
studio['Median_Gross_Rent'] = twoBR['Median_Gross_Rent'] * 0.81
# ----------------------------------------------------------------------------
# All the texts
## Sidebar
sidebar_top = "Top"
sidebar_afford = "Affordability"
sidebar_imap = "Exploring Housing History"
sidebar_census = "Census Information"
## Header
title = "Charlottesville Housing Affordability:  "
subtitle = "Building a Picture of Who Can Afford What"
header_text = '''Our goal is to bring attention to housing affordability issues
in the Charlottesville community. Below, you can explore what you can currently 
afford with our price prediction tool. Additionally, you can see where housing 
prices are headed and understand where they’ve been historically. '''
## Affordability
#afford_title = "What Can You Afford?"
#afford_dropdown_title = "Learn more about our neighborhoods:"
#afford_dropdown_industry_desc = "By Industry:"
#afford_dropdown_industry_opts = ["Industry 1", "Industry 2", "Industry 3"]
#afford_dropdown_industry_default = afford_dropdown_industry_opts[0]
afford_dropdown_person_info_title = "Affordability Calculator:"
afford_input_salary_desc = "Household Income:"
afford_input_salary_default = 26000
afford_dropdown_homeSize_desc = "Rental Size:"
afford_dropdown_homeSize_opts = ['Studio', '1 Bedroom', '2 Bedrooms']
afford_dropdown_homeSize_default = afford_dropdown_homeSize_opts[1]
afford_input_adults_desc = 'Adults:'
afford_input_adults_default = 1
afford_input_kids_desc = "Kids:"
afford_input_kids_default = 0
afford_input_childcare_desc = "# in Childcare:"
afford_input_childcare_default = 0
afford_input_age_desc = "Your Age:"
afford_input_age_default = "30"
afford_dropdown_transport_desc = "Transportation Type:"
afford_dropdown_transport_opts = ['CAT Public Bus', 'Personal Vehicle']
afford_dropdown_transport_default = afford_dropdown_transport_opts[0]
afford_dropdown_vehicle_desc = "Vehicle Type:"
afford_dropdown_vehicle_opts = ['Small Sedan', 'Medium Sedan', 
                                'Compact SUV', 'Medium SUV', 
                                'Pickup', 'Hybrid', 'Electric']
afford_dropdown_vehicle_default = afford_dropdown_vehicle_opts[0]
afford_input_hcare_desc = "Healthcare (Annually):"
afford_input_hcare_default = ""
afford_input_tech_desc = "Technology (Monthly):"
afford_input_tech_default = 100
afford_input_tech_tip = "Cell phone plan, internet, etc."
afford_dropdown_tax_desc = "Tax Status:"
afford_dropdown_tax_opts = ['Single', 'Married', 'Head of House']
afford_dropdown_tax_default = afford_dropdown_tax_opts[0]
afford_button = "Calculate"
afford_dropdown_lod_desc = "Level of Detail"
afford_dropdown_lod_opts = ["Neighborhood", "Individual Properties"]
afford_dropdown_lod_default = afford_dropdown_lod_opts[0]
afford_prediction_text = "You can afford 0% of houses in cville."
afford_prediction_algo = "ALICE affordability info"
## History
history_title = "History of Real Estate Sales"
history_description = '''Click on the legend of plot to hide and unhide one category.'''
history_zoning_title = "By Zoning"
history_zoning_checklist_single = "Single family"
history_zoning_checklist_two = "Two family"
history_zoning_checklist_multi = "Multi family and others"
history_neighborhood_title = "By Neighborhood"
## Neighborhood
## Industry and Sector Counts of the civilian employed population aged 16 and 
##   older in Charlottesville
HOVER_TEMPLATE_PCT = '<i>Sector</i>: %{data.name}' + \
                 '<br>%{value:.2f}% of Total Employed<br>' + \
                 'Industries: <b>%{customdata}</b>' + \
                 '<extra></extra>'
IND_SECTOR_TITLE = 'Industries and Sectors of Charlottesville Residents (% of Total Employed Age 16+ Civilians)'
sector_legend = "Sector"

# Industry by Neighborhood
neighborhood_title = "Industries by Neighborhood"
neighborhood_legend = "Neighborhood"
HOVER_TEMPLATE_PCT_HOOD = '%{value:.2f}% of Total Employed<br>' + \
                 'Industries: <b>%{customdata}</b>' + \
                 '<extra></extra>'
IND_NEIGHBORHOOD_TITLE = 'Industries of {hood} Residents (% of Total Employed Age 16+ Civilians)'

## Census
census_title = "Census Information"
## footnote
source = '''Data from Charlotteville Open Data Portal. Last update March 1, 2022.
Prices have been adjusted for inflation. Only sales with state code Residential 
(urban/suburban) and Multifamily are included.'''
# ----------------------------------------------------------------------------
# Data processing for census_plot
colsHHInc = ['GEOID', 'hhInc10E', 'hhInc10to15E', 'hhInc15to20E', 
             'hhInc20to25E', 'hhInc25to30E', 'hhInc30to35E', 
             'hhInc35to40E', 'hhInc40to45E', 'hhInc45to50E', 
             'hhInc50to60E', 'hhInc60to75E', 'hhInc75to100E', 
             'hhInc100to125E', 'hhInc125to150E', 'hhInc150to200E',
             'hhInc200E']
hhIncDF = census_simple[colsHHInc]
hhIncPivot = pd.wide_to_long(hhIncDF, stubnames="hhInc", i="GEOID", j="bracket", suffix='\\w+')
hhIncPivot = hhIncPivot.reset_index().reindex(["GEOID", "bracket", "hhInc"], axis=1)
hhIncPcts = hhIncPivot.groupby(hhIncPivot['bracket']).agg({'hhInc':'sum'}).reset_index()
n = sum(hhIncPcts['hhInc'])
hhIncPcts['hhInc'] = 100 * hhIncPcts['hhInc'] / sum(hhIncPcts['hhInc'])
hhIncPcts = hhIncPcts.reindex([1,2,5,7,8,9,10,11,12,13,14,15,0,3,4,6])
hhIncPcts['bracket'] = '$' + hhIncPcts['bracket'].str[:-1] + 'k'
hhIncPcts.at[1,'bracket'] = "< " + hhIncPcts['bracket'][1]
hhIncPcts.at[6,'bracket'] = hhIncPcts['bracket'][6] + "+"

# ----------------------------------------------------------------------------
# Building dash
year = np.arange(1945, 2021, 1, dtype=int)
neighborhood = ["Neighborhood Average", "Individual"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(
    [
        # Sidebar
        dbc.Navbar([
            dbc.Button("☰", id='sidebar_button', className="background2 left_text title", 
                       style={"margin-left": "0"}),
            dbc.Collapse(
                [
                    dbc.NavItem(dbc.NavLink(sidebar_top, href="#", external_link=True, 
                                            className="background2 left_text subtitle")),
                    #dbc.NavItem(dbc.NavLink(sidebar_afford, href="#afford_title", 
                    #                        external_link=True, className="background2 left_text subtitle")),
                    dbc.NavItem(dbc.NavLink(sidebar_census, href="#census_title", external_link=True, 
                                            className="background2 left_text subtitle")),
                ], id="sidebar", is_open=False, 
                style={"width": "400px", "margin-left": "0", "position": "fixed", "top": "80px"}, className="background"),
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src = 'assets/title.png', style={'height':'50px'}), className="ml-5"),
                    ],
                    align="center",
                    className="g-0"
                )
            ),
        ], className="sidebar", color="#132C36", sticky="top"),
        # Header
        #html.Div([
        #    html.Div(
        #    [
        #        html.Span(title, className="left_text title"),
        #        html.Span(subtitle, className="left_text subtitle"),
        #        html.Span(header_text, className="left_text bodytext"),
        #    ], className="subcontainer"),
        #    html.Img(src="assets/title.png", style={'height':'60%', 'weight':'60%'}, className="subcontainer")
        #], className="grid_container background", style={'textAlign': 'center'}),
        # Affordability
        html.Div(
            [
                # Neighborhood dropdown for industry chart
                html.Div([
                    createDropdown(dropdown_neighborhood, dropdown_neighborhood_lod_opts,
                                   dropdown_neighborhood_default, dd_id="dropdown_neighborhood",
                                   dd_style={"width": "200px"}, grid_width="1fr", clearable=False),
                ], className="neighborhood_drop"),
                #html.Span(afford_title, className="center_text title", id="afford_title"),
                html.Div([
                    dcc.Graph(id="afford_map", style={"width": "100%"}),
                    html.Div([
                        #html.Span(afford_dropdown_title, className="left_text subtitle"),
                        # Industry
                        #createDropdown(afford_dropdown_industry_desc, afford_dropdown_industry_opts,
                        #               afford_dropdown_industry_default, dd_id="afford_dropdown_industry",
                        #               dd_style={"width": "200px"}),
                        # Personal information
                        html.Hr(className="center_text title"),
                        html.Span(afford_dropdown_person_info_title, className="left_text subtitle"),
                        createInput(afford_input_salary_desc, "number", afford_input_salary_default, 
                                    ip_id="afford_input_salary"),
                        createDropdown(afford_dropdown_homeSize_desc, afford_dropdown_homeSize_opts,
                                       afford_dropdown_homeSize_default, dd_id="afford_dropdown_homeSize",
                                       clearable=False),
                        createNumericInput(afford_input_adults_desc, afford_input_adults_default,
                                           minimum=1, maximum=10, ip_id="afford_input_adults"),
                        createNumericInput(afford_input_kids_desc, afford_input_kids_default, 
                                           maximum=10, ip_id="afford_input_kids"),
                        createNumericInput(afford_input_childcare_desc, afford_input_kids_default, 
                                           maximum=10, ip_id="afford_input_childcare",
                                           desc_id = "afford_input_cc_desc_id"),
                        createNumericInput(afford_input_age_desc, afford_input_age_default,
                                           maximum=130, ip_id="afford_input_age"),
                        createDropdown(afford_dropdown_transport_desc, afford_dropdown_transport_opts,
                                       afford_dropdown_transport_default, dd_id="afford_dropdown_transport",
                                       clearable=False),
                        createDropdown(afford_dropdown_vehicle_desc, afford_dropdown_vehicle_opts,
                                       afford_dropdown_vehicle_default, dd_id="afford_dropdown_vehicle",
                                       desc_id="afford_dropdown_vehicle_desc_id", clearable=False),
                        createInput(afford_input_hcare_desc, "number", afford_input_hcare_default,
                                    ip_id="afford_input_hcare"),
                        createNumericInput(afford_input_tech_desc, afford_input_tech_default,
                                           maximum=1000, ip_id="afford_input_tech"),
                        dbc.Tooltip(afford_input_tech_tip, target="afford_input_tech", 
                                    placement='bottom'),
                        createDropdown(afford_dropdown_tax_desc, afford_dropdown_tax_opts,
                                       afford_dropdown_tax_default, dd_id="afford_dropdown_tax",
                                       clearable=False),
                    ], className="subcontainer")
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 2fr) 1fr"}),
                html.Div([
                    html.Div([
                        dcc.Slider(min=1945, max=2021, step=1, value=2020, 
                                   tooltip={"placement": "bottom", "always_visible": True},
                                   id="afford_slider_year")
                    ], style={"width": "100%"}),
                    createDropdown(afford_dropdown_lod_desc, afford_dropdown_lod_opts,
                                   afford_dropdown_lod_default, dd_id="afford_dropdown_lod", 
                                   dd_style={"width": "200px"}, clearable=False, searchable = False),
                    html.Button(afford_button, id="afford_button", className="right_text subtitle",
                                style={"background-color": "#FFA858", "color": "#000000"}),
                ], className="grid_container", style={"grid-template-columns": "minmax(600px, 4fr) 2fr 1fr"}),
                html.Div(afford_prediction_text, id="afford_result", className="center_text subtitle"),
                # Algorithm description
                #html.Div(afford_prediction_algo, id="afford_neighborhood", className="left_text bodytext")
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Sector/Industry and Neighborhood/Industry charts
        html.Div(
            [
                #html.Span(sector_title, id="sector_title", className="center_text title"),
                dcc.Graph(id='neighborhood_plot', style={'display': 'inline-block'}),
                dcc.Graph(id='sector_plot', figure=plotIndustrySector(), style={'display': 'inline-block'}),
            ], className="subcontainer"),
        html.Hr(className="center_text title"),
        # Neighborhood characteristics
        # History of price
        html.Div([
            html.Span(history_title, id="history_title", className="center_text title"),
            html.Span(history_description, className="left_text bodytext"),
            # By zoning
            html.Span(history_zoning_title, className="center_text subtitle"),
            dcc.Graph(id='history_zoning_num_plot', style={"width": "100%"},     
                      config={'displayModeBar': False}, figure=history_zoning_num()),
            dcc.Graph(id='history_zoning_price_plot', style={"width": "100%"},
                      config={'displayModeBar': False}, figure=history_zoning_price()),
            # By neighborhood
            html.Span(history_neighborhood_title, className="center_text subtitle"),
            dcc.Graph(id='history_neighborhood_num_plot', style={"width": "100%"},     
                      config={'displayModeBar': False}),
            dcc.Graph(id='history_neighborhood_price_plot', style={"width": "100%"},
                      config={'displayModeBar': False}),
        ], className="subcontainer"),
        # Census
        html.Div([
            html.Span(census_title, id="census_title", className="center_text title"),
            dcc.Graph(id='bar_plot', figure=plothhInc())
        ], className="subcontainer"),
        # Disclaimers
        html.Div([dcc.Markdown(children=source)], className="subcontainer left_text bodytext"),
    ], className="container background")

# Collapsable sidebar
@app.callback(Output("sidebar", "is_open"),
              [Input("sidebar_button", "n_clicks"), State("sidebar", "is_open")])
def sidebar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
   Output(component_id='afford_input_childcare', component_property='style'),
   Output(component_id='afford_input_cc_desc_id', component_property='style'),
   Output(component_id='afford_input_childcare', component_property='max'),
   [Input(component_id='afford_input_kids', component_property='value')])
def show_hide_childCare(kidCount):

    if kidCount is None:
        return ({'display': 'none'}, 
                {'display': 'none'},
                0)
    elif kidCount > 0:
        return ({'display': 'block', "width": "150px"}, 
                {'display': 'block', "width": "150px"},
                kidCount)
    else:
        return ({'display': 'none'}, 
                {'display': 'none'},
                0)

@app.callback(
   Output(component_id='afford_dropdown_vehicle', component_property='style'),
   Output(component_id='afford_dropdown_vehicle_desc_id', component_property='style'),
   [Input(component_id='afford_dropdown_transport', component_property='value')])
def show_hide_vehicle(currentTransport):

    optsTransport = afford_dropdown_transport_opts
    if currentTransport == optsTransport[0]:
        return ({'display': 'none'}, 
                {'display': 'none'})
    else:
        return ({'display': 'block', "width": "150px"}, 
                {'display': 'block', "width": "150px"})

@app.callback(
    Output('dropdown_neighborhood', 'value'),
    Input('afford_map', 'clickData'))
def printNeighborhood(clickData):
    if clickData is None:
        return dropdown_neighborhood_lod_opts[0]
    return(str(clickData['points'][len(clickData['points']) - 1]['hovertext']))

@app.callback(
   Output(component_id='afford_input_hcare', component_property='placeholder'),
   [Input("afford_input_salary", "value"),
    Input("afford_input_adults", "value"),
    Input("afford_input_kids", "value"),
    Input("afford_input_age", "value")])
def update_hcare_placeholder(incomeStr, adultCount, kidCount, ageStr):

    if incomeStr is None:
        return ''
    age = int(ageStr)
    income = int(incomeStr)
    totalOccupants = int(adultCount) + int(kidCount)
    # switch for premium
    if totalOccupants == 1:
        premium = premiumHealthcareData.iloc[0, 1]
    elif totalOccupants == 2:
        premium = premiumHealthcareData.iloc[1, 1]
    else:
        premium = premiumHealthcareData.iloc[2, 1]
    # switch for out-of-pocket
    if income < 15000:
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 3]
    elif income >= 15000 and income < 30000:
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 4]
    elif income >= 30000 and income < 40000:
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 5]
    elif income >= 40000 and income < 50000:
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 6]
    elif income >= 50000 and income < 70000:
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 7]
    elif income >= 70000 and (income < 100000 or age < 25):
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 8]
    else:
        oopCost = oopHealthcareData.iloc[getAgeIdx(age), 9]

    total = int(premium + oopCost)
    return '{} is average'.format(total)

# Function for creating plot of industry employment populations by neighborhood
@app.callback(
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

# Update expense defaults and affordability message
@app.callback(Output('afford_result', 'children'),
              [Input("afford_button", "n_clicks"), 
               State('afford_input_salary', 'value'),
               State('afford_dropdown_homeSize', 'value'),
               State('afford_input_adults', 'value'),
               State('afford_input_kids', 'value'),
               State('afford_input_childcare', 'value'),
               State('afford_input_age', 'value'),
               State('afford_dropdown_transport', 'value'),
               State('afford_dropdown_vehicle', 'value'),
               State('afford_input_hcare', 'value'),
               State('afford_input_hcare', 'placeholder'),
               State('afford_input_tech', 'value'),
               State('afford_dropdown_tax' ,'value'),
               State('dropdown_neighborhood', 'value')])
def update_expenses(n, income, homeSize, adultCount, kidCount, ccCount, ageStr,
                    transportType, vehicleType, hcareStr, hcarePlace, techStr, 
                    taxStatus, hood):

    # Starting message
    if income is None:
        return 'Enter your information to see whether Charlottesville \
             is affordable for you!'
    # get switch options from global vars
    optsSize = afford_dropdown_homeSize_opts
    optsTransport = afford_dropdown_transport_opts
    optsVehicle = afford_dropdown_vehicle_opts
    # convert age to int
    age = int(ageStr)
    # determine seniority
    senior = (age >= 65)
    # convert hcare to int or use avg
    if hcareStr is None:
        myHealthcare = int(hcarePlace.split()[0])
    else:
        myHealthcare = int(hcareStr)
    # convert tech to int
    myTech = int(techStr)
    monthlyExpenses = 0.0
    # switch for rental size dropdown
    if homeSize == optsSize[0]:
        myHousing = studio.loc[(studio['Neighborhood'] == hood)]['Median_Gross_Rent'].values[0]
    elif homeSize == optsSize[1]:
        myHousing = oneBR.loc[(oneBR['Neighborhood'] == hood)]['Median_Gross_Rent'].values[0]
    elif homeSize == optsSize[2]:
        myHousing = twoBR.loc[(twoBR['Neighborhood'] == hood)]['Median_Gross_Rent'].values[0]
    # switch for food age group
    if age < 2:
        myFood = foodData.iloc[0, 3]
    elif age >= 2 and age <= 3:
        myFood = foodData.iloc[1, 3]
    elif age >= 4 and age <= 5:
        myFood = foodData.iloc[2, 3]
    elif age >= 6 and age <= 8:
        myFood = foodData.iloc[3, 3]
    elif age >= 9 and age <= 11:
        myFood = foodData.iloc[4, 3]
    elif age >= 12 and age <= 13:
        myFood = foodData.iloc[5, 3]
    elif age >= 14 and age <= 19:
        myFood = foodData.iloc[6, 3]
    elif age >= 20 and age <= 50:
        myFood = foodData.iloc[7, 3]
    elif age >= 51 and age <= 70:
        myFood = foodData.iloc[8, 3]
    else:
        myFood = foodData.iloc[9, 3]
    # Add housing cost
    monthlyExpenses = monthlyExpenses + myHousing
    # Add childcare cost (currently using Toddler Family Child Care for all kids in cc)
    monthlyExpenses = monthlyExpenses + int(ccCount) * 584.0
    # Add food cost (currently replicating adults age and using age 9-11 for all kids)
    myFood = myFood + (int(adultCount) - 1) * myFood
    myFood = myFood + int(kidCount) * foodData.iloc[4, 3]
    monthlyExpenses = monthlyExpenses + myFood
    # Add transport cost (currently assuming 15k mileage for every vehicle type)
    if transportType == optsTransport[0]:
        if senior:
            myTransport = 10.0 # cost of CAT monthly for seniors
        else:
            myTransport = 20.0 # cost of CAT monthly for non-seniors
    else:
        if vehicleType == optsVehicle[0]:
            myTransport = transportData.iloc[1, 3] # small sedan
        elif vehicleType == optsVehicle[1]:
            myTransport = transportData.iloc[4, 3] # medium sedan
        elif vehicleType == optsVehicle[2]:
            myTransport = transportData.iloc[7, 3] # compact suv
        elif vehicleType == optsVehicle[3]:
            myTransport = transportData.iloc[10, 3] # medium suv
        elif vehicleType == optsVehicle[4]:
            myTransport = transportData.iloc[13, 3] # pickup
        elif vehicleType == optsVehicle[5]:
            myTransport = transportData.iloc[16, 3] # hybrid
        elif vehicleType == optsVehicle[6]:
            myTransport = transportData.iloc[19, 3] # EV
    monthlyExpenses = monthlyExpenses + myTransport
    # Add healthcare cost
    monthlyExpenses = monthlyExpenses + (myHealthcare / 12.0)
    # Add technology cost
    monthlyExpenses = monthlyExpenses + myTech
    # Add tax cost
    monthlyExpenses = monthlyExpenses + getTax(taxStatus, int(income), int(adultCount), int(kidCount))
    # Add misc cost
    monthlyExpenses = monthlyExpenses * 1.1
    # Calculate pct of hhIncome spent on housing
    housingPct = ((12 * myHousing) / income) * 100
    # Determine affordability by comparing expenses to income
    canAfford = (12 * monthlyExpenses - income)
    # gather result message
    if canAfford < 0:
        affordMessage = 'Affordable: About {:.2f}% of your household\'s \
            income would be spent on gross rent. Your approximate living \
            expenses are ${:,} annually.'.format(housingPct, int(monthlyExpenses * 12))
    else:
        affordMessage = 'Not affordable: About {:.2f}% of your household\'s \
            income would be spent on gross rent. Your approximate living \
            expenses are ${:,} annually.'.format(housingPct, int(monthlyExpenses * 12))
    return affordMessage


# Update affordability graph
@app.callback(Output("afford_map", "figure"),
              [Input("afford_button", "n_clicks"), State("afford_slider_year", "value"),
               State("afford_dropdown_lod", "value")])
def update_afford_map(n, y, lod):
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
                                   center={"lat": 38.0293, "lon": -78.4767}, 
                                   zoom=12, 
                                   )
        fig.update_traces(hovertemplate="<br>".join([
            "%{hovertext}",
            "",
            "Average Sale Price in Neighborhood: $%{customdata[0]}",
            "Number of Sales Recorded: %{customdata[1]}"]))
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
                                   center={"lat": 38.0293, "lon": -78.4767}, 
                                   zoom=14,
                                  )
        fig.update_traces(hovertemplate="<br>".join([
            "%{hovertext}",
            "",
            "Total Sale Price: $%{customdata[0]}",
            "Acreage: %{customdata[1]}",
            "Last sale on %{customdata[2]}",
            "Zoning: %{customdata[3]}"]))
    fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                      mapbox_style=mapbox_style,
                      margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


@app.callback(Output("history_neighborhood_num_plot", "figure"),
              [Input("dropdown_neighborhood", "value"),])
def history_neighborhood_num(neigh):
    fig = go.Figure()
    sales_year_neighborhood = sales_clean_simple[sales_clean_simple["Neighborhood"] == neigh]
    syn = sales_year_neighborhood.sort_values("SaleDate").set_index("SaleDate").rolling("730.5D").agg({"SaleAmountAdjusted": ["count", "median"]}).reset_index()
    fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"]["count"] * 0.5, name=neigh))
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Number of Sales",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig


@app.callback(Output("history_neighborhood_price_plot", "figure"),
              [Input("dropdown_neighborhood", "value"),])
def history_neighborhood_price(neigh):
    fig = go.Figure(data=go.Scatter(x=sales_year["SaleDate"], y=sales_year["SaleAmountAdjusted"]["median"], 
                                    name="All Sales"))
    sales_year_neighborhood = sales_clean_simple[sales_clean_simple["Neighborhood"] == neigh].sort_values("SaleDate").set_index("SaleDate")
    sales_year_neighborhood["SaleAmountAdjusted"] = hampel(sales_year_neighborhood["SaleAmountAdjusted"], 7, imputation=True)
    syn = sales_year_neighborhood.rolling("730.5D").agg({"SaleAmountAdjusted": ["count", "median"]}).reset_index()
    fig.add_trace(go.Scatter(x=syn["SaleDate"], y=syn["SaleAmountAdjusted"]["median"], name=neigh))
    fig.update_layout(xaxis_title="Year",
                      yaxis_title="Yearly Median Sale Price [$, inflation adjusted]",
                      margin=go.layout.Margin(l=0, r=0, b=0, t=0),
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)",
                      autosize=True,
                      font=dict(size=16, color="rgb(255,255,255)"))
    fig['data'][0]['showlegend'] = True
    return fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=True)
