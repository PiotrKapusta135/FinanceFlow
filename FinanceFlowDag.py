import sys
sys.path.append('/home/piotrek/Projects/FinanceFlow')

import Scraper
import config_file

from airflow import DAG
from airflow.operators.python import PythonOperator

from datetime import datetime

def get_recent_data_and_load_to_source():
    schema = '"Trading_source"."Stocks"'
    for symbol in config_file.symbols:
        Scraper.get_recent_data(symbol, schema)

def get_and_preprocess_source_data():
    for symbol in config_file.symbols:
        df = Scraper.get_data_from_db('Trading_source', 'Stocks', symbol)
        df = Scraper.preprocess(df, symbol)
        Scraper.load_to_db(df, 'Trading')
    
with DAG(dag_id='FinanceFlow',
         start_date=datetime(2023, 10, 22),
         schedule_interval='@daily',
         catchup=False) as dag:
    
    get_recent_data = PythonOperator(task_id='get_recent_data',
                                     python_callable=get_recent_data_and_load_to_source)
    
    get_and_preprocess_source_data = PythonOperator(task_id='get_and_preprocess_source_data', 
                                                    python_callable=get_and_preprocess_source_data)
    
    get_recent_data >> get_and_preprocess_source_data