import datetime
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

df = pd.read_csv(
    'data/dummy.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H1('Fraud Detection Dashboard', style={
                'color': 'blue', 'fontSize': 54}),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        html.H3('Recent 10 Cases for Each Category'),
        dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{"name": i, "id": i} for i in df.columns]
        ),
        dcc.Interval(
            id='interval-component',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]

# Multiple components can update everytime interval gets fired.


@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    satellite = Orbital('TERRA')
    data = {
        'time': [],
        'Latitude': [],
        'Longitude': [],
        'Altitude': []
    }

    # Collect some data
    for i in range(180):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        lon, lat, alt = satellite.get_lonlatalt(
            time
        )
        data['Longitude'].append(lon)
        data['Latitude'].append(lat)
        data['Altitude'].append(alt)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=1, cols=2, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 30, 'b': 30, 't': 30
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}
    # Add / update graph using append_trace
    # fig.append_trace({
    #     'x': data['time'],
    #     'y': data['Altitude'],
    #     'name': 'Altitude',
    #     'mode': 'lines+markers',
    #     'type': 'scatter'
    # }, row=1, col=1)

    # fig.add_trace({
    #     'x': data['Longitude'],
    #     'y': data['Latitude'],
    #     'text': data['time'],
    #     'name': 'Longitude vs Latitude',
    #     'mode': 'lines+markers',
    #     'type': 'scatter'
    # }, row=1, col=2)

    # Add a static graph with add_trace
    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4, 5, 6], y=[1, 2, 2, 2, 2, 3]),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4, 5, 6], y=[0, 1, 1, 2, 2, 2]),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4, 5, 6], y=[0, 0, 1, 2, 3, 4]),
        row=1, col=1)

    fig.add_trace(
        go.Scatter(x=[1, 2, 3, 4, 5, 6], y=[1, 1, 2, 2, 2, 3]),
        row=1, col=1)

    fig.add_trace(
        go.Bar(x=["No Risk", "Low Risk", "Med Risk", "High Risk"],
               y=[10, 3, 2, 5]),
        row=1, col=2)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
