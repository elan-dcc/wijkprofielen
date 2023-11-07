import dash
from dash import dcc, html, Input, Output, State, callback
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
import json

dash.register_page(__name__, path='/')

#Z edit for use on her machine:
#path = 'C:/Users/fq_am/Pyhton Scripts/GGDH ver 3.0 data/App local/data/'
import os
path = '../data/'

path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")
#Z end edit.

#geojsondata = gpd.read_file(path + 'wijk_2016_6.geojson')

geo_df= gpd.read_file(path + 'wijk_2023_v0.shp')

geo_df= geo_df.to_crs(epsg=4326)
# geojsondata = geojsondata.explode(index_parts=False)
# df_info = pd.read_csv(path + 'WijkEenzaamheid2016.csv')

# geo_df = geojsondata.merge(df_info, left_on="WK_CODE", right_on= "wijkcode")

geo_df.rename(columns ={'WK_CODE':'WKC'}, inplace = True)

values_region= ["'s-Gravenhage", "Haaglanden", "Leiden", "Roaz", "Wassenaar"]

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

values_hadoks= ["'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar"]

values_all_regions = values_haaglanden + values_roaz

geo_df = geo_df.query("GM_NAAM in @values_all_regions")
 
with open(path + 'wijkgeo_all_file.json') as f:
    geo_df_fff = json.load(f)


df_numeric = pd.read_csv(path + 'df_numeric_ver_2.csv', sep=',', encoding='latin-1')
df_count = pd.read_csv(path + 'df_count_ver_2.csv', sep=',',encoding= 'latin-1')
df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])


#TODO: I propose to use a clean dataset upfront, opposed to cleaning it everytime a user opens the dashboard.

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

# End stuff that shouldn't be done here.
colorscale = ["#402580", "#38309F", "#3C50BF", "#4980DF", "#56B7FF", "#6ADDFF", "#7FFCFF", "#95FFF5", "#ABFFE8", "#C2FFE3", "#DAFFE6"]

columns = [col for col in df.columns.to_list() if col not in ['WKC', 'GMN', 'Wijknaam', 'YEAR']]


drop_var = dcc.Dropdown(
        columns,
        'Total_Population',
        id = 'drop_var_id',
        clearable=False,
        searchable=False        
    )


drop_municipality = dcc.Dropdown(
        id = 'drop_municipality',
        clearable=False, 
        searchable=False, 
        options=[
            {'label': "Hadoks Area", 'value': "HadoksArea"},
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
        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
    )

layout = html.Div([
            html.Div(
                dbc.Accordion([
                    dbc.AccordionItem([
                        html.Div([
                            html.Div([html.Label('Choose a variable to plot :', id= 'choose_variable'), drop_var], style={'width': '30%','display': 'inline-block'}),
                            html.Div([html.Label('Choose a region to plot:', id='choose_area'), drop_municipality], style={'width': '15%','display': 'inline-block'}),
                            html.Div([html.Label('Choose neighbourhoods to plot:', id= 'choose_wijk'),
                                dcc.Dropdown(
                                    columns,
                                    # 'Total_Population',
                                    id = 'drop_municipality_spec_id',
                                    clearable=True,
                                    searchable=True, 
                                    multi=True
                                )
                            ], style={'width': '55%','display': 'inline-block'}),
                            html.Div([
                                daq.Slider(
                                    id = 'slider_map',
                                    handleLabel={"showCurrentValue": True,"label": "Year"},
                                    size=1000, 
                                    color='#ADD8E6'
                                )
                            ],  id= 'sliderContainer')
                        ]),
                    ], title="Variable, Region and Year Selection :")
                ], className = 'box'), id = "dashnav"
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.H1(id='title_map'),
                        html.H2('Click on a tile to see the trendline!'), 
                        dcc.Graph(id='map', style={'position':'relative',  'height':'466px', 'top':'10px'})
                    ], className='box'),
                    html.Div([
                        html.H1(id='wijk_trend_label'),
                        html.H2('Click the button and legends to know more!'),
                        
                        dcc.Graph(id='wijk_trend_fig', style={'height':'400px'}),
                    ], className='box', style={'position':'relative'})                        
                ], id= 'leftcell'),    
                html.Div([
                    html.Div([   
                        html.H1(id='title_bar'),           
                        dcc.Graph(id='bar_fig', style={'height':'982px'}), 
                    ], className='box')                    
                ], id= 'rightcell')
            ], id="graphContainer")
        ], style={'display': 'block'})      



#------------------------------------------------------ Callbacks ------------------------------------------------------

@callback(
    [ 
        Output('drop_municipality_spec_id', 'options'),
        Output('drop_municipality_spec_id', 'value'),
       
    ],
    [
        Input('drop_municipality', 'value')
    ]
)

def update_slider(wijk_name): #TODO: This isn't regarding the slider, lol.
    if wijk_name == 'HadoksArea':    
        dff = df.query("GMN in @values_hadoks")
        options = list(dff.Wijknaam.unique()) 
    else:
        dff = df[df.GMN == wijk_name]
        options = list(dff.Wijknaam.unique())
        
    return options, options


@callback(
    [ 
        Output('slider_map', 'min'),
        Output('slider_map', 'max'),
        Output('slider_map', 'marks'),
        Output('slider_map', 'value'),
    ],
    [
        Input('drop_var_id', 'value'),
        Input('drop_municipality', 'value'),
    ]
)
def update_slider(xaxis_column_name, municipality):

    #TODO data:would have preferred to use GM_code
    if municipality == "HadoksArea":
         temp_df = df.query("GMN in @values_hadoks").copy()
    else:
        temp_df = df[df.GMN == municipality].copy()
    temp_df.dropna(subset=xaxis_column_name, inplace= True)
    min = temp_df["YEAR"].min()
    max = temp_df["YEAR"].max()
    marks = {str(i):str(i) for i in [str(i) for i in range(min, max)]}

    #TODO data: If there are just 0s for a certain municipality for a certain category in a year, obv there will be an error, but that's data mismanagement. Not my problem, lol. Should have been nans.
    return min, max, marks, max


@callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value')
    )

def update_graph_map(year_value, xaxis_column_name, wijk_name, wijk_spec
                 ):
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
    Input('slider_map', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value')
    )

def update_graph_bar(year_value, xaxis_column_name, wijk_name, wijk_spec):
    
    dff = df[df['YEAR'] == year_value]
    #TODO: this could be improved by making the colorscale in the scope above continuous and just extracting 3 values (lowest, mid and highest)
    colorscale = ["#6ADDFF", "#4980DF", "#402580"]
    
    if len(wijk_spec) == 0 :
        dff = dff[dff['GMN'] == "'s-Gravenhage"][dff['Wijknaam'] ==' Wijk 28 Centrum']
        fig = px.bar(x=dff[xaxis_column_name],
                y=dff['Wijknaam'],
                # color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )

    elif (len(wijk_spec) > 0) & (len(wijk_spec) < 3):

        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[xaxis_column_name], ascending=False).reset_index()    
        fig = px.bar(x=dff[xaxis_column_name],
                y=dff['Wijknaam'],
                # color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )
    else:
        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[xaxis_column_name], ascending=False).reset_index()   
        dff['group'] = pd.qcut(dff[xaxis_column_name], 3, labels=['Low', 'Medium', 'High'])
        
        fig = px.bar(x=dff[xaxis_column_name],
                y=dff['Wijknaam'],
                color=dff['group'],
                hover_name=dff['Wijknaam'],
                color_discrete_sequence=colorscale
                )  
     
    
    fig.update_traces(customdata=dff['Wijknaam'])

    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   
    fig.update_yaxes(title=xaxis_column_name)
    fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
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
    State('map', 'figure'),
    prevent_initial_call=False)

def update_graph(clickData, 
                 xaxis_column_name, wijk_name, wijk_spec,
                 f):

    if len(wijk_spec) == 0:
        dff = df[df['GMN'] == "'s-Gravenhage"][df['Wijknaam'] ==' Wijk 28 Centrum']
    else:
        dff = df.query("Wijknaam in @wijk_spec")

    wijk_dict = {}
    for i in range(len(dff['Wijknaam'].unique())):
        wijk_dict[dff['Wijknaam'].unique()[i]] = i

    fig = px.line(dff, x='YEAR', y=  xaxis_column_name, color='Wijknaam', color_discrete_sequence=colorscale)

    fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),

                type="date"
            ),
            
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
                                ),
                                #  dict(
                                #     # args=["visible", True],
                                #     args=[{'visible':False}, [37] ],
                                #     label="Remove Prediction",
                                #     method="restyle"
                                # ),
                            ]),
                            pad={"r": 0, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))
# asu
    if clickData is None:
        title = '{} - {}'.format(xaxis_column_name, " Wijk 28 Centrum")
        
        fig.update_traces(visible="legendonly") 
        
        fig.data[wijk_dict[list(wijk_dict.keys())[0]]].visible=True 

        return title, fig
    

    else:
        i = clickData['points'][0]['pointNumber']
        city = f['data'][0]['hovertext'][i]
        title = '{} - {}'.format(xaxis_column_name, city)

        fig.update_traces(visible="legendonly") 

        fig.data[wijk_dict[city]].visible=True 

        return title, fig
    

