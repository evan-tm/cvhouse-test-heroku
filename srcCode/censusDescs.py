# ------------------Census texts------------------#

text = {
    "LOADING": "Loading...",
    "IND_CITY_TITLE": 'Industries of Charlottesville Residents by Year (% of Total Employed Age 16+ Civilians)',
    "IND_CITY_LEGEND_TITLE": 'Sector',
    "IND_X_TITLE": '<b>Employed Population (%)</b>',
    "IND_Y_TITLE": '<b>Industries</b>',
    "IND_CITY_HOVER": 'Industries: <b>%{customdata}</b>' + \
                 '<br>%{value:.2f}% of Total Employed' + \
                 '<extra></extra>',
    "IND_NEIGHBORHOOD_TITLE": 'Industries of {hood} Residents (% of Total Employed Age 16+ Civilians)',
    "IND_NEIGHBORHOOD_LEGEND_TITLE": "Neighborhood",
    "IND_NEIGHBORHOOD_HOVER": '%{value:.2f}% of Total Employed<br>' + \
                 'Industries: <b>%{customdata}</b>' + \
                 '<extra></extra>',
    "AGE_CITY_TITLE": 'Population Chart for Charlottesville, Virginia',
    "AGE_LEGEND_TITLE": 'Sex',
    "AGE_X_TITLE": '<b>Population (%)</b>',
    "AGE_Y_TITLE": '<b>Age Group</b>',
    "AGE_CITY_HOVER": 'Age Group: <b>%{data.name}</b>' + \
                 '<br>%{value:.2f}% of Total Population<br>' + \
                 '<b>%{customdata}</b> People' + \
                 '<extra></extra>',
    "AGE_NEIGHBORHOOD_TITLE": 'Population Chart for {hood} (% of Total)',
    "AGE_NEIGHBORHOOD_HOVER":  'Age Group: <b>%{data.name}</b>' + \
                            '<br>%{value:.2f}% of Neighborhood\'s Population<br>' + \
                            '<b>%{customdata}</b> People<br>' + \
                            '<extra></extra>',
    "RACE_CITY_TITLE": 'Population by Race and Ethnicity for Charlottesville, Virginia (% of Total)',
    "RACE_X_TITLE": '<b>Population (%)</b>',
    "RACE_Y_TITLE": '<b>Race and Ethnicity</b>',
    "RACE_NEIGHBORHOOD_TITLE": 'Population by Race and Ethnicity for {hood} (% of Total)',
    "SIZE_CITY_TITLE": "Population by Year for Central Virginia Cities",
    "SIZE_X_TITLE": '<b>Year</b>',
    "SIZE_Y_TITLE": '<b>Population</b>',
    "INCOME_CITY_TITLE": "Median Household Income by Year for " + \
                            "Central Virginia Cities ($)",
    "INCOME_DIST_CITY_TITLE": 'Households by Income for Charlottesville, Virginia (% of Total)',
    "INCOME_X_TITLE": '<b>Households (%)</b>',
    "INCOME_Y_TITLE": '<b>Income Bracket</b>',
    "INCOME_CITY_Y_TITLE": "<b>Median Household Income ($)</b>",
    "INCOME_NEIGHBORHOOD_TITLE": 'Households by Income Bracket for {hood} (% of Total)',
    "OCC_CITY_TITLE": 'Occupancy Status of Charlottesville Households (% of Total Households)',
    "OCC_CITY_HOVER": '<i>Status</i>: <b>%{data.name}</b>' + \
                 '<br>%{value:.2f}% of Total Households<br>' + \
                 '%{customdata} Households<br>' + \
                 '<extra></extra>',
    "OCC_NEIGHBORHOOD_TITLE": 'Occupancy Status of {hood} Households (% of Total Households)',
    "OCC_NEIGHBORHOOD_HOVER": '<i>Status</i>: <b>%{data.name}</b>' + \
                            '<br>%{value:.2f}% of Neighborhood\'s Households<br>' + \
                            '%{customdata} Households<br>' + \
                            '<extra></extra>',
    "OCC_ANNOTATE": '%{value:.2f}%<br>%{customdata} Households',
    "TENURE_CITY_TITLE": 'Tenure of Charlottesville Households (% of Total Households)',
    "TENURE_NEIGHBORHOOD_TITLE": 'Tenure of {hood} Households (% of Total Households)'
}

opts = {
    "CITY_LIST": ['Charlottesville', 'Staunton', 'Harrisonburg', 
                         'Blacksburg', 'Petersburg', 'Fredericksburg']
}

default = {

}

ttips = {
    
}