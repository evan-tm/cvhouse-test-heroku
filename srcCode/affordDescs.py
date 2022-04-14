
text = {
    "DD_MAIN_TITLE": "Affordability Calculator:", 
    "IN_INCOME": "Household income:",
    "IN_AGE": "How old is each resident?",
    "DD_PEOPLE": "Your household:",
    "DD_PAY": "Rent or buy?",
    "DD_HOMESIZE": "What rental size?",
    "IN_CC": "Kids in childcare:",
    "DD_TRANSPORT": "How do you get around?",
    "DD_VEHICLE": "What type of vehicle?",
    "IN_HCARE": "Healthcare (annual $):",
    "IN_TECH": "Technology (monthly $):",
    "DD_TAX": "Tax filing status:",
    "CALC_BUTTON": "Calculate",
    "DD_LOD": "Level of Detail:",
    "LOADING": "Loading...",
}

opts = {
    "DD_PEOPLE": [],
    "DD_PAY": ['Renting', 'Buying'],
    "DD_HOMESIZE": ['Studio', '1 Bedroom', '2 Bedrooms', '3 Bedrooms', '4 Bedrooms'],
    "DD_TRANSPORT": ['CAT Public Bus', 'Personal Vehicle'],
    "DD_VEHICLE": ['Small Sedan', 'Medium Sedan', 
                    'Compact SUV', 'Medium SUV', 
                    'Pickup', 'Hybrid', 'Electric'],
    "DD_TAX": ['Single', 'Married', 'Head of House'],
    "DD_LOD": ["Neighborhood", "Individual Properties"],
    "DD_HOOD": ['10th & Page', 'Barracks / Rugby', 'Barracks Road',
                              'Belmont','Fifeville',"Fry's Spring", 'Greenbrier',
                              'Jefferson Park Avenue', 'Johnson Village', 'Lewis Mountain',
                              'Locust Grove', 'Martha Jefferson', 'North Downtown',
                              'Ridge Street', 'Rose Hill', 'Starr Hill',
                              'The Meadows', 'Venable', 'Woolen Mills']

}

default = {
    "IN_INCOME": 26000,
    "DD_PEOPLE": "",
    "IN_AGE": "30",
    "DD_PAY": opts['DD_PAY'][0],
    "DD_HOMESIZE": opts['DD_HOMESIZE'][1],
    "IN_CC": 0,
    "DD_TRANSPORT": opts['DD_TRANSPORT'][0],
    "DD_VEHICLE": opts['DD_VEHICLE'][0],
    "IN_HCARE": "Enter amount",
    "IN_TECH": 100,
    "DD_TAX": opts['DD_TAX'][0],
    "DD_LOD": opts['DD_LOD'][0],
    "AFFORD_MSG": 'Enter your \
                information to see whether Charlottesville is affordable for \
                you!'
}

ttips = {
    "IN_INCOME": "Annual $, pre-tax",
    "IN_HCARE": "Leave blank to use average; Includes premiums and out-of-pocket costs",
    "IN_TECH": "Cell phone plan, internet, etc.",
}