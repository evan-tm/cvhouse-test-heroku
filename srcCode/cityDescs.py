# ------------------City page texts------------------#

text = {
    "MAIN_TITLE": "City page:",
    "LOADING": "Loading...",
    "VIEW_BUTTON": "Change view",
    "DROPDOWN_CENSUS": "Describe Charlottesville Population by",
    "DROPDOWN_CENSUS_HH": "Describe Charlottesville Households by",
    "DROPDOWN_HISTORY": "",
    "FOOTNOTE": '''Prices have been adjusted for inflation to 2022 dollars. \
        Only sales with state code Residential (urban/suburban) and \
        Multifamily are included.'''
}

opts = {
    "DROPDOWN_CENSUS": ['Age', 'Industry', 'Race and Ethnicity', 'Size'],
    "DROPDOWN_CENSUS_HH": ['Median Income', 'Income Distribution', 'Occupancy', 'Tenure'],
    "DROPDOWN_HISTORY": ['Median Price', 'Sales Quantity']
}

default = {
    "DROPDOWN_CENSUS": opts['DROPDOWN_CENSUS'][1],
    "DROPDOWN_CENSUS_HH": opts['DROPDOWN_CENSUS_HH'][0],
    "DROPDOWN_HISTORY": opts['DROPDOWN_HISTORY'][0]
}

ttips = {
    
}