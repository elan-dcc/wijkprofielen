import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div([
    html.H1('Changelog'),
    html.P("This page contains what changes relatively to the last updated version"),

    html.H2('Version 2.2 - 25/11/2024'),
    dcc.Markdown(
    """
    1. Area coverage :
    - Fix Zoetermeer, Lisse and Hillegom neighbourhood (Wijk)  
    2. Add variables related to referral info
    3. Fix JSON file read on Hadoks page (request JSON file posing some issues)
        
    """),
    
    html.H2('Version 2.1 - 24/10/2024'),
    dcc.Markdown(
    """
    1. Area coverage :
    - Change dashboard name to ELAN Dashboard
    - Neighbourhood / Wijk page changes :
        - Fix bug-related duplicated Wijk name in the drop-down list
        - Remove several variables to choose from to plot
    - Add several links and contacts to "About Us" page
        
    """),

    html.H2('Version 2 - 11/08/2024'),
    dcc.Markdown(
    """
    1. Area coverage :

    - ELAN covered area :
        - Leiden and other : Alphen aan den Rijn, Hillegom, Kaag en Braassem, Katwijk, Leiden, Leiderdorp, Lisse, Nieuwkoop, Noordwijk, Oegstgeest, Teylingen, Voorschoten, Zoeterwoude
        - Delft and other: Delft, Midden-Delfland, Pijnacker-Nootdorp, Westland
        - Zoetermeer
    - Additional : Waddinxveen, Bodegraven-Reeuwijk
    - Hadoks Area : 's-Gravenhage, Leidschendam-Voorburg, Rijswijk, Wassenaar
    
    2. Working pages are :

    - Neighbourhood: contains infographics of past variables per Neighbourhood
        - Add variable themes, to reduce the number of variables shown in the dropdown variable input
        - Fix the translation
        - Merge the variables in the Opioid page to the Nighbourhood page
    - Supply and Demand: contains a clustering and projection of selected variables per Neighbourhood in Collaboration with Hadoks
        - Fix the bivariate cluster size (in the call back function)
    - Heartfailure: contains infographics of heart failure patients
        - Add brief infomation cards
        - Add basic demographics bar chart
        - Add multi level sunburst chart
    - Remove "Work in progress" theme pages
    """),

    html.H2('Version 1 - 17/01/2024'),
    dcc.Markdown(
    """
    1. Area coverage :

    - Den Haag and other : s-Gravenhage, Leidschendam-Voorburg, Rijswijk, Wassenaar

    - Hadoks Area : 's-Gravenhage, Leidschendam-Voorburg, Rijswijk, Wassenaar
    
    2. Working pages are :

    - Neighbourhood: contains infographics of past variables per Neighbourhood
    - Supply and Demand: contains a clustering and projection of selected variables per Neighbourhood in Collaboration with Hadoks
    - Opioid page
        - Variables available are Alcohol abuse, Medication abuse, Loneliness, BMI, and Opioid medication user
        - Add a basic map chart
        - Add scatter and line chart
    - Other theme projects/pages are still "Work in Progress"
    """)
    ])
