import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1('About'),
    html.P([html.A('GGDH-ELAN', href='https://gezondengelukkigdenhaag.nl/', target='_blank'),
           ',',
           html.A('Microdata CBS', href='https://www.cbs.nl/en-gb/our-services/customised-services-microdata/microdata-conducting-your-own-research', target='_blank')])
    ])