import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

df = pd.read_csv("machine-use.csv", sep = ';')

app.layout = html.Div(children=[
    html.H1(children='Vizualizácia využitia strojov', style={"text-align" : "center"}),

    

    html.Div(children=[
        html.Div(children=[
            html.Label('Vyber posilňovňu', style={}),
            dcc.Dropdown(
                id="posID",
                options=[
                    {'label': 'Golem', 'value': 'pos1'},
                    {'label': 'Borovicový háj', 'value': 'pos2'},
                    {'label': 'Family gym Oáza', 'value': 'pos3'},
                    {'label': 'Family gym Cassovar', 'value': 'pos4'},
                    {'label': 'Astoria', 'value': 'pos5'}
                ],
                value='pos1',)
            ],
            style={"border-width" : "1px", 
                "border-style":"solid", 
                "width" : "40%", 
                "text-align": "center", 
                "border-color": "black",
                "border-radius": "3px",
                "display": "inline-block",
                "margin-left": "100px"
            }),
        html.Div(children=[
            html.Label('Vyber mesiac', style={}),
            dcc.Dropdown(
                id="monthID",
                options=[
                    {'label': 'Január', 'value': 'january'},
                    {'label': 'Február', 'value': 'february'},
                    {'label': 'Marec', 'value': 'march'},
                    {'label': 'Apríl', 'value': 'april'}
                ],
                value='january',)
            ],
            style={"border-width" : "1px", 
                "border-style":"solid", 
                "width" : "40%", 
                "text-align": "center", 
                "border-color": "black",
                "border-radius": "3px",
                "display": "inline-block",
                "margin-right": "100px",
                "float": "right",
            }),
        ],
        style={}
    ),

    daq.ToggleSwitch(
        id='toggle-switch',
        value=False
    ),
    html.Label("Zmeniť graf", style={"text-align": "center"}),
    
    dcc.Graph(
        id='graph',
        figure={},
        style={"width" : "80%", "margin": "0 auto"}
    ),
    html.Div(children=[
        html.Div(children=[
            html.Div("Najviac využívané stroje:", style={"font-weight":"bold"}),
            html.Div(id='maxVal')
            ],
            style={"border-width" : "3px", 
            "border-style":"solid", 
            "width" : "40%", 
            "text-align": "center", 
            "border-color": "black",
            "border-radius": "20px",
            "display": "inline-block",
            "margin-left": "100px"
            }),
        html.Div(children=[
            html.Div("Najmenej využívané stroje:", style={"font-weight":"bold"}),
            html.Div(id='minVal')
            ],
            style={"border-width" : "3px", 
            "border-style":"solid", 
            "width" : "40%", 
            "text-align": "center", 
            "border-color": "black",
            "border-radius": "20px",
            "display": "inline-block",
            "float": "right",
            "margin-right": "100px"
            }),
    ],
        style={"marginBottom": 10, "overflow": "hidden",
               } )
])

@app.callback(
    Output('graph', 'figure'),
    Output('maxVal', 'children'),
    Output('minVal', 'children'),
    [Input('posID', 'value'),
     Input('toggle-switch', 'value'),
     Input('monthID', 'value'),
     ])
def update_graph(pos, toggle, month):

    dff = df.loc[df['month'] == month]

    if (toggle == False):

        fig = px.bar(dff, x=pos, y="machine", color="category")
        fig.update_layout(xaxis_title="Počet použití stroja",
                          yaxis_title="Názov stroja",
                          legend_title="Kategória stroja",
            font=dict(
            family="Arial",
            size=12,
            color="black"
        ))
    else:
        fig = px.pie(dff, values = pos, names = "machine")
        fig.update_traces(hoverinfo='label+percent', textinfo='label+value', textfont_size=12)

    max5 = dff.nlargest(5, pos, keep="first")
    max5String = listToString(max5["machine"].values)
    
    min5 = dff.nsmallest(5, pos, keep="first")
    min5String = listToString(min5["machine"].values)

    return fig, max5String, min5String


def listToString(s): 
    str1 = []

    for ele in s: 
        str1.append(ele)
        str1.append(html.Br())

    return str1

if __name__ == '__main__':
    app.run_server(debug=True)
