import pandas as pd
import yfinance as yf
#import snscrape.modules.twitter as sntwitter

import config_file
import logging

from sqlalchemy.types import String, Float, Date, BigInteger
from sqlalchemy import create_engine

from datetime import timedelta, datetime, date


logging.basicConfig(filename='logs.log', format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%d-%m-%y %H:%M:%S', filemode='a', level=logging.INFO)

logger = logging.getLogger()

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
try:
    engine = create_engine(url)
    logger.info('Connection created')
except Exception as msg:
    logger.error(msg)

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
def preprocess(df, symbol):
    df['Symbol'] = symbol
    df = df.reset_index()
    return df
   
def load_to_db(df, schema):
    try:    
        df.to_sql('Stocks', engine, schema=schema, if_exists='append', index=False,
                  dtype=types)
        logger.info('Data saved to db')
    except Exception as msg:
        logger.error('Error while saving historical data to db: ' + msg)
    
def get_historical_data(symbol, start_date):
    logger.info('Getting historical data for {}'.symbol)
    try:
        df = yf.download(symbol, start_date)
        logger.info('Data collected succesfully')
    except Exception as msg:
        logger.error('Error while collecting historical data: {}'.format(msg))
    df = preprocess(df, symbol)
    load_to_db(df)
        
def get_recent_data(symbol, schema):
    logger.info('Getting recent data for {}'.format(symbol))
    query = 'select max("Date") from {0}.{1} where "Symbol" = {2}'.format('"Trading"', '"Stocks"', "'" + symbol + "'")
    try:
        max_date = pd.read_sql(query, engine)['max'][0]
    except Exception as msg:
        logger.error("Error while checking max date: {}".format(msg))
    if str(max_date) == datetime.today().strftime('%Y-%m-%d'):
        logger.error("Max date is equal to today's date")
        pass
    else:
        try:
            start_date = max_date + timedelta(days=1)
            df = yf.download(symbol, start=start_date )
            logger.info('Data collected succesfully')
        except Exception as msg:
            logger.error('Error while collecting recent data: {}'.format(msg))
        df = preprocess(df, symbol)
        load_to_db(df, schema)
        
def get_data_from_db(schema, table, date):
    query = 'SELECT * FROM {0}.{1} where "Date"' 
    df = pd.
        
'''
def get_historical_tweets(start_year, start_month, start_day, keyword):
    df = pd.DataFrame()
    start = date(start_year, start_month, start_day)
    start = start.strftime('%Y-%m-%d')
    query = keyword + 'since:' + start + '-filter:links -filter:replies'
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        df.iloc[i] = [tweet.id, tweet.date, tweet.content]                                                    
    return df
'''