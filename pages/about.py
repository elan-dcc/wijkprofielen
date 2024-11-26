import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.graph_objects as go
import os

dash.register_page(__name__)

layout = html.Div([
    html.H1('About the Dashboard'),
    dcc.Markdown(
    ["""
    Dit dashboard is gemaakt om onderzoekers, gezondheidswerkers en beleidsmakers in de publieke 
    gezondheidssector te verbeteren en te betrekken. Elke dashboardpagina vertegenwoordigt 
    verschillende onderzoeken die we hebben gedaan op Health Campus Den Haag en LUMC met 
    behulp van gegevens uit onze ELAN-dataomgeving.

    Neem voor meer informatie over het dashboard contact met ons op:
    <br />
    
    elan.dcc@lumc.nl
    
    """],
    dangerously_allow_html=True,
    ),
    html.H1('ELAN'),
    dcc.Markdown(
        [
    """
    Binnen ELAN werken zorgverleners uit de regio samen met de afdeling Public Health en 
    Eerstelijnsgeneeskunde en de Health Campus Den Haag van het LUMC aan ondersteuning, 
    vernieuwing en verbetering van de zorg.
    
    ELAN-H/GP (Huisartsen) is een uniek huisartsen-netwerk met (op dit moment) meer dan 140 
    deelnemende huisartsen en data van meer dan 800.000 patiënten in de ELAN-huisartsendata. 
    Via ELAN-H zijn inmiddels tientallen onderzoeken verricht en we hopen dat in de komende jaren voort 
    te kunnen zetten.

    Voor meer informatie:
    
    <br />
    
    <dccLink href="https://www.lumc.nl/over-het-lumc/partners/elan/" children="ELAN" /> 
    
    <br />
    
    <dccLink href="www.elanresearch.nl" children="ELAN Research" /> 
    
    <br />
    
    <dccLink href="https://www.lumc.nl/siteassets/over-het-lumc/partners/elan/data-governance.pdf" children="ELAN Data Governance" /> 
    
    """
        ],
        dangerously_allow_html=True,
    ),
    html.H1('Hadoks / Supply and Demand Themes'),
    dcc.Markdown(
    """
    Dashboard gemaakt in samenwerking met Hadoks
    """),
    html.H1('Hartfalen Themes'),
    dcc.Markdown(
    """
        Dashboard in samenwerking met hart- en vaatonderzoeksgroep
    """),
#     html.P([html.A('GGDH-ELAN', href='https://gezondengelukkigdenhaag.nl/', target='_blank'),
#            ',',
#            html.A('Microdata CBS', href='https://www.cbs.nl/en-gb/our-services/customised-services-microdata/microdata-conducting-your-own-research', target='_blank')])
    ])
