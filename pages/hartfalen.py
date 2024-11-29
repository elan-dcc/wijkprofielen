# import dash
# from dash import html

# dash.register_page(__name__)

# layout = html.Div([
#     html.H1('Work In Progress hartfalen')], className='middle')

import dash
import pandas as pd
from dash import Dash, html, dcc, Input, Output, State, callback, Patch
import dash_bootstrap_components as dbc
import plotly.express as px
# import dash_ag_grid as dag
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__)

path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")
DT_PRI_CVD = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_CVD')
DT_PRI_Gender = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender')
DT_PRI_Age = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Age')
DT_PRI_Ethnicity = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Ethnicity')
DT_PRI_SES = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_SES')
DT_PRI_Gender_Age = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age')
DT_PRI_Gender_Age_Ethnicity = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age_Ethnicity')
DT_PRI_Gender_Age_SES = pd.read_excel(open(path + ('Primary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age_SES')

DT_SEC_CVD = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_CVD')
DT_SEC_Gender = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender')
DT_SEC_Age = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Age')
DT_SEC_Ethnicity = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Ethnicity')
DT_SEC_SES = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_SES')
DT_SEC_Gender_Age = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age')
DT_SEC_Gender_Age_Ethnicity = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age_Ethnicity')
DT_SEC_Gender_Age_SES = pd.read_excel(open(path + ('Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age_SES')

DT_COMB_CVD = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_CVD')
DT_COMB_Gender = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender')
DT_COMB_Age = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Age')
DT_COMB_Ethnicity = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Ethnicity')
DT_COMB_SES = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_SES')
DT_COMB_Gender_Age = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age')
DT_COMB_Gender_Age_Ethnicity = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age_Ethnicity')
DT_COMB_Gender_Age_SES = pd.read_excel(open(path + ('Primary_and_Secondary_Care_Data_version_1.xlsx'), 'rb'), sheet_name='DT_Gender_Age_SES')

drop_data = html.Div(
    [
        dbc.Label("Select dataset"),
        dcc.Dropdown(
            id = 'data_id_hartfalen',
            clearable=False, 
            searchable=False, 
            # below could be improved as well eventually, by extracting all regions from the data + the special_regions
            options=[
                {'label': "ELAN-Huisarts", 'value': "ELAN-Huisarts"},
                {'label': 'ELAN-Ziekenhuis', 'value': 'ELAN-Ziekenhuis'},
                {'label': "ELAN-Huisarts-Ziekenhuis", 'value': "ELAN-Huisarts-Ziekenhuis"}
                ],
            value="ELAN-Huisarts", 
            className = "custom_select"
        )
    ],  className="mb-4",
)


year_dropdown = html.Div(
    [
        dbc.Label("Select year"),
        dcc.Dropdown(id = 'drop_select_year_hartfalen', clearable=False, searchable=False, className= "custom_select"),
    ],  className="mb-4",
)

drop_area = html.Div(
    [
        dbc.Label("Select area"),
        dcc.Dropdown(
            id = 'area_id_hartfalen',
            clearable=False, 
            searchable=False, 
            # below could be improved as well eventually, by extracting all regions from the data + the special_regions
            options=[
                {'label': "'s-gravenhage en omstreken", 'value': "'s-gravenhage en omstreken"},
                {'label': "Leiden en omstreken", 'value': 'Leiden en omstreken'},
                # {'label': 'Delft en omstreken', 'value': 'Delft en omstreken'},
                {'label': 'Zoetermeer', 'value': 'Zoetermeer'}
                ],
            value="Leiden en omstreken", 
            className = "custom_select"
        )
    ],  className="mb-4",
)


ELANH_card = dcc.Markdown(
    """
    ELAN-H (Huisartsen) is een uniek huisartsen-netwerk met (op dit moment) meer dan 140 
    deelnemende huisartsen en data van meer dan 800.000 patiënten in de ELAN-huisartsendata. 
    Via ELAN-H zijn inmiddels tientallen onderzoeken verricht en we hopen dat in de komende jaren voort 
    te kunnen zetten.
    """)

ELAN_GGDH_card = dcc.Markdown(
    """
    Gezond en Gelukkig Den Haag (GGDH) wordt door de afdeling PHEG op de LUMC-Campus Den Haag
    en het LUMC ondersteund met de data-infrastructuur van ELAN-GGDH. In ELAN-GGDH delen niet
    alleen huisartsen, maar ook de ziekenhuizen, de gemeente en in de toekomst ook andere
    zorgverleners gepseudonimiseerde gegevens met het CBS als “trusted third party”. Dankzij het CBS
    kunnen deze gepseudonimiseerde gegevens nog verder worden verrijkt met gegevens die het CBS al
    onder haar hoede heeft, zoals huishoudsamenstelling en inkomen.
    """
    #     [Data source](https://paygap.ie/)
    # [Data source GitHub](https://github.com/zenbuffy/irishGenderPayGap/tree/main)
    # [Plotly Community Forum](https://community.plotly.com/t/figure-friday-2024-week-32/86401)
)

ELAN_GGDH_H_card = dcc.Markdown(
    """
    ELAN-H (Huisartsen) is een uniek huisartsen-netwerk met (op dit moment) meer dan 140 
    deelnemende huisartsen en data van meer dan 800.000 patiënten in de ELAN-huisartsendata. 
    Via ELAN-H zijn inmiddels tientallen onderzoeken verricht en we hopen dat in de komende jaren voort 
    te kunnen zetten.

    Gezond en Gelukkig Den Haag (GGDH) wordt door de afdeling PHEG op de LUMC-Campus Den Haag
    en het LUMC ondersteund met de data-infrastructuur van ELAN-GGDH. In ELAN-GGDH delen niet
    alleen huisartsen, maar ook de ziekenhuizen, de gemeente en in de toekomst ook andere
    zorgverleners gepseudonimiseerde gegevens met het CBS als “trusted third party”. Dankzij het CBS
    kunnen deze gepseudonimiseerde gegevens nog verder worden verrijkt met gegevens die het CBS al
    onder haar hoede heeft, zoals huishoudsamenstelling en inkomen.
    """
        # [Data source](https://paygap.ie/)
    # [Data source GitHub](https://github.com/zenbuffy/irishGenderPayGap/tree/main)
    # [Plotly Community Forum](https://community.plotly.com/t/figure-friday-2024-week-32/86401)
)


info = dbc.Accordion([
    dbc.AccordionItem(id="accordion-info"),
    # dbc.AccordionItem(data_card, title="Data Source")
],  start_collapsed=False)

# 

control_panel = dbc.Card(
    dbc.CardBody(
        dbc.Row(
    [
        dbc.Col(dbc.Row([drop_data,year_dropdown, drop_area]), md=4),
        # dbc.Col(),
        dbc.Col(info, md=8),
    ]
),
        className="bg-light",
    ),
    className="mb-4"
)



layout = dbc.Container(
    [
        dcc.Store(id="data-cvd", data={}),
        dcc.Store(id="data-gender", data={}),
        dcc.Store(id="data-age", data={}),
        dcc.Store(id="data-eth", data={}),
        dcc.Store(id="data-ses", data={}),
        dcc.Store(id="data-gender-age", data={}),
        dcc.Store(id="data-gender-age-eth", data={}),
        dcc.Store(id="data-gender-age-ses", data={}),
            html.Div([html.Button("Variable, Region and Year Selection :", id="accordionbutton_hartfalen", className="accordionbutton_open"), 
            html.Div([
            control_panel#, info 
            ], id="control_panel_hartfalen", className="accordeon_open")
            ],id="accordionheader", className='box'),
            html.Div(
                [
                    # dcc.Markdown(id="title"),
                    html.Div([
                        dbc.Row([dbc.Col(html.Div(id="stat_info-card"))]),#, dbc.Col( html.Div(id="bonusgap-card"))
                    ]),
                ],  className='box'
            ),
        html.Div([
            dcc.Tabs(id='graph-tabs', value='overview', children=[
                    dcc.Tab(label='Overview', value='overview'),
                    dcc.Tab(label='Level 2', value='gender_age_content'),
                    dcc.Tab(label='Level 3 ETH', value='gender_age_eth_content'),
                    dcc.Tab(label='Level 3 SES', value='gender_age_ses_content'),

                ], style={'marginTop': '15px', 'width':'600px','height':'50px'}),
            dcc.Loading([
                    html.Div(id='tabs-content')
                ],type='default',color='#deb522'),

            # html.Div(id="bar-chart-card", className="mt-4")

        ], className='box'),
        
        
        
    ],
    fluid=True,
)

#------------------------------------------------------ Callbacks ------------------------------------------------------

#Custom accordeon
@callback(
    Output("control_panel_hartfalen", "className"),
    Output("accordionbutton_hartfalen", "className"),
    [Input("accordionbutton_hartfalen", "n_clicks")],
    [State("control_panel_hartfalen", "className")],
    prevent_initial_call=True
)

def toggle_navbar_collapse(n, classname):
    if classname == "accordeon_open":
        return "accordeon_collapsed", "accordionbutton_closed"
    return "accordeon_open", "accordionbutton_open"

@callback(
    Output("data-cvd", "data"),
    Output("data-gender", "data"),
    Output("data-age", "data"),
    Output("data-eth", "data"),
    Output("data-ses", "data"),
    Output("data-gender-age", "data"),
    Output("data-gender-age-eth", "data"),
    Output("data-gender-age-ses", "data"),
    Input('drop_select_year_hartfalen', 'value'),
    Input('data_id_hartfalen', 'value'),
    Input('area_id_hartfalen', 'value')
)
def pin_selected_report(year, data_elan, area):
    if data_elan == 'ELAN-Huisarts':
         records_cvd = DT_PRI_CVD[(DT_PRI_CVD.YEAR == year) & (DT_PRI_CVD.gem_sector == area)].to_dict("records")
         records_gender = DT_PRI_Gender[(DT_PRI_Gender.YEAR == year) & (DT_PRI_Gender.gem_sector == area)].to_dict("records")
         records_age = DT_PRI_Age[(DT_PRI_Age.YEAR == year) & (DT_PRI_Age.gem_sector == area)].to_dict("records")
         records_eth = DT_PRI_Ethnicity[(DT_PRI_Ethnicity.YEAR == year) & (DT_PRI_Ethnicity.gem_sector == area)].to_dict("records")
         records_ses = DT_PRI_SES[(DT_PRI_SES.YEAR == year) & (DT_PRI_SES.gem_sector == area)].to_dict("records")
         records_gender_age = DT_PRI_Gender_Age[(DT_PRI_Gender_Age.YEAR == year) & (DT_PRI_Gender_Age.gem_sector == area)].to_dict("records")
         records_gender_age_eth = DT_PRI_Gender_Age_Ethnicity[(DT_PRI_Gender_Age_Ethnicity.YEAR == year) & (DT_PRI_Gender_Age_Ethnicity.gem_sector == area)].to_dict("records")
         records_gender_age_ses = DT_PRI_Gender_Age_SES[(DT_PRI_Gender_Age_SES.YEAR == year) & (DT_PRI_Gender_Age_SES.gem_sector == area)].to_dict("records")

    elif data_elan == 'ELAN-Ziekenhuis':
         records_cvd = DT_SEC_CVD[(DT_SEC_CVD.YEAR == year) & (DT_SEC_CVD.gem_sector == area)].to_dict("records")
         records_gender = DT_SEC_Gender[(DT_SEC_Gender.YEAR == year) & (DT_SEC_Gender.gem_sector == area)].to_dict("records")
         records_age = DT_SEC_Age[(DT_SEC_Age.YEAR == year) & (DT_SEC_Age.gem_sector == area)].to_dict("records")
         records_eth = DT_SEC_Ethnicity[(DT_SEC_Ethnicity.YEAR == year) & (DT_SEC_Ethnicity.gem_sector == area)].to_dict("records")
         records_ses = DT_SEC_SES[(DT_SEC_SES.YEAR == year) & (DT_SEC_SES.gem_sector == area)].to_dict("records")
         records_gender_age = DT_SEC_Gender_Age[(DT_SEC_Gender_Age.YEAR == year) & (DT_SEC_Gender_Age.gem_sector == area)].to_dict("records")
         records_gender_age_eth = DT_SEC_Gender_Age_Ethnicity[(DT_SEC_Gender_Age_Ethnicity.YEAR == year) & (DT_SEC_Gender_Age_Ethnicity.gem_sector == area)].to_dict("records")
         records_gender_age_ses = DT_SEC_Gender_Age_SES[(DT_SEC_Gender_Age_SES.YEAR == year) & (DT_SEC_Gender_Age_SES.gem_sector == area)].to_dict("records")

    else:
         records_cvd = DT_COMB_CVD[(DT_COMB_CVD.YEAR == year) & (DT_COMB_CVD.gem_sector == area)].to_dict("records")
         records_gender = DT_COMB_Gender[(DT_COMB_Gender.YEAR == year) & (DT_COMB_Gender.gem_sector == area)].to_dict("records")
         records_age = DT_COMB_Age[(DT_COMB_Age.YEAR == year) & (DT_COMB_Age.gem_sector == area)].to_dict("records")
         records_eth = DT_COMB_Ethnicity[(DT_COMB_Ethnicity.YEAR == year) & (DT_COMB_Ethnicity.gem_sector == area)].to_dict("records")
         records_ses = DT_COMB_SES[(DT_COMB_SES.YEAR == year) & (DT_COMB_SES.gem_sector == area)].to_dict("records")
         records_gender_age = DT_COMB_Gender_Age[(DT_COMB_Gender_Age.YEAR == year) & (DT_COMB_Gender_Age.gem_sector == area)].to_dict("records")
         records_gender_age_eth = DT_COMB_Gender_Age_Ethnicity[(DT_COMB_Gender_Age_Ethnicity.YEAR == year) & (DT_COMB_Gender_Age_Ethnicity.gem_sector == area)].to_dict("records")
         records_gender_age_ses = DT_COMB_Gender_Age_SES[(DT_COMB_Gender_Age_SES.YEAR == year) & (DT_COMB_Gender_Age_SES.gem_sector == area)].to_dict("records")

    return records_cvd, records_gender, records_age, records_eth, records_ses, records_gender_age, records_gender_age_eth, records_gender_age_ses


@callback(
    Output('drop_select_year_hartfalen', 'options'),
    Output('drop_select_year_hartfalen', 'value'),
    Output('accordion-info', 'children'),
    Output('accordion-info', 'title'),
    # Output("title", "children"),
    Input('data_id_hartfalen', 'value'),
    Input('area_id_hartfalen', 'value')
    # Input('select_language', 'alt')
)
def update_slider(data_elan, area ):

    if data_elan == 'ELAN-Huisarts':
         year_options = list(range(2010, 2023))
         year_value = 2020
         info = ELANH_card
         info_title="About ELAN-Huisarts Data" 
    elif data_elan == 'ELAN-Ziekenhuis':
         year_options = list(range(2010, 2021))
         year_value = 2020
         info = ELAN_GGDH_card
         info_title="About ELAN-Ziekenhuis Data"
    else:
         year_options = list(range(2010, 2021))
         year_value = 2020
         info = ELAN_GGDH_H_card
         info_title="About ELAN-GGDH-H Data"

    

    return year_options, year_value, info, info_title#, stat_title

@callback(
    Output('tabs-content', 'children'),
    Input('graph-tabs', 'value'),
    Input("data-gender", "data"),
    Input("data-age", "data"),
    Input("data-eth", "data"),
    Input("data-ses", "data"),
    Input("data-gender-age", "data"),
    Input("data-gender-age-eth", "data"),
    Input("data-gender-age-ses", "data")
)
def update_tab(tab, data_gender, data_age, data_eth, data_ses, data_gender_age, data_gender_age_eth, data_gender_age_ses):
    

    colorscale_bar = [# SES5, SES4, SES3 / Other, SES2 / Suriname, SES1 / Dutch, Age above 70, Age 50to70, Age 30to50, Age below30, gender Mannen, gender Vrouwen
                        "#38309F", "#3C50BF","#4980DF","#56B7FF","#6ADDFF","#18362E","#007649", "#4C9F87", "#D4E8E2", "#99d98c", "#d9ed92"
                    ]
                    
    fig_bar = make_subplots(2, 2, specs=[[{"type": "bar"}, {"type": "bar"}],
                                    [ {"type": "bar"}, {"type": "bar"}]
                                    ],
        subplot_titles=('Gender', "Age", 'Ethnicity', 'SES'))

    dff = pd.DataFrame(data_gender)
    dff['sum'] = dff.groupby(['gem_sector', 'YEAR'])['Total_CVD_Patient_Level'].transform(lambda g: g.sum())
    dff['value_percent'] = dff['Total_CVD_Patient_Level'] * 100/ dff['sum']

    # fig_1 = px.bar(DT_DEMOGRAPH_GENDER[DT_DEMOGRAPH_GENDER.YEAR == 2020], x="gem_sector", y="value_percent", color="Gender")
    fig_1 = go.Figure(data=[
        go.Bar(name='Mannen', x=dff[(dff.Gender == 'Mannen')].gem_sector, y=dff[(dff.Gender == 'Mannen')].value_percent, legendgroup="Mannen",marker_color=colorscale_bar[9], customdata = dff[(dff.Gender == 'Mannen')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='Vrouwen', x=dff[(dff.Gender == 'Vrouwen')].gem_sector, y=dff[(dff.Gender == 'Vrouwen')].value_percent, legendgroup="Vrouwen",marker_color=colorscale_bar[10], customdata = dff[(dff.Gender == 'Vrouwen')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}')
    ])

    dff = pd.DataFrame(data_age)
    dff['sum'] = dff.groupby(['gem_sector', 'YEAR'])['Total_CVD_Patient_Level'].transform(lambda g: g.sum())
    dff['value_percent'] = dff['Total_CVD_Patient_Level'] * 100/ dff['sum']
    # fig_2 = px.bar(DT_DEMOGRAPH_AGE[DT_DEMOGRAPH_AGE.YEAR == 2020], x="gem_sector", y="value_percent", color="Age")
    fig_2 = go.Figure(data=[
        go.Bar(name='below30', x=dff[(dff.Age == 'below30')].gem_sector, y=dff[(dff.Age == 'below30')].value_percent, legendgroup="below30",marker_color=colorscale_bar[8], customdata = dff[(dff.Age == 'below30')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='30to50', x=dff[(dff.Age == '30to50')].gem_sector, y=dff[(dff.Age == '30to50')].value_percent, legendgroup="30to50",marker_color=colorscale_bar[7], customdata = dff[(dff.Age == '30to50')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='50to70', x=dff[(dff.Age == '50to70')].gem_sector, y=dff[(dff.Age == '50to70')].value_percent, legendgroup="50to70",marker_color=colorscale_bar[6], customdata = dff[(dff.Age == '50to70')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='above70', x=dff[(dff.Age == 'above70')].gem_sector, y=dff[(dff.Age == 'above70')].value_percent, legendgroup="above70",marker_color=colorscale_bar[5], customdata = dff[(dff.Age == 'above70')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}')
    ])

    dff = pd.DataFrame(data_eth) 
    dff['sum'] = dff.groupby(['gem_sector', 'YEAR'])['Total_CVD_Patient_Level'].transform(lambda g: g.sum())
    dff['value_percent'] = dff['Total_CVD_Patient_Level'] * 100/ dff['sum']
    # fig_3 = px.bar(DT_DEMOGRAPH_ETHNICITY[DT_DEMOGRAPH_ETHNICITY.YEAR == 2020], x="gem_sector", y="value_percent", color="Ethnicity")
    fig_3 = go.Figure(data=[
        go.Bar(name='Native Dutch', x=dff[(dff.Ethnicity == 'Native Dutch')].gem_sector, y=dff[(dff.Ethnicity == 'Native Dutch')].value_percent, legendgroup="Native Dutch",marker_color=colorscale_bar[4], customdata = dff[(dff.Ethnicity == 'Native Dutch')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='Suriname', x=dff[(dff.Ethnicity == 'Suriname')].gem_sector, y=dff[(dff.Ethnicity == 'Suriname')].value_percent, legendgroup="Suriname",marker_color=colorscale_bar[3], customdata = dff[(dff.Ethnicity == 'Suriname')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='Other', x=dff[(dff.Ethnicity == 'Other')].gem_sector, y=dff[(dff.Ethnicity == 'Other')].value_percent, legendgroup="Other",marker_color=colorscale_bar[2], customdata = dff[(dff.Ethnicity == 'Other')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}')
    ])

    dff = pd.DataFrame(data_ses) 
    dff['sum'] = dff.groupby(['gem_sector', 'YEAR'])['Total_CVD_Patient_Level'].transform(lambda g: g.sum())
    dff['value_percent'] = dff['Total_CVD_Patient_Level'] * 100/ dff['sum']
    # fig_4 = px.bar(DT_DEMOGRAPH_SES[DT_DEMOGRAPH_SES.YEAR == 2020], x="gem_sector", y="value_percent", color="SES")
    fig_4 = go.Figure(data=[
        go.Bar(name='SES1', x=dff[(dff.SES == 'SES1')].gem_sector, y=dff[(dff.SES == 'SES1')].value_percent, legendgroup="SES1", marker_color=colorscale_bar[4], customdata = dff[(dff.SES == 'SES1')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='SES2', x=dff[(dff.SES == 'SES2')].gem_sector, y=dff[(dff.SES == 'SES2')].value_percent, legendgroup="SES2", marker_color=colorscale_bar[3], customdata = dff[(dff.SES == 'SES2')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='SES3', x=dff[(dff.SES == 'SES3')].gem_sector, y=dff[(dff.SES == 'SES3')].value_percent, legendgroup="SES3", marker_color=colorscale_bar[2], customdata = dff[(dff.SES == 'SES3')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='SES4', x=dff[(dff.SES == 'SES4')].gem_sector, y=dff[(dff.SES == 'SES4')].value_percent, legendgroup="SES4", marker_color=colorscale_bar[1], customdata = dff[(dff.SES == 'SES4')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}'),
        go.Bar(name='SES5', x=dff[(dff.SES == 'SES5')].gem_sector, y=dff[(dff.SES == 'SES5')].value_percent, legendgroup="SES5", marker_color=colorscale_bar[0], customdata = dff[(dff.SES == 'SES5')][['gem_sector','Total_CVD_Patient_Level']], hovertemplate = '<b>%{customdata[0]}</b><br>Percentage: %{y:.2f} - Number: %{customdata[1]}')
    ])

    fig_bar.add_trace(fig_1.data[0], 1, 1)
    fig_bar.add_trace(fig_1.data[1], 1, 1)
    fig_bar.add_trace(fig_2.data[0], 1, 2)
    fig_bar.add_trace(fig_2.data[1], 1, 2)
    fig_bar.add_trace(fig_2.data[2], 1, 2)
    fig_bar.add_trace(fig_2.data[3], 1, 2)
    fig_bar.add_trace(fig_3.data[0], 2, 1)
    fig_bar.add_trace(fig_3.data[1], 2, 1)
    fig_bar.add_trace(fig_3.data[2], 2, 1)
    fig_bar.add_trace(fig_4.data[0], 2, 2)
    fig_bar.add_trace(fig_4.data[1], 2, 2)
    fig_bar.add_trace(fig_4.data[2], 2, 2)
    fig_bar.add_trace(fig_4.data[3], 2, 2)
    fig_bar.add_trace(fig_4.data[4], 2, 2)


    dff = pd.DataFrame(data_gender_age_ses) 
    colorscale_SES = [
                # SES1,SES3,SES2,SES4,SES5, Age 30to50, Age 50to70, Age above 70, Age below30, gender Mannen, gender Vrouwen
                "#6ADDFF","#4980DF","#56B7FF","#3C50BF","#38309F","#4C9F87","#007649","#18362E","#D4E8E2","#99d98c","#d9ed92"
                ]
    fig_G_A_S = px.sunburst(dff, path=[ 'Gender', 'Age', 'SES'], values='Total_CVD_Patient_Level', color='Gender')
    fig_G_A_S.update_traces(
        marker_colors=[
            colorscale_SES[c] for c in pd.factorize(fig_G_A_S.data[0].labels)[0]
        ],
        leaf_opacity=1,
    )

    dff = pd.DataFrame(data_gender_age_eth) 
    colorscale_ETH = [# Dutch, Other, Suriname, Age 30to50, Age 50to70, Age above 70, Age below30, gender Mannen, gender Vrouwen
                        "#6ADDFF","#4980DF","#56B7FF","#4C9F87","#007649","#18362E","#D4E8E2","#99d98c","#d9ed92"
                  ]
    
    fig_G_A_E = px.sunburst(dff, path=[ 'Gender', 'Age', 'Ethnicity'], values='Total_CVD_Patient_Level', color='Gender')
    fig_G_A_E.update_traces(
        marker_colors=[
            # for color palete, check https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express
            colorscale_ETH[c] for c in pd.factorize(fig_G_A_E.data[0].labels)[0]
        ],
        leaf_opacity=1,
    )

    dff = pd.DataFrame(data_gender_age) 
    colorscale_G_A = [# Age 30to50, Age 50to70, gender Mannen, gender Vrouwen, Age above 70, Age below30
                        "#4C9F87","#007649","#18362E","#D4E8E2","#99d98c","#d9ed92", 
                  ]
    fig_G_A = px.sunburst(dff, path=[ 'Gender', 'Age'], values='Total_CVD_Patient_Level', color='Gender')
    fig_G_A.update_traces(
        marker_colors=[
            # for color palete, check https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express
            colorscale_G_A[c] for c in pd.factorize(fig_G_A.data[0].labels)[0]
        ],
        leaf_opacity=1,
    )

    if tab == 'overview':
        # fig1, fig2, fig3, fig4 = generate_visualizations1(data, splits)
        return dbc.Card([
        dbc.CardHeader(html.H2("Hartfalen Patients Overview"), className="text-center"),
        dcc.Graph(figure=fig_bar, style={"height":800}, config={'displayModeBar': False})
    ])
    elif tab == 'gender_age_content':
        return dbc.Card([
        dbc.CardHeader(html.H2("Hartfalen Patients by Gender Age"), className="text-center"),
        dcc.Graph(figure=fig_G_A, style={"height":800}, config={'displayModeBar': False})
    ])
    elif tab == 'gender_age_eth_content':
        return dbc.Card([
        dbc.CardHeader(html.H2("Hartfalen Patients by Gender Age and Ethnicity"), className="text-center"),
        dcc.Graph(figure=fig_G_A_E, style={"height":800}, config={'displayModeBar': False})
    ])
    elif tab == 'gender_age_ses_content':
        return dbc.Card([
        dbc.CardHeader(html.H2("Hartfalen Patients by Gender Age and SES"), className="text-center"),
        dcc.Graph(figure=fig_G_A_S, style={"height":800}, config={'displayModeBar': False})
    ])



@callback(
    Output("stat_info-card", "children"),
    Input("data-cvd", "data"),
    Input('drop_select_year_hartfalen', 'value'),
    Input('data_id_hartfalen', 'value'),
    Input('area_id_hartfalen', 'value')
)
def make_pay_gap_card(data_cvd,year_value,data_elan,area):

    dff = pd.DataFrame(data_cvd)
    dff.columns = dff.columns.str.replace(r'_DBC', '')
    dff.columns = dff.columns.str.replace(r'_ICPC', '')
    dff.columns = dff.columns.str.replace(r'_COMB', '')

    stat_title = '{} Hartfalen Patients {} Data Overview - {}'.format(year_value, data_elan, area)
    Hartfalen = dbc.Alert(dcc.Markdown(
        f"""
        ** Hartfalen Patients **  
        ### {dff['Total_CVD_Patient'].values[0]}
        """,
    ), id="tooltip-target", color="#6ADDFF")

    # Polyfarmacie = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** Polyfarmacie User** 
    #         ### {int(dff['UniqueMed_ICPC_CAT'].values[0] *100/dff['Total_CVD_Patient'].values[0])} % 
    #         """,
    # ), color="#6ADDFF")

    Diabetes = dbc.Alert(dcc.Markdown(
        f"""
            ** Diabetes Medication ** 
            ### {int(dff['DIAB_MED'].values[0] *100/dff['Total_CVD_Patient'].values[0])} %
            """,
    ), color="#6ADDFF")

    Cholestherol = dbc.Alert(dcc.Markdown(
        f"""
            ** Cholestherol Medication ** 
            ### {int(dff['CHOL_MED'].values[0] *100/dff['Total_CVD_Patient'].values[0])} %
            """,
    ), color="#6ADDFF")

    Diuretics_raas_beta = dbc.Alert(dcc.Markdown(
        f"""
            ** All Blood Pressure Medication ** 
            ### {int(dff['DIURETICS_RAAS_BETA'].values[0] *100/dff['Total_CVD_Patient'].values[0])} %
            """,
    ), color="#6ADDFF")

    Diuretics_only = dbc.Alert(dcc.Markdown(
        f"""
            ** Diuretics Medication ** 
            ### {int(dff['DIURETICS_Only'].values[0] *100/dff['Total_CVD_Patient'].values[0])} %
            """,
    ), color="#6ADDFF")

    Diuretics_beta = dbc.Alert(dcc.Markdown(
        f"""
            ** Diuretics & Beta Medication** 
            ### {int(dff['DIURETICS_BETA'].values[0] *100/dff['Total_CVD_Patient'].values[0])} %
            """,
    ), color="#6ADDFF")

    Diuretics_raas = dbc.Alert(dcc.Markdown(
        f"""
            ** Diuretics & RAAS Medication** 
            ### {int(dff['DIURETICS_RAAS'].values[0] *100/dff['Total_CVD_Patient'].values[0])} %
            """,
    ), color="#6ADDFF")

    # BMI_obese = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** Obese Person ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # BMI_Overweight = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** Overweight Person ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # BMI_Normalweight = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** Normal Weight Person ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # NTPR = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** NTPR Measurement ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # ACP = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** ACP Care Plan ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # ACP_3years = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** ACP 3 Years Care Plan ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # CVRM_HA = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** CVRM Huisarts ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    # CVRM_SPEC = dbc.Alert(dcc.Markdown(
    #     f"""
    #         ** CVRM Specialist ** 
    #         ### {dff['Median Hourly Gap']}  
    #         """,
    # ), color="#6ADDFF")

    ZVWHUISARTS = dbc.Alert(dcc.Markdown(
        f"""
            ** Huisarts kosten ** 
            ### \u20ac {int(dff['ZVWKHUISARTS'].values[0])}  
            """,
    ), color="#6ADDFF")

    ZVWZIEKEN = dbc.Alert(dcc.Markdown(
        f"""
            ** Ziekenhuis kosten ** 
            ### \u20ac {int(dff['ZVWKZIEKENHUIS'].values[0])}  
            """,
    ), color="#6ADDFF")

    ZVWFARMACIE = dbc.Alert(dcc.Markdown(
        f"""
            ** Farmacie kosten ** 
            ### \u20ac {int(dff['ZVWKFARMACIE'].values[0])}  
            """,
    ), color="#6ADDFF")

    ZVWKOSTENTOTAAL = dbc.Alert(dcc.Markdown(
        f"""
            ** Total kosten ** 
            ### \u20ac {int(dff['ZVWKOSTENTOTAAL'].values[0])}  
            """,
    ), id="tooltip-target", color="#6ADDFF")


    if data_elan == 'ELAN-Huisarts':
        hartfalen_tooltip = dbc.Tooltip(
            "Total count of people that diagnosed with Heart Failure over a year, "
            "(ICPC Code : K77*)",
            target="tooltip-target",
        )
    elif data_elan == 'ELAN-Ziekenhuis':
        hartfalen_tooltip = dbc.Tooltip(
            "Total count of people that diagnosed with Heart Failure over a year, "
            "(DBC Code - Specialist Code | 0320-301, 0320-302)",
            target="tooltip-target",
        )
    else:
        hartfalen_tooltip = dbc.Tooltip(
            "Total count of people that diagnosed with Heart Failure over a year, "
            "(ICPC Code : K77*) and (DBC Code - Specialist Code | 0320-301, 0320-302)",
            target="tooltip-target",
        )

    card =  dbc.Card([
        dbc.CardHeader(html.H2(stat_title), className="text-center"),
        dbc.CardBody([
            dbc.Row([dbc.Col(Hartfalen), hartfalen_tooltip], className="text-center"),
            dbc.Accordion([ dbc.AccordionItem(html.Div([dbc.Row([dbc.Col(Cholestherol), dbc.Col(Diabetes), dbc.Col(Diuretics_raas_beta)], className="text-center"), 
                                                        dbc.Row([ dbc.Col(Diuretics_only), dbc.Col(Diuretics_beta), dbc.Col(Diuretics_raas)], className="text-center")]), title="Medication User"),
                            # dbc.AccordionItem(dbc.Row([dbc.Col(BMI_obese), dbc.Col(BMI_Overweight), dbc.Col(BMI_Normalweight), dbc.Col(NTPR)], className="text-center"), title="Medical Measurement"),
                            # dbc.AccordionItem(dbc.Row([dbc.Col(ACP), dbc.Col(ACP_3years), dbc.Col(CVRM_HA), dbc.Col(CVRM_SPEC)], className="text-center"), title="ICPC Code"),
                            dbc.AccordionItem(dbc.Row([dbc.Col(ZVWHUISARTS), dbc.Col(ZVWZIEKEN), dbc.Col(ZVWFARMACIE), dbc.Col(ZVWKOSTENTOTAAL)], className="text-center"), title="Average ZVW Kosten") ],  start_collapsed=True)
        ])
    ])
    return card


