from dash import Dash, html, dcc, Output, Input, callback
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from flask import Flask, request
import json


#Define the Flask app.
server = Flask(__name__)

#Define the Plotly Dash app.
app = Dash(__name__, server=server, url_base_pathname='/Ignition_Graph_Return/')

#Create Web Layout. Generate HTML to be served.
app.layout = html.Div(children=[
            html.Div([dcc.Graph(id='main_graph')]),
            html.Div([daq.ToggleSwitch(id='state', value=False)]),
    ],
    id="layout"
    )

#Decorator used as interface to flask web components. 
@server.route('/Ignition_Graph/', methods=['GET'])
def get_content():
    try:
        global jdata
        data = request.args.get("data")
        jdata = json.loads(data)
        return app.index()
    except:
        return "Ooops! That didnt work. Try adding ?data= plus any data you would like to graph in json format."

#Decorator used as interface to dash web components. 
@app.callback(
    Output(component_id='main_graph', component_property='figure'),
    [Input(component_id='state', component_property='value')
     ]
)
def update_main_graph(state):
    
    df = pd.DataFrame(jdata)
    fig = go.Figure()

    fig.data = []

    for (cols, col_data) in df.iteritems():
        if 'index' in df:
            if cols == 'index':
                x_data = col_data.values
            else:
                y_data = col_data.values
                fig.add_trace(go.Scatter(x=x_data, y=y_data, name=cols))
        else:
            y_data = col_data.values
            fig.add_trace(go.Scatter(y=y_data, name=cols))

    return fig




#Run Server
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8055', debug=False)
