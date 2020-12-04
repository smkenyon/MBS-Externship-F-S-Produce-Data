"""
marketnews_dashboard
Uses dash framework to plot USDA Market News specialty commodities data.
Author: Stephen Kenyon
Date: 11/13/2020
Copyright 2020, Rutgers MBS, NJBDA, F&S Produce
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import os
import pandas as pd
from dash.dependencies import Input
from dash.dependencies import Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data_files = os.listdir('Data')
commodity_list = [file[:file.find("_")] for file in data_files]  # commodity names contained before first underscore in data directory
dfs = dict(zip(commodity_list, data_files))

"""
So the way that this works - we set out the layout with dcc.core html components and stuff. 
After we set up the layout - we can build a separate function that updates the layout through 
the app callback decorator. This wraps our update function

Inside of the update function - we actually load the data from file to save on memory
Then we plot using the plotly function that we played around with in jupyter lab.
"""

df = pd.read_csv('Data//' + data_files[0])
terminal_markets = df['City Name'].unique()
origin = df['Origin'].unique()

app.layout = html.Div([
    html.H1("F&S Produce MarketNews Dashboard", style={'text-align':'center'}),
    html.Div([

        html.Div([
            html.Label(["Commodity Selector",
                dcc.Dropdown(
                    id='commodity-selector',
                    options=[{'label':i, 'value':i} for i in commodity_list],
                    value=commodity_list[0]
                )
            ],
            style={'width': '96%', 'display': 'inline-block'})
        ]),
        html.Div([
            html.Div([
                html.Label(["Terminal Market",
                    dcc.Dropdown(
                        id='terminal-market',
                        options=[{'label': i, 'value': i} for i in terminal_markets],
                        value=terminal_markets[0]
                    )]),
            ],
                style={'width': '48%', 'display': 'inline-block'}
            ),
            html.Div([
                html.Label(["Origin",
                    dcc.Dropdown(
                        id='origin',
                        options=[{'label': i, 'value': i} for i in origin],
                        value=origin[0]
                    )]),
            ],
                style={'width': '48%', 'display': 'inline-block'})
        ]),
        
        dcc.Graph(id='produce-time-series')
    ])
])
"""
@app.callback(
    Output(),
    Input()
)
def set_dropdowns():
    pass

@app.callback(
    Output(),
    Input()
)
def set_dropdowns_value():
    pass
"""
@app.callback(
    Output('produce-time-series', 'figure'),
    Input('commodity-selector', 'value'),
    Input('terminal-market', 'value'),
    Input('origin', 'value')
)
def update_graph(commodity_name, terminal_market, origin_city):

    df = pd.read_csv("Data//" + dfs[commodity_name])
    filtered = df[(df['City Name']==terminal_market) & (df['Origin']==origin_city)]
    midpoint = (filtered['High Price'] + filtered['Low Price'])/2
    midpoint.name = 'Midpoint Price'
    plot_df = pd.concat([filtered['Date'], midpoint], axis=1)
    plot_df['Date'] = pd.to_datetime(plot_df['Date'])
    
    fig = px.line(x=plot_df['Date'], y=plot_df['Midpoint Price'])
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate")
            ])
        ),
        title="Date"
    )
    fig.update_yaxes(
        title="Price ($)"
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
