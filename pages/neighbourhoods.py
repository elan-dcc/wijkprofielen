import dash
from dash import dcc, html, Input, Output, State, callback
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

Delft_region = ('Westland', 'Delft', 'Pijnacker-Nootdorp', 'Midden-Delfland')
Denhaag_region = ('Leidschendam-Voorburg', "'s-Gravenhage", 'Wassenaar', 'Rijswijk')
Leiden_region = ('Alphen aan den Rijn', 'Leiden', 'Hillegom', 'Lisse', 'Noordwijk', 'Oegstgeest', 'Katwijk', 'Kaag en Braassem', 'Nieuwkoop', 'Teylingen', 'Leiderdorp', 'Voorschoten', 'Zoeterwoude')
ELAN_region = ("'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar", 
             "Alphen aan den Rijn", "Hillegom", "Kaag en Braassem", "Katwijk", 
             "Leiden","Leiderdorp", "Lisse", "Nieuwkoop","Noordwijk","Oegstgeest",
             "Teylingen", "Voorschoten", "Zoeterwoude", "Delft", "Midden-Delfland", 
             "Pijnacker-Nootdorp", "Westland", "Zoetermeer", "Waddinxveen", "Bodegraven-Reeuwijk"
             )
Hadoks_region = ("'s-Gravenhage", "Leidschendam-Voorburg", "Rijswijk", "Wassenaar")

values_all_regions = values_haaglanden + values_roaz

# values_values_hadoks_gementee = [s + "Gemeente " for s in values_hadoks]

#this way, we can always extend the number of special regions, without having to tamper with the rest of the code
#could even be read in from a file or sth to keep it from being hardcoded.
special_regions = {"Hadoks' area": Hadoks_region, 'Delft en omstreken':Delft_region, 'Leiden en omstreken':Leiden_region, "'s-gravenhage en omstreken":Denhaag_region, 'ELAN area':ELAN_region}


dash.register_page(__name__, path='/')

path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")

geo_df= gpd.read_file(path + 'wijk_2023_v0.shp')

geo_df= geo_df.to_crs(epsg=4326)

geo_df.rename(columns ={'WK_CODE':'WKC'}, inplace = True)

geo_df = geo_df.query("GM_NAAM in @values_all_regions")

df_numeric = pd.read_csv(path + 'df_numeric_ver_6.csv', sep=',', encoding='latin-1')
df_numeric.rename(columns ={'gem_name':'GMN'}, inplace = True)
# Update the 'WKN' column based on conditions in the 'GMN' column 
df_numeric.loc[(df_numeric['WKN'] == 'Buitengebied') & (df_numeric['GMN'] == 'Lisse'), 'WKN'] = 'Buitengebied Lisse' 
df_numeric.loc[(df_numeric['WKN'] == 'Buitengebied') & (df_numeric['GMN'] == 'Hillegom'), 'WKN'] = 'Buitengebied Hillegom'
df_count = pd.read_csv(path + 'df_count_ver_6.csv', sep=',',encoding= 'latin-1')
df_count.rename(columns ={'Total_All_Pop':'Total_Population'}, inplace = True)
df = df_count.merge(df_numeric, on=['WKC','WKN','GMN','YEAR'])
# df = df_count.copy()
df = df.astype({"YEAR": int})

var_def_dict = {}
with open(path + 'Variables_Definition.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_dict[s[0]] = s[1].split('\n')[0]

var_def_NL_dict = {}
with open(path + 'Variables_Definition_NL.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_NL_dict[s[0]] = s[1].split('\n')[0]

var_def_data_dict = {}
with open(path + 'Variables_Data_Sources.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_data_dict[s[0]] = s[1].split('\n')[0]

var_def_data_NL_dict = {}
with open(path + 'Variables_Data_Sources_NL.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_data_NL_dict[s[0]] = s[1].split('\n')[0]

var_def_label_dict = {}
with open(path + 'Variables_Label_short.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_label_dict[s[0]] = s[1].split('\n')[0]

var_def_label_NL_dict = {}
with open(path + 'Variables_Label_NL_short.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_label_NL_dict[s[0]] = s[1].split('\n')[0]

def method_trans_dict(dict_var, trans_label):
    return [value for value,label in dict_var.items() if label == trans_label]

# change negative values to 0
cols = df.select_dtypes(include=np.number).columns
df[cols] = df[cols].clip(lower=0)

# End clean-up

#headers and orig_columns are here to support i18n
headers = df.columns.to_list().copy()
columns = [col for col in headers if col not in ['WKC', 'GMN', 'WKN', 'YEAR']]
orig_columns = columns.copy()

df[columns] = df[columns].round(4)


# Person_var = ['AGE_MEAN', '%_Gender_Mannen',
#                 '%_Gender_Vrouwen', '%_0to20', '%_21to40', '%_41to60', '%_61to80',
#                 '%_Above80', '%_MajorEthnicity_Native Dutch',
#                 '%_MajorEthnicity_Western', '%_MajorEthnicity_Non-Western',
#                 '%_MinorEthnicity_Marokko', '%_MinorEthnicity_Suriname',
#                 '%_MinorEthnicity_Turkije','%_MinorEthnicity_Voormalige Nederlandse Antillen en Aruba']

Person_var = ['AGE_MEAN', 'Gender_Mannen',
                'Gender_Vrouwen', '0to20', '21to40', '41to60', '61to80',
                'Above80', 'MajorEthnicity_Native Dutch', 'MajorEthnicity_Other']

# Huishouden_var = ['%_Multiperson_Household', '%_HouseholdType_Institutional', '%_Moving_count_above_1', '%_Lifeevents_count_above_2','Moving_Count_MEAN', 'Lifeevents_Count_MEAN']
Huishouden_var = ['Multiperson_Household', 'HouseholdType_Institutional']

# Socioecon_var = ['Income_MEAN', '%_Low_Income', '%_Debt_Mortgage', '%_Debt_Poor', '%_Wanbet', 
#                  '%_Employee', '%_Unemployment_benefit_user', '%_Welfare_benefit_user', '%_Other_social_benefit_user', '%_Sickness_benefit_user', '%_Pension_benefit_user',
#                  '%_WMO_user', '%_WLZ_user']

Socioecon_var = ['Income_MEAN']

Zorgkosten_var = ['ZVWKOSTENTOTAAL_MEAN', 'ZVWKHUISARTS_MEAN', 'ZVWKHUISARTS_NO_REG_MEAN', 'ZVWKZIEKENHUIS_MEAN', 'ZVWKFARMACIE_MEAN', 'ZVWKOSTENPSYCHO_MEAN',
                  'ZVWKHUISARTS_user', 'ZVWKFARMACIE_user', 'ZVWKZIEKENHUIS_user', 'ZVWKOSTENPSYCHO_user']

Medicatie_var = [
                # 'UniqueMed_Count_MEAN', 
                'UniqueMed_Count_5', 'UniqueMed_Count_10',
                'HVZ_Medication_user', 'DIAB_Medication_user', 'BLOEDDRUKV_Medication_user',
                'CHOL_Medication_user', 'DIURETICS_Medication_user', 'DIURETICS_RAAS_BETA_Medication_user', 
                # '%_OPIOID_Medication_user',
                # '%_Opioid_user_no_death', 
                 'Opioid_user_2Years_no_death']

# Eerstelijns_var = ['%_Opioid_user_no_death_primary','%_Opioid_user_2Years_no_death_primary', '%_ICPC_Hartfalen_patients', 
#                 '%_Medication_Dependency_patients', '%_Medication_Dependency_3Years_patients','%_Medication_Dependency_5Years_patients',
#                 '%_Alcohol_Dependency_patients', '%_Alcohol_Dependency_3Years_patients', '%_Alcohol_Dependency_5Years_patients', 
#                 '%_Loneliness_patients', '%_Loneliness_3Years_patients', '%_Loneliness_5Years_patients', 
#                 '%_ICPC_Obesitas_patients', '%_BMI_NormalWeight', '%_BMI_Obese', '%_BMI_OverWeight', '%_BMI_UnderWeight']

# Secundaire_var = ['%_Hypertensie_patients', '%_COPD_patients', 
#                 '%_Diabetes_I_patients', '%_Diabetes_II_patients',
#                 '%_Hartfalen_patients', 
#                 '%_OMA_patients', '%_Morbus_Parkinson_patients',
#                 '%_Heupfractuur_patients', '%_BMIUP45_patients',
#                 '%_Lung_Cancer_patients', '%_Colon_Cancer_patients',
#                 '%_Back_pain_patients']

# Eerstelijns_Secundaire_var = ['%_Opioid_user_no_death_comb', '%_Opioid_user_2Years_no_death_comb', '%_Hartfalen_PrimarynSecondary_patients', 
#                 '%_Primary_care_patients_in_Secondary_care','%_Proxy_Primary_care_refer_to_Secondary_care']

Ander_var = ['JGDHULP_user', 
             # '%_GEDETINEERDENTAB', '%_SHNTAB', 
             'HBOPL_Low', 'HBOPL_Mid', 'HBOPL_High', 
             'HGOPL_Low', 'HGOPL_Mid', 'HGOPL_High',
             'Primary_care_patients_in_Secondary_care', 'Proxy_Primary_care_refer_to_Secondary_care'
            ]

var_dict = {'Person':Person_var,
             'Huishouden':Huishouden_var,
             'Socioecon':Socioecon_var,
             'Zorgkosten':Zorgkosten_var,
             'Medicatie':Medicatie_var,
             # 'Eerstelijns zorg':Eerstelijns_var,
             # 'Secundaire zorg':Secundaire_var,
             # 'Eerstelijns en Secundaire zorg':Eerstelijns_Secundaire_var,
             'Ander':Ander_var
             }
            

drop_var_theme = dcc.Dropdown(
        id = 'drop_var_theme_id',
        clearable=True, 
        searchable=True, 
        multi=True,
        # below could be improved as well eventually, by extracting all regions from the data + the special_regions
        options=[
            {'label': "Person", 'value': "Person"},
            {'label': 'Huishouden', 'value': 'Huishouden'},
            {'label': "Socioecon", 'value': "Socioecon"},
            {'label': 'Zorgkosten', 'value': 'Zorgkosten'},
            {'label': 'Medicatie', 'value': 'Medicatie'},
            # {'label': 'Eerstelijns zorg', 'value': 'Eerstelijns zorg'},
            # {'label': "Secundaire zorg", 'value': "Secundaire zorg"},
            # {'label': "Eerstelijns en Secundaire zorg", 'value': 'Eerstelijns en Secundaire zorg'},
            {'label': 'Ander', 'value': 'Ander'}
            ],
        value=["Person","Huishouden", "Socioecon", "Zorgkosten", "Medicatie", 
               # "Eerstelijns zorg", "Secundaire zorg", "Eerstelijns en Secundaire zorg", 
               "Ander"], 
        className = "custom_select"
    )

drop_var = dcc.Dropdown(
    # make display variable different than value label
        options=[{'label': var_label, 'value': var_value} for var_value, var_label in var_def_label_dict.items()],
        value = 'Total_ICPCPat_Pop',
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
            {'label': 'Leiden', 'value': 'Leiden'},
            {'label': "Lisse", 'value': "Lisse"},
            {'label': 'Leidschendam-Voorburg', 'value': 'Leidschendam-Voorburg'},
            {'label': 'Wassenaar', 'value': 'Wassenaar'},
            {'label': 'Zoetermeer', 'value': 'Zoetermeer'},
            {'label': "'s-gravenhage en omstreken", 'value': "'s-gravenhage en omstreken"},
            {'label': "Leiden en omstreken", 'value': 'Leiden en omstreken'},
            {'label': 'Delft en omstreken', 'value': 'Delft en omstreken'},
            {'label': 'ELAN area', 'value': 'ELAN area'},
            {'label': "Hadoks' area", 'value': "Hadoks' area"}
            ],
        value="ELAN area", 
        className = "custom_select"
    )

layout = html.Div([
            html.Div(
                html.Div([html.Button("Variable, Region and Year Selection :", id="accordionbutton", className="accordionbutton_open"), 
                    html.Div([
                        html.Div([
                        
                            html.Div([html.Div([html.Label('Choose variable theme(s) to choose:', id= 'choose_theme', htmlFor= 'drop_var_theme_id'), drop_var_theme], id= 'select_theme'),
                                      html.Div([html.Label('Choose a variable to plot:', id= 'choose_variable', htmlFor= 'drop_var_id'), drop_var], id= 'select_variable'),
                                      ], id= 'variableContainer'),
                            
                            html.Div([html.Label('Choose a region to plot:', id='choose_area', htmlFor= 'drop_municipality'), drop_municipality], id = 'select_region'),
                            html.Div([html.Label('Choose neighbourhoods to plot:', id= 'choose_wijk', htmlFor= 'drop_municipality_spec_id'),
                                dcc.Dropdown(
                                    columns,
                                    id = 'drop_municipality_spec_id',
                                    clearable=False,
                                    searchable=True, 
                                    multi=True,
                                    className="custom_select"
                                ),
                                html.Div(html.Button('Clear', id="clear_me_button"), className="clear_me")
                            ], id='select_neighbourhoods'),
                            html.Div([
                                html.P("Select a year", id='select_year'),
                                dcc.Slider(step=1, id = 'slider_select_year'),
                                dcc.Dropdown( id = 'drop_select_year', className= "custom_select") #when resolution is small, slider is no longer practical
                            ],  id= 'sliderContainer')
                        ], id= 'select_container'),
                    ], id="control_panel", className="accordeon_open")
                ], id="accordionheader", className = 'box'), id = "dashnav"
            ),
            html.Div([
                        html.H1(id='title_var_def'),
                        html.P('Definition :', id='var_def_expl'), 
                        html.P('Data sources :', id='var_def_data'),
                        html.P(['Broncode : ' , html.A( "Github", href = "https://github.com/elan-dcc/data-loading"), '(Work in Progress)'], id='var_def_code'),
                        html.P(['ELAN Research Ticket code : ' , html.A( "ELAN Ticket", href = "https://www.elanresearch.nl/"), '(Work in Progress)'], id='var_def_ticket'),
                
                    ], className='box'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H1(id='title_map'),
                        html.P('Click on a tile to see the trendline!', id='geospat_expl'), 
                        dcc.Graph(id='map', config={"displayModeBar": False, 'scrollZoom': True})
                    ], className='box'),
                    html.Div([
                        html.H1(id='wijk_trend_label'),
                        html.P('Click the button and legends to know more!', id='linechart_expl'),
                        
                        dcc.Graph(id='wijk_trend_fig', config={"displayModeBar": False}),
                        html.Div(id="line_legend"),
                        dcc.Checklist( id= 'line_menu', className= "line_menu_hidden",
                                       inline=True), html.Button('Show menu', id="line_menu_button") 
                    ], className='box')                        
                ], id= 'leftcell'),    
                html.Div([
                    html.Div([   
                        html.H1(id='title_bar'),           
                        dcc.Graph(id='bar_fig', config={"displayModeBar": False, "scrollZoom": False}), 
                    ], className='box')                    
                ], id= 'rightcell')
            ], id="graphContainer")
        ], id="dataContainer")      

#------------------------------------------------------ Callbacks ------------------------------------------------------
#Custom accordeon
@callback(
    Output("control_panel", "className"),
    Output("accordionbutton", "className"),
    [Input("accordionbutton", "n_clicks")],
    [State("control_panel", "className")],
    prevent_initial_call=True
)

def toggle_navbar_collapse(n, classname):
    if classname == "accordeon_open":
        return "accordeon_collapsed", "accordionbutton_closed"
    return "accordeon_open", "accordionbutton_open"



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
    Output('choose_theme', 'children'),
    Output('choose_variable', 'children'),
    Output('choose_area', 'children'),
    Output('choose_wijk', 'children'),
    Output('select_year', 'children'),
    Output('accordionbutton', 'children'),
    Output('drop_var_id', 'options'),
    Output('drop_var_id', 'value'),
    Input('drop_var_theme_id','value'),
    Input('session', 'data')
)
def localise(themes, language):

    global columns
    linechart_expl = (tr.translate("linechart explanation"))
    geospat_expl = (tr.translate('geospat explanation'))
    choose_theme = (tr.translate('select theme'))
    choose_variable = (tr.translate('select variable'))
    choose_area = (tr.translate('select area'))
    choose_neighborhoud = (tr.translate('select neighbourhood'))
    select_year = (tr.translate('select year'))
    control_panel = (tr.translate('control panel'))

    choosen_columns = ['Total_Population','Total_ICPCPat_Pop']+ sum([var_dict.get(key) for key in themes],[])

    #updating visualisations + dropdown menus
    drop_var = tr.translate_list(choosen_columns)
    # ugly
    drop_var_value = tr.translate('Total_ICPCPat_Pop')
    columns = drop_var
    df.columns = tr.translate_list(headers)
    
    return linechart_expl, geospat_expl, choose_theme, choose_variable, choose_area, choose_neighborhoud, select_year, control_panel, drop_var, drop_var_value


@callback(
    Output('drop_municipality_spec_id', 'options'),
    Output('drop_municipality_spec_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('clear_me_button', 'n_clicks'), # custom clear feature (event trigger)
    Input('session', 'data')
)
def update_select_neighbourhoods(munipality, clear_click, language):
    '''
    Present the neighbourhoods of the selected region to the user
    '''      
    if language == tr.Language.EN.value:
        year = 'YEAR'
    else:
        year = 'Jaar'

    if munipality in special_regions.keys():    
        dff = df.query("GMN in @special_regions[@munipality]")
    else:
        dff = df[(df.GMN == munipality)] #TODO: maybe change to GMcode?

    dff = dff[dff[year] == 2022] #YEAR gets translated by the translate feature to jaar. fixed. 

    # labels = dict(zip(dff.WKC, dff.WKN))
    # options = [*labels]
    labels = dict(zip(set(dff.WKN), set(dff.WKN)))
    options = [*labels]
    
    if (dash.callback_context.triggered_id == "clear_me_button"):
        return labels, []
       
    return labels, options

@callback(
    Output('slider_select_year', 'min'),
    Output('slider_select_year', 'max'),
    Output('slider_select_year', 'marks'),
    Output('slider_select_year', 'value'),
    Output('drop_select_year', 'options'),
    Output('drop_select_year', 'value'),
    Output('title_var_def', 'children'),
    Output('var_def_expl', 'children'),
    Output('var_def_data', 'children'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_select_year', 'value'),
    Input('select_language', 'alt')
)
def update_slider(xaxis_column_name, municipality, drop_value, language):
    '''
    Sets the slider to values corresponding the data of the chosen region.
    The drop_select_year dropdown menu and the drop_value variable were added for responsive web design.
    '''
    #TODO data:would have preferred to use GM_code
    if municipality in special_regions.keys():
         temp_df = df.query("GMN in @special_regions[@municipality]").copy()
    else:
        temp_df = df[df.GMN == municipality].copy()

    title_def = '{}'.format(xaxis_column_name)

    if language == 'en':
        year = 'YEAR'
        variable_name= method_trans_dict(var_def_label_dict, xaxis_column_name)[0]
        var_def = 'Defintion : {}'.format(var_def_dict.get(variable_name))
        var_def_data = 'Data Sources : {}'.format(var_def_data_dict.get(variable_name))
    else:
        year = 'Jaar'
        variable_name = method_trans_dict(var_def_label_NL_dict, xaxis_column_name)[0]
        var_def = 'Definitie : {}'.format(var_def_NL_dict.get(variable_name))
        var_def_data = 'Gegevensbronnen : {}'.format(var_def_data_NL_dict.get(variable_name))
    
    temp_df.dropna(subset=xaxis_column_name, inplace= True)

    min = temp_df[year].min()
    max = temp_df[year].max()
    
    marks = {str(i):str(i) for i in [str(i) for i in range(min, max +1)]}

    value = max

    return min, max, marks, value, list(range(min, max)), value, title_def, var_def, var_def_data


@callback(
    Output('map', 'figure'),
    Output('title_map', 'children'),
    Input('slider_select_year', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value'),
    Input('select_language', 'alt')
    )

def update_graph_map(year_value, xaxis_column_name, wijk_name, wijk_spec, language):
    '''
    Select the appropriate data to display in the map fig
    '''

    if language == 'en':
        year = 'YEAR'
        total_pop = 'Total Population'
        
    else:
        year = 'Jaar'
        total_pop = 'Totale bevolking'
        
    dff = df[df[year] == year_value]

    title = '{} - {} - {}'.format(xaxis_column_name, wijk_name, year_value)

    dff = dff.query("WKN in @wijk_spec")
    # dff = dff.drop_duplicates(subset='WKN', keep="last")
    # dff = dff.dropna(subset=[xaxis_column_name])

    fig = px.choropleth_mapbox(dff, geojson=geo_df, color=xaxis_column_name,
                            locations="WKC", featureidkey="properties.WKC", opacity = 0.5,
                            center={"lat": 52.0705, "lon": 4.3003}, color_continuous_scale=colorscale_inverted,
                            mapbox_style="carto-positron", zoom=10, hover_name="WKN",
                            custom_data=['GMN', xaxis_column_name,total_pop])
    
    fig.update_traces(hovertemplate='<b><b>Wijk</b>: %{hovertext}</b>'+ '<br><b><b>Gemeente</b>: %{customdata[0]}</b><br>' +'<br><b>Waarde</b>: %{customdata[1]}<br>' +'<b>Bevolking</b>: %{customdata[2]}')  

    
    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)', lakecolor='#4E5D6C'),
                                autosize=True,
                                font = {"size": 12, "color":"black"},
                                margin={"r":0,"t":10,"l":10,"b":50},
                                paper_bgcolor='white',
                                showlegend=True
                            )
    # get value with keys 
    
    
    return fig, title

# create a new column that put each row into a group of 4 numbers based on the value of a column quartile

@callback(
    Output('title_bar', 'children'),
    Output('bar_fig', 'figure'),
    Input('slider_select_year', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value'),
    Input('select_language', 'alt')
    )

def update_graph_bar(year_value, xaxis_column_name, wijk_name, wijk_spec, language):
    '''
    Update the bar chart based on new values
    '''

    if language == 'en':
        year = 'YEAR'
        variable = method_trans_dict(var_def_label_dict, xaxis_column_name)[0]
    else:
        year = 'Jaar'
        variable = method_trans_dict(var_def_label_NL_dict, xaxis_column_name)[0]

    dff = df[df[year] == year_value]
    
    if len(wijk_spec) == 0:
        fig = px.bar(x=[0, 10],
                y=[0, 0]
                )
        fig.update_xaxes(showticklabels=False)
        fig.update_yaxes(showticklabels=False)
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )        
        
        return ["No neighbourhood selected"], fig    
    else:
        dff = dff.query("WKN in @wijk_spec")
        dff = dff.sort_values(by=[xaxis_column_name], ascending=False).reset_index()
        dff = dff.drop_duplicates(subset='WKN', keep="last")
        dff = dff.dropna(subset=[xaxis_column_name])
        
        fig = px.bar(dff, xaxis_column_name, 'WKN', color= xaxis_column_name,
                hover_name='WKN', color_continuous_scale=colorscale_inverted,
                height= max(500, 30 * dff.shape[0]), text='WKN', custom_data=['GMN'])

    title = '{} - {} - {}'.format((xaxis_column_name), wijk_name, year_value,variable)   
    #title = tr.translate("Bargraph title")
    # fig.update_yaxes(title=xaxis_column_name)
    # fig.update_xaxes(title=wijk_name)
    fig.update_layout(geo= {'bgcolor': 'red'},
                      autosize= True,
                      font = {"size": style["fontsize"], "color": style["color"]},
                      paper_bgcolor='white', 
                      yaxis={'categoryorder':'total ascending'},
                      xaxis_title=None,
                      yaxis_title=None,
                      hovermode='closest',
                      plot_bgcolor='rgba(0, 0, 0, 0)',
                      margin=dict(l=0, r=0, t=20, b=20),
                    #   showlegend=False
                      )
    
    fig.update_coloraxes(showscale=False)
       
    fig.update_traces(width= 0.8,
        hovertemplate='<b>%{hovertext}</b>'+ '<br><b>%{customdata[0]}</b><br>' +'<br><b>Value</b>: %{x}<br>'
    )  
    fig.update_yaxes(showticklabels=False)
    fig.update_xaxes(gridcolor='rgba(0,126,255,.24)')

    return [title], fig

selected_wijken = set()

@callback(
    Output('line_menu', 'options'),
    Output('line_menu', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value'),
    Input('map', 'clickData'),
    Input('select_language', 'alt')

)
def update_line_menu(select_munic, select_wijken, map_values,language):
    '''
    Custom legend/menu for line chart
    '''
    global selected_wijken

    if language == 'en':
        year = 'YEAR'
        
    else:
        year = 'Jaar'

    #when user selects a new region
    if (dash.callback_context.triggered_id == "drop_municipality"):
        selected_wijken = set()
    elif map_values is not None:
        map_values = map_values['points'][0]['hovertext']
        if map_values not in selected_wijken:
            selected_wijken.add(map_values)
        else:
            selected_wijken.remove(map_values)

    dff = df[df.WKN.isin(select_wijken) & (df[year] == 2022)]     
    # select_wijken = df[df.WKC.isin(select_wijken) & (df[year] == 2022)].set_index("WKC").to_dict()["WKN"]
    select_wijken = dict(zip(dff.WKN, dff.WKN )) 
    
    #select_wijken = {df[df.WKC == select_wijken[i]].WKN: select_wijken[i] for i in range(len(select_wijken))} 
    return select_wijken, [*selected_wijken]

@callback(
    Output('line_menu', 'className'),
    Output('line_menu_button', 'children'),
    Input('line_menu_button', 'n_clicks'),
    State('line_menu', 'className'),
    prevent_initial_call=True
    )
def change_button_style(n_clicks, buttonClass):
    # will only get triggered if button is pressed
    if buttonClass == "line_menu_visible":
        return "line_menu_hidden", "Show menu"
    else:
        return "line_menu_visible", "Hide menu"

@callback(
    Output('wijk_trend_label', 'children'),
    Output('wijk_trend_fig', 'figure'),
    Output('line_legend', 'children'),
    Input('map', 'clickData'),
    Input('line_menu', 'value'),
    Input('drop_var_id', 'value'),
    Input('drop_municipality', 'value'),
    Input('drop_municipality_spec_id', 'value'),
    Input('select_language', 'alt'),
    prevent_initial_call=False
    )
#TODO: CLEANUP
#TODO: use WKC instead of Wijknaam. What if you're plotting neighbourhoods
# with the same new from different cities?
def update_graph(mapData, menu_data,
                 xaxis_column_name, area, wijk_spec, language):
    '''
    Update line graph 
    '''
                     
    dff = df.query("WKN in @wijk_spec")
                     
    global selected_wijken
    if language == 'en':
        year = 'YEAR'
        variable = method_trans_dict(var_def_label_dict, xaxis_column_name)[0]
        no_wijk_label = "No neighbourhood selected"
        dff = dff.drop_duplicates(subset=['WKN','YEAR'], keep="last")
    else:
        year = 'Jaar'
        variable = method_trans_dict(var_def_label_NL_dict, xaxis_column_name)[0]
        no_wijk_label = "Geen buurt geselecteerd"
        dff = dff.drop_duplicates(subset=['WKN','Jaar'], keep="last")

    

    # x_trendline = dff[dff[xaxis_column_name].notnull()][year].tolist()
    # y_trendline = dff[dff[xaxis_column_name].notnull()][xaxis_column_name].tolist()

    # z_trendline = np.polyfit(x_trendline, y_trendline, 1)
    # p_trendline = np.poly1d(z_trendline)

    if len(selected_wijken) == 0 and (dash.callback_context.triggered_id != "line_menu"):
        fig = px.line(x=[0, 10], y=[0, 0])
        # fig = px.line(x=list(set(x_trendline)), y=p_trendline(list(set(x_trendline))).round(4)).update_traces(mode='lines+markers')#, patch={"line": {"dash": "longdash"}}
        # fig.add_trace(go.Scatter(x=x_trendline, y=p_trendline(x_trendline), mode='markers'))#, dash = "dot"

        fig.update_xaxes(showticklabels=False, visible=False)
        fig.update_yaxes(showticklabels=False, visible=False)
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )        
        selected_wijken = set()
        #TODO: change the class to hide the graph + make the "Show menu button" loud
        return no_wijk_label, fig, []    
    
    
    # dff = dff.drop_duplicates(subset=['WKN','YEAR'], keep="last")
    
    fig = px.line(dff, x=year, y= xaxis_column_name, color='WKC', custom_data=['WKN'],
                  color_discrete_sequence=px.colors.qualitative.Alphabet
                #   height= max(150, 30 * dff.shape[0]),
                  )
    
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b>' +'<br><b>Jaar</b>: %{x|%Y}<br><b>Waarde:</b> %{y}', name="")

    fig.update_layout(
        showlegend = False,
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        xaxis={"rangeslider":{"visible": True}, "type": "date"},
        font = {"size": style["fontsize"], "color": style["color"]},
        margin=dict(l=0, r=0, t=20, b=20)
    )
  
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='white',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='white',
        gridcolor='lightgrey'
    )

  
    if mapData is None: #change chart based on selection from the select
        title = '{}'.format(var_def_label_dict.get(xaxis_column_name)) # TODO
        
        fig.update_traces(visible="legendonly")

        selected_wijken = set()

    elif mapData is not None: #User can click on neighbourhoods in the map to affect the linechart.
        clicked_name = mapData['points'][0]['hovertext']
        title = '{} - {}'.format(var_def_label_dict.get(xaxis_column_name), clicked_name) #TODO
        
        #note that in this specific case, selected_wijken is already being 
        # updated in the line_menu function
    

    if (dash.callback_context.triggered_id == "line_menu"):
        menu_data = set(menu_data)
        difference = selected_wijken.difference(menu_data)
        if difference:
            selected_wijken -= difference
        else:
            selected_wijken.update(menu_data)
        
    #This is performed every time now.
    for wijk in fig.data:
        if set(dff[(dff.WKC == wijk.legendgroup) & (dff[year] == 2022)].WKN.unique()).issubset(selected_wijken):
        # if (wijk.legendgroup) in (selected_wijken):
            wijk.visible= True
            
        else:
            wijk.visible= False
        
        

    # title= '{} - {} - {} '.format(wijk.legendgroup, type(selected_wijken), wijk)
   #SO UGLY
    if len(selected_wijken) == 0:
        fig = px.line(x=[0, 10], y=[0, 0])
        fig.update_xaxes(showticklabels=False, visible=False)
        fig.update_yaxes(showticklabels=False, visible=False)
        fig.update_layout(
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)'
        )        
    
    #use to make custom (non-interactive) legend
    legend = []
    
    look_up = dff[dff.WKN.isin(selected_wijken) & (dff[year] == 2022)].set_index("WKC").to_dict()["WKN"]
    
    title= '{} - {}'.format(xaxis_column_name, area)# list(look_up.values())

    for wijk in fig.data:
        if wijk.visible:
            legend.append(html.Div([html.Div(className="legendcolor", style={'background-color': wijk.line.color}),look_up[wijk.legendgroup]], className="legenditem"))
                                    
    return title, fig, legend
