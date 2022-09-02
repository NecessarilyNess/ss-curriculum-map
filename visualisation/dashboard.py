from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from base64 import b64encode
import numpy as np

import sys
sys.path.append('/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code')


from helper_functions import *
from module_dict_updates import *
from search_file import *
from module_comparisons import *

all_modules = all_modules_dict('./module_dict.json','/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/module_csv_files','./module_csv_files/%s')
index1 = 1
index2 = 2
repeat_or_cluster = 1
min_val = 0.2 #so far it appears that 0.3 is a good number for determining meaningful similarity, 0.1 for weak similarity
max_val = 1
write_destination = "/Users/vanessamadu/Documents/StudentShapers/StudentShapers_code/test.xlsx"
info_index = 0


np.random.seed(1)

app = Dash(__name__)


app.layout = html.Div([
    html.H4('Rendering options of plots in Dash '),
    html.P("Choose render option:"),
    dcc.RadioItems(
        id='render-option',
        options=['interactive', 'image'],
        value='image'
    ),
    html.Div(id='output'),
])


@app.callback(
    Output("graph", "figure"), 
    Input("Module code", "Module code"))
def filter_heatmap(cols):
    data = repeat_similarity(all_modules, index1, index2, info_index)
    fig = px.imshow(data[cols],
                labels=dict(x="Module code", y="Module code", color="Relative number of repeats"),
                x= module_codes,
                y= module_codes
               )
    return fig

app.run_server(debug=True)