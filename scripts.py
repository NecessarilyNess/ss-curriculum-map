from helper_functions import *
from module_dict_updates import *
from search_file import *
from module_comparisons import *

all_modules = all_modules_dict('./module_dict.json', '/Users/christinezhang/ss-curriculum-map/module_csv_files', './module_csv_files/%s')


index1 = 1 #Takes the value 1 or 2. 1 indicates the taught keywords of module 1. 2 indicates the prerequite keywords of module 1
index2 = 1 #Takes the values 1 or 2. 1 indicates the taught keywords of module 2. 2 indicates the prerequite keywords of module 2
repeat_or_cluster = 1 #Takes the values 1 or 2. 1 indicates the similarity score based on the number of repeated keywords. 2 indicates similarity score based on 'clustering' (for details see the Score Generating section).
min_val = 0.2 #Takes a value between 0 and 1 (threshold for two modules to be considered similar)
max_val = 1 #Takes a value between 0 and 1 (upper limit of similarity being considered.)
write_destination = "/Users/christinezhang/Desktop/SS_write_to.xlsx" #Replace that with the full path to the xslx file you want to write to.
module_codes = list(all_modules.keys())

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

app = Dash(__name__)


app.layout = html.Div(children=[
    html.H1(children='Module similarity'),

    html.Div(children='''
        A heatmap to display the relative overlap between modules.
    '''),

    html.Label('Year'),

    dcc.Checklist(
        id='years',
        options=[1, 2, 3, 4],
        value=[1, 2, 3, 4]
    ),

    html.Label('Sections'),

    dcc.Checklist(
        id='categories',
        options=['pure', 'applied', 'statistics'],
        value=['pure', 'applied', 'statistics']
    ),

    dcc.Graph(
        id='modules-heatmap'
    ),

    html.Label('Year 2 Modules'),

    dcc.Checklist(
        id='yr2modules',
        options=[code_to_name(all_modules, code) for code in year_filter(all_modules, [2])],
        value=['linear algebra and numerical analysis', 'multivariable calculus and differential equations', 
               'statistics']
    ),

    dcc.Graph(
        id='sankey-diagram'
    )
])


@app.callback(
    Output('modules-heatmap', 'figure'),
    Input('years', 'value'), 
    Input('categories', 'value'))
def filter_heatmap(selected_years, selected_categories):
    filtered_modules = year_and_section_filter(all_modules, selected_years, selected_categories)
    filtered_data = repeat_similarity(all_modules, filtered_modules, index1, index2, info_index=0)
    fig = px.imshow(filtered_data, labels=dict(x="Module Code", y="Module Name", color="Relative number of repeats"),
                 x=filtered_modules,
                 y=filtered_modules
                         )
    fig.update_traces(x = [code_to_name(all_modules, code) for code in filtered_modules],
                      y = [code_to_name(all_modules, code) for code in filtered_modules],
                      hovertemplate='%{x}<br>%{y}<br>Relative number of repeats: %{z}<extra></extra>')
    fig.update_xaxes(tickmode = 'array',
                     tickvals = np.linspace(0, 20, len(filtered_modules)),
                     ticktext = filtered_modules)
    return fig

@app.callback(
    Output('sankey-diagram', 'figure'),
    Input('yr2modules', 'value'))
def filter_sankey(selected_yr2modules):  
    yr1modules = [code_to_name(all_modules, code) for code in year_filter(all_modules, [1])]
    module_code_list = year_filter(all_modules, [1, 2])
    module_list = yr1modules + selected_yr2modules
    sankey_data = repeat_similarity(all_modules, module_code_list, 1, 2, info_index=0)
    sankey = go.Figure(data=[go.Sankey(
        node = dict(
        pad = 15,
        thickness = 20,
        line = dict(color = "black", width = 0.5),
        label = module_list,
        color = "blue"
        ),
        link = dict(
        source = [0, 1, 0, 2, 3, 3, 2, 3, 4, 5], # indices correspond to labels, eg A1, A2, A1, B1, ...
        target = [2, 3, 3, 4, 4, 5, 6, 7, 10, 11],
        value = [8, 4, 2, 8, 4, 2, 2, 2, 2, 2] #unfinished
    ))])
    return sankey
if __name__ == '__main__':
    app.run_server(debug=True)