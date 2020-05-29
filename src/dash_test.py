import datetime, time
import pandas as pd
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pymongo import MongoClient

from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

# df = pd.read_csv(
#     'data/dummy.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
def get_data():
    client = MongoClient('localhost', 27017)
    db = client['fraud_study']
    collection = db['fraud_data']

    risk_range = [-1, .2, .5, .7, 1]
    risks = ['No Risk','Low Risk','Medium Risk','High Risk']
    blank = np.full((1000,len(risks)),' ')
    df = pd.DataFrame(blank, columns=risks)

    for i in range(1,5):
        query = (collection
                 .find({'probability': {'$gt': risk_range[i-1], '$lte': risk_range[i]}})
                 .sort('time', -1)
                 .limit(1000)
                )

        for j, entry in enumerate(query):

            out = ''
            id_ = entry['data']['object_id']
            name = entry['data']['name']
            t = datetime.datetime.fromtimestamp(entry['time'])
            out += (f'ID: {id_}, TIME: {t.replace(second=0, microsecond=0)}, NAME: {name[:40]}')
            df.iloc[j,i-1] = out
    
    return df

while True:
    df = get_data()
    num = 10

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app.layout = html.Div(
        html.Div([
            html.H1('Fraud Detection Dashboard', style={
                    'color': 'blue', 'fontSize': 54}),
            dcc.Graph(id='example-graph',
                      figure={'data': [ {'x': ["No Risk", "Low Risk", "Medium Risk", "High Risk"], 'y': df.nunique().values-1, 'type': 'bar', 'name': 'Total Cases'}, ], 'layout': { 'title': 'Total Cases By Category' } } ),
            html.H3('Recent 10 Cases for Each Category'),
            dash_table.DataTable(
                data=df.iloc[:num,0:2].to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns[0:2]],
                style_cell={'textAlign': 'left'}
            ),
            dash_table.DataTable(
                data=df.iloc[:num,2:4].to_dict('records'),
                columns=[{"name": i, "id": i} for i in df.columns[2:4]],
                style_cell={'textAlign': 'left'}
            ),
            dcc.Interval(
                id='interval-component',
                interval=1*1000,  # in milliseconds
                n_intervals=0
            )
        ])
    )
    


    if __name__ == '__main__':
        app.run_server(debug=True)
    time.sleep(5)