import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from matplotlib.colors import LinearSegmentedColormap, to_hex
import geopandas as gpd
import requests
import json
import math

import os
import util.translate as tr
import util.bivariate_plot 

from util.bivariate_plot import conf_defaults
from util.bivariate_plot import recalc_vars
from util.bivariate_plot import set_interval_value
from util.bivariate_plot import prepare_df
from util.bivariate_plot import create_legend
from util.bivariate_plot import create_bivariate_map

# style
color_sets = {
    'pink-blue':   ['#e8e8e8', '#ace4e4', '#5ac8c8', 
                    '#dfb0d6', '#a5add3', '#5698b9', 
                    '#be64ac', '#8c62aa', '#3b4994'],
    'teal-red':    ['#eae3f5', '#e4acac', '#c85a5a', 
                    '#b0d5df', '#ad9ea5', '#985356', 
                    '#64acbe', '#627f8c', '#574249'],
    'blue-organe': ['#fef1e4', '#fab186', '#f3742d',  
                    '#97d0e7', '#b0988c', '#ab5f37', 
                    '#18aee5', '#407b8f', '#5c473d']
}

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

values_hadoks= ["'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar"]

#this way, we can always extend the number of special regions, without having to tamper with the rest of the code
#could even be read in from a file or sth to keep it from being hardcoded.
special_regions = {"Hadoks' area": values_hadoks}


dash.register_page(__name__)

path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/").replace("pages" + "/../","")
# path= "https://raw.githubusercontent.com/AmmarFaiq/GGDH-Dashboard/main/data/"

geo_df= gpd.read_file(path + 'wijk_2023_v0.shp')

geo_df= geo_df.to_crs(epsg=4326)

geo_df.rename(columns ={'WK_CODE':'WKC'}, inplace = True)

geo_df = geo_df.query("GM_NAAM in @values_all_regions")

# geofilepath = requests.get('https://raw.githubusercontent.com/AmmarFaiq/GGDH-Dashboard/main/data/' + 'wijkgeo_file.json')
# geofilepath = requests.get(path + 'wijkgeo_file.json')
# geo_df_fff = json.loads(geofilepath.content)

with open((path + 'wijkgeo_file.json'), "r") as infile:
    geo_df_fff = json.loads(infile.read())



df_numeric = pd.read_csv(path + 'df_numeric_ver_3.csv', sep=',', encoding='latin-1')
df_count = pd.read_csv(path + 'df_count_ver_3.csv', sep=',',encoding= 'latin-1')
df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])

df_demand_CLUSTERED = pd.read_csv(path + 'df_demand_CLUSTERED_3.csv')
df_demand_CLUSTERED_proj = pd.read_csv(path + 'df_demand_CLUSTERED_proj_3.csv')
data_projected_clust_pred = pd.read_csv(path + 'data_projected_clust_pred_3.csv')

# change negative values to 0
cols = data_projected_clust_pred.select_dtypes(include=np.number).columns
data_projected_clust_pred[cols] = data_projected_clust_pred[cols].clip(lower=0)
data_projected_clust_pred['Total_Population'] = data_projected_clust_pred['Total_Population'].astype(int)

# change negative values to 0
cols = df_demand_CLUSTERED_proj.select_dtypes(include=np.number).columns
df_demand_CLUSTERED_proj[cols] = df_demand_CLUSTERED_proj[cols].clip(lower=0)
df_demand_CLUSTERED_proj['Total_Population'] = df_demand_CLUSTERED_proj['Total_Population'].astype(int)

df_demand_CLUSTERED_Year = pd.read_csv(path + 'df_demand_CLUSTERED_Year_3.csv')

df_supply_CLUSTERED = pd.read_csv(path + 'df_supply_CLUSTERED_3.csv')
df_supply_CLUSTERED = df_supply_CLUSTERED.drop(columns=['GMN'])

# order df_demand_CLUSTERED_Year by YEAR
df_demand_CLUSTERED_Year = df_demand_CLUSTERED_Year.sort_values(by=['YEAR','Cluster_Reworked'])

df_demand_CLUSTERED_Year['Cluster_Reworked'] = df_demand_CLUSTERED_Year['Cluster_Reworked'].astype(str)

df_projected = pd.read_csv(path + 'data_projected_3.csv')

#cleaning up temp/dummy dataset
df = df[df.YEAR < 2022]
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

MEDICATION_COLUMN_NAME = ['UniqueMed_Count', '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                     '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10'
                     ]

INCOME_COLUMN_NAME = ['Income_MEAN', '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                      '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user',
                      '%_Low_Income', '%_Debt_Mortgage', #
                     ]

for variable_name in INCOME_COLUMN_NAME:
    df[variable_name] = df[[variable_name]].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)

for cost in COSTS_COLUMN_NAME:
    df[cost] = df[cost].mask(((df['YEAR'] <2009) | (df['YEAR'] >2020)), np.nan)
    
for income in INCOME_COLUMN_NAME:
    df[income] = df[income].mask(((df['YEAR'] <2011) | (df['YEAR'] >2021)), np.nan)

df['%_Wanbet'] = df['%_Wanbet'].mask(((df['YEAR'] <2010) | (df['YEAR'] >2021)), np.nan)
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

df['Total_ZVWKHUISARTS'] = df['ZVWKHUISARTS_MEAN'] * df['Total_Population']

#headers and orig_columns are here to support i18n
# headers = df.columns.to_list().copy()
# columns = [col for col in headers if col not in ['WKC', 'GMN', 'Wijknaam', 'YEAR']]
# orig_columns = columns.copy()
NUMERIC_COLUMN_NAME = ['AGE','Person_in_Household','Income','Moving_Count','Lifeevents_Count','UniqueMed_Count',
                       'ZVWKOSTENTOTAAL','ZVWKFARMACIE','ZVWKHUISARTS','ZVWKHUISARTS_NO_REG','ZVWKZIEKENHUIS','ZVWKFARMACIE','ZVWKOSTENPSYCHO']

CATEGORICAL_COLUMN_NAME = ['Total_Population', 
                           '%_Gender_Vrouwen', '%_0to20', '%_21to40', '%_41to60', '%_61to80', '%_Above80',
                           '%_MajorEthnicity_Native Dutch', '%_MajorEthnicity_Western','%_MajorEthnicity_Non-Western', 
                           '%_MinorEthnicity_Marokko', '%_MinorEthnicity_Suriname', '%_MinorEthnicity_Turkije', '%_MinorEthnicity_Voormalige Nederlandse Antillen en Aruba',
                           '%_Multiperson_Household', '%_HouseholdType_Institutional',
                           '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user',
                           '%_Other_social_benefit_user', '%_Sickness_benefit_user','%_Pension_benefit_user', 
                           '%_Moving_count_above_1','%_Lifeevents_count_above_2', 
                           '%_Low_Income', '%_Debt_Mortgage', '%_Debt_Poor', '%_Wanbet',
                           '%_WMO_user','%_WLZ_user',
                           '%_ZVWKHUISARTS_user', '%_ZVWKFARMACIE_user', '%_ZVWKZIEKENHUIS_user', '%_ZVWKOSTENPSYCHO_user', 
                           '%_HVZ_Medication_user','%_DIAB_Medication_user','%_BLOEDDRUKV_Medication_user', '%_CHOL_Medication_user',
                           '%_UniqueMed_Count_>=5', '%_UniqueMed_Count_>=10', 
                           '%_Hypertensie_patients', '%_COPD_patients', '%_Diabetes_I_patients','%_Diabetes_II_patients', '%_Chronic_Hartfalen_patients', '%_Morbus_Parkinson_patients', '%_Heupfractuur_patients','%_BMIUP45_patients',
                           '%_HGOPL_Low','%_HGOPL_Mid', '%_HGOPL_High'
                           ]



predictors_column = ['Total_Population', '%_HVZ_Medication_user', '%_71to80', '%_Chronic_Hartfalen_patients','%_DIAB_Medication_user', '%_CHOL_Medication_user','%_Unemployment_benefit_user', '%_WMO_user', '%_Debt','UniqueMed_Count', '%_WLZ_user', 'ZVWKHUISARTS']

predicted_column = ['Average GP Care Cost','Total GP Care Cost']

bivariate_column = ['Vulnerable population', 'Average GP Care Cost 2020', 'Ratio Average GP Care Cost 2030 / 2020', 'Cluster Weighted Average GP Care Cost 2020', 'Cluster Weighted Average GP Care Cost 2030 / 2020']

supply_column = ['Supply Cluster', 'Doctors', 'Nurses', 'Practices']
                                                    


layout = html.Div([
            html.Div([
                html.Div(
                    html.Div([html.Button("Region Selection:", id="accordionbutton_sd", className="accordionbutton_open"),
                        html.Div([
                            html.Div([
                                html.Div([
                                    html.Label('Choose a region to plot:', id='choose_area_hadoks'),
                                    dcc.Dropdown(
                                        id = 'drop_wijk_hadoks',
                                        clearable=False, 
                                        searchable=False, 
                                        options=[
                                            {'label': "Hadoks Area", 'value': "Hadoks Area"},
                                            {'label': "'s-gravenhage", 'value': "'s-gravenhage"},
                                            {'label': "Rijswijk", 'value': "Rijswijk"},
                                            {'label': 'Leidschendam-Voorburg', 'value': 'Leidschendam-Voorburg'},
                                            {'label': 'Wassenaar', 'value': 'Wassenaar'},
                                            ],
                                            value="Hadoks Area", 
                                            style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}
                                            )], style={'width': '15%','display': 'inline-block'}),
                                html.Div([
                                    html.Label('Choose a cluster region (2020):', id='choose_cluster_hadoks'),
                                    dcc.Dropdown(
                                        options=["1","2","3","4"],
                                        value=["1","2","3","4"],
                                        id = 'choose_cluster_id_hadoks',
                                        clearable=False,
                                        multi=True,
                                        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
                                        ], style={'width': '15%','display': 'inline-block'}),
                                html.Div([
                                    html.Label('Choose neighbourhoods to plot:', id='choose_wijk_hadoks'),
                                    dcc.Dropdown(
                                        # CATEGORICAL_COLUMN_NAME + NUMERIC_COLUMN_NAME,
                                        # 'Total_Population',
                                        id = 'drop_wijk_spec_id_hadoks',
                                        clearable=True,
                                        searchable=True, 
                                        multi=True,
                                        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'}),
                                        ], style={'width': '70%','display': 'inline-block'})
                                    ])
                        ], id="control_panel_sd", className="accordeon_open")  #title="Region Selection :")
                    ], id="accordionheader", className = 'box')
                ),                
                    
                html.Div([
                    html.Div([
                        html.Div([ 
                            html.Div([
                                html.Div([
                                    html.Label(id='title_map_hadoks', style={'font-size':'medium','padding-bottom': '10%'}), 
                                    html.Br(),
                                    
                                ], style={'width': '70%'}),
                            ], className='row'),

                            html.Div([
                                html.P("Select year of interest", id='select_year_hadoks'),
                                dcc.Slider(step=1, marks = {i:str(i) for i in [(i) for i in range(2012, 2021)]}, min = 2012, max = 2020, value=2020, id = 'slider_select_year_hadoks'),
                                # dcc.Dropdown( id = 'drop_select_year_hadoks', className= "custom_select") #when resolution is small, slider is no longer practical
                            ], style={ 'width': '70%'}, id= 'sliderContainer'),
                            
                            dcc.Graph(id='map_hadoks', style={'position':'relative',  'height':'500px', 'top':'10px'}),
                        ], className='box'),
                        
                        html.Div([
                            html.Label(id='wijk_trend_label_hadoks', style={'font-size': 'medium'}),
                            html.Br(),
                            html.Br(),
                            html.Div([

                                html.Div([
                                    html.Label('Aggregation :', id='choose_agg'),
                                    dbc.RadioItems(
                                        id='agg_type', 
                                        className='radio',
                                        options=[dict(label='Wijk', value=0), dict(label='Cluster', value=1)],
                                        value=1, 
                                        inline=True
                                        )
                                ], style={'width': '30%','display': 'inline-block'}),

                                html.Div([
                                    html.Label(' Choose a projection variable :', id='choose_predictors'),
                                    dcc.Dropdown(
                                        predicted_column,
                                        'Average GP Care Cost',
                                        id = 'drop_var_post_id_hadoks',
                                        clearable=False,
                                        searchable=False, 
                                        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
                                ], style={'width': '30%','display': 'inline-block'}),
                                    
                            ], style={'display':'flex', 'justify-content':'space-between'}),
                            html.Br(),

                            dcc.Graph(id='wijk_trend_fig_hadoks', style={'height':'800px'}),

                        ], className='box', style={'position':'relative'}), 

                        html.Div([
                            html.Label(id='bivariate_cluster_label_hadoks', style={'font-size': 'medium'}),

                            html.Br(),
                            html.Br(),

                            html.Div([

                                html.Div([
                                    html.Label(' Choose a supply variable :', id='choose_supply'),
                                    dcc.Dropdown(
                                        supply_column,
                                        'Supply Cluster',
                                        id = 'supply_var_id',
                                        clearable=False,
                                        searchable=False, 
                                        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
                                ], style={'width': '30%','display': 'inline-block'}),

                                html.Div([
                                    html.Label(' Choose a demand variable :', id='choose_demand'),
                                    dcc.Dropdown(
                                        bivariate_column,
                                        'Vulnerable population',
                                        id = 'demand_var_id',
                                        clearable=False,
                                        searchable=False, 
                                        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
                                ], style={'width': '30%','display': 'inline-block'}),

                                html.Div([
                                    html.Label(' Choose a graph style :', id='choose_bivariate_style_label_hadoks'),
                                    dbc.RadioItems(
                                        id='choose_bivariate_style_hadoks', 
                                        className='radio',
                                        options=[dict(label='Bivariate', value=0), dict(label='Univariate', value=1)],
                                        value=0, 
                                        inline=True)
                                ], style={'width': '30%','display': 'inline-block'}),
                                
                            ], style={'display':'flex', 'justify-content':'space-between'}),

                            html.Br(),
                            html.Br(),
                                
                            dcc.Graph(id='bivariate_fig_hadoks', style={}),

                        ], className='box', style={'position':'relative'}),
                            
                        html.Div([
                            html.Label(id='wijk_trend_label_all_var_hadoks', style={'font-size': 'medium'}),
                                
                            html.Br(),
                            html.Br(),

                            html.Div([
                                    
                                html.Div([
                                    html.Label('Aggregation :', id='choose_agg_all_var'),
                                    dbc.RadioItems(
                                        id='agg_type_all_var', 
                                        className='radio',
                                        options=[dict(label='Wijk', value=0), dict(label='Cluster', value=1)],
                                        value=0, 
                                        inline=True)
                                    ], style={'width': '30%','display': 'inline-block'}),

                                html.Div([
                                    html.Label(' Choose a projection variable :', id='choose_predictors_all'),
                                    dcc.Dropdown(
                                        CATEGORICAL_COLUMN_NAME + NUMERIC_COLUMN_NAME,
                                        'Total_Population',
                                        id = 'drop_all_var_id_hadoks',
                                        clearable=False,
                                        searchable=False, 
                                        style= {'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
                                ], style={'width': '30%','display': 'inline-block'}),
                                    
                            ], style={'display':'flex', 'justify-content':'space-between'}),
                            
                            html.Br(),

                            dcc.Graph(id='wijk_trend_fig_all_var_hadoks', style={'height':'900px'}),

                        ], className='box', style={'position':'relative'})  
                    ]),           
                ], style={'width': '100%', 'box-sizing': 'border-box'}),
            ], style={'display': 'block'}),      
    ], className='main'),
        



#------------------------------------------------------ Callbacks ------------------------------------------------------
#Custom accordeon
@callback(
    Output("control_panel_sd", "className"),
    Output("accordionbutton_sd", "className"),
    [Input("accordionbutton_sd", "n_clicks")],
    [State("control_panel_sd", "className")],
    prevent_initial_call=True
)

def toggle_navbar_collapse(n, classname):
    if classname == "accordeon_open":
        return "accordeon_collapsed", "accordionbutton_closed"
    return "accordeon_open", "accordionbutton_open"




@callback(
    [ 
        Output('drop_wijk_spec_id_hadoks', 'options'),
        Output('drop_wijk_spec_id_hadoks', 'value')
    ],
    [
        Input('drop_wijk_hadoks', 'value'),
        Input('choose_cluster_id_hadoks', 'value')
    ]
)
def update_slider_hadoks(wijk_name,cluster_num):

    if wijk_name == 'Hadoks Area':    
        # add 'Gemeente ' to each values_hadoks in the list
        # 
        hadoks_area_gementee = ["Gemeente 's-Gravenhage", 'Gemeente Wassenaar', 'Gemeente Rijswijk', 'Gemeente Leidschendam-Voorburg']
        dff = df_demand_CLUSTERED_Year.query("GMN in @hadoks_area_gementee")     
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
        
    elif wijk_name == "'s-gravenhage":    

        dff = df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.GMN == "Gemeente 's-Gravenhage"]        
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
        
    elif wijk_name == "Wassenaar":    

        dff = df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.GMN == "Gemeente Wassenaar"]
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
        
    else:
        dff = df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.GMN == ('Gemeente ' + wijk_name)]
        options = list(dff.Wijknaam.unique())
        dff = dff[dff.YEAR == 2020].query("Cluster_Reworked in @cluster_num")
        options2 = list(dff.Wijknaam.unique())
       
    return options, options2


@callback(
    Output('map_hadoks', 'figure'),
    Output('title_map_hadoks', 'children'),
    Input('drop_wijk_hadoks', 'value'),
    Input('drop_wijk_spec_id_hadoks', 'value'),
    Input('slider_select_year_hadoks', 'value')
    )
def update_graph_map_hadoks( 
    wijk_name, 
    wijk_spec,
    cluster_year
                 ):
    
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                  "#7FFCFF",
            "#95FFF5",
            "#ABFFE8",
            "#C2FFE3",
            "#DAFFE6"
                  ]


    title = 'Clustering of Neighbourhoods in ' + wijk_name + ' in ' + str(cluster_year)
        
    dff = df_demand_CLUSTERED_Year.query("Wijknaam in @wijk_spec")
    dff = dff[dff.YEAR == cluster_year]
                     
    dff['Cluster Name'] = dff['Cluster_Reworked'].map({
                                                        '1':'1 - Higher Care Cost - Lower SES - Younger Population - Higher Ethnic Minority', 
                                                       '2':'2 - Higher Care Cost-Higher SES - Older Population - Lower Ethnic Minority', 
                                                       '3':'3 - Lower Care Cost - Lower SES - Younger Population - Higher Minority', 
                                                       '4' :'4 - Lower Care Cost - Higher SES - Older Population - Lower Minority',
                                                       '0':'5 - Mix Care Cost - Mix SES - Mix Population - Mix Minority'
                                                       })


    fig = px.choropleth_mapbox(dff, geojson=geo_df, color="Cluster Name",
                                    locations="WKC", featureidkey="properties.WKC", opacity = 0.4,
                                    center={"lat": 52.1, "lon": 4.24},
                                    mapbox_style="carto-positron", zoom=9.5,hover_name="Wijknaam", 
                                                            #animation_frame="YEAR",
                                    color_discrete_map={
                                                        '1 - Higher Care Cost - Lower SES - Younger Population - Higher Ethnic Minority':'red',
                                                        '2 - Higher Care Cost-Higher SES - Older Population - Lower Ethnic Minority':'firebrick',
                                                        '3 - Lower Care Cost - Lower SES - Younger Population - Higher Minority':'sandybrown',
                                                        '4 - Lower Care Cost - Higher SES - Older Population - Lower Minority':'darkorange',
                                                        '5 - Mix Care Cost - Mix SES - Mix Population - Mix Minority':'orange'}
                                    )
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":50},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title


@callback(
    Output('wijk_trend_label_hadoks', 'children'),
    Output('wijk_trend_fig_hadoks', 'figure'),
    Input('drop_var_post_id_hadoks', 'value'),
    Input('drop_wijk_hadoks', 'value'),
    Input('drop_wijk_spec_id_hadoks', 'value'),
    Input('agg_type', 'value'),
    prevent_initial_call=False)
def update_demand_graph_hadoks(
                 variable_name, 
                 wijk_name, wijk_spec,
                 agg_type
                 
                 ):
    
    
        
    dff1 = df.query("Wijknaam in @wijk_spec")
    dff2 = df_projected.query("Wijknaam in @wijk_spec")

    dff1 = dff1.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')
    dff2 = dff2.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')

    # dff1 = dff1[dff1.YEAR <= 2020]

    dff1_add = dff1[dff1.YEAR==2020][dff2.columns.drop(['Projection_demand','Total cost GP care'])]
    dff1_add.rename(columns={'ZVWKHUISARTS_MEAN':'Projection_demand', 'Total_ZVWKHUISARTS':'Total cost GP care'}, inplace=True)
    # dff2 = dff1_add.append(dff2)
    dff2 = pd.concat([dff1_add, dff2], ignore_index=True)

    # GROUPBY dff1 VALUE PER CLUSTER
    dff1_agg = dff1.groupby(['YEAR', 'Cluster_Reworked']).agg({'ZVWKHUISARTS_MEAN':'mean', 'Total_ZVWKHUISARTS':'mean'}).reset_index()
    dff2_agg = dff2.groupby(['YEAR', 'Cluster_Reworked']).agg({'Projection_demand':'mean', 'Total cost GP care':'mean'}).reset_index()

    wijk_dict = {}
    for i in range(len(dff1['WKC'].unique())):
        wijk_dict[dff1['Wijknaam'].unique()[i]] = i
    
    # colorscale = ["#402580", 
    #               "#38309F", 
    #               "#3C50BF", 
    #               "#4980DF", 
    #               "#56B7FF",
    #               "#6ADDFF",
    #             "#7FFCFF",
    #             "#95FFF5",
    #             "#ABFFE8",
    #             "#C2FFE3",
    #             "#DAFFE6"
    #               ]
    colorscale = ["#03045E", "#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#FF9E00", "#FF9100", "#FF8500", "#FF6D00", "#FF5400"]
    
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if variable_name == 'Average GP Care Cost':

        variable_name_1 = 'ZVWKHUISARTS_MEAN'
        variable_name_2 = 'Projection_demand'
    else:
        variable_name_1 = 'Total_ZVWKHUISARTS'
        variable_name_2 = 'Total cost GP care'

    if agg_type == 0:
        title = 'Projection of Demand in the Neighbourhoods of ' + wijk_name + ' - ' + variable_name 
        color_index = 0
        for wijk in wijk_dict.keys():
            if color_index == len(colorscale):
                color_index = 0
            fig.add_trace(
                go.Scatter(x=dff1[dff1['Wijknaam'] == wijk]['YEAR'], 
                        y=dff1[dff1['Wijknaam'] == wijk][variable_name_1], 
                        mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk),
            )
            fig.add_trace(
                go.Scatter(x=dff2[dff2['Wijknaam'] == wijk]['YEAR'], 
                        y=dff2[dff2['Wijknaam'] == wijk][variable_name_2], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk,
                            showlegend=False),
            )
            color_index += 1
    
                                                        
    else:
        title = 'Projection of Demand in Clusters of ' + wijk_name + ' - ' + variable_name 
        colorscale=['red', 'firebrick','sandybrown', 'darkorange']
        color_index = 0
        for n in range(1,5):
            fig.add_trace(
                    go.Scatter(x=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                            y=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)][variable_name_1], 
                            mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=n, legendgroup=n),
                )
            

            fig.add_trace(
                go.Scatter(x=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                        y=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)][variable_name_2], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=n, legendgroup=n,
                            showlegend=False),
            )
            color_index += 1

    fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                # type="linear"
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
                            pad={"r": 50, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))

    return title, fig


@callback(
    Output('bivariate_fig_hadoks', 'figure'),
    Output('bivariate_cluster_label_hadoks', 'children'),
    Input('drop_wijk_hadoks', 'value'),
    Input('drop_wijk_spec_id_hadoks', 'value'),
    Input('supply_var_id', 'value'),
    Input('demand_var_id', 'value'),
    Input('choose_bivariate_style_hadoks', 'value')
    )
def update_graph_bivariate_map_hadoks( 
    wijk_name, 
    wijk_spec,
    supply_var,
    demand_var,
    bivariate_style
                 ):
    
    # Load conf defaults
    conf = conf_defaults()
    
    colorscale = ["#402580", 
                  "#38309F", 
                  "#3C50BF", 
                  "#4980DF", 
                  "#56B7FF",
                  "#6ADDFF",
                  "#7FFCFF",
            "#95FFF5",
            "#ABFFE8",
            "#C2FFE3",
            "#DAFFE6"
                  ]


    title = 'Figure of {} vs {} - {}'.format( supply_var, demand_var, wijk_name)
        
    dff_demand = df_demand_CLUSTERED.query("Wijknaam in @wijk_spec")

    # demand_var_id
    # supply_var_id

    # merge supply and demand
    df_supply_demand_CLUSTERED_only = dff_demand[dff_demand.YEAR == 2020].merge(df_supply_CLUSTERED, on=['WKC'], how='left')[['WKC','GMN','Wijknaam','ZVWKHUISARTS_MEAN','Cluster_Reworked_Number','cluster_y','Total_Population','Doctors','Nurses','Practices']]
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.merge(df_projected[df_projected.YEAR == 2030][['WKC','Projection_demand','Total_Population']], on=['WKC'], how='left')

    # Supply Cluster values assignment for supply index
    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 2, 2,
                                                            df_supply_demand_CLUSTERED_only['cluster_y'])

    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 3, 0.5, 
                                                            df_supply_demand_CLUSTERED_only['supply_cluster_value'])

    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 1, 0.25,
                                                            df_supply_demand_CLUSTERED_only['supply_cluster_value'])

    df_supply_demand_CLUSTERED_only['supply_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['cluster_y'] == 0, 0.1,
                                                            df_supply_demand_CLUSTERED_only['supply_cluster_value'])

    # Population Cluster values assignment for vulnerable population
    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 1, 2,
                                                            df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'])

    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 2, 1.8,
                                                            df_supply_demand_CLUSTERED_only['population_cluster_value'])

    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 4, 1,
                                                            df_supply_demand_CLUSTERED_only['population_cluster_value'])                                                        

    df_supply_demand_CLUSTERED_only['population_cluster_value'] = np.where(df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number'] == 3, 0.8,
                                                            df_supply_demand_CLUSTERED_only['population_cluster_value'])
    


    df_supply_demand_CLUSTERED_only['population_cluster'] = df_supply_demand_CLUSTERED_only['Cluster_Reworked_Number']
    df_supply_demand_CLUSTERED_only['supply_cluster'] = df_supply_demand_CLUSTERED_only['cluster_y']

    df_supply_demand_CLUSTERED_only['ratio'] = df_supply_demand_CLUSTERED_only['Projection_demand'] / df_supply_demand_CLUSTERED_only['ZVWKHUISARTS_MEAN'] 

    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.rename(columns={'Total_Population_y':'Total_Population_2030'})
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.rename(columns={'Total_Population_x':'Total_Population_2020'})
    df_supply_demand_CLUSTERED_only.fillna(0, inplace=True)
    weighted_avg_2030 = lambda x: sum(x['Total_Population_2030'] * x['Projection_demand']) / sum(x['Total_Population_2030'])
    weighted_avg_2020 = lambda x: sum(x['Total_Population_2020'] * x['ZVWKHUISARTS_MEAN']) / sum(x['Total_Population_2020'])
    weighted_avg_2030_df = df_supply_demand_CLUSTERED_only.groupby('population_cluster').apply(weighted_avg_2030).to_frame('weighted_avg_2030').reset_index()
    weighted_avg_2020_df = df_supply_demand_CLUSTERED_only.groupby('population_cluster').apply(weighted_avg_2020).to_frame('weighted_avg_2020').reset_index()
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.merge(weighted_avg_2030_df, on='population_cluster')
    df_supply_demand_CLUSTERED_only = df_supply_demand_CLUSTERED_only.merge(weighted_avg_2020_df, on='population_cluster')

    df_supply_demand_CLUSTERED_only['weighted_ratio'] = df_supply_demand_CLUSTERED_only['weighted_avg_2030'] / df_supply_demand_CLUSTERED_only['weighted_avg_2020'] 


    match supply_var:

        case 'Supply Cluster':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'supply_cluster_value':'y'})
      
            conf['hover_y_label'] = 'Supply'  # Label to appear on hover
            conf['legend_y_label'] = 'Supply '  # y variable label for the legend
        

        case 'Doctors':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'Doctors':'y'})
      
            conf['hover_y_label'] = 'Doctors'  # Label to appear on hover
            conf['legend_y_label'] = 'Doctors '  # y variable label for the legend

        case 'Nurses':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'Nurses':'y'})
      
            conf['hover_y_label'] = 'Nurses'  # Label to appear on hover
            conf['legend_y_label'] = 'Nurses '  # y variable label for the legend

        case 'Practices':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_only.rename(columns={'Practices':'y'})
      
            conf['hover_y_label'] = 'Practices'  # Label to appear on hover
            conf['legend_y_label'] = 'Practices '  # y variable label for the legend


    match demand_var:

        case 'Vulnerable population':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'population_cluster_value':'x'})
        
            conf['hover_x_label'] = 'Vulnerable population'  # Label to appear on hover
            conf['legend_x_label'] = 'Vulnerable population'  # x variable label for the legend 

        case 'Average GP Care Cost 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'ZVWKHUISARTS_MEAN':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2020'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2020'  # x variable label for the legend 

        case 'Ratio Average GP Care Cost 2030 / 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'ratio':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2030/2020'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2030/2020'  # x variable label for the legend 
            conf['legend_font_size'] = 8  # Legend font size

        case 'Cluster Weighted Average GP Care Cost 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'weighted_avg_2020':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2020 per Cluster'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2020 per Cluster'  # x variable label for the legend
            conf['legend_font_size'] = 7  # Legend font size 

        case 'Cluster Weighted Average GP Care Cost 2030 / 2020':

            df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.rename(columns={'weighted_ratio':'x'})
        
            conf['hover_x_label'] = 'GP Care Cost 2030/2020 per Cluster'  # Label to appear on hover
            conf['legend_x_label'] = 'GP Care Cost 2030/2020 per Cluster'  # x variable label for the legend 
            conf['legend_font_size'] = 6  # Legend font size

    
    

    # Override some variables
    conf['plot_title'] = ''
    conf['width'] = 1100  # Width of the final map container
    conf['ratio'] = 0.5  # Ratio of height to width
    conf['height'] = 350 #conf['width'] * conf['ratio']  # Width of the final map container
    conf['center_lat'] = 52.1  # Latitude of the center of the map
    conf['center_lon'] = 4.24  # Longitude of the center of the map
    conf['map_zoom'] = 9  # Zoom factor of the map
    # Define settings for the legend
    conf['line_width'] = 1  # Width of the rectagles' borders
    

    # if 
    
    med_x = np.median(df_supply_demand_CLUSTERED_bivariate['x'])
    med_y = np.median(df_supply_demand_CLUSTERED_bivariate['y'])

    def my_logic(row):
        if (row["y"] <= med_y) & (row["x"] <= med_x):
            return 'D - Low Supply - Low Demand'
        
        elif (row["y"] <= med_y) & (row["x"] > med_x):
            return 'A - Low Supply - High Demand'
        
        elif (row["y"] > med_y) & (row["x"] <= med_x):
            return 'C - High Supply - Low Demand'
        
        elif (row["y"] > med_y) & (row["x"] > med_x):
            return 'B - High Supply - High Demand'
        else:
            return 'demand = {} - {} + supply = {} - {}'.format(row["x"],med_x,row["y"],med_y)
        
    df_supply_demand_CLUSTERED_bivariate["Supply Demand Cluster"] = df_supply_demand_CLUSTERED_bivariate.apply(my_logic, axis=1)


    if bivariate_style == 0:
        fig = create_bivariate_map(df_supply_demand_CLUSTERED_bivariate[['WKC', 'Wijknaam', 'x', 'y']], color_sets['teal-red'], geo_df_fff, name='Wijknaam', 
                               ids='WKC', conf=conf)
        
    else:
        df_supply_demand_CLUSTERED_bivariate = df_supply_demand_CLUSTERED_bivariate.sort_values(['Supply Demand Cluster'], ascending=[True])
        fig = px.choropleth_mapbox(df_supply_demand_CLUSTERED_bivariate, geojson=geo_df, color="Supply Demand Cluster",
                                        locations="WKC", featureidkey="properties.WKC", opacity = 0.4,
                                        center={"lat": 52.1, "lon": 4.24},
                                        mapbox_style="carto-positron", zoom=9.5, hover_name="Wijknaam", 
                                                                # animation_frame="YEAR", 
                                        color_discrete_map={
                                                            'A - Low Supply - High Demand':'#c85a5a',
                                                            'B - High Supply - High Demand':'#985356',
                                                            'D - Low Supply - Low Demand':'#b0d5df',
                                                            'C - High Supply - Low Demand':'#64acbe'}
        )
    

    

    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=False,
                                  font = {"size": 9, "color":"black"},
                                  margin={"r":0,"t":10,"l":10,"b":10},
                                  paper_bgcolor='white'
                                  )
    
    return fig, title

# 
# 
# 
@callback(
    Output('wijk_trend_label_all_var_hadoks', 'children'),
    Output('wijk_trend_fig_all_var_hadoks', 'figure'),
    Input('drop_all_var_id_hadoks', 'value'),
    Input('drop_wijk_hadoks', 'value'),
    Input('drop_wijk_spec_id_hadoks', 'value'),
    Input('agg_type_all_var', 'value'),
    prevent_initial_call=False)
def update_graph_predictors(
                 variable_name, 
                 wijk_name, wijk_spec,
                 agg_type_all
                 
                 ):
    
    
        
    dff1 = df.query("Wijknaam in @wijk_spec")
    # dff2 = data_projected_clust_pred.query("Wijknaam in @wijk_spec")
    # dff2.drop(columns=['Cluster_Reworked_Number'], inplace=True)

    dff2 = df_demand_CLUSTERED_proj.query("Wijknaam in @wijk_spec")
    # dff2.drop(columns=['Cluster_Reworked'], inplace=True)

    dff1 = dff1.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')
    dff2 = dff2.merge(df_demand_CLUSTERED_Year[df_demand_CLUSTERED_Year.YEAR == 2020][['WKC','Cluster_Reworked']], on=['WKC'], how='left')

    # dff2 = dff2[dff2.columns.drop(['Projection_demand','Total cost GP care'])]
    dff1 = dff1[dff1.YEAR <= 2020]

    dff1_add = dff1[dff1.YEAR==2020]
    # dff2 = dff1_add.append(dff2)
    dff2 = pd.concat([dff1_add, dff2], ignore_index=True)
                         
                         
    if variable_name in NUMERIC_COLUMN_NAME :
        variable_name = variable_name + "_MEAN"
    else:
        variable_name = variable_name
    
   

    wijk_dict = {}
    for i in range(len(dff1['WKC'].unique())):
        wijk_dict[dff1['Wijknaam'].unique()[i]] = i
    
    colorscale = ["#03045E", "#023E8A", "#0077B6", "#0096C7", "#00B4D8", "#FF9E00", "#FF9100", "#FF8500", "#FF6D00", "#FF5400"]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # # GROUPBY dff1 VALUE PER CLUSTER
    dff1_agg = dff1.groupby(['YEAR', 'Cluster_Reworked']).agg({variable_name:'mean'}).reset_index()
    dff2_agg = dff2.groupby(['YEAR', 'Cluster_Reworked']).agg({variable_name:'mean'}).reset_index()

    if agg_type_all == 0:
        title = 'Projection of a Variable in the Neighbourhoods of ' + wijk_name + ' - ' + variable_name 
        color_index = 0
        for wijk in wijk_dict.keys():
            if color_index == len(colorscale):
                color_index = 0
            fig.add_trace(
                go.Scatter(x=dff1[dff1['Wijknaam'] == wijk]['YEAR'], 
                        y=dff1[dff1['Wijknaam'] == wijk][variable_name], 
                        mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk),
            )
            fig.add_trace(
                go.Scatter(x=dff2[dff2['Wijknaam'] == wijk]['YEAR'], 
                        y=dff2[dff2['Wijknaam'] == wijk][variable_name], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=wijk, legendgroup=wijk,
                            showlegend=False),
            )
            color_index += 1
    
                                                        
    else:
        title = 'Projection of a Variable in the Clusters of ' + wijk_name + ' - ' + variable_name 
        colorscale=['red', 'firebrick','sandybrown', 'darkorange']
        color_index = 0
        for n in range(1,5):
            fig.add_trace(
                    go.Scatter(x=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                            y=dff1_agg[dff1_agg['Cluster_Reworked'] == str(n)][variable_name], 
                            mode='lines+markers', line={'dash': 'solid', 'color': colorscale[color_index]}, name=n, legendgroup=n),
                )
            

            fig.add_trace(
                go.Scatter(x=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)]['YEAR'], 
                        y=dff2_agg[dff2_agg['Cluster_Reworked'] == str(n)][variable_name], 
                        mode='lines', line={'dash': 'dash', 'color': colorscale[color_index]}, name=n, legendgroup=n,
                            showlegend=False),
            )
            color_index += 1

    fig.update_layout(
            xaxis=dict(
                rangeslider=dict(
                    visible=True
                ),
                # type="linear"
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
                            pad={"r": 50, "t": -20},
                            showactive=False,
                            x=1,
                            xanchor="right",
                            y=1.1,
                            yanchor="top"
                        ),
                    ]
              ))

    return title, fig
