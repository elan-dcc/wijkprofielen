import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages= True)

server = app.server

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(html.A(html.Img(src= app.get_asset_url('hc-dh-logo.png')), href= 'https://healthcampusdenhaag.nl/nl/')),
                    dbc.Col([html.H1("ELAN Neighbourhood Dashboard"), html.P('Last updated October 2023')], id= 'headersub')
                ],
                align="center",
                className="g-0",
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [dcc.Link('Neighbourhood', href= '/'),
                    dcc.Link('Supply vs Demand', href='/supplydemand'),
                    dcc.Link("Diabetes", href="/diabetes"),
                    dcc.Link("Palliative care", href="/palliative"),
                    dcc.Link("Young care", href="/young")],
                    className="ms-auto"
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    id= 'header',
    className="mb-5"
)

footer = html.Div([
                html.Div([
                    html.P([
                        html.H1('Health Campus Den Haag'),'Turfmarkt 99', html.Br(), '3rd floor', html.Br(), '2511 DP, Den Haag'])
                ], className= 'footerelement'), 
                html.Div([
                    html.Ul([html.Li(dcc.Link('About', href= '/about')), html.Li(dcc.Link('changelog', href= '/changelog')), html.Li("link to Elan?")])
                ], className= 'footerelement'),
                html.Div([
                    html.H1('Partners'),
                    html.A([html.Img(src=app.get_asset_url('lumc-1-500x500.jpg'))], href='https://www.lumc.nl/en/'),
                    html.A([html.Img(src=app.get_asset_url('uni_leiden-500x500.jpg'))], href='https://www.universiteitleiden.nl/en'),
                    html.A([html.Img(src=app.get_asset_url('hhs-500x500.jpg'))], href='https://www.dehaagsehogeschool.nl/'),                                                   
                    html.A([html.Img(src=app.get_asset_url('hmc-1-500x500.jpg'))], href='https://www.haaglandenmc.nl/'),  
                    html.A([html.Img(src=app.get_asset_url('haga_ziekenhuis-500x500.jpg'))], href='https://www.hagaziekenhuis.nl/home/'),
                    html.A([html.Img(src=app.get_asset_url('hadoks-1-500x500.jpg'))], href='https://www.hadoks.nl/'),
                    html.A([html.Img(src=app.get_asset_url('parnassia-500x500.jpg'))], href='https://www.parnassia.nl/'),
                    html.A([html.Img(src=app.get_asset_url('rienier_de_graaf-500x500.jpg'))], href='https://reinierdegraaf.nl/'),
                    html.A([html.Img(src=app.get_asset_url('gemeente_dh-500x500.jpg'))], href='https://www.denhaag.nl/nl.htm'),
                    ], id = 'partners', className = 'footerelement'),
            ], id = 'footer')


app.layout = html.Div([navbar,    
    html.Div(html.Div(html.Div(dash.page_container, id='main', className= 'toggle'))),
    footer
])


#------------------------------------------------------ Callbacks ------------------------------------------------------

# navigation
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open



if __name__ == '__main__':
    app.run_server(debug=True, port=8080)




