import Scraper
from datetime import date

symbols = ['AAPL', 'TSLA', 'CDR.WA', 'MSFT', '^GSCP', 'GC=F', 'CL=F']
keywords = ['Apple', 'Tesla', 'CD Project', 'Microsoft', 'S&P500', 'Gold', 'Oil']
stocks = dict(zip(symbols, keywords))

for symbol in symbols:
    Scraper.get_recent_data(symbol)
