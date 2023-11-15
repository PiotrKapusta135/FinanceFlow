from dash import Dash, dcc, html, dash_table
import pandas as pd
import config_file
from sqlalchemy import create_engine
from dash.dependencies import Input
from dash.dependencies import Output


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

data.head()


app = Dash(__name__)

'''app.layout = html.Div([
    html.Div(children='My first dash app'),
    dash_table.DataTable(data=data.to_dict('records'), page_size=10)
    ])

app.run()'''

app.layout = html.Div(
    html.Div([
        html.H1('Stocks Analysis'),
        html.P('App for stock analysis - to be improved'),
        dcc.Dropdown(
            id='datatable_dropdown',
            options=[{"label":sy, "value":sy} for sy in symbols],
            placeholder='Select symbol',
            multi=False,
            value=data['Symbol'].values,),
        dcc.Graph(
            id='line_graph',
            figure={
                'data':[
                    {
                        'x':data['Date'],
                        'y':data['Open'],
                        'type':'lines'
                        },
                    ],
                'layout':{'title':'Open price of Apple Stocks'},
                },
            ),
        dash_table.DataTable(
            id='datatable',
            columns=[{'name':i, "id":i} for i in data.columns],
            data=data.to_dict('records'), page_size=10)]))

@app.callback(
    Output('datatable', 'data'),
    Input('datatable_dropdown', 'value'))

@app.callback(
    Output('line_graph', 'data'),
    Input('datatable_dropdown', 'value'))

def display_table(symbol):
    symbol_x = data[data.Symbol.isin([symbol])]
    return symbol_x.to_dict("records")  
        
'''       
        dcc.Graph(
            figure={
                'data':[
                    {
                        'x':data['Date'],
                        'y':data['Close'],
                        'type':'lines'
                        },
                    ],
                'layout':{'Close price of Apple Stocks'},
            },
            ),
        ]
    )
    ]
)'''
    
app.run(debug=True)
