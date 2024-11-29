# import dash
# from dash import html

# dash.register_page(__name__)

# layout = html.Div([
#     html.H1('Work In Progress')], className='middle')




import dash
from dash import dcc, html, Input, Output, State, callback
import numpy as np
import pandas as pd
import plotly.express as px
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap, to_hex
import os
import util.translate as tr
import dash_bootstrap_components as dbc

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


# values_values_hadoks_gementee = [s + "Gemeente " for s in values_hadoks]

#this way, we can always extend the number of special regions, without having to tamper with the rest of the code
#could even be read in from a file or sth to keep it from being hardcoded.
# special_regions = {"Hadoks' area": values_hadoks}


dash.register_page(__name__)

# path = '../data/'
# path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")
path= "https://raw.githubusercontent.com/AmmarFaiq/GGDH-Dashboard/main/data/"

geo_df= gpd.read_file(path + 'wijk_2023_v0.shp')

geo_df= geo_df.to_crs(epsg=4326)

geo_df.rename(columns ={'WK_CODE':'WKC'}, inplace = True)


values_haaglanden=["'s-Gravenhage",
        "Delft","Leidschendam-Voorburg",
        "Midden-Delfland", 
        "Pijnacker-Nootdorp","Rijswijk",
        "Wassenaar","Westland","Zoetermeer"]



values_ELAN=["'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar",
              "Alphen aan den Rijn", "Hillegom", "Kaag en Braassem", "Katwijk",
              "Leiden","Leiderdorp", "Lisse", "Nieuwkoop","Noordwijk","Oegstgeest",
              "Teylingen", "Voorschoten", "Zoeterwoude", "Delft", "Midden-Delfland",
              "Pijnacker-Nootdorp", "Westland", "Zoetermeer", "Waddinxveen", "Bodegraven-Reeuwijk"
             ]


values_all_regions = values_haaglanden + values_ELAN

values_hadoks= ("'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar")

# 'Delft en omstreken', "'s-gravenhage en omstreken", 'Leiden en omstreken', 'Andere ELAN-Regio', 'Zoetermeer'
# special_regions = {"Hadoks' area": values_hadoks, }

geo_df = geo_df.query("GM_NAAM in @values_all_regions")

# df_numeric = pd.read_csv(path + 'df_numeric_ver_3.csv', sep=',', encoding='latin-1')
# df_count = pd.read_csv(path + 'df_count_ver_3.csv', sep=',',encoding= 'latin-1')
# df = df_count.merge(df_numeric, on=['WKC','Wijknaam','GMN','YEAR'])

df = pd.read_csv(path + 'Opioid_data_summary.csv', sep=',',  dtype={'wc': str, 'gem': str}, encoding='latin-1')
df.loc[df.wc.str.match(r'\b\d{5}\b'), 'wc'] = '0' + df.loc[df.wc.str.match(r'\b\d{5}\b'), 'wc']
df.loc[df.wc.str.match(r'\b\d{6}\b'), 'wc'] = 'WK' + df.loc[df.wc.str.match(r'\b\d{6}\b'), 'wc']

# df = pd.read_csv('C:/Users/fq_am/Pyhton Scripts/GITHUB/New folder/GGDH-Dashboard/data/Opioid data summary.csv', sep=',',  dtype={'wc': str, 'gem': str}, encoding='latin-1')
# df.loc[df.wc.str.match(r'\b\d{5}\b'), 'wc'] = '0' + df.loc[df.wc.str.match(r'\b\d{5}\b'), 'wc']
# df.loc[df.wc.str.match(r'\b\d{6}\b'), 'wc'] = 'WK' + df.loc[df.wc.str.match(r'\b\d{6}\b'), 'wc']

headers = df.columns.to_list().copy()
columns = [col for col in headers if col not in ['wc', 'gem_name', 'gem', 'gem_sector','WKN','YEAR']]


# headers = df.columns.to_list().copy()
columns_count = [col for col in headers if col not in ['wc', 'gem_name', 'gem', 'gem_sector','WKN','YEAR', 'ZVWKHUISARTS',
       'ZVWKFARMACIE', 'ZVWKZIEKENHUIS', 'ZVWKOSTENTOTAAL', 'UniqueMed',
       'UniqueMed_ICPC', 'Latest_BMI', 'AGE', 'INHGESTINKH',
]]

columns_ELAN = ['Total_All_Pop', 'Total_ICPCDiag_Pop', 'Total_ICPCPat_Pop','UniqueMed_ICPC','UniqueMed_ICPC_CAT_1', 'Ext_UniqueMed_ICPC_CAT_1', 'Latest_BMI','Medication_Dependency_ICPC_1', 'Alcohol_Dependency_ICPC_1', 'Loneliness_ICPC_1', 
'Obesitas_ICPC_1','OPIOID_MED_ICPC_1','OPIOID_ICPC_BELOW55_1','OPIOID_ICPC_MULTIPLE_BELOW55_1','NO_DEATH_OPIOID_MULTIPLE_ICPC_1','Laag_inkomen_Medication_Dependency_ICPC_1', 'Laag_inkomen_OPIOID_MED_ICPC_1',
'Laag_inkomen_OPIOID_MULTIPLE_ICPC_1']

columns_CBS = [col for col in columns if col not in columns_ELAN]

columns_CBS_COUNT = ['Gender_Vrouwen', 'AGE_CAT_0to5', 'AGE_CAT_6to10', 'AGE_CAT_11to20',
       'AGE_CAT_21to30', 'AGE_CAT_31to40', 'AGE_CAT_41to50', 'AGE_CAT_51to60',
       'AGE_CAT_61to70', 'AGE_CAT_71to80', 'AGE_CAT_>81','SES_CAT_SES1', 'SES_CAT_SES2', 'SES_CAT_SES3', 'SES_CAT_SES4',
       'SES_CAT_SES5', 'Laag_inkomen_1', 'Wanbet_1', 'UniqueMed_CAT_1', 'Ext_UniqueMed_CAT_1',
       'OPIOID_MED1', 'OPIOID_BELOW55_1',
       'OPIOID_MULTIPLE_BELOW55_1', 
       'NO_DEATH_OPIOID_MULTIPLE_1', 
       'Laag_inkomen_OPIOID_MED_1',
       'Laag_inkomen_OPIOID_MULTIPLE_1']

columns_ELAN_COUNT = [
       'UniqueMed_ICPC_CAT_1', 'Ext_UniqueMed_ICPC_CAT_1','Medication_Dependency_ICPC_1', 'Alcohol_Dependency_ICPC_1',
       'Loneliness_ICPC_1', 'Obesitas_ICPC_1', 
       'OPIOID_MED_ICPC_1', 'OPIOID_ICPC_BELOW55_1', 'OPIOID_ICPC_MULTIPLE_BELOW55_1', 'NO_DEATH_OPIOID_MULTIPLE_ICPC_1',
       'Laag_inkomen_Medication_Dependency_ICPC_1','Laag_inkomen_OPIOID_MED_ICPC_1',
       'Laag_inkomen_OPIOID_MULTIPLE_ICPC_1']



df.loc[(df.WKN.str.contains("Centrum") & df.gem_name.str.contains("Lisse")), columns_count] /= 7
df.loc[(df.WKN.str.contains("Centrum") & df.gem_name.str.contains("Zoetermeer")), columns_count] /= 2.3
df.loc[(df.WKN.str.contains("Centrum") & df.gem_name.str.contains("'s-Gravenhage")), columns_count] /= 2.25

df.loc[(df.WKN.str.contains("Wijk 00") & df.gem_name.str.contains("Leiderdorp")), columns_count] /= 54410/16210
df.loc[(df.WKN.str.contains("Wijk 00") & df.gem_name.str.contains("Nieuwkoop")), columns_count] /= 54410/11955
df.loc[(df.WKN.str.contains("Wijk 00") & df.gem_name.str.contains("Voorschoten")), columns_count] /= 54410/25665

df.loc[(df.WKN.str.contains("Wijk 01") & df.gem_name.str.contains("Leiderdorp")), columns_count] /= 15880/3340
df.loc[(df.WKN.str.contains("Wijk 01") & df.gem_name.str.contains("Rijswijk")), columns_count] /= 15880/4680
df.loc[(df.WKN.str.contains("Wijk 01") & df.gem_name.str.contains("Waddinxveen")), columns_count] /= 15880/8564

df.loc[(df.WKN.str.contains("Wijk 02") & df.gem_name.str.contains("Leiderdorp")), columns_count] /= 30430/8105
df.loc[(df.WKN.str.contains("Wijk 02") & df.gem_name.str.contains("Rijswijk")), columns_count] /= 30430/10480
df.loc[(df.WKN.str.contains("Wijk 02") & df.gem_name.str.contains("Waddinxveen")), columns_count] /= 30430/11845

df.loc[(df.WKN.str.contains("Wijk 04") & df.gem_name.str.contains("Rijswijk")), columns_count] /= 11480/5165
df.loc[(df.WKN.str.contains("Wijk 04") & df.gem_name.str.contains("Waddinxveen")), columns_count] /= 11480/5988

df[columns_count] = df[columns_count].round(0)

for names in columns_CBS_COUNT:
    df[names] = round(df[names] *100 / df['Total_All_Pop'], 2)
for names in columns_ELAN_COUNT:
    df[names] = round(df[names] *100 / df['Total_ICPCPat_Pop'], 2)

layout = html.Div([
    html.Div([

        html.Div([
            html.Label('Choose an area aggregation to show:', id='opioid-choose_group'),
            dcc.RadioItems(
                ['Gementee Group', 'Gementee'],
                'Gementee Group',
                id='opioid-radio-group-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
            html.Label('Choose a region to plot:', id='opioid-choose_area'),
            dcc.Dropdown(
                id='opioid-drop-loc-column', clearable=False
            )
            
        ],
        style={'width': '40%', 'display': 'inline-block'}),

        html.Div([
            # html.Div([html.H2("?", id= 'tooltip-group-id'), 
            # html.Label('Choose a dataset to show:', id='opioid-choose_dataset')], style={'display': 'inline-block'}),
            html.Label('Choose a dataset to show:', id='opioid-choose_dataset'),
            dcc.RadioItems(
                ['CBS', 'ELAN'],
                'CBS',
                id='opioid-radio-data-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            ),
            dbc.Tooltip(
            # "Select dataset to plot; " + "  \n" + " CBS =  National Statistics Data, Medical records taken from Vektis; " + "  \n" + " ELAN : selected primary care data",
            dcc.Markdown('Select dataset to plot;\nCBS =  National Statistics Data and Medical records taken from Vektis;\nELAN : Rountinely registered medical data from volunteered GP', style={'white-space':'pre'}),
            target="opioid-choose_dataset",
            placement= 'top'
            ),

                html.Div([
                html.Label('Choose a main variable to plot (Y-axis):', id='opioid-choose_y'),
                dcc.Dropdown(
                    # columns,
                    # 'OPIOID_MED1',
                    id='drop-opiod-column', clearable=False
                ),
                ], style={'width': '49%', 'display': 'inline-block'}),

                html.Div([
                html.Label('Choose a secondary variable to plot (X-axis):', id='opioid-choose_x'),
                dcc.Dropdown(
                    ['YEAR'] + columns ,
                    'YEAR',
                    id='drop-opiod-column-x', clearable=False
                )
                ], style={'width': '49%', 'display': 'inline-block'})
                

            
        ], style={'width': '58%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'padding': '10px 5px'
    }),
    html.Div(dcc.Slider(
        df['YEAR'].min(),
        df['YEAR'].max(),
        step=None,
        id='opioid-year-slider',
        value=2020,
        marks={str(year): str(year) for year in df['YEAR'].unique()}
    ), style={ 'padding': '20px 20px 20px 20px'}),

    html.Div([
        html.H5(id='opioid-title-map'),
        dcc.Graph(
            id='opioid-map'
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        html.H5(id='opioid-title-scatter'),
        dcc.Graph(
            id='opioid-scatter'
        )
    ], style={'display': 'inline-block', 'width': '49%'}),

    
])



@callback(
    Output('opioid-drop-loc-column', 'options'),
    Output('opioid-drop-loc-column', 'value'),
    Input('opioid-radio-group-type', 'value')

)
def update_select_gem(group_option):
    '''
    Present the neighbourhoods of the selected region to the user
    '''      

    if group_option == 'Gementee Group':
        options = list(df.gem_sector) + ['Alle ELAN Regio']
        labels = list(df.gem_sector) + ['Alle ELAN Regio']
        labels = {options[i]: labels[i] for i in range(len(options))}
        value = 'Leiden en omstreken'
    else:
        options = list(df.gem_name.sort_values())
        labels = list(df.gem_name.sort_values())
        labels = {options[i]: labels[i] for i in range(len(options))}
        value = 'Lisse'
       
    return labels, value

@callback(
    Output('drop-opiod-column', 'options'),
    Output('drop-opiod-column', 'value'),
    Input('opioid-radio-data-type', 'value')

)
def update_select_variables(data_option):
    '''
    Present the neighbourhoods of the selected region to the user
    '''      

    if data_option == 'CBS':
        options = list(columns_CBS)
        labels = list(columns_CBS)
        labels = {options[i]: labels[i] for i in range(len(options))}
        value = 'OPIOID_MED1'
    else:
        options = list(columns_ELAN)
        labels = list(columns_ELAN)
        labels = {options[i]: labels[i] for i in range(len(options))}
        value = 'OPIOID_MED_ICPC_1'
       
    return labels, value

@callback(
    Output('opioid-map', 'figure'),
    Output('opioid-title-map', 'children'),
    Input('opioid-radio-group-type', 'value'),
    Input('opioid-drop-loc-column', 'value'),
    Input('drop-opiod-column', 'value'),
    Input('opioid-year-slider', 'value'))
def update_graph(gem_group, gem_value,
                 variable,
                 year_value):
    
    dff = df[df['YEAR'] == year_value]

    if gem_group == 'Gementee Group':
        if gem_value == 'Alle ELAN Regio':
            dff = dff.copy()
        else:
            dff = dff[dff.gem_sector == gem_value]
    else:
        dff = dff[dff.gem_name == gem_value]

    fig = px.choropleth_mapbox(dff, geojson=geo_df, color=variable,
                            locations="wc", featureidkey="properties.WKC", opacity = 0.5,
                            center={"lat": 52.0705, "lon": 4.3003}, #color_continuous_scale=colorscale_inverted,
                            mapbox_style="carto-positron", zoom=9, hover_name="WKN", custom_data=[variable, 'gem_name']
                            )

    fig.update_traces(hovertemplate='<b>%{customdata[1]} - %{hovertext}</b>' +'<br><b>Waarde</b>:  %{customdata[0]}<br>')  

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    title = '{} - {} - {} '.format(variable, gem_value, year_value)

    return fig, title


@callback(
    Output('opioid-scatter', 'figure'),
    Output('opioid-title-scatter', 'children'),
    Input('opioid-radio-group-type', 'value'),
    Input('opioid-drop-loc-column', 'value'),
    Input('drop-opiod-column', 'value'),
    Input('drop-opiod-column-x', 'value'),
    Input('opioid-year-slider', 'value'))
def update_graph(gem_group, gem_value,
                 variable,
                 variable_x,
                 year_value):

    if gem_group == 'Gementee Group':
        if gem_value == 'Alle ELAN Regio':
            dff = df.copy()
            color_group = 'gem_name'
        else:
            dff = df[df.gem_sector == gem_value]
            color_group = 'gem_name'
    else:
        dff = df[df.gem_name == gem_value]
        color_group = 'WKN'

    if variable_x == 'YEAR':
        fig = px.line(dff, x=variable_x, y=variable, color=color_group,
                 custom_data=[variable, 'gem_name', 'WKN'])
        title = '{} - {} - {} - All Years'.format(variable, variable_x, gem_value)
    else:
        fig = px.line(dff[dff.YEAR == year_value], x=variable_x, y=variable, color=color_group,
                 custom_data=[variable, 'gem_name', 'WKN'])
        title = '{} - {} - {} - {} '.format(variable, variable_x, gem_value, year_value)

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    

    return fig, title


