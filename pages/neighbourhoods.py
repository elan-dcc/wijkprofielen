import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap, to_hex
import os
import util.translate as tr

# style
colorscale = ["#402580", "#38309F", "#3C50BF", "#4980DF", "#56B7FF", "#6ADDFF", "#7FFCFF", "#95FFF5", "#ABFFE8", "#C2FFE3", "#DAFFE6"]

colorscale_inverted = ["#DAFFE6", "#C2FFE3", "#ABFFE8", "#95FFF5", "#7FFCFF", "#6ADDFF", "#56B7FF", "#4980DF", "#3C50BF", "#38309F", "#402580"]
elan_cm = LinearSegmentedColormap.from_list("pretty_elan", colorscale, N=len(colorscale))
    
style = {"fontsize": 12,
         "color": "#808080",
         "slider": "#ADD8E6"}

def get_colors(min_thresh: float, resample: int) -> list:
    '''helper function to sample colours'''
    step = (1 - min_thresh)/resample
    return [to_hex(elan_cm(i)) for i in np.arange(0, 1.0-min_thresh, step)] 
# end style

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


# values_all_regions_gementee = [s + "Gemeente " for s in values_all_regions]
# values_all_regions = [s + "Gemeente " for s in values_all_regions]


values_hadoks= ("'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar")

# values_values_hadoks_gementee = [s + "Gemeente " for s in values_hadoks]

#this way, we can always extend the number of special regions, without having to tamper with the rest of the code
#could even be read in from a file or sth to keep it from being hardcoded.
special_regions = {"Hadoks' area": values_hadoks}


dash.register_page(__name__, path='/')

path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")

geo_df= gpd.read_file(path + 'wijk_2023_v0.shp')

geo_df= geo_df.to_crs(epsg=4326)

geo_df.rename(columns ={'WK_CODE':'WKC'}, inplace = True)

geo_df = geo_df.query("GM_NAAM in @values_all_regions")



df_numeric = pd.read_csv(path + 'df_numeric_ver_3.csv', sep=',', encoding='latin-1')
df_count = pd.read_csv(path + 'df_count_ver_3.csv', sep=',',encoding= 'latin-1')
df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])

#cleaning up temp/dummy dataset
df = df[df.YEAR < 2023]
df = df[df.YEAR > 2009]
df = df[df.WKC != 'WK1916--']
# REMOVE word "Wijk " if we found double the words in column Wijknaam (Wijk Wijk)
df['Wijknaam'] = df['Wijknaam'].str.replace('Wijk Wijk ', 'Wijk ')
# REMOVE word "Wijk " if we found double the words in column Wijknaam (Wijk Wijk)
df['GMN'] = df['GMN'].str.replace('Gemeente ', '')

# change negative values to 0
cols = df.select_dtypes(include=np.number).columns
df[cols] = df[cols].clip(lower=0)

# remove column %_AGE_CAT_71to80 
df.drop(['%_AGE_CAT_71to80'], axis=1, inplace=True)

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

df['%_UniqueMed_Count_>=5'].mask(((df['YEAR'] <2009) | (df['YEAR'] >2021)), np.nan)
df['%_UniqueMed_Count_>=10'].mask(((df['YEAR'] <2009) | (df['YEAR'] >2021)), np.nan)

df['%_JGDHULP_user'] = df['%_JGDHULP_user'].mask(((df['YEAR'] <2015) ), np.nan)

df['%_SHNTAB'] = df['%_SHNTAB'].mask(((df['YEAR'] <2015) ), np.nan)

df['%_HBOPL_Low'] = df['%_HBOPL_Low'].mask(((df['YEAR'] <2013) ), np.nan)
df['%_HBOPL_Mid'] = df['%_HBOPL_Mid'].mask(((df['YEAR'] <2013) ), np.nan)
df['%_HBOPL_High'] = df['%_HBOPL_High'].mask(((df['YEAR'] <2013) ), np.nan)

df['%_HGOPL_Low'] = df['%_HGOPL_Low'].mask(((df['YEAR'] <2013) ), np.nan)
df['%_HGOPL_Mid'] = df['%_HGOPL_Mid'].mask(((df['YEAR'] <2013) ), np.nan)
df['%_HGOPL_High'] = df['%_HGOPL_High'].mask(((df['YEAR'] <2013) ), np.nan)


# End clean-up

#headers and orig_columns are here to support i18n
headers = df.columns.to_list().copy()
columns = [col for col in headers if col not in ['WKC', 'GMN', 'Wijknaam', 'YEAR']]
orig_columns = columns.copy()

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
            {'label': "'s-gravenhage", 'value': "'s-Gravenhage"},
            {'label': "Rijswijk", 'value': "Rijswijk"},
            {'label': 'Leidschendam-Voorburg', 'value': 'Leidschendam-Voorburg'},
            {'label': 'Wassenaar', 'value': 'Wassenaar'},
            {'label': "Hadoks' area", 'value': "Hadoks' area"},
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
                            html.Div([html.Label('Choose a variable to plot:', id= 'choose_variable', htmlFor= 'drop_var_id'), drop_var], id= 'select_variable'),
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
                                html.P("Select a year", id='select_year'),
                                dcc.Slider(step=1, id = 'slider_select_year'),
                                dcc.Dropdown( id = 'drop_select_year', className= "custom_select") #when resolution is small, slider is no longer practical
                            ],  id= 'sliderContainer')
                        ], id= 'select_container'),
                    ], title="Variable, Region and Year Selection :", id="control_panel")
                ], className = 'box'), id = "dashnav"
            ),
            html.Div([
                html.Div([
                    html.Div([
                        html.H1(id='title_map'),
                        html.P('Click on a tile to see the trendline!', id='geospat_expl'), 
                        dcc.Graph(id='map')
                    ], className='box'),
                    html.Div([
                        html.H1(id='wijk_trend_label'),
                        html.P('Click the button and legends to know more!', id='linechart_expl'),
                        
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
        ], id="dataContainer")      

#------------------------------------------------------ Callbacks ------------------------------------------------------
# Getting the language from the session, and changing the class of the dataContainer
@callback(
    Output('dataContainer', 'className'),
    Input('session', 'data')
)
def get_language(data):
    return data

#localisation (chained)
@callback(
    Output('linechart_expl', 'children'),
    Output('geospat_expl', 'children'),
    Output('choose_variable', 'children'),
    Output('choose_area', 'children'),
    Output('choose_wijk', 'children'),
    Output('select_year', 'children'),
    Output('control_panel', 'title'),
    Output('drop_var_id', 'options'),
    Output('drop_var_id', 'value'),
    Input('session', 'data')
)
def localise(language):
    global columns
    linechart_expl = (tr.translate("linechart explanation"))
    geospat_expl = (tr.translate('geospat explanation'))
    choose_variable = (tr.translate('select variable'))
    choose_area = (tr.translate('select area'))
    choose_neighborhoud = (tr.translate('select neighbourhood'))
    select_year = (tr.translate('select year'))
    control_panel = (tr.translate('control panel'))
    
    #updating visualisations + dropdown menus
    drop_var = tr.translate_list(orig_columns)
    # ugly
    drop_var_value = tr.translate('Total_Population')
    columns = drop_var
    df.columns = tr.translate_list(headers)
    return linechart_expl, geospat_expl, choose_variable, choose_area, \
        choose_neighborhoud, select_year, control_panel, drop_var, drop_var_value


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
    
    min = temp_df[tr.translate("YEAR")].min()
    max = temp_df[tr.translate("YEAR")].max()
    
    marks = {str(i):str(i) for i in [str(i) for i in range(min, max +1)]}

    value = max

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
    dff = df[df[tr.translate('YEAR')] == year_value]

    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)
        
    dff = dff.query("Wijknaam in @wijk_spec")

    fig = px.choropleth_mapbox(dff, geojson=geo_df, color=xaxis_column_name,
                            locations=tr.translate("WKC"), featureidkey="properties.WKC", opacity = 0.5,
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
    dff = df[df[tr.translate('YEAR')] == year_value]
    
    if len(wijk_spec) == 0:
        fig = px.bar(x=[0, 10],
                y=[0, 0]
                )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        
        return "No neighbourhood selected", fig    
    else:
        dff = dff.query("Wijknaam in @wijk_spec")
        dff = dff.sort_values(by=[xaxis_column_name], ascending=False).reset_index()   

        fig = px.bar(dff, xaxis_column_name, 'Wijknaam', color= xaxis_column_name,
                hover_name='Wijknaam', color_continuous_scale=colorscale
                )
        

    fig.update_traces(hovertemplate=
                  '<b>%{hovertext}</b>:' +
                  '<br><b>Value</b>: %{x}<br>')  

    fig.update_layout(hovermode="y")
        
    title = '{} - {} - {} '.format(xaxis_column_name, wijk_name, year_value)   
    # fig.update_yaxes(title=xaxis_column_name)
    # fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo= {'bgcolor': 'rgba(0,0,0,0)'},
                      autosize= False,
                      font = {"size": style["fontsize"], "color": style["color"]},
                      paper_bgcolor='white', 
                      yaxis={'categoryorder':'total ascending'}
                    #   showlegend=False
                      )
    fig.update_coloraxes(showscale=False)
    

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
    dff = dff.sort_values(by=[tr.translate('YEAR'), xaxis_column_name], ascending=False).reset_index()

    fig = px.line(dff, x=tr.translate('YEAR'), y=  xaxis_column_name, color='Wijknaam', color_discrete_sequence=colorscale_inverted)

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
    

