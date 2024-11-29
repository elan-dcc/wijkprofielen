import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.graph_objects as go
import os

dash.register_page(__name__)

path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")

df_h = pd.read_excel(open(path + ('Codebook_shorter.xlsx'), 'rb'), sheet_name='Huisartsen')
df_cbs = pd.read_excel(open(path + ('Codebook_shorter.xlsx'), 'rb'), sheet_name='CBS')

layout = html.Div([
    html.H1('ELAN-GP'),
    dcc.Markdown(
    """
    ELAN-H/GP (Huisartsen) is een uniek huisartsen-netwerk met (op dit moment) meer dan 140 
    deelnemende huisartsen en data van meer dan 800.000 patiënten in de ELAN-huisartsendata. 
    Via ELAN-H zijn inmiddels tientallen onderzoeken verricht en we hopen dat in de komende jaren voort 
    te kunnen zetten.
    """),
    html.P([html.A('ELAN-H', href='https://elan-dcc.github.io/researchers/gp_data/', target='_blank')]),
    dash_table.DataTable(
       columns=[
              {'name': 'Hoofdgroep', 'id': 'Hoofdgroep', 'type': 'text'},
              {'name': 'Beschrijving', 'id': 'Beschrijving', 'type': 'text'},
       ],
       data=df_h.to_dict('records'),
       filter_action='native',
       style_data={
           'whiteSpace': 'normal',
            
       },
       style_cell={'textAlign': 'left'}
       ),

    html.P(''),
    
    html.H1('ELAN-CBS'),
    dcc.Markdown(
    """
    Gezond en Gelukkig Den Haag (GGDH) wordt door de afdeling PHEG op de LUMC-Campus Den Haag
    en het LUMC ondersteund met de data-infrastructuur van ELAN-CBS. In ELAN-CBS delen niet
    alleen huisartsen, maar ook de ziekenhuizen, de gemeente en in de toekomst ook andere
    zorgverleners gepseudonimiseerde gegevens met het CBS als “trusted third party”. Dankzij het CBS
    kunnen deze gepseudonimiseerde gegevens nog verder worden verrijkt met gegevens die het CBS al
    onder haar hoede heeft, zoals huishoudsamenstelling en inkomen.
    """
    # [Data source](https://paygap.ie/)
    # [Data source GitHub](https://github.com/zenbuffy/irishGenderPayGap/tree/main)
    # [Plotly Community Forum](https://community.plotly.com/t/figure-friday-2024-week-32/86401)
    ),
    html.P([html.A('ELAN-CBS', href='https://www.cbs.nl/nl-nl/onze-diensten/maatwerk-en-microdata/microdata-zelf-onderzoek-doen/catalogus-microdata', target='_blank')]),
    dash_table.DataTable(
       columns=[
              {'name': 'Hoofdgroep', 'id': 'Hoofdgroep', 'type': 'text'},
              {'name': 'Beschrijving', 'id': 'Beschrijving', 'type': 'text'},
       ],
       data=df_cbs.to_dict('records'),
       filter_action='native',
       style_data={
           'whiteSpace': 'normal',
       },
       style_cell={'textAlign': 'left'}
       ),
    html.P(''),
    ])