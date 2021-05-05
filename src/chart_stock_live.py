import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

#https://stooq.com
start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 22)
df = web.DataReader(
    ['AMZN', 'GOOGL', 'FB', 'PFE', 'MRNA', 'BNTX'],
    'stooq',
    start = start,
    end = end
)
#df = df.melt(
# ignore_index = false,
# value_name = "price"
# ).reset_index()
df = df.stack().reset_index()
# print(df[:15])

# https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{
        'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'
    }]
)

# Layout section: Bootstrap (https://hackertheme.com/bootstrap-cheatsheet/)
# **************************************************************************
app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
            html.H1("Dashboard -- Stock Exchanges", className='text-center text-primary mb-4'),
            width=12
            )
    ),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='dpdn1',
                multi=False,
                value='AMZN',
                options=[{
                    'label': x,
                    'value': x
                } for x in sorted(
                    df['Symbols'].unique()
                )],
            ),
            dcc.Graph(
                id='line-fig1',
                figure={}     
            )
        ],
        xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(
                id='dpdn2',
                multi=False,
                value=['PFE', 'BNTX'],
                options=[{
                    'label': x,
                    'value': x
                } for x in sorted(
                    df['Symbols'].unique()
                )],
            ),
            dcc.Graph(
                id='line-fig2',
                figure={}     
            )
        ]),
    ], no_gutters=True, justify='start'), #Horizontal:start, center, end, between, around

    dbc.Row([
        dbc.Col([
            html.P(
                "Select Common Stock:",
                style={'textDecoration': 'underline'}
            ),
            dcc.Checklist(
                id='checklist1',
                value=['FB', 'GOOGL', 'AMZN'],
                options=[{
                    'label': x, 'value': x
                } for x in sorted(df['Symbols'].unique())],
                labelClassName='mr-3'
            ),
            dcc.Graph(
                id='hist1',
                figure={}
            ),
        ], xs=12, sm=12, md=12, lg=5, xl=5),

        dbc.Col([
            dbc.Card([
                dbc.CardBody(
                    html.P(
                        "We're better together, Help each other out!",
                        className="card-text"
                    )
                ),
                dbc.CardImg(
                    src="https://media.giphy.com/media/Ll0jnPa6IS8eI/giphy.gif",
                    bottom=True
                ),
            ],
            style={'width': '24rem'},
            )
        ], xs=12, sm=12, md=12, lg=5, xl=5 
        )
    ], align='center') #Vertical: start, center, end
], fluid=True)


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single
@app.callback(
    Output('line-fig1', 'figure'),
    Input('dpdn1', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols']==stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('dpdn2', 'value')
)

def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2


# Histogram
@app.callback(
    Output('hist1', 'figure'),
    Input('checklist1', 'value')
)

def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2020-12-22']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)