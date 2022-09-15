# ------------------Neighborhood page------------------#
import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import srcCode.toolbarDescs as tb
import srcCode.resourcesDescs as rd
import srcCode.dashFuncs as df

dash.register_page(__name__)

layout = html.Div(
    [
        # Top bar
        df.createTopBar(),
        html.Br(),
        html.Div(
        [
                html.H3(rd.text['MAIN_TITLE'], className = "center_text title"),
                html.Br(),
                html.Span(rd.text['SOURCES_HOOD'], className="left_text bodytext"), 
                html.Span(rd.text['THANKS'], className="left_text bodytext"), 
                df.createArrowLink(rd.text['THANKSLINK'], rd.links['THANKS']),
                # C-VILLE Weekly links
                html.Span(rd.text["CVILLE_WEEKLY"], className="left_text bodytext"),
                df.createArrowLink(rd.text['CVILLE_1'], rd.links['CVILLE_1']),
                df.createArrowLink(rd.text['CVILLE_2'], rd.links['CVILLE_2']),
                df.createArrowLink(rd.text['CVILLE_3'], rd.links['CVILLE_3']),
                df.createArrowLink(rd.text['CVILLE_4'], rd.links['CVILLE_4']),
                # Cvillepedia
                html.Span(rd.text["CVILLEPEDIA"], className="left_text bodytext"),
                df.createArrowLink(rd.text['CVP'], rd.links['CVP']),
                # CvilleTomorrow links
                html.Span(rd.text["CVILLETOMORROW"], className="left_text bodytext"),
                df.createArrowLink(rd.text['CVT_1'], rd.links['CVT_1']),
                df.createArrowLink(rd.text['CVT_2'], rd.links['CVT_2']),
                html.Br(),
                html.Br(),
                # affordability links
                html.Span(rd.text["AFFORD"], className="left_text bodytext"),
                df.createArrowLink(rd.text['METHODS'], rd.links['METHODS']),
                html.Br(),
                html.Br(),
                html.Span(rd.text["CENSUS"], className="left_text bodytext"),
                df.createArrowLink(rd.text['SEXBYAGE'], rd.links['SEXBYAGE']),
                df.createArrowLink(rd.text['INCOME'], rd.links['INCOME']),
                df.createArrowLink(rd.text['INDUSTRY'], rd.links['INDUSTRY']),
                df.createArrowLink(rd.text['RACE'], rd.links['RACE']),
                html.Br(),
                html.Br(),
                html.Span(rd.text["SALES"], className="left_text bodytext"),
                df.createArrowLink(rd.text['HISTORY'], rd.links['HISTORY']),
                html.Br(),
                html.Br(),
                html.Span(rd.text["QOL_MAP"], className="left_text bodytext"),
                df.createArrowLink(rd.text['TRANSPORT'], rd.links['TRANSPORT']),
                df.createArrowLink(rd.text['OPENST'], rd.links['OPENST']),
                html.Br(),
                #dcc.Link('Take me back up', href='#', className = "left_text links_text"),
        ], className = "subcontainer")
    ], className = "container background")
