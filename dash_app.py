from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input
from dash.dependencies import Output
import dash_auth

import plotly.express as px

import pandas as pd
from datetime import date, datetime
import config_file
from sqlalchemy import create_engine


user = config_file.user
password = config_file.password
db = config_file.db
host = config_file.host
port = config_file.port

url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, 
                                                password,
                                                host,
                                                port,
                                                db)

engine = create_engine(url)
query = 'select * from "Trading"."Stocks" where "Symbol" in (\'AAPL\', \'TSLA\')'

data = pd.read_sql(query, engine)
symbols = data['Symbol'].unique().tolist()
kpis = ['Open', 'High', 'Low', 'Close', 'Adj Close',
       'Volume']

data.head()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
#auth = dash_auth.BasicAuth(app, config_file.usernames_passwords)

app.layout = html.Div(
    html.Div([
        html.H1(children='Stocks Analysis', style={'textAlign':'center'}),
        html.P(children='App for stock analysis - to be improved',  style={'textAlign':'center'}),
        html.Hr(),
        dcc.Dropdown(
            id='symbol_dropdown',
            options=[{"label":sy, "value":sy} for sy in symbols],
            placeholder='Select stock',
            multi=False,
            value='AAPL'),
        dcc.Dropdown(
            id='kpi_dropdown',
            options=[{'label':kpi, 'value':kpi} for kpi in kpis],
            multi=False,
            value='Open',
            placeholder='Select KPI'),
        dcc.Graph(
            id='line_graph',
            figure={
                },
            ),
        dcc.DatePickerRange(
            id='date_picker',
            min_date_allowed=data['Date'].min(),
            max_date_allowed=data['Date'].max(),
            initial_visible_month=data['Date'].min(),
            start_date=data['Date'].min(),
            end_date=data['Date'].max(),
            display_format='DD/MM/YYYY'),
        dash_table.DataTable(
            id='datatable',
            columns=[{'name':i, "id":i} for i in data.columns],
            data=data.to_dict('records'), page_size=10)]))

@app.callback(
    Output('line_graph', 'figure'),
    [Input('symbol_dropdown', 'value'), Input('kpi_dropdown', 'value')],
    Input('date_picker', 'start_date'), Input('date_picker', 'end_date'))
def upgrade_graph(symbol, kpi, start_date, end_date):
    fig = px.line(data.loc[data['Symbol']==symbol],
                  data.loc[(datetime.date(data['Date'])>=datetime.strptime(start_date, '%Y-%m-%d'))
                           & (datetime.date(data['Date'])<=datetime.strptime(end_date, '%Y-%m-%d'))], 
                  kpi,
                  title='{0} price of {1} Stocks'.format(kpi, symbol),)
    return fig

@app.callback(
    Output('datatable', 'data'),
    Input('symbol_dropdown', 'value'))
def display_table(symbol):
    symbol_x = data[data.Symbol.isin([symbol])]
    return symbol_x.to_dict("records")  
        

    
app.run(debug=True)


datetime.strptime(data['Date'].max(), '%Y-%m-%d')
