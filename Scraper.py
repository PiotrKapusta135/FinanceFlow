import pandas as pd
import yfinance as yf
import credentials

import logging

from sqlalchemy.types import String, Float, Date, BigInteger
from sqlalchemy import create_engine

from datetime import timedelta

user = credentials.user
password = credentials.password
db = credentials.db
host = credentials.host
port = credentials.port

url = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(user, 
                                                password,
                                                host,
                                                port,
                                                db)

engine = create_engine(url)

types = {'Symbol':String(10),
         'Date':Date,
         'Open':Float,
         'High':Float,
         'Low':Float,
         'Close':Float,
         'Adj Close':Float,
         'Volume':BigInteger()
         }

#First load
'''
ticker_list = ['AAPL', 'TSLA', 'CDR.WA', 'MSFT', '^GSCP', 'GC=F', 'CL=F']
start_date = '2000-1-1'

columns = ['Symbol', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
df = pd.DataFrame(columns=columns)



for symbol in ticker_list:
    tmp = yf.download(symbol, start=start_date)
    tmp['Symbol'] = symbol
    tmp = tmp.reset_index()
    df = pd.concat([df, tmp])        
    df.to_sql('Stocks', engine, schema='Trading', if_exists='replace', index=False,
              dtype=types)

 '''

   
def get_historical_data(symbol, start_date):
    #engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    values = yf.download(symbol, start_date)
    values = preprocess(values, symbol)
    values.to_sql('Stocks', engine, schema='Trading', if_exists='append', index=False,
                  dtype=types)
    
def get_recent_data(symbol):
    #engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    query = 'select max("Date") from {0}.{1}'.format('"Trading"', '"Stocks"')
    start_date = pd.read_sql(query, engine)[max][0] + timedelta(days=1)
    df = yf.download(symbol, start=start_date )
    df = preprocess(df, symbol)
    df.to_sql('Stocks', engine, schema="Trading", if_exists='append', index=False,
              dtype=types)

def preprocess(df, symbol):
    df['Symbol'] = symbol
    df = df.reset_index()
    return df


