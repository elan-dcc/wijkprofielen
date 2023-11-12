import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
import json
from matplotlib.colors import LinearSegmentedColormap, to_hex
import os

# style
colorscale = ["#402580", "#38309F", "#3C50BF", "#4980DF", "#56B7FF", "#6ADDFF", "#7FFCFF", "#95FFF5", "#ABFFE8", "#C2FFE3", "#DAFFE6"]
elan_cm = LinearSegmentedColormap.from_list("pretty_elan", colorscale, N=len(colorscale))
    
style = {"fontsize": 12,
         "color": "#808080",
         "slider": "#ADD8E6"}

def get_colors(min_thresh: float, resample: int) -> list:
    '''helper function to sample colours'''
    step = (1 - min_thresh)/resample
    return [to_hex(elan_cm(i)) for i in np.arange(0, 1.0-min_thresh, step)] 
# end style

dash.register_page(__name__, path='/')


path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")


#geojsondata = gpd.read_file(path + 'wijk_2016_6.geojson')

geo_df= gpd.read_file(path + 'wijk_2023_v0.shp')

geo_df= geo_df.to_crs(epsg=4326)
# geojsondata = geojsondata.explode(index_parts=False)
# df_info = pd.read_csv(path + 'WijkEenzaamheid2016.csv')

# geo_df = geojsondata.merge(df_info, left_on="WK_CODE", right_on= "wijkcode")

geo_df.rename(columns ={'WK_CODE':'WKC'}, inplace = True)


values_haaglanden=["'s-Gravenhage",
        "Delft","Leidschendam-Voorburg",
        "Midden-Delfland", 
        "Pijnacker-Nootdorp","Rijswijk",
        "Wassenaar","Westland","Zoetermeer"]

values_roaz=["'s-Gravenhage", "Alphen aan den Rijn", "Bodegraven-Reeuwijk",
        "Delft","Gouda","Hillegom", "Kaag en Braassem","Katwijk",
        "Krimpenerwaard","Leiden","Leiderdorp", "Leidschendam-Voorburg",
        "Lisse","Midden-Delfland","Nieuwkoop","Noordwijk","Oegstgeest",
        "Pijnacker-Nootdorp","Rijswijk","Teylingen","Voorschoten", "Waddinxveen",
        "Wassenaar","Westland","Zoetermeer","Zoeterwoude","Zuidplas"]

values_all_regions = values_haaglanden + values_roaz

geo_df = geo_df.query("GM_NAAM in @values_all_regions")


values_hadoks= ("'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar")

#this way, we can always extend the number of special regions, without having to tamper with the rest of the code
#could even be read in from a file or sth to keep it from being hardcoded.
special_regions = {"Hadoks' area": values_hadoks}
 
with open(path + 'wijkgeo_all_file.json') as f:
    geo_df_fff = json.load(f)


df_numeric = pd.read_csv(path + 'df_numeric_ver_2.csv', sep=',', encoding='latin-1')
df_count = pd.read_csv(path + 'df_count_ver_2.csv', sep=',',encoding= 'latin-1')
df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])


#cleaning up temp/dummy dataset

COSTS_COLUMN_NAME = ['ZVWKOSTENTOTAAL_MEAN', 'ZVWKHUISARTS_MEAN', 'ZVWKHUISARTS_NO_REG_MEAN', 
                     'ZVWKZIEKENHUIS_MEAN','ZVWKFARMACIE_MEAN', 'ZVWKFARMACIE_MEAN', 'ZVWKOSTENPSYCHO_MEAN',
                     '%_ZVWKHUISARTS_user', '%_ZVWKFARMACIE_user', '%_ZVWKZIEKENHUIS_user', '%_ZVWKOSTENPSYCHO_user'
                     ]

MEDICATION_COLUMN_NAME = ['UniqueMed_Count_MEAN', 'UniqueMed_Count_SD', '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                      '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10', 
                     ]
   
INCOME_COLUMN_NAME = ['Income_MEAN', '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                      '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user',
                      '%_Low_Income', '%_Debt_Mortgage',
                     ]

for med in MEDICATION_COLUMN_NAME:
    df[med] = df[med].mask(((df['YEAR'] <2009) | (df['YEAR'] >2021)), np.nan)
    
for cost in COSTS_COLUMN_NAME:
    df[cost] = df[cost].mask(((df['YEAR'] <2009) | (df['YEAR'] >2020)), np.nan)
    
for income in INCOME_COLUMN_NAME:
    df[income] = df[income].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)
    
df['%_Wanbet'] = df['%_Wanbet'].mask(( (df['YEAR'] <2010) | (df['YEAR'] >2021) ) , np.nan)
df['%_WLZ_user'] = df['%_WLZ_user'].mask(( (df['YEAR'] <2015) | (df['YEAR'] >2021) ) , np.nan)
df['%_WMO_user'] = df['%_WMO_user'].mask(( (df['YEAR'] <2015) | (df['YEAR'] >2022) ) , np.nan)


df['Income_MEAN'] = df['Income_MEAN'].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)

df['%_WMO_user'] = df['%_WMO_user'].mask(((df['YEAR'] <2015) ), np.nan)
df['%_WLZ_user'] = df['%_WLZ_user'].mask(((df['YEAR'] <2015) ), np.nan)

df['ZVWKOSTENTOTAAL_MEAN'] = df['ZVWKOSTENTOTAAL_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKFARMACIE_MEAN'] = df['ZVWKFARMACIE_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKHUISARTS_MEAN'] = df['ZVWKHUISARTS_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKHUISARTS_NO_REG_MEAN'] = df['ZVWKHUISARTS_NO_REG_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKZIEKENHUIS_MEAN'] = df['ZVWKZIEKENHUIS_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKFARMACIE_MEAN'] = df['ZVWKFARMACIE_MEAN'].mask( (df['YEAR'] >2020), np.nan)
df['ZVWKOSTENPSYCHO_MEAN'] = df['ZVWKOSTENPSYCHO_MEAN'].mask( (df['YEAR'] >2020), np.nan)

df['%_ZVWKHUISARTS_user'] = df['%_ZVWKHUISARTS_user'].mask( (df['YEAR'] >2020), np.nan)
df['%_ZVWKFARMACIE_user'] = df['%_ZVWKFARMACIE_user'].mask( (df['YEAR'] >2020), np.nan)
df['%_ZVWKZIEKENHUIS_user'] = df['%_ZVWKZIEKENHUIS_user'].mask( (df['YEAR'] >2020), np.nan)
df['%_ZVWKOSTENPSYCHO_user'] = df['%_ZVWKOSTENPSYCHO_user'].mask( (df['YEAR'] >2020), np.nan)

# End clean-up

columns = [col for col in df.columns.to_list() if col not in ['WKC', 'GMN', 'Wijknaam', 'YEAR']]


drop_var = dcc.Dropdown(
        columns,
        'Total_Population',
        id = 'drop_var_id',
        clearable=False,
        searchable=False,
        className = "custom_select"
    )


drop_municipality = dcc.Dropdown(
        id = 'drop_municipality',
        clearable=False, 
        searchable=False, 
        # below could be improved as well eventually, by extracting all regions from the data + the special_regions
        options=[
            {'label': "Hadoks' area", 'value': "Hadoks' area"},
            {'label': "'s-gravenhage", 'value': "'s-Gravenhage"},
            {'label': "Rijswijk", 'value': "Rijswijk"},
            {'label': 'Leidschendam-Voorburg', 'value': 'Leidschendam-Voorburg'},
            {'label': 'Wassenaar', 'value': 'Wassenaar'},
            # {'label': 'Roaz', 'value': 'Roaz'},
            # {'label': "Haaglanden", 'value': 'Haaglanden'},
            # {'label': 'Leiden', 'value': 'Leiden'},
            # {'label': 'Delft', 'value': 'Delft'}
            ],
        value="'s-Gravenhage", 
        className = "custom_select"
    )

layout = html.Div([
            html.Div(
                dbc.Accordion([
                    dbc.AccordionItem([
                        html.Div([
                            html.Div([html.Label('Choose a variable to plot :', id= 'choose_variable', htmlFor= 'drop_var_id'), drop_var], id= 'select_variable'),
                            html.Div([html.Label('Choose a region to plot:', id='choose_area', htmlFor= 'drop_municipality'), drop_municipality], id = 'select_region'),
                            html.Div([html.Label('Choose neighbourhoods to plot:', id= 'choose_wijk', htmlFor= 'drop_municipality_spec_id'),
                                dcc.Dropdown(
                                    columns,
                                    id = 'drop_municipality_spec_id',
                                    clearable=True,
                                    searchable=True, 
                                    multi=True,
                                    className= "custom_select"
                                )
                            ], id='select_neighbourhoods'),
                            html.Div([
                                "Select year of interest",
                                dcc.Slider(step=1, id = 'slider_select_year'),
                                dcc.Dropdown( id = 'drop_select_year', className= "custom_select") #when resolution is small, slider is no longer practical
                            ],  id= 'sliderContainer')
                        ], id= 'select_container'),
                    ], title="Variable, Region and Year Selection :")
                ], className = 'box'), id = "dashnav"
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.H1(id='title_map'),
                        html.P('Click on a tile to see the trendline!'), 
                        dcc.Graph(id='map')
                    ], className='box'),
                    html.Div([
                        html.H1(id='wijk_trend_label'),
                        html.P('Click the button and legends to know more!'),
                        
                        dcc.Graph(id='wijk_trend_fig'),
                    ], className='box')                        
                ], id= 'leftcell'),    
                html.Div([
                    html.Div([   
                        html.H1(id='title_bar'),           
                        dcc.Graph(id='bar_fig'), 
                    ], className='box')                    
                ], id= 'rightcell')
            ], id="graphContainer")
        ])      

#------------------------------------------------------ Callbacks ------------------------------------------------------

@callback(
    Output('drop_municipality_spec_id', 'options'),
    Output('drop_municipality_spec_id', 'value'),
    Input('drop_municipality', 'value')
)
def update_select_neighbourhoods(wijk_name):
    '''
    Present the neighbourhoods of the selected region to the user
    '''
    if wijk_name in special_regions.keys():    
        dff = df.query("GMN in @special_regions[@wijk_name]")
        options = list(dff.Wijknaam.unique()) 
    else:
        dff = df[df.GMN == wijk_name]
        options = list(dff.Wijknaam.unique())
        
    return options, options

@callback(
    Output('slider_select_year', 'min'),
    Output('slider_select_year', 'max'),
    Output('slider_select_year', 'marks'),
    Output('slider_select_year', 'value'),
    Output('drop_select_year', 'options'),
    Output('drop_select_year', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_select_year', 'value')
)

def update_slider(xaxis_column_name, municipality, drop_value):
    '''
    Sets the slider to values corresponding the data of the chosen region.
    The drop_select_year dropdown menu and the drop_value variable were added for responsive web design.
    '''
    #TODO data:would have preferred to use GM_code
    if municipality in special_regions.keys():
         temp_df = df.query("GMN in @special_regions[@municipality]").copy()
    else:
        temp_df = df[df.GMN == municipality].copy()
    temp_df.dropna(subset=xaxis_column_name, inplace= True)
    
    min = temp_df["YEAR"].min()
    max = temp_df["YEAR"].max()
    
    marks = {str(i):str(i) for i in [str(i) for i in range(min, max)]}

    value = max
    if (drop_value):
        value = drop_value

    return min, max, marks, value, list(range(min, max)), value


@callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('slider_select_year', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value')
    )

def update_graph_map(year_value, xaxis_column_name, wijk_name, wijk_spec
                 ):
    '''
    Select the appropriate data to display in the map fig
    '''
    dff = df[df['YEAR'] == year_value]

    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)
        
    dff = dff.query("Wijknaam in @wijk_spec")

    fig = px.choropleth_mapbox(dff, geojson=geo_df, color=xaxis_column_name,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.5,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale,
                            mapbox_style="carto-positron", zoom=10, hover_name="Wijknaam")
    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title

# create a new column that put each row into a group of 4 numbers based on the value of a column quartile

@callback(
    Output('title_bar', 'children'),
    Output('bar_fig', 'figure'),
    Input('slider_select_year', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value')
    )

def update_graph_bar(year_value, xaxis_column_name, wijk_name, wijk_spec):
    '''
    Update the bar chart based on new values
    '''
    dff = df[df['YEAR'] == year_value]
    
    if len(wijk_spec) == 0:
        fig = px.bar(x=[0, 10],
                y=[0, 0]
                )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        return "No neighbourhood selected", fig

    elif len(wijk_spec) < 3:
        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[xaxis_column_name], ascending=False).reset_index()    
        fig = px.bar(dff, xaxis_column_name, 'Wijknaam',
                hover_name='Wijknaam', color_discrete_sequence=get_colors(0, 1))
        
    else:
        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[xaxis_column_name], ascending=False).reset_index()   
        dff['group'] = pd.qcut(dff[xaxis_column_name], 3, labels=['Low', 'Medium', 'High'])

        fig = px.bar(dff, xaxis_column_name, 'Wijknaam', color= 'group',
                hover_name='Wijknaam', color_discrete_sequence=get_colors(0.2, 3))
        

    fig.update_traces(hovertemplate=
                  '<b>%{hovertext}</b>:' +
                  '<br><b>Value</b>: %{x}<br>')  

    fig.update_layout(hovermode="y")
        
    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   
    fig.update_yaxes(title=xaxis_column_name)
    fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo= {'bgcolor': 'rgba(0,0,0,0)'},
                      autosize= False,
                      font = {"size": style["fontsize"], "color": style["color"]},
                      paper_bgcolor='white', 
                      yaxis={'categoryorder':'total ascending'}
                      )

    return title, fig

@callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Input('map', 'clickData'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value'),
    prevent_initial_call=False
    )

def update_graph(clickData, 
                 xaxis_column_name, wijk_name, wijk_spec):
    '''
    Update line graph 
    '''

    if len(wijk_spec) == 0:
        fig = px.line(x=[0, 10], y=[0, 0])
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        return "No neighbourhood selected", fig    
    
    dff = df.query("Wijknaam in @wijk_spec")
    
    fig = px.line(dff, x='YEAR', y=  xaxis_column_name, color='Wijknaam', color_discrete_sequence=colorscale)

    fig.update_layout(xaxis={
        "rangeslider":{"visible": True},
        "type": "date"
        },font = {"size": style["fontsize"], "color": style["color"]} 
    )
    
    fig.update_layout(dict(updatemenus=[
                        dict(
                            type = "buttons",
                            direction = "left",
                            buttons=list([
                                
                                dict(
                                    args=["visible", True],
                                    label="Select All",
                                    method="restyle"
                                ),
                                dict(
                                    args=[{'visible':'legendonly'} ],
                                    label="Remove All",
                                    method="restyle"
                                )
                            ]),
                            pad={"r": 0, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        )
                    ]
              ))
    
    if clickData is None: #change chart based on selection from the select
        title = '{} - {}'.format(xaxis_column_name, dff["Wijknaam"].unique()[0])
        
        fig.update_traces(visible="legendonly")

        fig.data[0].visible=True 

    else: #User can click on neighbourhoods in the map to affect the linechart. 
        title = '{} - {}'.format(xaxis_column_name, clickData['points'][0]['hovertext'])
        fig.update_traces(visible="legendonly") 
        fig.data[clickData['points'][0]['pointIndex']].visible=True 

    return title, fig
    

