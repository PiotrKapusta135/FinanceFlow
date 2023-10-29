from dash import Dash, dcc, html
import pandas as pd
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
query = 'select * from "Trading"."Stocks" where "Symbol" = \'AAPL\''

data = pd.read_sql(query, engine)

data.head()

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children='Stocks Analysis'),
        html.P(children=('App for stock analysis - to be improved'),
        ),
        dcc.Graph(
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

app.run_server(debug=True)
