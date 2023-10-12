import pandas as pd
import yfinance as yf
import logging

ticker_list = ['AAPL', 'TSLA', 'CDR.WA', 'MSFT', '^GSCP', 'GC=F', 'CL=F']

start_date = pd.to_datetime('2000/01/01', yearfirst=True)
end_date = pd.Timestamp.now()
dates_range= pd.date_range(start_date, end_date)
ticks = len(dates_range) / 730
dates = []
for i in range(int(ticks)+1):
    dates.append(start_date + pd.Timedelta(days=730 * i))

for symbol in ticker_list:
    if symbol == 'AAPL':
        apple = yf.download(symbol, '2000-1-1', interval='1h')