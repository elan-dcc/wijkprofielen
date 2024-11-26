import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.graph_objects as go
import os

dash.register_page(__name__)

path = '../data/'
path = os.path.join(os.path.dirname(__file__), path).replace("\\","/")

# df_h = pd.read_excel(open(path + ('Codebook_shorter.xlsx'), 'rb'), sheet_name='Huisartsen')
# df_cbs = pd.read_excel(open(path + ('Codebook_shorter.xlsx'), 'rb'), sheet_name='CBS')

var_def_label_NL_dict = {}
with open(path + 'Variables_Label_NL_short.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_label_NL_dict[s[0]] = s[1].split('\n')[0]

var_def_NL_dict = {}
with open(path + 'Variables_Definition_NL_short.txt', mode='r') as f2:
    for line in f2:
        s = line.split(':')
        var_def_NL_dict[s[0]] = s[1].split('\n')[0]


var_def_label_NL = pd.DataFrame([{"columns": key, "Label": value} for key, value in var_def_label_NL_dict.items()])
var_def_NL = pd.DataFrame([{"columns": key, "Definition": value} for key, value in var_def_NL_dict.items()])

df_label_def_nl = var_def_label_NL.merge(var_def_NL, on=['columns'])[['Label','Definition']]


layout = html.Div([
    html.H1('Variables Definition'),   
    dash_table.DataTable(
       columns=[
              {'name': 'Label', 'id': 'Label', 'type': 'text'},
              {'name': 'Definition', 'id': 'Definition', 'type': 'text'},
       ],
       data=df_label_def_nl.to_dict('records'),
       filter_action='native',
       style_data={
           'whiteSpace': 'normal',
       },
       style_cell={'textAlign': 'left'}
       ),
])
