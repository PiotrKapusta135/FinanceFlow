import pandas as pd
import yfinance as yf

import logging

from sqlalchemy import create_engine

from datetime import timedelta




#First load
'''
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
ticker_list = ['AAPL', 'TSLA', 'CDR.WA', 'MSFT', '^GSCP', 'GC=F', 'CL=F']
start_date = '2000-1-1'

for symbol in ticker_list:
    if symbol == 'AAPL':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
    elif symbol == 'TSLA':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
    elif symbol == 'CDR.WA':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
    elif symbol == 'MSFT':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
    elif symbol == '^GSCP':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
    elif symbol == 'GC=F':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
    elif symbol == 'CL=F':
        df = yf.download(symbol, start=start_date)
        df.to_sql(symbol, engine, schema='Trading', if_exists='replace')
'''

def get_historical_data(symbol, start_date, table_name):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    values = yf.download(symbol, start_date)
    values.to_sql(table_name, engine, schema='Trading', if_exists='replace')
    
def get_recent_data(symbol):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    query = 'select max("Date") from {0}.{1}'.format('"Trading"', '"' + symbol + '"')
    start_date = pd.read_sql(query, engine)[max][0] + timedelta(days=1)
    values = yf.download(symbol, start=start_date )
    values.to_sql(symbol, engine, schema="Trading", if_exists='append')


