import Scraper


symbols = ['AAPL', 'TSLA', 'CDR.WA', 'MSFT', '^GSPC', 'GC=F', 'CL=F']

for symbol in symbols:
    Scraper.get_recent_data(symbol)
