# ------------------Affordability functions------------------#

# modules to import
import pandas as pd
from dash import Input, Output, State, dcc, html, callback
import srcCode.affordDescs as ad

# Rental affordability data
rentData = pd.read_csv('data/acsRent2019.csv')
# Childcare affordability data
ccareData = pd.read_csv('data/childcareCosts.csv')
# Food affordability data
foodData = pd.read_csv('data/foodCosts.csv')
# Transportation affordability data
transportData = pd.read_csv('data/transportCosts.csv')
# Mortgage affordability data
mortgageData = [1612.0, (0.0095 * 399628.7) / 12.0]
# Health care out-of-pocket affordability data
oopHealthcareData = pd.read_csv('data/oopHealthcareAnnual.csv')
# Health care premium affordability data
premiumHealthcareData = pd.read_csv('data/premiumHealthcare.csv')

## logic for getting correct index to pull from oopData
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
## in: income, totalOccupants, age
## out: placeholder string for healthcare input
def get_hcare_placeholder(income, totalOccupants, age, premData, oopData):
    # switch for premium
    if totalOccupants == 1:
        premium = premData.iloc[0, 1]
    elif totalOccupants == 2:
        premium = premData.iloc[1, 1]
    else:
        premium = premData.iloc[2, 1]
    # switch for out-of-pocket
    if income < 15000:
        oopCost = oopData.iloc[getAgeIdx(age), 3]
    elif income >= 15000 and income < 30000:
        oopCost = oopData.iloc[getAgeIdx(age), 4]
    elif income >= 30000 and income < 40000:
        oopCost = oopData.iloc[getAgeIdx(age), 5]
    elif income >= 40000 and income < 50000:
        oopCost = oopData.iloc[getAgeIdx(age), 6]
    elif income >= 50000 and income < 70000:
        oopCost = oopData.iloc[getAgeIdx(age), 7]
    elif income >= 70000 and (income < 100000 or age < 25):
        oopCost = oopData.iloc[getAgeIdx(age), 8]
    else:
        oopCost = oopData.iloc[getAgeIdx(age), 9]

    total = int(premium + oopCost)
    return '{} is average'.format(total)

## Gets the housing payment based on the current neighborhood
## in: paymentType (renting/buying), homeSize (for rental size),
##     rentData, mortgageData, current neighborhood,
##     payment options, and size options
## out: monthly housing payment
def get_housing_payment(paymentType, homeSize, 
                        dfRent, mortgageData, 
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
    else:
        return mortgageData[0]

## Gets the food payment for the household
## in: age of user, adultCount, kidCount, foodData
## out: monthly food payment for household
def get_food_payment(age, adultCount, kidCount, foodData):
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

    # Add food cost (currently replicating adults age and using age 9-11 for all kids)
    myFood += (adultCount - 1) * myFood
    myFood += kidCount * foodData.iloc[4, 3]

    return myFood

## Gets the transportation payment for the household
## in: type of transportation, vehicle type if applicable, senior status,
##     transportation data, transportation options, vehicle options
## out: monthly transportation payment
def get_transport_payment(transportType, vehicleType, senior, 
                          transportData, optsTransport, optsVehicle):

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
    
    return myTransport

@callback(
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
                {'display': 'block', "width": "150px"})

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
    Input("afford_input_adults", "value"),
    Input("afford_input_kids", "value"),
    Input("afford_input_age", "value")])
def update_hcare_placeholder(incomeStr, adultCount, kidCount, ageStr):

    if incomeStr is None:
        return ''
    totalOccupants = int(adultCount) + int(kidCount)
    return get_hcare_placeholder(int(incomeStr), totalOccupants, 
                                 int(ageStr), premiumHealthcareData,
                                 oopHealthcareData)

# Update expense defaults and affordability message
@callback(Output('afford_result', 'children'),
          [Input("afford_button", "n_clicks"), 
          State('afford_input_salary', 'value'), 
          State('afford_dropdown_pay', 'value'), 
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
def update_expenses(n, income, paymentType, homeSize, adultCount, kidCount, ccCount, ageStr,
                    transportType, vehicleType, hcareStr, hcarePlace, techStr, 
                    taxStatus, hood):

    # Starting message
    if income is None:
        return 'Enter your information to see whether Charlottesville \
             is affordable for you!'
    # get switch options from global vars
    optsSize = ad.opts['DD_HOMESIZE']
    optsTransport = ad.opts['DD_TRANSPORT']
    optsVehicle = ad.opts['DD_VEHICLE']
    optsPayment = ad.opts['DD_PAY']
    # convert age to int
    age = int(ageStr)
    # determine seniority
    senior = (age >= 65)
    # convert hcare to int or use avg
    if hcareStr is None:
        myHealthcare = int(hcarePlace.split()[0])
    else:
        myHealthcare = int(hcareStr)
    # initialize monthly expenses variable with the housing payment
    monthlyExpenses = get_housing_payment(paymentType, homeSize, 
                                          rentData, mortgageData, 
                                          hood, optsPayment, optsSize)
    myHousing = monthlyExpenses
    # Add childcare cost (currently using Toddler Family Child Care for all kids in cc)
    monthlyExpenses += int(ccCount) * 584.0
    # Add food cost (currently replicating adults age and using age 9-11 for all kids)
    monthlyExpenses += get_food_payment(age, int(adultCount), 
                                        int(kidCount), foodData)
    # Add transport cost (currently assuming 15k mileage for every vehicle type)
    monthlyExpenses += get_transport_payment(transportType, vehicleType, 
                                             senior, transportData, 
                                             optsTransport, optsVehicle)
    # Add healthcare cost
    monthlyExpenses += (myHealthcare / 12.0)
    # Add technology cost
    monthlyExpenses += int(techStr)
    # Add tax cost
    monthlyExpenses += get_tax(taxStatus, int(income), 
                                  int(adultCount), int(kidCount), 
                                  ad.opts['DD_TAX'])
    # check whether to add real estate tax for cville
    if paymentType == optsPayment[1]:
        monthlyExpenses += mortgageData[1]
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