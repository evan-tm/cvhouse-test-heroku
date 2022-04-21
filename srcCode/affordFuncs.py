# ------------------Affordability functions------------------#

# modules to import
import pandas as pd
from dash import Input, Output, State, dcc, html, callback
import srcCode.affordDescs as ad
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

# Rental affordability data
rentData = pd.read_csv('data/calculator/acsRent2020.csv')
# Mortgage affordability data
mortgageData = pd.read_csv('data/calculator/acsMortgage2020.csv')
# Childcare affordability data
ccareData = pd.read_csv('data/calculator/childcareCosts.csv')
# Food affordability data
foodData = pd.read_csv('data/calculator/foodCosts.csv')
# Transportation affordability data
transportData = pd.read_csv('data/calculator/transportCosts.csv')
# Health care out-of-pocket affordability data
oopHealthcareData = pd.read_csv('data/calculator/oopHealthcareAnnual.csv')
# Health care premium affordability data
premiumHealthcareData = pd.read_csv('data/calculator/premiumHealthcare.csv')
# Neighborhood data
ns = gpd.read_file('neighborhood_simple.geojson')
ns = ns.set_index('NAME')

mapbox_token_public = "pk.eyJ1IjoiZXZhbi10bSIsImEiOiJjbDFlYTlncTMwM2J3M2RwbDdjaXc2bW02In0.cxB8jf_1CFeoeVUAuOsYuA"
mapbox_style = "mapbox://styles/evan-tm/cl1ik4lmv003z15ru0ip4isbz"

## logic for getting correct index to pull from oopData
## in: age to find group for
## out: indexes for age_group rows
def getAgeIdx(age):
    if age < 25:
        return 3, 24
    elif age >= 25 and age < 35:
        return 7, 25
    elif age >= 35 and age < 45:
        return 11, 26
    elif age >= 45 and age < 55:
        return 15, 27
    elif age >= 55 and age < 65:
        return 19, 28
    else:
        return 23, 29

## Builds an integer list of household member ages from a str or str list
## in: str / str list
## out: int list of ages
def getAgeList(people):
    ages = []
    if isinstance(people, str):
        if people != '':
            ages.append(int(people))
    else:
        for ageStr in people:
            if ageStr != '':
                ages.append(int(ageStr))
    return ages

## Get the monthly childcare payment given the type and number of kids
## in: number of childcare kids, type of care
## out: monthly payment in $
def get_cc_payment(ccCount, ccType, optsCC):

    if ccType == optsCC[0]:
        return ccCount * 584.0
    else:
        return ccCount * 1268.0

## Approximates monthly tax payment for a given income
## in: status, income, adultCount, kidCount, tax options
## out: monthly tax
def get_tax(status, income, adultCount, kidCount, optsTax):
    
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

## Calculates average healthcare cost given income, occupants, and age
## as well as the data for premiums and out-of-pocket costs
## in: income, totalOccupants, age, premiums data, oop data
## out: placeholder string for healthcare input
def get_hcare_placeholder(income, totalOccupants, ageList, premData, oopData):
    # switch for premium
    if totalOccupants == 1:
        premium = premData.iloc[0, 1]
    # assuming employee-plus-one premium for two people
    elif totalOccupants == 2:
        premium = premData.iloc[1, 1]
    # assuming family premium for 3+ people
    else:
        premium = premData.iloc[2, 1]
    # get out-of-pocket costs for each person
    oopCost = 0.0
    for age in ageList:
        costIdx, peopleIdx = getAgeIdx(age)
        # switch for out-of-pocket
        if income < 15000:
            oopCost += oopData.iloc[costIdx, 3] / oopData.iloc[peopleIdx, 3]
        elif income >= 15000 and income < 30000:
            oopCost += oopData.iloc[costIdx, 4] / oopData.iloc[peopleIdx, 4]
        elif income >= 30000 and income < 40000:
            oopCost += oopData.iloc[costIdx, 5] / oopData.iloc[peopleIdx, 5]
        elif income >= 40000 and income < 50000:
            oopCost += oopData.iloc[costIdx, 6] / oopData.iloc[peopleIdx, 6]
        elif income >= 50000 and income < 70000:
            oopCost += oopData.iloc[costIdx, 7] / oopData.iloc[peopleIdx, 7]
        elif income >= 70000 and (income < 100000 or age < 25):
            oopCost += oopData.iloc[costIdx, 8] / oopData.iloc[peopleIdx, 8]
        else:
            oopCost += oopData.iloc[costIdx, 9] / oopData.iloc[peopleIdx, 9]

    total = int(premium + oopCost)
    return '{} is average'.format(total)

## Gets the housing payment based on the current neighborhood
## in: paymentType (renting/buying), homeSize (for rental size),
##     rentData, mortgageData, current neighborhood,
##     payment options, and size options
## out: monthly housing payment
def get_housing_payment(paymentType, homeSize, 
                        dfRent, dfMortgage, 
                        hood, optsPayment, optsSize):

    # switch for payment type dropdown
    if paymentType == optsPayment[0]:
        # switch for rental size dropdown
        if homeSize == optsSize[0]:
            return dfRent.loc[(dfRent['Neighborhood'] == hood)]['studio'].values[0]
        elif homeSize == optsSize[1]:
            return dfRent.loc[(dfRent['Neighborhood'] == hood)]['oneBR'].values[0]
        elif homeSize == optsSize[2]:
            return dfRent.loc[(dfRent['Neighborhood'] == hood)]['twoBR'].values[0]
        elif homeSize == optsSize[3]:
            return dfRent.loc[(dfRent['Neighborhood'] == hood)]['threeBR'].values[0]
        elif homeSize == optsSize[4]:
            return dfRent.loc[(dfRent['Neighborhood'] == hood)]['fourBR'].values[0]
    else:
        return dfMortgage.loc[(dfMortgage['Neighborhood'] == hood)].values[0][1]

## Gets the food payment for the household
## in: age of user, foodData
## out: monthly food payment for household
def get_food_payment(ages, foodData):
    myFood = 0.0
    for age in ages:
        # switch for food age group
        if age < 2:
            myFood += foodData.iloc[0, 3]
        elif age >= 2 and age <= 3:
            myFood += foodData.iloc[1, 3]
        elif age >= 4 and age <= 5:
            myFood += foodData.iloc[2, 3]
        elif age >= 6 and age <= 8:
            myFood += foodData.iloc[3, 3]
        elif age >= 9 and age <= 11:
            myFood += foodData.iloc[4, 3]
        elif age >= 12 and age <= 13:
            myFood += foodData.iloc[5, 3]
        elif age >= 14 and age <= 19:
            myFood += foodData.iloc[6, 3]
        elif age >= 20 and age <= 50:
            myFood += foodData.iloc[7, 3]
        elif age >= 51 and age <= 70:
            myFood += foodData.iloc[8, 3]
        else:
            myFood += foodData.iloc[9, 3]

    return myFood

## Gets the transportation payment for the household
## in: type of transportation, vehicle type if applicable, senior status,
##     transportation data, transportation options, vehicle options
## out: monthly transportation payment
def get_transport_payment(transportType, vehicleType, senior, 
                          transportData, optsTransport, optsVehicle):

    myTransport = 0.0
    # Add transport cost (currently assuming 15k mileage for every vehicle type)
    if transportType == optsTransport[0]:
        for isSenior in senior:
            if isSenior:
                myTransport += 10.0 # cost of CAT monthly for seniors
            else:
                myTransport += 20.0 # cost of CAT monthly for non-seniors
    else:
        if vehicleType == optsVehicle[0]:
            myTransport += transportData.iloc[1, 3] # small sedan
        elif vehicleType == optsVehicle[1]:
            myTransport += transportData.iloc[4, 3] # medium sedan
        elif vehicleType == optsVehicle[2]:
            myTransport += transportData.iloc[7, 3] # compact suv
        elif vehicleType == optsVehicle[3]:
            myTransport += transportData.iloc[10, 3] # medium suv
        elif vehicleType == optsVehicle[4]:
            myTransport += transportData.iloc[13, 3] # pickup
        elif vehicleType == optsVehicle[5]:
            myTransport += transportData.iloc[16, 3] # hybrid
        elif vehicleType == optsVehicle[6]:
            myTransport += transportData.iloc[19, 3] # EV
    
    return myTransport

## Returns a plot of the affordability map based on afford calculator results
## in: data from afford calculator output
## out: figure representing the data
def plotAffordMap(ns):
    # school zones chloropleth
    fig = px.choropleth_mapbox(ns, geojson = ns.geometry, 
                            locations = ns.index,
                            #hover_name = ns.index,
                            color = ns.afford,
                            center={"lat": 38.039, "lon": -78.47826},
                            zoom=12, opacity = 0.5,
                            color_discrete_map={'Affordable':'green',
                                            'Unaffordable':'orange'},
                            labels={'afford': 'Results:'})
    fig.update_layout(mapbox_accesstoken=mapbox_token_public, 
                    mapbox_style=mapbox_style,
                    margin=go.layout.Margin(l=0, r=0,  b=0, t=0),
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    autosize=True,
                    font={'size': 16, 'color': "rgb(255,255,255)"})
    fig.update_traces(hovertemplate=None, hoverinfo = 'skip')

    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig

# updates the style and options in the household dropdown when the
# "add a person" button (id=age_button) is pressed
@callback(
    Output('afford_dropdown_people', 'options'),
    Output('afford_dropdown_people', 'value'),
    Output('afford_dropdown_people', 'style'),
    Output('afford_dropdown_people_desc_id', 'style'),
    [Input('age_button', 'n_clicks')],
    [State('afford_input_age', 'value'),
     State('afford_dropdown_people', 'options'),
     State('afford_dropdown_people', 'value')],
)
def update_dropdown_people(n_clicks, new_value, current_options, current_values):
    
    if not n_clicks:
        return (current_options, current_values, 
            {'display': 'none'}, {'display': 'none'})
    # editing dropdown menu options based on input
    current_options.append({'label': new_value, 'value': new_value})
    return_values = []
    if isinstance(current_values, str):
        return_values.append(current_values)
    else:
        return_values = current_values
    return_values.append(new_value)
    ## setting height of dropdown based on number of people
    ages = getAgeList(current_values)
    # checking size of household
    if len(ages) < 3:
        return (current_options, return_values,
                ad.dd_style, ad.text_style)
    elif len(ages) < 5:
        return (current_options, return_values,
                ad.dd_style_2, ad.text_style)
    elif len(ages) < 7:
        return (current_options, return_values,
                ad.dd_style_3, ad.text_style)
    else:
        return (current_options, return_values,
                ad.dd_style_4, ad.text_style)

@callback(
   Output(component_id='afford_input_childcare', component_property='style'),
   Output(component_id='afford_input_cc_desc_id', component_property='style'),
   Output(component_id='afford_input_childcare', component_property='max'),
   Output(component_id='afford_dropdown_childcare', component_property='style'),
   Output(component_id='afford_dropdown_cc_desc_id', component_property='style'),
   [Input(component_id='afford_dropdown_people', component_property='value'),
    Input(component_id='afford_input_childcare', component_property='value')])
def show_hide_childCare(people, cc_kids):

    # convert age list of str to list of ints
    ages = getAgeList(people)
    kidCount = sum([age < 13 for age in ages])
    if kidCount is None:
        return ({'display': 'none'}, 
                {'display': 'none'},
                0,
                {'display': 'none'},
                {'display': 'none'})
    elif kidCount > 0:
        if cc_kids is None:
            return ({'display': 'block', "width": "150px"}, 
                    {'display': 'block', "width": "150px"},
                    kidCount,
                    {'display': 'none'},
                    {'display': 'none'})
        elif cc_kids > 0:
            return ({'display': 'block', "width": "150px"}, 
                    {'display': 'block', "width": "150px"},
                    kidCount,
                    {'display': 'block', "width": "150px"}, 
                    {'display': 'block', "width": "200px"})
        else:
            return ({'display': 'block', "width": "150px"}, 
                    {'display': 'block', "width": "150px"},
                    kidCount,
                    {'display': 'none'},
                    {'display': 'none'})
    else:
        return ({'display': 'none'}, 
                {'display': 'none'},
                0,
                {'display': 'none'},
                {'display': 'none'})

@callback(
   Output(component_id='afford_dropdown_vehicle', component_property='style'),
   Output(component_id='afford_dropdown_vehicle_desc_id', component_property='style'),
   [Input(component_id='afford_dropdown_transport', component_property='value')])
def show_hide_vehicle(currentTransport):

    optsTransport = ad.opts['DD_TRANSPORT']
    if currentTransport == optsTransport[0]:
        return ({'display': 'none'}, 
                {'display': 'none'})
    else:
        return ({'display': 'block', "width": "150px"}, 
                {'display': 'block', "width": "200px"})

@callback(
   Output(component_id='afford_dropdown_homeSize', component_property='style'),
   Output(component_id='afford_dropdown_homeSize_desc_id', component_property='style'),
   [Input(component_id='afford_dropdown_pay', component_property='value')])
def show_hide_homeSize(currentPay):

    optsPayment = ad.opts['DD_PAY']
    if currentPay == optsPayment[1]:
        return ({'display': 'none'}, 
                {'display': 'none'})
    else:
        return ({'display': 'block', "width": "150px"}, 
                {'display': 'block', "width": "150px"})

@callback(
   Output(component_id='afford_input_hcare', component_property='placeholder'),
   [Input("afford_input_salary", "value"),
    Input("afford_dropdown_people", "value")])
def update_hcare_placeholder(incomeStr, people):

    if incomeStr is None or people is None:
        return ''
    # convert age list of str to list of ints
    ages = getAgeList(people)
    totalOccupants = len(ages)
    return get_hcare_placeholder(int(incomeStr), totalOccupants, 
                                 ages, premiumHealthcareData,
                                 oopHealthcareData)

# Update expense defaults and affordability message
@callback(Output('qol_dropdown', 'value'),
          Output('qol_dropdown', 'options'),
          Output('afford_result', 'children'),
          Output('results_map', 'figure'),
          [Input("afford_button", "n_clicks"), 
          State('afford_input_salary', 'value'), 
          State('afford_dropdown_people', 'value'),
          State('afford_dropdown_pay', 'value'), 
          State('afford_dropdown_homeSize', 'value'), 
          State('afford_input_childcare', 'value'),
          State('afford_dropdown_childcare', 'value'),
          State('afford_dropdown_transport', 'value'),
          State('afford_dropdown_vehicle', 'value'),
          State('afford_input_hcare', 'value'),
          State('afford_input_hcare', 'placeholder'),
          State('afford_input_tech', 'value'),
          State('afford_dropdown_tax' ,'value'),
          State('qol_dropdown', 'options'),
          State('qol_dropdown', 'value')])
def update_expenses(n, income, people, paymentType, homeSize, ccCount, ccType,
                    transportType, vehicleType, hcareStr, hcarePlace, 
                    techStr, taxStatus, qolOpts, currentQOL):

    global ns
    # Starting message
    if income is None or people is None:
        return currentQOL, qolOpts, 'Enter your information to see whether \
            Charlottesville is affordable for you!', go.Figure()
    # get switch options from global vars
    optsSize = ad.opts['DD_HOMESIZE']
    optsCC = ad.opts['DD_CC']
    optsTransport = ad.opts['DD_TRANSPORT']
    optsVehicle = ad.opts['DD_VEHICLE']
    optsPayment = ad.opts['DD_PAY']
    # convert age list of str to list of ints
    ages = getAgeList(people)
    if len(ages) == 0:
        return currentQOL, qolOpts, 'Please add members to your household \
            using the Add Person button!', go.Figure()
    adultCount = sum([age >= 18 for age in ages])
    kidCount = len(ages) - adultCount
    # determine seniority
    senior = [age >= 65 for age in ages]
    # convert hcare to int or use avg
    if hcareStr is None:
        myHealthcare = int(hcarePlace.split()[0])
    else:
        myHealthcare = int(hcareStr)
    # initialize monthly expenses variable with the housing payment
    housingPayments = []
    for hood in ad.opts['DD_HOOD']:
        housingPayments.append(get_housing_payment(paymentType, homeSize, 
                                                    rentData, mortgageData, 
                                                    hood, optsPayment, optsSize))
    monthlyExpenses = [x for x in housingPayments]
    # Add childcare cost (currently using Toddler Family Child Care for all kids in cc)
    if ccCount is not None:
        monthlyExpenses = [x+get_cc_payment(int(ccCount), ccType, optsCC)
                            for x in monthlyExpenses]
    # Add food cost
    monthlyExpenses = [x+get_food_payment(ages, foodData) for x in monthlyExpenses]
    # Add transport cost (currently assuming 15k mileage for every vehicle type)
    monthlyExpenses = [x+get_transport_payment(transportType, vehicleType, 
                        senior, transportData, optsTransport, optsVehicle) 
                        for x in monthlyExpenses]
    # Add healthcare cost
    monthlyExpenses = [x+(myHealthcare / 12.0) for x in monthlyExpenses]
    # Add technology cost
    monthlyExpenses = [x+int(techStr) for x in monthlyExpenses]
    # Add tax cost NEED TO FIX WITH NEW ADULT TAGS
    monthlyExpenses = [x+get_tax(taxStatus, int(income), 
                        int(adultCount), int(kidCount), 
                        ad.opts['DD_TAX']) for x in monthlyExpenses]
    # check whether to add real estate tax for cville
    if paymentType == optsPayment[1]:
        monthlyExpenses = [x+((0.0095 * 399628.7) / 12.0) for x in monthlyExpenses]
    # Add misc cost
    monthlyExpenses = [x*1.1 for x in monthlyExpenses]
    # Calculate pct of hhIncome spent on housing
    avgHousing = sum(housingPayments) / len(housingPayments)
    housingAvgPct = ((12 * avgHousing) / int(income)) * 100
    # Getting average monthly expenses
    avgExpenses = sum(monthlyExpenses) / len(monthlyExpenses)
    # Determine affordability by comparing expenses to income
    expensesDict = dict(zip(ad.opts['DD_HOOD'], monthlyExpenses))
    afford = []
    for x in ns.index:
        if ((expensesDict[x] * 12 - int(income)) >= 0):
            afford.append('Unaffordable')
        else:
            afford.append('Affordable')
    ns['afford'] = afford
    # add affordability map to options if not there
    if not any(d['label'] == 'Affordability' for d in qolOpts):
        qolOpts.append({'label': 'Affordability', 'value': 'Affordability'})
    # gather result message
    afford_count = ns['afford'].str.contains('Affordable').sum()
    if afford_count > 0:
        affordMessage = '{}/19 of Charlottesville\'s neighborhoods are \
            estimated to be affordable for you as shown on the map above. \
            About {:.2f}% of your household\'s income would be spent on \
            housing. Your approximate living expenses are ${:,} \
            annually. Your affordable neighborhoods can be seen on the map \
            above.'.format(afford_count, housingAvgPct, int(avgExpenses * 12))
    else:
        affordMessage = 'About {:.2f}% of your household\'s income would be \
            spent on housing. Your approximate living expenses are ${:,} \
            annually, which exceeds the estimated cost of living in \
            Charlottesville.'.format(housingAvgPct, int(avgExpenses * 12))
    return 'Affordability', qolOpts, affordMessage, plotAffordMap(ns)